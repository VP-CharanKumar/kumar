import uuid
import json
from typing import Dict, Any, Optional, Tuple

try:
    from sqlalchemy.orm import Session
except ImportError:
    Session = Any
from app.models.database import Conversation, Message, EnvironmentalProfileModel, RecommendationModel
from app.models.environmental import EnvironmentalProfile
from app.models.schemas import ChatResponse, ScientificAnalysisResponse
from app.services.profile_service import ProfileService
from app.services.environmental_reasoning import EnvironmentalReasoningEngine
from app.services.recommendation_service import RecommendationService
from app.services.citation_service import CitationService
from app.services.gemini_service import GeminiService
from app.rag.retriever import RAGRetriever
from app.utils.logger import logger

class ConversationService:
    def __init__(
        self,
        db: Session,
        retriever: Optional[RAGRetriever] = None,
        reasoning_engine: Optional[EnvironmentalReasoningEngine] = None,
        recommendation_service: Optional[RecommendationService] = None,
        citation_service: Optional[CitationService] = None,
        gemini_service: Optional[GeminiService] = None
    ):
        self.db = db
        self.retriever = retriever or RAGRetriever()
        self.reasoning_engine = reasoning_engine or EnvironmentalReasoningEngine()
        self.citation_service = citation_service or CitationService()
        self.recommendation_service = recommendation_service or RecommendationService(self.citation_service)
        self.gemini_service = gemini_service or GeminiService()

    def get_or_create_conversation(self, conversation_id: Optional[str]) -> Tuple[Conversation, EnvironmentalProfile]:
        """Fetch existing conversation or create a new session."""
        if conversation_id:
            conv = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conv:
                profile_model = self.db.query(EnvironmentalProfileModel).filter(EnvironmentalProfileModel.conversation_id == conv.id).first()
                if profile_model:
                    p_dict = {k: getattr(profile_model, k) for k in EnvironmentalProfile.model_fields.keys() if hasattr(profile_model, k)}
                    return conv, EnvironmentalProfile(**p_dict)
                return conv, EnvironmentalProfile()

        # Create new
        new_id = conversation_id or str(uuid.uuid4())
        conv = Conversation(id=new_id, title="Ecological Intelligence Assessment")
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv, EnvironmentalProfile()

    def update_profile_in_db(self, conv_id: str, profile: EnvironmentalProfile):
        """Save updated environmental profile to SQLite."""
        prof_model = self.db.query(EnvironmentalProfileModel).filter(EnvironmentalProfileModel.conversation_id == conv_id).first()
        p_dict = profile.model_dump()
        
        if not prof_model:
            prof_model = EnvironmentalProfileModel(conversation_id=conv_id, **p_dict)
            self.db.add(prof_model)
        else:
            for k, v in p_dict.items():
                if v is not None:
                    setattr(prof_model, k, v)
            self.db.add(prof_model)
        self.db.commit()

    def process_user_turn(self, conversation_id: Optional[str], user_message: str, profile_override: Optional[Dict[str, Any]] = None) -> ChatResponse:
        """Process one conversational cycle: parse inputs, update memory, determine whether to clarify or analyze."""
        conv, current_profile = self.get_or_create_conversation(conversation_id)

        # 1. Store user message in DB
        msg_user = Message(conversation_id=conv.id, sender="user", content=user_message)
        self.db.add(msg_user)
        self.db.commit()

        # 2. Extract & merge environmental profile
        updated_profile = ProfileService.extract_from_text(user_message, current_profile)
        if profile_override:
            for k, v in profile_override.items():
                if v is not None and hasattr(updated_profile, k):
                    setattr(updated_profile, k, v)

        self.update_profile_in_db(conv.id, updated_profile)

        # 3. Detect data gaps
        missing_vars = ProfileService.detect_missing_variables(updated_profile)
        known_count = updated_profile.count_known_variables()

        # Decision threshold:
        # If user provided very minimal context (known variables < 2) and didn't provide specific values, ask clarifying questions first!
        if known_count < 2 and missing_vars:
            clarifying_questions = ProfileService.generate_clarifying_questions(missing_vars)
            assistant_reply = (
                "To conduct a high-confidence ecological assessment and identify multi-variable environmental interactions, "
                "I need a few critical baseline parameters for your site:\n\n" +
                "\n".join([f"{i+1}. {q}" for i, q in enumerate(clarifying_questions)])
            )
            msg_asst = Message(conversation_id=conv.id, sender="assistant", content=assistant_reply)
            self.db.add(msg_asst)
            self.db.commit()

            return ChatResponse(
                conversation_id=conv.id,
                message=assistant_reply,
                environmental_profile=updated_profile,
                missing_variables=missing_vars,
                clarifying_questions=clarifying_questions,
                has_analysis=False,
                analysis=None,
                retrieved_evidence=[]
            )

        # 4. We have sufficient data to run the scientific RAG & reasoning pipeline
        retrieved_chunks = self.retriever.retrieve_for_profile(updated_profile.model_dump(), top_k=5)
        variables_used, interactions, uncertainties = self.reasoning_engine.analyze_interactions(updated_profile, retrieved_chunks)
        recs, monitoring = self.recommendation_service.generate_recommendations(updated_profile, retrieved_chunks, variables_used)
        
        # Validate citations
        for r in recs:
            _, val_sources, _ = self.citation_service.validate_citations(r.evidence, retrieved_chunks)
            r.evidence = val_sources

        # Format sources for transparency
        sources_formatted = self.citation_service.format_sources_for_response(retrieved_chunks)

        # Gemini scientific synthesis
        scientific_assessment = self.gemini_service.synthesize_scientific_response(
            profile=updated_profile,
            variables_used=variables_used,
            interactions=interactions,
            recommendations=recs,
            monitoring_plan=monitoring,
            retrieved_chunks=retrieved_chunks,
            user_message=user_message
        )

        analysis_obj = ScientificAnalysisResponse(
            assessment=scientific_assessment,
            known_variables=updated_profile.get_known_variables_list(),
            missing_variables=missing_vars,
            variables_used_for_reasoning=variables_used,
            environmental_interactions=interactions,
            recommendations=recs,
            monitoring_plan=monitoring,
            sources=sources_formatted,
            uncertainties=uncertainties,
            clarifying_questions=[]
        )

        # Save recommendations to DB
        for r in recs:
            rec_db = RecommendationModel(
                conversation_id=conv.id,
                action=r.action,
                why_it_works=r.why_it_works,
                impacted_metrics=json.dumps(r.impacted_metrics),
                expected_direction=json.dumps(r.expected_direction),
                time_horizon=r.time_horizon,
                confidence=r.confidence,
                evidence_sources=json.dumps(r.evidence),
                tradeoffs=json.dumps(r.tradeoffs),
                monitoring_plan=json.dumps([m.model_dump() for m in monitoring])
            )
            self.db.add(rec_db)

        # Save assistant message to DB
        msg_asst = Message(conversation_id=conv.id, sender="assistant", content=scientific_assessment)
        self.db.add(msg_asst)
        self.db.commit()

        return ChatResponse(
            conversation_id=conv.id,
            message=scientific_assessment,
            environmental_profile=updated_profile,
            missing_variables=missing_vars,
            clarifying_questions=[],
            has_analysis=True,
            analysis=analysis_obj,
            retrieved_evidence=sources_formatted
        )

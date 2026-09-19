from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.schemas import AnalyzeRequest, ScientificAnalysisResponse
from app.services.profile_service import ProfileService
from app.services.environmental_reasoning import EnvironmentalReasoningEngine
from app.services.recommendation_service import RecommendationService
from app.services.citation_service import CitationService
from app.services.gemini_service import GeminiService
from app.rag.retriever import RAGRetriever

router = APIRouter(prefix="/api", tags=["Analysis"])

@router.post("/analyze", response_model=ScientificAnalysisResponse)
def analyze_environment(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    retriever = RAGRetriever()
    reasoning_engine = EnvironmentalReasoningEngine()
    citation_service = CitationService()
    recommendation_service = RecommendationService(citation_service)
    gemini_service = GeminiService()

    missing_vars = ProfileService.detect_missing_variables(payload)
    retrieved_chunks = retriever.retrieve_for_profile(payload.model_dump(), top_k=5)
    variables_used, interactions, uncertainties = reasoning_engine.analyze_interactions(payload, retrieved_chunks)
    recs, monitoring = recommendation_service.generate_recommendations(payload, retrieved_chunks, variables_used)

    # Validate citations
    for r in recs:
        _, val_sources, _ = citation_service.validate_citations(r.evidence, retrieved_chunks)
        r.evidence = val_sources

    sources_formatted = citation_service.format_sources_for_response(retrieved_chunks)

    assessment = gemini_service.synthesize_scientific_response(
        profile=payload,
        variables_used=variables_used,
        interactions=interactions,
        recommendations=recs,
        monitoring_plan=monitoring,
        retrieved_chunks=retrieved_chunks,
        user_message="Direct structured environmental telemetry submission."
    )

    clarifying = ProfileService.generate_clarifying_questions(missing_vars) if len(variables_used) < 3 else []

    return ScientificAnalysisResponse(
        assessment=assessment,
        known_variables=payload.get_known_variables_list(),
        missing_variables=missing_vars,
        variables_used_for_reasoning=variables_used,
        environmental_interactions=interactions,
        recommendations=recs,
        monitoring_plan=monitoring,
        sources=sources_formatted,
        uncertainties=uncertainties,
        clarifying_questions=clarifying
    )

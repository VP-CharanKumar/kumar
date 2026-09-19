import json
from typing import Dict, Any, List, Optional
from app.config import settings
from app.models.environmental import EnvironmentalProfile
from app.models.schemas import ScientificAnalysisResponse, MultiMetricInteraction, RecommendationItem, MonitoringItem
from app.utils.logger import logger

class GeminiService:
    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_google_gemini_api_key_here":
            try:
                from google import genai
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info("Initialized Gemini GenAI client successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize Google GenAI SDK: {e}")

    def synthesize_scientific_response(
        self,
        profile: EnvironmentalProfile,
        variables_used: List[str],
        interactions: List[MultiMetricInteraction],
        recommendations: List[RecommendationItem],
        monitoring_plan: List[MonitoringItem],
        retrieved_chunks: List[Dict[str, Any]],
        user_message: str = ""
    ) -> str:
        """Use Gemini to produce an authoritative, natural scientific synthesis grounded strictly in evidence."""
        if not self.client:
            return self._build_deterministic_synthesis(profile, variables_used, interactions, recommendations)

        evidence_snippets = "\n".join([
            f"- [{c.get('category')} | {c.get('title')}]: {c.get('content')[:350]}..."
            for c in retrieved_chunks[:4]
        ])

        system_instruction = (
            "You are Darukaa.Earth AI Environmental Scientist, an expert in agroecology, soil science, and conservation biology. "
            "Your mandate: Deliver non-obvious, deeply reasoned, evidence-grounded scientific ecological assessments. "
            "Never output generic platitudes like 'use sustainable practices'. "
            "Explain physical, microbial, and hydrological mechanisms explicitly connecting at least three environmental variables. "
            "Rely strictly on the provided scientific evidence excerpts (FAO, IPCC, IPBES, UNEP, USDA). "
            "Acknowledge data limitations and uncertainty conservatively."
        )

        prompt = (
            f"User Inquiry: {user_message}\n\n"
            f"Environmental Profile Variables Provided:\n{json.dumps(profile.model_dump(exclude_none=True), indent=2)}\n\n"
            f"Multi-Metric Variables Coupled: {', '.join(variables_used)}\n\n"
            f"Retrieved Peer-Reviewed Evidence Excerpts:\n{evidence_snippets}\n\n"
            f"Synthesize an authoritative scientific diagnosis explaining how these variables interact and why the prescribed interventions work."
        )

        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_REASONING_MODEL,
                contents=prompt,
                config={"system_instruction": system_instruction, "temperature": 0.2}
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini API generation failed or throttled ({e}). Using deterministic scientific synthesis.")

        return self._build_deterministic_synthesis(profile, variables_used, interactions, recommendations)

    def _build_deterministic_synthesis(
        self,
        profile: EnvironmentalProfile,
        variables_used: List[str],
        interactions: List[MultiMetricInteraction],
        recommendations: List[RecommendationItem]
    ) -> str:
        """Deterministic scientific diagnosis used when offline or in test mode."""
        p = profile.model_dump()
        lines = []
        lines.append("### Scientific Environmental Assessment")
        lines.append(
            f"Based on ecological profile analysis across **{len(variables_used)} coupled parameters** "
            f"({', '.join(variables_used)}), the target parcel exhibits structural biological vulnerability."
        )
        
        if interactions:
            lines.append("\n#### Multi-Metric Mechanistic Couplings:")
            for inter in interactions:
                lines.append(f"- **{inter.interaction_type} ({' ↔ '.join(inter.variables)})**: {inter.description}")
        
        if recommendations:
            lines.append("\n#### Priority Interventions & Physiological Basis:")
            for rec in recommendations:
                lines.append(f"- **{rec.action}** ({rec.time_horizon}, Confidence: {rec.confidence}): {rec.why_it_works}")

        return "\n".join(lines)

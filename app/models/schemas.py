from typing import Optional, List, Dict, Any

try:
    from pydantic import BaseModel, Field
except ImportError:
    class Field:
        def __init__(self, default=None, description=None, default_factory=None, **kwargs):
            self.default = default
            self.description = description
            self.default_factory = default_factory

    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

        def model_dump(self, exclude_none=False) -> Dict[str, Any]:
            res = {}
            for k in dir(self):
                if not k.startswith("_") and not callable(getattr(self, k)):
                    val = getattr(self, k)
                    if exclude_none and val is None:
                        continue
                    res[k] = val
            return res

from app.models.environmental import EnvironmentalProfile

class RecommendationItem(BaseModel):
    action: str = Field(..., description="Specific recommended ecological or agronomic intervention")
    why_it_works: str = Field(..., description="Scientific mechanisms and physiological/biological basis")
    impacted_metrics: List[str] = Field(default_factory=list, description="List of environmental metrics positively affected")
    expected_direction: List[str] = Field(default_factory=list, description="Quantified directional improvements when evidence supports")
    time_horizon: str = Field(..., description="Short Term (0-12m), Medium Term (1-3y), or Long Term (3+y)")
    confidence: str = Field(..., description="HIGH, MEDIUM, or LOW based on data & evidence match")
    evidence: List[str] = Field(default_factory=list, description="Authoritative scientific sources and reports")
    tradeoffs: List[str] = Field(default_factory=list, description="Known agronomic constraints or potential tradeoffs")

class MonitoringItem(BaseModel):
    indicator: str = Field(..., description="Specific metric to measure (e.g., Soil Organic Carbon %)")
    frequency: str = Field(..., description="Measurement schedule (e.g., Annually post-harvest, Monthly)")
    method: str = Field(..., description="Scientific testing protocol or methodology")
    target: str = Field(..., description="Target threshold for positive ecological progression")

class MultiMetricInteraction(BaseModel):
    variables: List[str] = Field(..., description="The coupled variables analyzed together (minimum 3)")
    interaction_type: str = Field(..., description="Compounding Stress, Buffer Synergy, Trophic Cascade, or Hydrological Coupling")
    description: str = Field(..., description="Mechanistic explanation of how the variables interact")
    evidence_support: Optional[str] = Field(None, description="Scientific reference substantiating this interaction")

class ScientificAnalysisResponse(BaseModel):
    assessment: str = Field(..., description="Holistic environmental assessment summary")
    known_variables: List[str] = Field(default_factory=list)
    missing_variables: List[str] = Field(default_factory=list)
    variables_used_for_reasoning: List[str] = Field(default_factory=list)
    environmental_interactions: List[MultiMetricInteraction] = Field(default_factory=list)
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    monitoring_plan: List[MonitoringItem] = Field(default_factory=list)
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    uncertainties: List[str] = Field(default_factory=list)
    clarifying_questions: List[str] = Field(default_factory=list)

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message describing land, farm, or ecological condition")
    conversation_id: Optional[str] = Field(None, description="Optional existing session ID for multi-turn memory")
    profile_override: Optional[Dict[str, Any]] = Field(None, description="Optional structured profile overrides")

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    environmental_profile: EnvironmentalProfile
    missing_variables: List[str]
    clarifying_questions: List[str]
    has_analysis: bool = False
    analysis: Optional[ScientificAnalysisResponse] = None
    retrieved_evidence: List[Dict[str, Any]] = Field(default_factory=list)

class AnalyzeRequest(EnvironmentalProfile):
    pass

class KnowledgeSearchResult(BaseModel):
    chunk_id: str
    title: str
    category: str
    source: str
    content: str
    score: float
    metadata: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    rag_chunks_indexed: int
    environment: str

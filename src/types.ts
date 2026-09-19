export interface EnvironmentalProfile {
  region?: string;
  latitude?: number;
  longitude?: number;
  land_use?: string;
  crop_type?: string;
  soil_ph?: number;
  soil_organic_carbon?: number;
  soil_moisture?: number;
  annual_rainfall_mm?: number;
  temperature_c?: number;
  habitat_type?: string;
  species_richness?: number;
  vegetation_cover_percent?: number;
  water_availability?: string;
  pollution_level?: string;
  pesticide_usage?: string;
  fertilizer_usage?: string;
  deforestation_pressure?: string;
  notes?: string;
}

export interface MultiMetricInteraction {
  variables: string[];
  interaction_type: string;
  description: string;
  evidence_support: string;
}

export interface RecommendationItem {
  action: string;
  why_it_works: string;
  impacted_metrics: string[];
  expected_direction: string[];
  time_horizon: string;
  confidence: "HIGH" | "MEDIUM" | "LOW";
  evidence: string[];
  tradeoffs: string[];
}

export interface MonitoringItem {
  indicator: string;
  frequency: string;
  method: string;
  target: string;
}

export interface RetrievedSource {
  id: string;
  title: string;
  category: string;
  snippet: string;
  relevance_score: number;
}

export interface ScientificAnalysis {
  assessment: string;
  known_variables: string[];
  missing_variables: string[];
  variables_used_for_reasoning: string[];
  environmental_interactions: MultiMetricInteraction[];
  recommendations: RecommendationItem[];
  monitoring_plan: MonitoringItem[];
  sources: RetrievedSource[];
  uncertainties: string[];
  clarifying_questions: string[];
}

export interface ChatMessage {
  id: string;
  sender: "user" | "assistant";
  content: string;
  timestamp: string;
  analysis?: ScientificAnalysis | null;
  clarifyingQuestions?: string[];
}

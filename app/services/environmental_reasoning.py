from typing import Dict, Any, List, Tuple
from app.models.environmental import EnvironmentalProfile
from app.models.schemas import MultiMetricInteraction
from app.utils.logger import logger

class EnvironmentalReasoningEngine:
    """Core scientific engine connecting multi-variable environmental feedback loops."""

    def analyze_interactions(self, profile: EnvironmentalProfile, retrieved_chunks: List[Dict[str, Any]]) -> Tuple[List[str], List[MultiMetricInteraction], List[str]]:
        """Identify interacting environmental variables and map causal feedback mechanisms.
        
        Returns:
            (variables_used, interactions_list, uncertainties)
        """
        p = profile.model_dump()
        variables_used = []
        interactions: List[MultiMetricInteraction] = []
        uncertainties: List[str] = []

        # Collect present variables
        if p.get("soil_organic_carbon") is not None:
            variables_used.append(f"Soil Organic Carbon ({p['soil_organic_carbon']}%)")
        if p.get("annual_rainfall_mm") is not None:
            variables_used.append(f"Annual Rainfall ({p['annual_rainfall_mm']} mm)")
        if p.get("land_use"):
            variables_used.append(f"Land Use ({p['land_use']})")
        if p.get("crop_type"):
            variables_used.append(f"Crop Regime ({p['crop_type']})")
        if p.get("soil_ph") is not None:
            variables_used.append(f"Soil pH ({p['soil_ph']})")
        if p.get("pesticide_usage"):
            variables_used.append(f"Pesticide Pressure ({p['pesticide_usage']})")
        if p.get("deforestation_pressure") or p.get("habitat_type"):
            variables_used.append(f"Habitat Connectivity / Fragment Structure")
        if p.get("water_availability"):
            variables_used.append(f"Hydrological Status ({p['water_availability']})")
        if p.get("soil_moisture") is not None:
            variables_used.append(f"Soil Moisture ({p['soil_moisture']}%)")

        soc = p.get("soil_organic_carbon")
        rainfall = p.get("annual_rainfall_mm")
        crop = (p.get("crop_type") or "").lower()
        land = (p.get("land_use") or "").lower()
        pesticide = (p.get("pesticide_usage") or "").lower()
        notes = (p.get("notes") or "").lower()

        # Coupling 1: SOC ↔ Rainfall Deficit ↔ Monoculture Cropping (Semi-Arid Matrix)
        if (soc is not None and soc < 0.8) and (rainfall is not None and rainfall < 500) and ("monoculture" in crop or "monoculture" in land or "wheat" in crop):
            interactions.append(MultiMetricInteraction(
                variables=["Soil Organic Carbon", "Annual Rainfall", "Monoculture Cropping"],
                interaction_type="Compounding Stress Spiral",
                description=(
                    f"Low SOC ({soc}%) diminishes available water holding capacity (~{int(soc*20000)} gal/acre equivalent). "
                    f"Coupled with rainfall deficit ({rainfall} mm/year) and uniform root extraction depth in wheat monoculture, "
                    "the topsoil suffers severe desiccation, aggregate breakdown, and microbial carbon starvation."
                ),
                evidence_support="FAO (2020) Recarbonizing Global Soils; USDA-NRCS (2021) Cropping Systems & Water Retention"
            ))

        # Coupling 2: Pesticide Pressure ↔ Pollinator Mortality ↔ Floral Simplification
        if ("frequent" in pesticide or "intensive" in pesticide) or ("pollinator" in notes or "bee" in notes):
            vars_for_this = ["Pesticide Intensity", "Floral Diversity", "Pollinator Density"]
            for v in vars_for_this:
                if v not in variables_used:
                    variables_used.append(v)
            interactions.append(MultiMetricInteraction(
                variables=vars_for_this,
                interaction_type="Trophic Collapse Loop",
                description=(
                    "Prophylactic agrochemical exposure (pyrethroids / neonicotinoids) suppresses wild solitary bee "
                    "navigation and immune resilience. When compounded by floral resource deserts in single-crop landscapes, "
                    "wild pollinator populations collapse and natural predatory insect control is eliminated."
                ),
                evidence_support="IPBES (2016) Thematic Assessment on Pollinators and Food Production"
            ))

        # Coupling 3: Forest Fragmentation ↔ Edge Microclimate ↔ Water Desiccation
        if ("fragment" in land or "fragment" in notes or "forest patches" in notes or p.get("deforestation_pressure")):
            vars_for_this = ["Forest Patch Isolation", "Edge Desiccation", "Ecological Connectivity"]
            for v in vars_for_this:
                if v not in variables_used:
                    variables_used.append(v)
            interactions.append(MultiMetricInteraction(
                variables=vars_for_this,
                interaction_type="Habitat Discontinuity",
                description=(
                    "Patch isolation exceeding 300-500 meters severely limits gene flow for small terrestrial fauna. "
                    "Exposed fragment perimeters elevate dry wind penetration, increasing leaf litter drying and tree canopy mortality."
                ),
                evidence_support="UNEP (2021) Generation Restoration; IPBES (2019) Global Assessment"
            ))

        # Coupling 4: Soil Moisture ↔ High Soil Compaction / Bare Ground ↔ Thermal Stress
        if (p.get("soil_moisture") is not None and p["soil_moisture"] < 12) or ("drought" in notes) or (rainfall is not None and rainfall < 350):
            vars_for_this = ["Soil Moisture Deficit", "Bare Soil Heat Flux", "Microbial Respiration"]
            for v in vars_for_this:
                if v not in variables_used:
                    variables_used.append(v)
            interactions.append(MultiMetricInteraction(
                variables=vars_for_this,
                interaction_type="Abiotic Heat-Moisture Amplification",
                description=(
                    "Bare, unmulched topsoils in low-moisture conditions reach 50-60°C midday surface temperatures. "
                    "This thermal shock arrests mycorrhizal spore germination and vaporizes residual capillary moisture."
                ),
                evidence_support="IPCC (2019) Climate Change & Land (SRCCL)"
            ))

        # Generic Multi-Metric Fallback if specific thresholds not crossed but >= 2 variables present
        if not interactions and len(variables_used) >= 2:
            interactions.append(MultiMetricInteraction(
                variables=variables_used[:3],
                interaction_type="Synergistic Ecological Interface",
                description="Soil, microclimatic, and vegetative factors interact to govern primary biological productivity and microbial stabilization.",
                evidence_support="FAO (2020) & IPCC (2019)"
            ))

        # 3-Variable Validation
        if len(variables_used) < 3:
            uncertainties.append(
                f"Analysis currently constrained: Only {len(variables_used)} variable(s) provided ({', '.join(variables_used)}). "
                "Reliable multi-metric ecological modeling requires at least 3 verified environmental dimensions."
            )

        return (variables_used, interactions, uncertainties)

    def validate_three_variables(self, variables_used: List[str]) -> bool:
        """Deterministic 3-Variable Validator constraint check."""
        return len(variables_used) >= 3

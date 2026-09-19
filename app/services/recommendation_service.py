from typing import Dict, Any, List, Tuple
from app.models.environmental import EnvironmentalProfile
from app.models.schemas import RecommendationItem, MonitoringItem
from app.services.citation_service import CitationService
from app.utils.logger import logger

class RecommendationService:
    def __init__(self, citation_service: CitationService = None):
        self.citation_service = citation_service or CitationService()

    def generate_recommendations(
        self,
        profile: EnvironmentalProfile,
        retrieved_chunks: List[Dict[str, Any]],
        variables_used: List[str]
    ) -> Tuple[List[RecommendationItem], List[MonitoringItem]]:
        """Generate scientifically grounded, evidence-backed recommendations tailored to environmental profile."""
        p = profile.model_dump()
        recs: List[RecommendationItem] = []
        monitoring: List[MonitoringItem] = []

        soc = p.get("soil_organic_carbon")
        rainfall = p.get("annual_rainfall_mm")
        crop = (p.get("crop_type") or "").lower()
        region = (p.get("region") or "").lower()
        pesticide = (p.get("pesticide_usage") or "").lower()
        notes = (p.get("notes") or "").lower()
        deforestation = (p.get("deforestation_pressure") or "").lower()
        soil_moisture = p.get("soil_moisture")

        # Confidence baseline: HIGH if >= 3 variables and evidence retrieved; MEDIUM otherwise
        base_confidence = "HIGH" if len(variables_used) >= 3 and len(retrieved_chunks) >= 2 else "MEDIUM"

        # Scenario 1: Semi-Arid Cereal Monoculture with Low SOC
        if (soc is not None and soc < 0.6) or ("wheat" in crop and "semi-arid" in region):
            recs.append(RecommendationItem(
                action="Integrate Drought-Hardy Legume Cover Crops (Cowpea / Sunn Hemp) into Cereal Rotation",
                why_it_works=(
                    "Rhizobium-inoculated legumes fix atmospheric nitrogen (30-60 kg N/ha) while exuding root glomalin "
                    "that aggregates fine soil particles. This boosts soil biological activity and elevates topsoil available water capacity."
                ),
                impacted_metrics=[
                    "Soil Organic Carbon (+0.15% to 0.30% annually)",
                    "Plant Available Water Capacity (+15-20%)",
                    "Arbuscular Mycorrhizal Fungi (AMF) Biomass"
                ],
                expected_direction=["Increasing SOC", "Increasing Water Retention", "Increasing Microbial Diversity"],
                time_horizon="Medium Term (1-3 years)",
                confidence=base_confidence,
                evidence=[
                    "FAO (2020) Recarbonizing Global Soils: Technical Manual Vol. 4",
                    "USDA-NRCS (2021) Soil Health Technical Note No. 450-06"
                ],
                tradeoffs=[
                    "In hyper-arid seasons (<300 mm), cover crops must be terminated early (stubble crimped) to prevent competition with main cash crops for residual subsoil moisture."
                ]
            ))

            recs.append(RecommendationItem(
                action="Establish Dispersed Native Parkland Agroforestry (Faidherbia albida / Acacia nilotica) at 25-35 trees/ha",
                why_it_works=(
                    "Faidherbia exhibits reverse phenology, maintaining canopy shade and nitrogen-rich leaf litter in dry months "
                    "while defoliating during rainy cereal germination. Deep taproots perform nocturnal hydraulic lift, moderating surface VPD by 15-20%."
                ),
                impacted_metrics=[
                    "Microclimatic Thermal Buffering (-2 to -4°C canopy temperature)",
                    "Subsoil Nutrient Cycling",
                    "Native Avian & Pollinator Perch Density"
                ],
                expected_direction=["Decreasing Evaporative Deficit", "Increasing Soil Nitrogen Pools"],
                time_horizon="Long Term (3+ years)",
                confidence=base_confidence,
                evidence=[
                    "ICRAF / CIFOR (2018) Agroforestry in Drylands: Tree-Crop-Soil Interactions"
                ],
                tradeoffs=[
                    "Requires 2 years of juvenile sapling protection against browsing livestock before trees achieve browse height."
                ]
            ))

            monitoring.append(MonitoringItem(
                indicator="Soil Organic Carbon (SOC %)",
                frequency="Annual post-harvest sampling (0-15 cm and 15-30 cm depths)",
                method="Dry combustion elemental analyzer or Walkley-Black titration",
                target="Increase baseline SOC from 0.3% to >=0.55% over 3 seasons"
            ))
            monitoring.append(MonitoringItem(
                indicator="Available Water Capacity (AWC)",
                frequency="Monthly during crop vegetative stages",
                method="Tensiometer or Time-Domain Reflectometry (TDR) probes",
                target="Maintain volumetric soil moisture >= 14% through 10-day dry spells"
            ))

        # Scenario 2: Pesticide Intensity & Pollinator Vulnerability
        if ("frequent" in pesticide or "intensive" in pesticide) or ("pollinator" in notes or "bee" in notes):
            recs.append(RecommendationItem(
                action="Establish 4-6m Wide Indigenous Flowering Conservation Strips & Transition to Dusk IPPM",
                why_it_works=(
                    "Perennial wildflower corridors providing 8-12 native nectar/pollen species restore continuous floral forage "
                    "outside main crop bloom. Halting daytime pesticide sprays and shifting to economic thresholds prevents lethal honeybee and solitary bee intoxication."
                ),
                impacted_metrics=[
                    "Wild Pollinator Abundance (+40% to 70% within 2 seasons)",
                    "Beneficial Arthropod Predator Ratio (Syrphidae, Carabidae)",
                    "Adjacent Crop Fruit-Set Percentage"
                ],
                expected_direction=["Increasing Pollinator Richness", "Decreasing Chemical Input Dependency"],
                time_horizon="Short Term (0-12 months)",
                confidence=base_confidence,
                evidence=[
                    "IPBES (2016) Thematic Assessment Report on Pollinators and Food Production",
                    "UNEP (2020) Environmental and Health Impacts of Pesticides and Fertilizers"
                ],
                tradeoffs=[
                    "Requires re-allocating 3-5% of field boundary area away from cash crop cultivation to native floral buffers."
                ]
            ))

            recs.append(RecommendationItem(
                action="Preserve Untilled Earthen Banks & Native Brush for Solitary Bee Nesting Refugia",
                why_it_works=(
                    "Over 70% of wild solitary bee species nest in undisturbed subterranean burrows. Eliminating boundary tillage "
                    "and providing dead pithy stems ensures reproductive overwintering habitats."
                ),
                impacted_metrics=[
                    "Ground-Nesting Solitary Bee Colony Density",
                    "Overwintering Survival Rate"
                ],
                expected_direction=["Increasing Nesting Success", "Stabilizing Pollination Redundancy"],
                time_horizon="Short Term (0-12 months)",
                confidence=base_confidence,
                evidence=[
                    "IPBES (2016) Assessment on Pollinators and Ecosystem Services"
                ],
                tradeoffs=[
                    "Field borders must remain mechanically undisturbed by heavy agricultural machinery."
                ]
            ))

            monitoring.append(MonitoringItem(
                indicator="Pollinator Visitation Frequency",
                frequency="Bi-weekly 15-minute visual transect walks during peak bloom",
                method="Standardized pan trap sampling and timed flower visitation surveys",
                target="Achieve >= 15 insect floral visits per 15-minute observation window"
            ))

        # Scenario 3: Forest Fragmentation & Connectivity
        if ("fragment" in notes or "fragment" in deforestation or p.get("deforestation_pressure")):
            recs.append(RecommendationItem(
                action="Install Native Stepping-Stone Riparian Corridors (25-40m width) Linking Forest Fragments",
                why_it_works=(
                    "Linear wooded linkages lower boundary dispersal resistance, restoring genetic gene flow for small mammals, "
                    "amphibians, and forest birds while buffering watercourses against agrochemical leaching."
                ),
                impacted_metrics=[
                    "Structural & Functional Landscape Connectivity Index",
                    "Avian & Arthropod Dispersal Success Rate (+25-35%)",
                    "Riparian Nitrate Runoff Filtration"
                ],
                expected_direction=["Decreasing Fragment Isolation", "Increasing Regional Species Richness"],
                time_horizon="Medium to Long Term (2-5 years)",
                confidence=base_confidence,
                evidence=[
                    "UNEP (2021) Becoming #GenerationRestoration: Ecosystem Restoration",
                    "IPBES (2019) Global Assessment Report on Biodiversity"
                ],
                tradeoffs=[
                    "Requires multi-landowner boundary agreements and exclusion of livestock grazing during sapling establishment."
                ]
            ))

            monitoring.append(MonitoringItem(
                indicator="Structural Connectivity & Canopy Cover",
                frequency="Annual high-resolution drone or satellite NDVI imagery",
                method="Landscape metric analysis (FRAGSTATS / GuidosToolbox)",
                target="Reduce Euclidean isolation between patches to < 200 meters"
            ))

        # Scenario 4: Drought & Moisture Stress
        if (soil_moisture is not None and soil_moisture < 12) or ("drought" in notes) or (rainfall is not None and rainfall < 350):
            recs.append(RecommendationItem(
                action="Construct Contour Water-Harvesting Swales with 30% Stubble Residue Retention",
                why_it_works=(
                    "Level contour swales and earthen berms decelerate storm runoff, converting destructive surface sheetwash "
                    "into deep soil infiltration lenses. Stubble mulch suppresses evaporative loss and lowers soil surface temperatures by 8-12°C."
                ),
                impacted_metrics=[
                    "Surface Runoff Reduction (30-45% reduction)",
                    "Subsoil Root Zone Moisture Infiltration",
                    "Topsoil Loss Prevention (<2 tonnes/ha/year)"
                ],
                expected_direction=["Increasing Deep Moisture Recharge", "Decreasing Soil Erosion"],
                time_horizon="Short to Medium Term (6-18 months)",
                confidence=base_confidence,
                evidence=[
                    "FAO (2019) Water Harvesting & Soil Moisture Conservation in Semi-Arid Regions",
                    "IPCC (2019) SRCCL Desertification & Land Degradation"
                ],
                tradeoffs=[
                    "Initial earthwork surveying and grading labor costs."
                ]
            ))

            monitoring.append(MonitoringItem(
                indicator="Soil Moisture Retention Post-Storm",
                frequency="Weekly following precipitation events",
                method="Volumetric moisture sensors at 20 cm and 50 cm depths",
                target="Maintain available water content > 12% for at least 14 days after a 20 mm storm"
            ))

        # Fallback if no specific condition matched
        if not recs:
            recs.append(RecommendationItem(
                action="Implement Minimal Tillage with Organic Compost Mulching and Rotational Green Manure",
                why_it_works=(
                    "Preserves undisturbed fungal mycorrhizae, limits carbon oxidation, and restores organic matter in depleted topsoils."
                ),
                impacted_metrics=["Soil Organic Carbon", "Microbial Biodiversity", "Infiltration Rate"],
                expected_direction=["Increasing Biological Resilience", "Decreasing Erosion"],
                time_horizon="Medium Term (1-2 years)",
                confidence="MEDIUM",
                evidence=["FAO (2020) Recarbonizing Global Soils"],
                tradeoffs=["May require specialized direct-seeding implements."]
            ))
            monitoring.append(MonitoringItem(
                indicator="Soil Structure & Bulk Density",
                frequency="Annual testing",
                method="Soil core cylinder density measurement",
                target="Bulk density < 1.35 g/cm³"
            ))

        return (recs, monitoring)

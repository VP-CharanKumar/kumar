import re
from typing import Dict, Any, List, Tuple
from app.models.environmental import EnvironmentalProfile

class ProfileService:
    @staticmethod
    def extract_from_text(text: str, existing_profile: EnvironmentalProfile = None) -> EnvironmentalProfile:
        """Extract environmental parameters from conversational text using heuristics and pattern matching."""
        profile_dict = existing_profile.model_dump() if existing_profile else EnvironmentalProfile().model_dump()
        text_lower = text.lower()

        # 1. Soil Organic Carbon (SOC)
        soc_match = (
            re.search(r'(?:soc|soil organic carbon|organic carbon)[^0-9%]{0,30}?([0-9]+(?:\.[0-9]+)?)\s*%', text_lower) or
            re.search(r'([0-9]+(?:\.[0-9]+)?)\s*%\s*(?:soc|soil organic carbon|organic carbon)', text_lower)
        )
        if soc_match:
            try:
                profile_dict["soil_organic_carbon"] = float(soc_match.group(1))
            except ValueError:
                pass

        # 2. Rainfall
        rain_match = (
            re.search(r'(?:rainfall|precipitation|rain)[^0-9]{0,30}?([0-9]+(?:\.[0-9]+)?)\s*(?:mm|millimeters)', text_lower) or
            re.search(r'([0-9]+(?:\.[0-9]+)?)\s*(?:mm|millimeters)\s*(?:annual\s+|seasonal\s+)?(?:rainfall|precipitation|rain)', text_lower) or
            re.search(r'(?:rainfall|precipitation|rain)\s*(?:is|about|around|of)?\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)', text_lower)
        )
        if rain_match:
            try:
                profile_dict["annual_rainfall_mm"] = float(rain_match.group(1))
            except ValueError:
                pass

        # 3. Soil pH
        ph_match = re.search(r'(?:soil\s+)?ph\s*(?:is|of|level)?\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)', text_lower)
        if ph_match:
            try:
                profile_dict["soil_ph"] = float(ph_match.group(1))
            except ValueError:
                pass

        # 4. Region / Biome
        if "semi-arid" in text_lower or "semi arid" in text_lower:
            profile_dict["region"] = "semi-arid"
        elif "arid" in text_lower:
            profile_dict["region"] = "arid"
        elif "tropical" in text_lower:
            profile_dict["region"] = "tropical"
        elif "temperate" in text_lower:
            profile_dict["region"] = "temperate"
        elif "mediterranean" in text_lower:
            profile_dict["region"] = "mediterranean"

        # 5. Crop Type & Monoculture
        if "wheat monoculture" in text_lower or ("monoculture" in text_lower and "wheat" in text_lower):
            profile_dict["crop_type"] = "wheat monoculture"
            profile_dict["land_use"] = "intensive agriculture"
        elif "monoculture" in text_lower:
            profile_dict["crop_type"] = "monoculture crop"
            profile_dict["land_use"] = "intensive agriculture"
        elif "wheat" in text_lower:
            profile_dict["crop_type"] = "wheat"
            profile_dict["land_use"] = "agriculture"
        elif "corn" in text_lower or "maize" in text_lower:
            profile_dict["crop_type"] = "maize"
            profile_dict["land_use"] = "agriculture"

        # 6. Pesticide Usage
        if any(w in text_lower for w in ["frequent pesticide", "heavy pesticide", "pesticides frequently", "spray regularly", "high pesticide"]):
            profile_dict["pesticide_usage"] = "frequent / intensive"
        elif "low pesticide" in text_lower or "organic" in text_lower:
            profile_dict["pesticide_usage"] = "low / organic"

        # 7. Pollinators
        if any(w in text_lower for w in ["pollinator", "pollinators", "fewer bees", "bee decline", "bees crashed"]):
            profile_dict["notes"] = (profile_dict.get("notes") or "") + " Observed acute pollinator decline."

        # 8. Forest Fragmentation
        if any(w in text_lower for w in ["fragmentation", "disconnected", "isolated forest", "broken patches", "forest patches"]):
            profile_dict["deforestation_pressure"] = "fragmented woodland patches"
            profile_dict["habitat_type"] = "fragmented forest mosaic"

        # 9. Drought / Water Stress
        if any(w in text_lower for w in ["drought", "dry soil", "water stress", "low water"]):
            profile_dict["water_availability"] = "drought-stressed"

        return EnvironmentalProfile(**profile_dict)

    @staticmethod
    def detect_missing_variables(profile: EnvironmentalProfile) -> List[str]:
        """Detect critical environmental data gaps necessary for high-confidence multi-metric analysis."""
        missing = []
        p = profile.model_dump()
        
        # Primary baseline variables
        if p.get("soil_organic_carbon") is None:
            missing.append("Soil Organic Carbon (SOC %)")
        if p.get("annual_rainfall_mm") is None:
            missing.append("Annual Rainfall / Moisture Regime (mm/year)")
        if not p.get("land_use") and not p.get("crop_type"):
            missing.append("Land-use and Cropping Pattern (e.g., monoculture, agroforestry)")
        if p.get("soil_ph") is None:
            missing.append("Soil pH (acidity / alkalinity)")
        if not p.get("water_availability"):
            missing.append("Water Source / Hydrological Status (rain-fed vs irrigated)")

        return missing

    @staticmethod
    def generate_clarifying_questions(missing_variables: List[str]) -> List[str]:
        """Generate targeted, scientific clarifying questions (2 to 4 questions max)."""
        questions = []
        for var in missing_variables[:3]:
            if "Soil Organic Carbon" in var:
                questions.append("Could you provide your approximate soil organic carbon (SOC %) or topsoil organic matter status?")
            elif "Annual Rainfall" in var:
                questions.append("What is the typical annual or seasonal rainfall pattern for your area (in mm or dry/wet seasonality)?")
            elif "Land-use" in var:
                questions.append("What is your current land-use regime and crop type (e.g., continuous monoculture, rotation, pasture)?")
            elif "Water Source" in var:
                questions.append("Is your parcel strictly rain-fed, or is supplemental irrigation or groundwater available?")
            elif "Soil pH" in var:
                questions.append("Do you know your approximate soil pH range (acidic <6.0, neutral 6.5-7.5, alkaline >7.5)?")

        if not questions and len(missing_variables) > 0:
            questions.append("Could you share additional specifics regarding your soil texture, topography, or recent chemical treatments?")

        return questions[:4]

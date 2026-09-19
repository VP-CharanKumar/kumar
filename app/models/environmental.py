from typing import Optional, List, Dict, Any

try:
    from pydantic import BaseModel, Field
except ImportError:
    class Field:
        def __init__(self, default=None, description=None, **kwargs):
            self.default = default
            self.description = description
    
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
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

        @classmethod
        @property
        def model_fields(cls):
            return {
                "region": None, "latitude": None, "longitude": None, "land_use": None,
                "crop_type": None, "soil_ph": None, "soil_organic_carbon": None,
                "soil_moisture": None, "annual_rainfall_mm": None, "temperature_c": None,
                "habitat_type": None, "species_richness": None, "vegetation_cover_percent": None,
                "water_availability": None, "pollution_level": None, "pesticide_usage": None,
                "fertilizer_usage": None, "deforestation_pressure": None, "notes": None
            }

class EnvironmentalProfile(BaseModel):
    region: Optional[str] = Field(None, description="Bioclimatic zone or geographic region (e.g., semi-arid, temperate)")
    latitude: Optional[float] = Field(None, description="Latitude in decimal degrees")
    longitude: Optional[float] = Field(None, description="Longitude in decimal degrees")
    land_use: Optional[str] = Field(None, description="Primary land cover or management (e.g., agriculture, pasture, forest)")
    crop_type: Optional[str] = Field(None, description="Crop or vegetation regime (e.g., wheat monoculture, intercropped legume)")
    soil_ph: Optional[float] = Field(None, description="Soil pH value (0.0 to 14.0)")
    soil_organic_carbon: Optional[float] = Field(None, description="Soil Organic Carbon percentage (SOC %)")
    soil_moisture: Optional[float] = Field(None, description="Volumetric soil moisture percentage (%)")
    annual_rainfall_mm: Optional[float] = Field(None, description="Mean annual precipitation in millimeters")
    temperature_c: Optional[float] = Field(None, description="Mean or peak ambient temperature in Celsius")
    habitat_type: Optional[str] = Field(None, description="Specific biome or habitat description")
    species_richness: Optional[int] = Field(None, description="Observed or estimated species count")
    vegetation_cover_percent: Optional[float] = Field(None, description="Canopy or ground vegetation cover percentage (%)")
    water_availability: Optional[str] = Field(None, description="Hydrological status (low, medium, high, drought-stressed)")
    pollution_level: Optional[str] = Field(None, description="Agrochemical or industrial pollution intensity")
    pesticide_usage: Optional[str] = Field(None, description="Frequency and class of pesticide applications")
    fertilizer_usage: Optional[str] = Field(None, description="Synthetic or organic fertilizer regime")
    deforestation_pressure: Optional[str] = Field(None, description="Tree loss or clearance pressure level")
    notes: Optional[str] = Field(None, description="Additional context or qualitative field observations")

    def __init__(self, **data):
        # Set all default fields
        fields = [
            "region", "latitude", "longitude", "land_use", "crop_type", "soil_ph",
            "soil_organic_carbon", "soil_moisture", "annual_rainfall_mm", "temperature_c",
            "habitat_type", "species_richness", "vegetation_cover_percent", "water_availability",
            "pollution_level", "pesticide_usage", "fertilizer_usage", "deforestation_pressure", "notes"
        ]
        for f in fields:
            setattr(self, f, data.get(f, None))
        super().__init__(**data)

    def count_known_variables(self) -> int:
        """Count non-null environmental variables populated in this profile."""
        non_null = 0
        for k, v in self.model_dump().items():
            if k not in ["notes", "latitude", "longitude"] and v is not None and v != "":
                non_null += 1
        return non_null

    def get_known_variables_list(self) -> List[str]:
        known = []
        for k, v in self.model_dump().items():
            if v is not None and v != "":
                known.append(f"{k}: {v}")
        return known

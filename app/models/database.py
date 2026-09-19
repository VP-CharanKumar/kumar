import datetime
import uuid

try:
    from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey, Boolean
    from sqlalchemy.orm import relationship
    from app.database.connection import Base

    class Conversation(Base):
        __tablename__ = "conversations"

        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        title = Column(String(255), default="New Ecological Assessment")
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

        messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.timestamp")
        profile = relationship("EnvironmentalProfileModel", back_populates="conversation", uselist=False, cascade="all, delete-orphan")
        recommendations = relationship("RecommendationModel", back_populates="conversation", cascade="all, delete-orphan")

    class Message(Base):
        __tablename__ = "messages"

        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
        sender = Column(String(20), nullable=False)
        content = Column(Text, nullable=False)
        timestamp = Column(DateTime, default=datetime.datetime.utcnow)

        conversation = relationship("Conversation", back_populates="messages")

    class EnvironmentalProfileModel(Base):
        __tablename__ = "environmental_profiles"

        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, unique=True)
        region = Column(String(100), nullable=True)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        land_use = Column(String(100), nullable=True)
        crop_type = Column(String(100), nullable=True)
        soil_ph = Column(Float, nullable=True)
        soil_organic_carbon = Column(Float, nullable=True)
        soil_moisture = Column(Float, nullable=True)
        annual_rainfall_mm = Column(Float, nullable=True)
        temperature_c = Column(Float, nullable=True)
        habitat_type = Column(String(100), nullable=True)
        species_richness = Column(Integer, nullable=True)
        vegetation_cover_percent = Column(Float, nullable=True)
        water_availability = Column(String(50), nullable=True)
        pollution_level = Column(String(50), nullable=True)
        pesticide_usage = Column(String(50), nullable=True)
        fertilizer_usage = Column(String(50), nullable=True)
        deforestation_pressure = Column(String(50), nullable=True)
        notes = Column(Text, nullable=True)
        updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

        conversation = relationship("Conversation", back_populates="profile")

    class RecommendationModel(Base):
        __tablename__ = "recommendations"

        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
        action = Column(Text, nullable=False)
        why_it_works = Column(Text, nullable=False)
        impacted_metrics = Column(Text, nullable=True)
        expected_direction = Column(Text, nullable=True)
        time_horizon = Column(String(50), nullable=False)
        confidence = Column(String(20), nullable=False)
        evidence_sources = Column(Text, nullable=True)
        tradeoffs = Column(Text, nullable=True)
        monitoring_plan = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)

        conversation = relationship("Conversation", back_populates="recommendations")

    class KnowledgeSourceModel(Base):
        __tablename__ = "knowledge_sources"

        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        source_id = Column(String(100), unique=True, nullable=False)
        title = Column(String(255), nullable=False)
        organization = Column(String(150), nullable=False)
        year = Column(Integer, nullable=False)
        category = Column(String(100), nullable=False)
        summary = Column(Text, nullable=False)
        doi_or_url = Column(String(255), nullable=True)
        evidence_level = Column(String(50), default="High")

except ImportError:
    class ColDesc:
        def __init__(self, name):
            self.name = name
        def __eq__(self, other):
            return (self.name, other)

    class ModelBase:
        id = ColDesc("id")
        conversation_id = ColDesc("conversation_id")

        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class Conversation(ModelBase):
        __tablename__ = "conversations"
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.title = kwargs.get("title", "New Ecological Assessment")
            self.created_at = kwargs.get("created_at", datetime.datetime.utcnow().isoformat())
            self.updated_at = kwargs.get("updated_at", datetime.datetime.utcnow().isoformat())
            self.messages = []
            self.profile = None
            self.recommendations = []
            super().__init__(**kwargs)

    class Message(ModelBase):
        __tablename__ = "messages"
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.conversation_id = kwargs.get("conversation_id", "")
            self.sender = kwargs.get("sender", "user")
            self.content = kwargs.get("content", "")
            self.timestamp = kwargs.get("timestamp", datetime.datetime.utcnow().isoformat())
            super().__init__(**kwargs)

    class EnvironmentalProfileModel(ModelBase):
        __tablename__ = "environmental_profiles"
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.conversation_id = kwargs.get("conversation_id", "")
            self.region = kwargs.get("region")
            self.latitude = kwargs.get("latitude")
            self.longitude = kwargs.get("longitude")
            self.land_use = kwargs.get("land_use")
            self.crop_type = kwargs.get("crop_type")
            self.soil_ph = kwargs.get("soil_ph")
            self.soil_organic_carbon = kwargs.get("soil_organic_carbon")
            self.soil_moisture = kwargs.get("soil_moisture")
            self.annual_rainfall_mm = kwargs.get("annual_rainfall_mm")
            self.temperature_c = kwargs.get("temperature_c")
            self.habitat_type = kwargs.get("habitat_type")
            self.species_richness = kwargs.get("species_richness")
            self.vegetation_cover_percent = kwargs.get("vegetation_cover_percent")
            self.water_availability = kwargs.get("water_availability")
            self.pollution_level = kwargs.get("pollution_level")
            self.pesticide_usage = kwargs.get("pesticide_usage")
            self.fertilizer_usage = kwargs.get("fertilizer_usage")
            self.deforestation_pressure = kwargs.get("deforestation_pressure")
            self.notes = kwargs.get("notes")
            self.updated_at = kwargs.get("updated_at", datetime.datetime.utcnow().isoformat())
            super().__init__(**kwargs)

    class RecommendationModel(ModelBase):
        __tablename__ = "recommendations"
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.conversation_id = kwargs.get("conversation_id", "")
            self.action = kwargs.get("action", "")
            self.why_it_works = kwargs.get("why_it_works", "")
            self.impacted_metrics = kwargs.get("impacted_metrics", "[]")
            self.expected_direction = kwargs.get("expected_direction", "[]")
            self.time_horizon = kwargs.get("time_horizon", "Medium Term")
            self.confidence = kwargs.get("confidence", "HIGH")
            self.evidence_sources = kwargs.get("evidence_sources", "[]")
            self.tradeoffs = kwargs.get("tradeoffs", "[]")
            self.monitoring_plan = kwargs.get("monitoring_plan", "[]")
            self.created_at = kwargs.get("created_at", datetime.datetime.utcnow().isoformat())
            super().__init__(**kwargs)

    class KnowledgeSourceModel(ModelBase):
        __tablename__ = "knowledge_sources"
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.source_id = kwargs.get("source_id", "")
            self.title = kwargs.get("title", "")
            self.organization = kwargs.get("organization", "")
            self.year = kwargs.get("year", 2020)
            self.category = kwargs.get("category", "general")
            self.summary = kwargs.get("summary", "")
            self.doi_or_url = kwargs.get("doi_or_url", "")
            self.evidence_level = kwargs.get("evidence_level", "High")
            super().__init__(**kwargs)

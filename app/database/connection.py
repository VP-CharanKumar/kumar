import os
import sqlite3
from pathlib import Path
from app.config import settings
from app.utils.logger import logger

# Ensure data directory exists
db_url = settings.DATABASE_URL
sqlite_path = db_url.replace("sqlite:///", "") if db_url.startswith("sqlite:///") else "./data/darukaa.db"
Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import declarative_base, sessionmaker

    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

except ImportError:
    # Standard library sqlite3 fallback for minimal python environments
    class MockBase:
        metadata = type("Meta", (), {"create_all": lambda *args, **kwargs: None})()

    Base = MockBase
    engine = None

    class SQLiteSession:
        def __init__(self, db_path=sqlite_path):
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self._ensure_tables()

        def _ensure_tables(self):
            cur = self.conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT,
                sender TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            cur.execute("""
            CREATE TABLE IF NOT EXISTS environmental_profiles (
                id TEXT PRIMARY KEY,
                conversation_id TEXT UNIQUE,
                region TEXT,
                latitude REAL,
                longitude REAL,
                land_use TEXT,
                crop_type TEXT,
                soil_ph REAL,
                soil_organic_carbon REAL,
                soil_moisture REAL,
                annual_rainfall_mm REAL,
                temperature_c REAL,
                habitat_type TEXT,
                species_richness INTEGER,
                vegetation_cover_percent REAL,
                water_availability TEXT,
                pollution_level TEXT,
                pesticide_usage TEXT,
                fertilizer_usage TEXT,
                deforestation_pressure TEXT,
                notes TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            cur.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id TEXT PRIMARY KEY,
                conversation_id TEXT,
                action TEXT,
                why_it_works TEXT,
                impacted_metrics TEXT,
                expected_direction TEXT,
                time_horizon TEXT,
                confidence TEXT,
                evidence_sources TEXT,
                tradeoffs TEXT,
                monitoring_plan TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
            cur.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_sources (
                id TEXT PRIMARY KEY,
                source_id TEXT UNIQUE,
                title TEXT,
                organization TEXT,
                year INTEGER,
                category TEXT,
                summary TEXT,
                doi_or_url TEXT,
                evidence_level TEXT
            )""")
            self.conn.commit()

        def add(self, obj):
            cur = self.conn.cursor()
            t_name = getattr(obj, "__tablename__", None)
            if not t_name:
                return
            cur.execute(f"PRAGMA table_info({t_name})")
            table_cols = [row[1] for row in cur.fetchall()]
            valid_cols = [c for c in table_cols if hasattr(obj, c) and getattr(obj, c) is not None]
            if not valid_cols:
                return
            placeholders = ", ".join(["?"] * len(valid_cols))
            col_names = ", ".join(valid_cols)
            vals = [getattr(obj, c) for c in valid_cols]
            cur.execute(f"INSERT OR REPLACE INTO {t_name} ({col_names}) VALUES ({placeholders})", vals)

        def commit(self):
            self.conn.commit()

        def refresh(self, obj):
            pass

        def delete(self, obj):
            cur = self.conn.cursor()
            t_name = getattr(obj, "__tablename__", None)
            obj_id = getattr(obj, "id", None)
            if t_name and obj_id:
                cur.execute(f"DELETE FROM {t_name} WHERE id = ?", (obj_id,))

        def rollback(self):
            self.conn.rollback()

        def close(self):
            self.conn.close()

        def query(self, model_cls):
            return SQLiteQuery(self.conn, model_cls)

    class SQLiteQuery:
        def __init__(self, conn, model_cls):
            self.conn = conn
            self.model_cls = model_cls
            self.t_name = getattr(model_cls, "__tablename__", "")
            self.filters = []

        def filter(self, expr):
            self.filters.append(expr)
            return self

        def first(self):
            cur = self.conn.cursor()
            query = f"SELECT * FROM {self.t_name}"
            params = []
            if self.filters:
                clauses = []
                for f in self.filters:
                    if isinstance(f, tuple) and len(f) == 2:
                        clauses.append(f"{f[0]} = ?")
                        params.append(f[1])
                if clauses:
                    query += " WHERE " + " AND ".join(clauses)
            cur.execute(query + " LIMIT 1", params)
            row = cur.fetchone()
            if not row:
                return None
            obj = self.model_cls()
            for k in row.keys():
                setattr(obj, k, row[k])
            return obj

        def count(self):
            cur = self.conn.cursor()
            cur.execute(f"SELECT COUNT(*) FROM {self.t_name}")
            return cur.fetchone()[0]

    def SessionLocal():
        return SQLiteSession()

    def get_db():
        db = SQLiteSession()
        try:
            yield db
        finally:
            db.close()

#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database.init_db import init_database
from app.database.connection import SessionLocal
from app.models.environmental import EnvironmentalProfile
from app.rag.ingest import ingest_knowledge_base
from app.rag.retriever import RAGRetriever
from app.services.environmental_reasoning import EnvironmentalReasoningEngine
from app.services.recommendation_service import RecommendationService
from app.services.citation_service import CitationService
from app.services.profile_service import ProfileService
from app.services.conversation_service import ConversationService

def run_system_verification():
    print("============================================================")
    print("DARUKAA.EARTH AI BIODIVERSITY SYSTEM VERIFICATION")
    print("============================================================")

    # 1. Database Initialization
    print("\n[1/7] Testing Database Layer...")
    init_database()
    db = SessionLocal()
    assert db is not None, "Database session failed to initialize"
    print("✓ Database initialized and seeded successfully.")

    # 2. Knowledge Ingestion
    print("\n[2/7] Testing RAG Ingestion Pipeline...")
    ingest_res = ingest_knowledge_base(force_reindex=False)
    assert ingest_res["chunks_indexed"] > 0 or ingest_res.get("total_store_count", 0) > 0
    print(f"✓ RAG Ingested {ingest_res.get('total_store_count')} chunks.")

    # 3. RAG Retrieval
    print("\n[3/7] Testing RAG Semantic Retrieval...")
    retriever = RAGRetriever()
    results = retriever.retrieve("soil organic carbon 0.3 semi-arid wheat monoculture", top_k=3)
    assert len(results) > 0, "RAG failed to retrieve relevant chunks"
    print(f"✓ Retrieved {len(results)} chunks. Top result: '{results[0]['title']}' (Score: {results[0]['score']})")

    # 4. Multi-Metric Reasoning & 3-Variable Validator
    print("\n[4/7] Testing Multi-Metric Reasoning Engine...")
    reasoning = EnvironmentalReasoningEngine()
    test_profile = EnvironmentalProfile(
        region="semi-arid",
        soil_organic_carbon=0.3,
        annual_rainfall_mm=420.0,
        land_use="agriculture",
        crop_type="wheat monoculture"
    )
    vars_used, interactions, uncertainties = reasoning.analyze_interactions(test_profile, results)
    is_valid_3var = reasoning.validate_three_variables(vars_used)
    print(f"Variables coupled: {vars_used}")
    print(f"Interactions found: {len(interactions)}")
    assert is_valid_3var, "3-variable validation failed on test profile"
    print(f"✓ 3-Variable Constraint PASSED: {len(vars_used)} variables coupled.")

    # 5. Recommendation Engine & Citation Validator
    print("\n[5/7] Testing Recommendation & Citation Validation...")
    citation_svc = CitationService()
    rec_svc = RecommendationService(citation_svc)
    recs, monitoring = rec_svc.generate_recommendations(test_profile, results, vars_used)
    assert len(recs) > 0, "Recommendation engine failed to produce recommendations"
    for r in recs:
        valid, val_srcs, _ = citation_svc.validate_citations(r.evidence, results)
        assert valid, f"Citation validation failed for {r.action}"
    print(f"✓ Generated {len(recs)} structured recommendations with {len(monitoring)} monitoring targets.")
    print(f"  Sample Action: '{recs[0].action}' ({recs[0].time_horizon}, Confidence: {recs[0].confidence})")

    # 6. Clarification Engine
    print("\n[6/7] Testing Clarification Engine on Sparse Input...")
    sparse_profile = ProfileService.extract_from_text("Biodiversity is declining on my land.")
    missing = ProfileService.detect_missing_variables(sparse_profile)
    questions = ProfileService.generate_clarifying_questions(missing)
    assert len(questions) >= 2, "Clarification engine did not ask sufficient questions"
    print(f"✓ Clarification Engine produced {len(questions)} targeted questions:")
    for q in questions:
        print(f"   - {q}")

    # 7. Conversational Memory & Merge
    print("\n[7/7] Testing Conversational Memory & Multi-turn Merge...")
    conv_svc = ConversationService(db)
    r1 = conv_svc.process_user_turn(None, "My farm is located in a semi-arid zone.")
    cid = r1.conversation_id
    r2 = conv_svc.process_user_turn(cid, "Annual rainfall is 420mm.")
    r3 = conv_svc.process_user_turn(cid, "Soil organic carbon is 0.3% and we cultivate wheat as a monoculture.")
    
    assert r3.has_analysis is True, "Conversation turn 3 failed to trigger analysis after variables were merged"
    assert r3.environmental_profile.soil_organic_carbon == 0.3
    assert r3.environmental_profile.annual_rainfall_mm == 420.0
    assert r3.environmental_profile.region == "semi-arid"
    print("✓ Conversational Memory retained all 3 parameters across sequential turns.")

    print("\n============================================================")
    print("ALL 7 SYSTEM SUBSYSTEM TESTS PASSED SUCCESSFULLY!")
    print("============================================================")
    db.close()

if __name__ == "__main__":
    run_system_verification()

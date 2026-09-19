import unittest
import json
from app.database.connection import SessionLocal
from app.services.conversation_service import ConversationService
from app.config import settings

class TestChatBot(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.service = ConversationService(self.db)

    def tearDown(self):
        self.db.close()

    def test_bot_sparse_site_triggers_clarification(self):
        """Test Case 1: Sparse site prompt must trigger clarifying questions rather than shallow advice."""
        result = self.service.process_user_turn(
            None,
            "I have noticed declining crop vigor and land degradation on my fields."
        )
        self.assertFalse(result.has_analysis)
        self.assertGreaterEqual(len(result.clarifying_questions), 2)
        self.assertGreater(len(result.missing_variables), 0)
        # Questions must ask about critical baseline variables
        questions_text = " ".join(result.clarifying_questions).lower()
        self.assertTrue("carbon" in questions_text or "rainfall" in questions_text or "crop" in questions_text)

    def test_bot_progressive_profile_accumulation(self):
        """Test Case 2: Multi-turn dialogue must incrementally accumulate variables into profile memory."""
        # Turn 1: Region & Biome
        r1 = self.service.process_user_turn(None, "I am operating in a semi-arid zone.")
        cid = r1.conversation_id
        
        # Turn 2: Rainfall parameter
        r2 = self.service.process_user_turn(cid, "Our average annual rainfall is around 420mm.")
        profile_t2 = r2.environmental_profile
        self.assertEqual(profile_t2.region, "semi-arid")
        self.assertEqual(profile_t2.annual_rainfall_mm, 420.0)

        # Turn 3: Topsoil SOC and cropping pattern
        r3 = self.service.process_user_turn(cid, "Our soil test showed SOC is 0.3% under wheat monoculture.")
        profile_t3 = r3.environmental_profile
        self.assertEqual(profile_t3.soil_organic_carbon, 0.3)
        self.assertTrue(r3.has_analysis)
        self.assertIsNotNone(r3.analysis)

    def test_bot_three_variable_rule_enforcement(self):
        """Test Case 3: Verify the reasoning engine connects at least 3 environmental variables."""
        prompt = "Managing dryland wheat monoculture in semi-arid region with 420mm rainfall and 0.3% soil organic carbon."
        res = self.service.process_user_turn(None, prompt)
        self.assertTrue(res.has_analysis)
        analysis = res.analysis
        self.assertGreaterEqual(len(analysis.variables_used_for_reasoning), 3)
        self.assertGreaterEqual(len(analysis.environmental_interactions), 1)
        interaction = analysis.environmental_interactions[0]
        self.assertGreaterEqual(len(interaction.variables), 3)

    def test_bot_pollinator_trophic_cascade(self):
        """Test Case 4: Verify agrochemical input coupled with pollinator decline triggers trophic assessment."""
        prompt = "We spray frequent pesticides and pyrethroids, and wild bees and pollinators have crashed."
        res = self.service.process_user_turn(None, prompt)
        profile = res.environmental_profile
        self.assertIn("frequent", profile.pesticide_usage)
        self.assertIsNotNone(profile.notes)

    def test_bot_citation_fidelity(self):
        """Test Case 5: Ensure every recommendation generated carries authoritative citations."""
        prompt = "Semi-arid wheat monoculture, annual rain 400mm, soil organic carbon 0.25%."
        res = self.service.process_user_turn(None, prompt)
        self.assertTrue(res.has_analysis)
        for rec in res.analysis.recommendations:
            self.assertGreater(len(rec.evidence), 0)
            self.assertIn(rec.confidence, ["HIGH", "MEDIUM", "LOW"])
            self.assertTrue(any(len(e) > 5 for e in rec.evidence))

    def test_bot_session_persistence_and_retrieval(self):
        """Test Case 6: Verify conversation state is persisted and retrievable by conversation ID."""
        r1 = self.service.process_user_turn(None, "Semi-arid farm with 450mm rainfall.")
        cid = r1.conversation_id
        loaded_conv, loaded_profile = self.service.get_or_create_conversation(cid)
        self.assertIsNotNone(loaded_conv)
        self.assertEqual(loaded_conv.id, cid)
        self.assertEqual(loaded_profile.region, "semi-arid")

    def test_bot_edge_cases(self):
        """Test Case 7: Gracefully handle empty string, whitespace, and special characters."""
        res_empty = self.service.process_user_turn(None, "   ")
        self.assertIsNotNone(res_empty.message)
        
        res_chars = self.service.process_user_turn(None, "!@#$%^&*()_+{}[]|:<>?")
        self.assertIsNotNone(res_chars.message)

if __name__ == "__main__":
    unittest.main()

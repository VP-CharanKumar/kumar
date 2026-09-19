import unittest
from app.database.connection import SessionLocal
from app.services.conversation_service import ConversationService
from app.services.profile_service import ProfileService

class TestConversationService(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.service = ConversationService(self.db)

    def tearDown(self):
        self.db.close()

    def test_progressive_profile_building(self):
        # Turn 1: Sparse statement (insufficient variables)
        res1 = self.service.process_user_turn(None, "I am concerned about ecosystem degradation and declining soil health on my land.")
        self.assertFalse(res1.has_analysis)
        self.assertGreaterEqual(len(res1.clarifying_questions), 2)
        cid = res1.conversation_id

        # Turn 2: Add region and rainfall
        res2 = self.service.process_user_turn(cid, "The site is located in a semi-arid zone with 420mm annual precipitation.")
        
        # Turn 3: Add soil organic carbon and crop
        res3 = self.service.process_user_turn(cid, "Tested soil organic carbon at 0.3% with continuous wheat monoculture.")
        self.assertTrue(res3.has_analysis)
        self.assertIsNotNone(res3.analysis)
        self.assertGreaterEqual(len(res3.analysis.variables_used_for_reasoning), 3)

    def test_clarifying_question_generation(self):
        profile = ProfileService.extract_from_text("My crops are struggling.")
        missing = ProfileService.detect_missing_variables(profile)
        questions = ProfileService.generate_clarifying_questions(missing)
        self.assertGreaterEqual(len(questions), 2)
        self.assertLessEqual(len(questions), 4)

if __name__ == "__main__":
    unittest.main()

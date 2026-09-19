import unittest
from app.services.citation_service import CitationService

class TestCitationValidator(unittest.TestCase):
    def setUp(self):
        self.service = CitationService()

    def test_canonical_sources_loaded(self):
        self.assertGreaterEqual(len(self.service.canonical_sources), 8, "Must load canonical scientific sources")

    def test_insufficient_evidence_refusal(self):
        # When no chunks are retrieved, must return clear insufficient evidence notice
        is_valid, sources, msg = self.service.validate_citations(["FAO Soil Manual"], [])
        self.assertFalse(is_valid)
        self.assertIn("insufficient", msg.lower())

    def test_valid_citation_matching(self):
        mock_chunks = [{
            "chunk_id": "chunk_1",
            "title": "Soil Health & Carbon Sequestration",
            "category": "soil_science",
            "content": "FAO (2020) Recarbonizing Global Soils reports that organic cover enhances moisture."
        }]
        is_valid, validated, msg = self.service.validate_citations(["FAO Recarbonizing Global Soils"], mock_chunks)
        self.assertTrue(is_valid)
        self.assertGreaterEqual(len(validated), 1)

if __name__ == "__main__":
    unittest.main()

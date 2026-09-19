import unittest
import urllib.request
import json
import os

class TestApiEndpoints(unittest.TestCase):
    BASE_URL = "http://localhost:3000"

    def test_01_health_endpoint(self):
        """Verify GET /api/health returns 200 OK and valid status."""
        req = urllib.request.Request(f"{self.BASE_URL}/api/health")
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertEqual(data.get("status"), "healthy")
            self.assertGreater(data.get("rag_chunks_indexed", 0), 0)

    def test_02_knowledge_search_endpoint(self):
        """Verify GET /api/knowledge/search returns matching scientific chunks."""
        req = urllib.request.Request(f"{self.BASE_URL}/api/knowledge/search?query=agroforestry")
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            results = json.loads(response.read().decode())
            self.assertIsInstance(results, list)
            self.assertGreater(len(results), 0)
            self.assertTrue(any("agroforestry" in r.get("title", "").lower() or "agroforestry" in r.get("content", "").lower() for r in results))

    def test_03_chat_sparse_triggers_clarification(self):
        """Verify POST /api/chat with sparse input returns clarifying questions."""
        payload = json.dumps({"message": "My crop yield is falling."}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.BASE_URL}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertIn("clarifying_questions", data)
            self.assertGreaterEqual(len(data["clarifying_questions"]), 2)

    def test_04_chat_three_variable_triggers_analysis(self):
        """Verify POST /api/chat with 3 coupled variables triggers full multi-metric analysis."""
        payload = json.dumps({
            "message": "Farmland in semi-arid region with 420mm rainfall. Soil organic carbon is 0.3% under wheat monoculture."
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.BASE_URL}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode())
            self.assertTrue(data.get("has_analysis"))
            analysis = data.get("analysis")
            self.assertIsNotNone(analysis)
            self.assertGreaterEqual(len(analysis.get("recommendations", [])), 1)
            self.assertGreaterEqual(len(analysis.get("environmental_interactions", [])), 1)

    def test_05_docx_submission_download(self):
        """Verify GET /api/submission/docx serves the real DOCX binary document."""
        req = urllib.request.Request(f"{self.BASE_URL}/api/submission/docx")
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            content_type = response.headers.get("Content-Type")
            self.assertIn("openxmlformats-officedocument", content_type)
            content = response.read()
            self.assertGreater(len(content), 10000)
            # Verify PK zip magic bytes (DOCX is a zip archive)
            self.assertEqual(content[:2], b"PK")

    def test_06_zip_submission_download(self):
        """Verify GET /api/submission/zip serves the full source archive."""
        req = urllib.request.Request(f"{self.BASE_URL}/api/submission/zip")
        with urllib.request.urlopen(req) as response:
            self.assertEqual(response.status, 200)
            content_type = response.headers.get("Content-Type")
            self.assertIn("zip", content_type)
            content = response.read()
            self.assertGreater(len(content), 50000)
            self.assertEqual(content[:2], b"PK")

if __name__ == "__main__":
    unittest.main()

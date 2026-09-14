from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StaticSafetyTests(unittest.TestCase):
    def test_incident_source_links_allow_only_http_https(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("function safeHttpUrl", html)
        self.assertIn("u.protocol==='http:'||u.protocol==='https:'", html)
        self.assertIn("sourceUrl=safeHttpUrl(e?.source?.url)", html)
        self.assertIn('rel="noopener noreferrer"', html)

    def test_snapshot_query_parameters_stay_same_origin(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("function safeSnapshotUrl", html)
        self.assertIn("u.origin!==location.origin", html)
        self.assertIn("safeSnapshotUrl(params.get('feed'),'verified.jsonl')", html)
        self.assertIn("safeSnapshotUrl(params.get('alerts'),'alerts.jsonl')", html)
        self.assertIn("MAX_SNAPSHOT_BYTES=5*1024*1024", html)
        self.assertIn("credentials:'same-origin'", html)

    def test_coordinator_surface_is_labelled_correctly(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Coordinator incident console", html)
        self.assertNotIn("<small>Volunteer field view</small>", html)

    def test_offline_map_has_local_style_fallback(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("const offlineStyle=", html)
        self.assertIn("style:navigator.onLine?", html)

    def test_volunteer_surface_is_present(self):
        html = (ROOT / "volunteer.html").read_text(encoding="utf-8")
        self.assertIn("worksite", html.lower())
        self.assertIn("assigned", html.lower())


if __name__ == "__main__":
    unittest.main()

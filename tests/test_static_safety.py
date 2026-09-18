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

    def test_incident_map_accepts_validated_area_geometry(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("function validPosition", html)
        self.assertIn("function validRing", html)
        self.assertIn("g?.type==='Polygon'", html)
        self.assertIn("g?.type==='MultiPolygon'", html)
        self.assertIn("id:'event-areas'", html)
        self.assertIn("id:'event-area-outline'", html)
        self.assertIn("geometryOf(e)", html)
        self.assertIn("Math.abs(lat)<=90&&Math.abs(lon)<=180", html)
        self.assertIn("ring[0][0]!==ring[ring.length-1][0]", html)

    def test_area_geometry_is_used_for_metrics_distance_and_bounds(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("allEvents.filter(e=>geometryOf(e)).length", html)
        self.assertIn("distanceKm(userLocation,geometryCenter(e))", html)
        self.assertIn("geometryPositions(f.geometry)", html)
        self.assertIn("focusEventGeometry(e)", html)

    def test_area_center_handles_antimeridian_wrapping(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("function wrappedLongitudeCenter", html)
        self.assertIn("largestGap", html)
        self.assertIn("const lon=wrappedLongitudeCenter(points)", html)
        self.assertIn("function positionsForBounds", html)
        self.assertIn("const bounded=positionsForBounds(points)", html)
        self.assertIn("bounded.forEach(p=>b.extend(p))", html)
        self.assertNotIn("(minLon+maxLon)/2", html)

    def test_volunteer_surface_is_public_snapshot_only(self):
        html = (ROOT / "volunteer.html").read_text(encoding="utf-8")
        self.assertIn("privacy-minimised public worksite snapshot", html)
        self.assertIn("function safeSnapshotUrl", html)
        self.assertIn("u.origin!==location.origin", html)
        self.assertIn("MAX_SNAPSHOT_BYTES=5*1024*1024", html)
        self.assertIn("credentials:'same-origin'", html)
        self.assertIn("crisisweave:last-worksites-public", html)
        self.assertNotIn("q.get('api')", html)
        self.assertNotIn("Live operational API", html)
        self.assertNotIn("coordinator_instructions", html)
        self.assertNotIn("assigned_team", html)

    def test_volunteer_geometry_is_bounded(self):
        html = (ROOT / "volunteer.html").read_text(encoding="utf-8")
        self.assertIn("Math.abs(lon)<=180&&Math.abs(lat)<=90", html)


if __name__ == "__main__":
    unittest.main()

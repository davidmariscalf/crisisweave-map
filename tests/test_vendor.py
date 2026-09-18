from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VendorPackagingTests(unittest.TestCase):
    def test_maplibre_package_is_pinned_and_integrity_checked(self):
        source = (ROOT / "vendor_maplibre.py").read_text(encoding="utf-8")
        self.assertIn('MAPLIBRE_VERSION = "5.6.1"', source)
        self.assertIn("PACKAGE_SHA512", source)
        self.assertIn("hashlib.sha512", source)
        self.assertIn("actual != PACKAGE_SHA512", source)
        self.assertIn('"package/dist/maplibre-gl.js"', source)
        self.assertIn('"package/dist/maplibre-gl.css"', source)
        self.assertIn('"package/LICENSE.txt"', source)


if __name__ == "__main__":
    unittest.main()

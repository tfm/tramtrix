import unittest
import os
from tramtrix.ojp import OJPApiClient
from tramtrix.config import OJP_API_KEY

class TestOJPApiClientIntegration(unittest.TestCase):
    def setUp(self):
        if not OJP_API_KEY:
            self.skipTest("OJP_API_KEY not set in environment")
        self.client = OJPApiClient()

    def test_resolve_stop_ref_real_api(self):
        """
        Integration test: Actually calls the API to resolve 'Zürich, Heuried'.
        """
        print("\n[Integration] Resolving 'Zürich, Heuried'...")
        stop_ref = self.client.resolve_stop_ref("Zürich, Heuried")
        print(f"[Integration] Resolved to: {stop_ref}")
        
        # We expect the stable ID for Heuried
        self.assertEqual(stop_ref, "8591190")

    def test_get_trip_results_real_api(self):
        """
        Integration test: Actually calls the API for trips between Heuried and Stauffacher.
        """
        stop_ref_origin = "8591190"  # Heuried
        stop_ref_destination = "8591381" # Stauffacher
        
        print("\n[Integration] Fetching trips...")
        results = self.client.get_trip_results(stop_ref_origin, stop_ref_destination)
        
        # We can't guarantee there are trams running (e.g. at 3 AM), but we can check the structure
        # If it returns a dict (empty or not), the parsing succeeded.
        self.assertIsInstance(results, dict)
        
        if results:
            print(f"[Integration] Found trips for lines: {list(results.keys())}")
        else:
            print("[Integration] No trips found (might be late night).")

if __name__ == "__main__":
    unittest.main()

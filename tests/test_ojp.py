import unittest
from unittest.mock import patch, MagicMock
from tramtrix.ojp import OJPApiClient
from datetime import datetime

class TestOJPApiClient(unittest.TestCase):
    def setUp(self):
        self.client = OJPApiClient(api_key="test_key", url="http://test.url")

    @patch("tramtrix.ojp.requests.post")
    def test_resolve_stop_ref_success_stop_point(self, mock_post):
        # Mock XML response with StopPointRef
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <OJP xmlns:siri="http://www.siri.org.uk/siri" xmlns:ojp="http://www.vdv.de/ojp">
            <OJPResponse>
                <siri:ServiceDelivery>
                    <OJPLocationInformationDelivery>
                        <PlaceResult>
                            <Place>
                                <StopPoint>
                                    <ojp:StopPointRef>8591341</ojp:StopPointRef>
                                </StopPoint>
                            </Place>
                        </PlaceResult>
                    </OJPLocationInformationDelivery>
                </siri:ServiceDelivery>
            </OJPResponse>
        </OJP>
        """
        mock_post.return_value = mock_response

        # Call method
        result = self.client.resolve_stop_ref("Schmiede Wiedikon")

        # Assertions
        self.assertEqual(result, "8591341")
        mock_post.assert_called_once()
    
    @patch("tramtrix.ojp.requests.post")
    def test_resolve_stop_ref_success_stop_place(self, mock_post):
        # Mock XML response with StopPlaceRef (alternative)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <OJP xmlns:siri="http://www.siri.org.uk/siri" xmlns:ojp="http://www.vdv.de/ojp">
            <OJPResponse>
                <siri:ServiceDelivery>
                    <OJPLocationInformationDelivery>
                        <PlaceResult>
                            <Place>
                                <StopPlace>
                                    <ojp:StopPlaceRef>8591381</ojp:StopPlaceRef>
                                </StopPlace>
                            </Place>
                        </PlaceResult>
                    </OJPLocationInformationDelivery>
                </siri:ServiceDelivery>
            </OJPResponse>
        </OJP>
        """
        mock_post.return_value = mock_response

        result = self.client.resolve_stop_ref("Stauffacher")
        self.assertEqual(result, "8591381")

    @patch("tramtrix.ojp.requests.post")
    def test_resolve_stop_ref_not_found(self, mock_post):
        # Mock empty/invalid response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<OJP></OJP>"
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.client.resolve_stop_ref("Unknown Stop")
        
        self.assertIn("Could not resolve stop reference", str(context.exception))

    @patch("tramtrix.ojp.requests.post")
    def test_resolve_stop_ref_api_error(self, mock_post):
        # Mock 500 status
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.client.resolve_stop_ref("Error Stop")
        
        self.assertIn("API call failed", str(context.exception))

    @patch("tramtrix.ojp.requests.post")
    def test_get_trip_results_success(self, mock_post):
        # Mock TripRequest response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <OJP xmlns:siri="http://www.siri.org.uk/siri" xmlns:ojp="http://www.vdv.de/ojp">
            <OJPResponse>
                <siri:ServiceDelivery>
                    <OJPTripDelivery>
                        <ojp:TripResult>
                            <ojp:Trip>
                                <ojp:Leg>
                                    <ojp:Service>
                                        <ojp:PublishedServiceName>
                                            <ojp:Text>9</ojp:Text>
                                        </ojp:PublishedServiceName>
                                    </ojp:Service>
                                    <ojp:LegBoard>
                                        <ojp:ServiceDeparture>
                                            <ojp:EstimatedTime>2026-01-06T12:00:00Z</ojp:EstimatedTime>
                                        </ojp:ServiceDeparture>
                                    </ojp:LegBoard>
                                </ojp:Leg>
                            </ojp:Trip>
                        </ojp:TripResult>
                        <ojp:TripResult>
                            <ojp:Trip>
                                <ojp:Leg>
                                    <ojp:Service>
                                        <ojp:PublishedServiceName>
                                            <ojp:Text>14</ojp:Text>
                                        </ojp:PublishedServiceName>
                                    </ojp:Service>
                                    <ojp:LegBoard>
                                        <ojp:ServiceDeparture>
                                            <ojp:EstimatedTime>2026-01-06T12:05:00Z</ojp:EstimatedTime>
                                        </ojp:ServiceDeparture>
                                    </ojp:LegBoard>
                                </ojp:Leg>
                            </ojp:Trip>
                        </ojp:TripResult>
                    </OJPTripDelivery>
                </siri:ServiceDelivery>
            </OJPResponse>
        </OJP>
        """
        mock_post.return_value = mock_response

        results = self.client.get_trip_results("REF_A", "REF_B")

        # Verify results
        self.assertIn("9", results)
        self.assertIn("14", results)
        
        # Check parsed time (should be datetime)
        self.assertEqual(len(results["9"]), 1)
        dt_9 = list(results["9"])[0]
        self.assertIsInstance(dt_9, datetime)
        # 12:00 UTC
        self.assertEqual(dt_9.hour, 12)
        self.assertEqual(dt_9.minute, 0)

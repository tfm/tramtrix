import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from .config import OJP_API_KEY, OJP_URL

class OJPApiClient:
    def __init__(self, api_key=OJP_API_KEY, url=OJP_URL):
        self.api_key = api_key
        self.url = url
        self.headers = {
            "Content-Type": "application/xml",
            "Accept": "application/xml",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.namespaces = {
            "ojp": "http://www.vdv.de/ojp",
            "siri": "http://www.siri.org.uk/siri",
        }

    def get_trip_results(self, stop_ref_origin, stop_ref_destination):
        now_iso = datetime.now(timezone.utc).isoformat()
        
        request_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<OJP xmlns="http://www.vdv.de/ojp" xmlns:siri="http://www.siri.org.uk/siri" version="2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.vdv.de/ojp OJP_changes_for_v1.1/OJP.xsd">
    <OJPRequest>
        <siri:ServiceRequest>
            <siri:RequestTimestamp>{now_iso}</siri:RequestTimestamp>
            <siri:RequestorRef>MENTZRegTest</siri:RequestorRef>
            <OJPTripRequest>
                <siri:RequestTimestamp>{now_iso}</siri:RequestTimestamp>
                <siri:MessageIdentifier>TR-1h2</siri:MessageIdentifier>
                <Origin>
                    <PlaceRef>
                        <siri:StopPointRef>{stop_ref_origin}</siri:StopPointRef>
                    </PlaceRef>
                </Origin>
                <Destination>
                    <PlaceRef>
                        <siri:StopPointRef>{stop_ref_destination}</siri:StopPointRef>
                    </PlaceRef>
                </Destination>
                <Params>
                    <ModeAndModeOfOperationFilter>
                        <Exclude>false</Exclude>
                        <PtMode>tram</PtMode>
                    </ModeAndModeOfOperationFilter>
                    <NumberOfResults>10</NumberOfResults>
                </Params>
            </OJPTripRequest>
        </siri:ServiceRequest>
    </OJPRequest>
</OJP>
"""

        response = requests.post(self.url, headers=self.headers, data=request_body)

        if response.status_code != 200:
            raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

        return self._parse_response(response.text)

    def _parse_response(self, xml_text):
        root = ET.fromstring(xml_text)
        trip_results = {}
        
        for trip_result in root.findall(".//ojp:TripResult", self.namespaces):
            # Parse individual trip legs keyed by PublishedServiceName
            for leg in trip_result.findall(".//ojp:Leg", self.namespaces):
                published_service_name_element = leg.find(".//ojp:PublishedServiceName", self.namespaces)
                published_service_name = None
                if published_service_name_element is not None:
                    published_service_name = published_service_name_element.findtext("ojp:Text", namespaces=self.namespaces)

                estimated_time_text = leg.findtext(".//ojp:EstimatedTime", namespaces=self.namespaces)
                estimated_time_text_iso = estimated_time_text.replace("Z", "+00:00") if estimated_time_text else None
                estimated_time = datetime.fromisoformat(estimated_time_text_iso) if estimated_time_text else None

                if published_service_name and estimated_time:
                    if published_service_name not in trip_results:
                        trip_results[published_service_name] = set()
                    trip_results[published_service_name].add(estimated_time)
        
        return trip_results

    def resolve_stop_ref(self, stop_name):
        """
        Resolves a stop name to a StopPointRef using OJP LocationInformationRequest.
        :param stop_name: The name of the stop to resolve.
        :return: The StopPointRef string.
        :raises Exception: If the stop cannot be found.
        """
        now_iso = datetime.now(timezone.utc).isoformat()
        
        request_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<OJP xmlns="http://www.vdv.de/ojp" xmlns:siri="http://www.siri.org.uk/siri" version="2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.vdv.de/ojp OJP_changes_for_v1.1/OJP.xsd">
    <OJPRequest>
        <siri:ServiceRequest>
            <siri:RequestTimestamp>{now_iso}</siri:RequestTimestamp>
            <siri:RequestorRef>MENTZRegTest</siri:RequestorRef>
            <OJPLocationInformationRequest>
                <siri:RequestTimestamp>{now_iso}</siri:RequestTimestamp>
                <siri:MessageIdentifier>LIR-001</siri:MessageIdentifier>
                <InitialInput>
                    <Name>{stop_name}</Name>
                </InitialInput>
                <Restrictions>
                    <Type>stop</Type>
                    <NumberOfResults>1</NumberOfResults>
                </Restrictions>
            </OJPLocationInformationRequest>
        </siri:ServiceRequest>
    </OJPRequest>
</OJP>
"""
        response = requests.post(self.url, headers=self.headers, data=request_body)

        if response.status_code != 200:
            raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

        # Parse response
        root = ET.fromstring(response.text)
        
        # Look for StopPlaceRef (or StopPointRef)
        stop_place_ref = root.findtext(".//ojp:StopPlaceRef", namespaces=self.namespaces)
        stop_point_ref = root.findtext(".//ojp:StopPointRef", namespaces=self.namespaces)
        
        ref = stop_place_ref or stop_point_ref
        
        if not ref:
            print(f"DEBUG: Response for {stop_name}:\n{response.text}")
            raise Exception(f"Could not resolve stop reference for '{stop_name}'")
            
        return ref

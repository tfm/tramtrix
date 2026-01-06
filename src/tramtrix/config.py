import os
from dotenv import load_dotenv

load_dotenv()

OJP_API_KEY = os.getenv("OJP_API_KEY")
OJP_URL = os.getenv("OJP_URL", "https://api.opentransportdata.swiss/ojp20")
AWTRIX_URL = os.getenv("AWTRIX_URL")


# Configuration for the stop
# Configuration for the stop
# Canonical stop names can be found at https://www.fahrplanfelder.ch/ or on SBB.ch
STOP_NAME_ORIGIN = os.getenv("STOP_NAME_ORIGIN", "Zürich, Heuried")
STOP_NAME_DESTINATION = os.getenv("STOP_NAME_DESTINATION", "Zürich, Stauffacher")

# List of tram lines to monitor
# Defaults to "9,14" if not specified
TRAM_LINES = [x.strip() for x in os.getenv("TRAM_LINES", "9,14").split(",") if x.strip()]

# Traffic light time rules (in minutes)
# Green window: TIME_AMBER_MAX < t <= TIME_GREEN_MAX
TIME_GREEN_MAX = int(os.getenv("TIME_GREEN_MAX", "6"))

# Amber window: TIME_AMBER_MIN <= t <= TIME_AMBER_MAX
# NOTE: TIME_AMBER_MAX is the boundary between Green and Amber
TIME_AMBER_MAX = int(os.getenv("TIME_AMBER_MAX", "3"))

# Below TIME_AMBER_MIN is too late (Red)
TIME_AMBER_MIN = int(os.getenv("TIME_AMBER_MIN", "2"))

# Update interval in seconds
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "60"))


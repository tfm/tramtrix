# Tramtrix

An Awtrix 3 application for a [Ulanzi clock](https://www.ulanzi.com/collections/clock/products/ulanzi-pixel-smart-clock-2882) to show upcoming tram departures using a traffic lights scheme to tell you whether it's a good time to leave home for the numbered tram:

- Green: there's a tram coming soon and you have a good amount of time, you'll be fine if you leave now
- Amber: hurry up, you'll just about make it!
- Red: you don't have enough time to make a tram that's arriving soon, or there's not one for a while

Here's an example for the trams number 9 and 14:

![Screenshot of display](example.png)

## Setup

1.  Get an API key from https://api-manager.opentransportdata.swiss/
2.  Clone the repository.
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file with your config:
    ```bash
    OJP_API_KEY="your_api_key_here"
    OJP_URL="https://api.opentransportdata.swiss/ojp20"
    AWTRIX_URL="http://myclock/api/custom?name=myapp"
    
    # Change to your start and end tram stop, and the lines you're 
    # interested in
    STOP_NAME_ORIGIN="Zürich, Heuried"
    STOP_NAME_DESTINATION="Zürich, Stauffacher"
    TRAM_LINES="9,14"
    
    # Traffic Light Rules (Minutes)
    TIME_GREEN_MAX=6
    TIME_AMBER_MAX=3
    TIME_AMBER_MIN=2
    
    # Update Interval (Seconds)
    UPDATE_INTERVAL=60
    ```
    
    > **Note:** Canonical stop names can be found on [SBB.ch](https://www.sbb.ch) or [Fahrplanfelder.ch](https://www.fahrplanfelder.ch/). The application automatically resolves valid stop names to their IDs at startup.

## Usage

Run the script:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src && python3 -m tramtrix.main
```

The application will:
1.  Resolve the configured stop names to IDs.
2.  Enter a loop, fetching data every `UPDATE_INTERVAL` seconds.
3.  Calculate the "Traffic Light" status for each tram line.
4.  Update your Awtrix clock.

## Testing

Run unit tests:
```bash
python3 -m unittest discover tests
```

Run integration tests (requires valid API Key):
```bash
python3 -m unittest tests/test_ojp_integration.py
```

## Structure

-   `src/tramtrix/main.py`: Entry point and main loop.
-   `src/tramtrix/ojp.py`: Handles communication with the Open Transport Data Swiss API (OJP 2.0).
-   `src/tramtrix/awtrix.py`: Handles communication with the Awtrix clock.
-   `src/tramtrix/traffic_light.py`: Traffic light colour calcaulations.
-   `src/tramtrix/config.py`: Configuration management via `python-dotenv`.

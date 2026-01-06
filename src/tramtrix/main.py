from .ojp import OJPApiClient
from .awtrix import AwtrixClient
from .traffic_light import calculate_traffic_light_colour, to_hex_color
from .config import (
    OJP_API_KEY, TRAM_LINES,
    STOP_NAME_ORIGIN, STOP_NAME_DESTINATION,
    UPDATE_INTERVAL
)
import sys
import time
from datetime import datetime, timezone

def main():
    if not OJP_API_KEY:
        print("Error: OJP_API_KEY environment variable is not set.")
        sys.exit(1)

    try:
        client = OJPApiClient()
        clock = AwtrixClient()

        print(f"Resolving StopPointRef for '{STOP_NAME_ORIGIN}'...")
        stop_ref_origin = client.resolve_stop_ref(STOP_NAME_ORIGIN)
        print(f"Found: {stop_ref_origin}")

        print(f"Resolving StopPointRef for '{STOP_NAME_DESTINATION}'...")
        stop_ref_destination = client.resolve_stop_ref(STOP_NAME_DESTINATION)
        print(f"Found: {stop_ref_destination}")

        print(f"Starting Tramtrix loop (Interval: {UPDATE_INTERVAL}s)")
        while True:
            try:
                print("Fetching tram data...")
                results = client.get_trip_results(
                    stop_ref_origin=stop_ref_origin,
                    stop_ref_destination=stop_ref_destination
                )
                
                line_colors = {}
                now = datetime.now(timezone.utc)
                for line in TRAM_LINES:
                    times = results.get(line, set())
                    status = calculate_traffic_light_colour(times)
                    color = to_hex_color(status)
                    line_colors[line] = color
                    
                    # Calculate minutes until next trams for debug
                    deltas = []
                    for t in times:
                        diff_min = (t - now).total_seconds() / 60
                        deltas.append(f"{diff_min:.1f}m")
                    deltas_str = ", ".join(sorted(deltas))

                    print(f"Line {line}: {status} ({color}) | Next: [{deltas_str}]")
                
                print("Updating clock...")
                clock.update_clock(line_colors)
                print("Done. Sleeping...")
                
                time.sleep(UPDATE_INTERVAL)

            except Exception as e:
                print(f"Error in loop: {e}")
                time.sleep(UPDATE_INTERVAL)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

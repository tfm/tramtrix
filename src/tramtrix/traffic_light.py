from datetime import datetime, timezone
from .config import TIME_GREEN_MAX, TIME_AMBER_MAX, TIME_AMBER_MIN

def calculate_traffic_light_colour(datetime_set):
    """
    Checks a set of datetimes against the current time and returns a status.
    
    :param datetime_set: A set of datetime objects
    :return: "GREEN" if any datetime is within the Green window,
             "AMBER" if none are Green but any are within the Amber window,
             otherwise "RED".
    """
    now = datetime.now(timezone.utc)
    found_green = False
    found_amber = False
    
    if not datetime_set:
        return "RED"

    for dt in datetime_set:
        # Calculate the time difference in seconds
        time_diff = (dt - now).total_seconds()
        
        abs_diff = abs(time_diff)
        
        # Green: 3 < t <= 6
        if abs_diff <= TIME_GREEN_MAX * 60 and abs_diff > TIME_AMBER_MAX * 60:
            found_green = True
        
        # Amber: 2 <= t <= 3
        if abs_diff <= TIME_AMBER_MAX * 60 and abs_diff >= TIME_AMBER_MIN * 60:
            found_amber = True
    
    # Determine the status
    if found_green:
        return "GREEN"
    elif found_amber:
        return "AMBER"
    else:
        return "RED"

def to_hex_color(color):
    if color == 'RED':
        return "a83632"
    elif color == 'GREEN':
        return "03fc14"
    elif color == 'AMBER':
        return "fcca03"
    else:
        return "ffffff"

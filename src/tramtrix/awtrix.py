import requests
from string import Template
from .config import AWTRIX_URL

class AwtrixClient:
    def __init__(self, url=AWTRIX_URL):
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
        }

    def update_clock(self, line_colors):
        """
        Updates the clock with the given line colors.
        :param line_colors: Dictionary of line number (str) to hex color (str)
                            e.g. {'9': 'a83632', '14': '03fc14'}
        """
        text_elements = []
        for line, color in line_colors.items():
            text_elements.append({
                "t": f"{line} ",  # Adding a space for visual separation
                "c": color
            })

        payload = {
            "text": text_elements,
            "repeat": 1
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=5)
            if response.status_code != 200:
                print(f"Warning: Clocky API call failed with status code {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not connect to Clocky: {e}")


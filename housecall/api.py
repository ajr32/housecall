"""
HouseCall - Home Assistant Inventory & Analysis Tool

Communicates with the Home Assistant REST API.
"""

import requests

from .config import HA_TOKEN, HA_URL


class HomeAssistantClient:
    """Simple client for the Home Assistant REST API."""

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json",
        })

    def get(self, endpoint):
        """Retrieve data from a Home Assistant API endpoint."""

        response = self.session.get(
            f"{HA_URL}{endpoint}",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()


client = HomeAssistantClient()


def get_config():
    return client.get("/api/config")


def get_states():
    return client.get("/api/states")
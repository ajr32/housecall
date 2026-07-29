"""
HouseCall - Home Assistant Inventory & Analysis Tool

Communicates with the Home Assistant REST API.
"""

import requests

from .config import HA_TOKEN, HA_URL
from .settings import settings
from .exceptions import APIError

class HomeAssistantClient:
    """
    Wrapper around the Home Assistant REST API.

    Manages authentication, HTTP requests, and connection handling.
    """

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json",
        })

    def test_connection(self):
        """Verify that Home Assistant is reachable."""

        self.get("/api/")

    def get(self, endpoint):
        """Retrieve data from a Home Assistant API endpoint."""

        try:
            response = self.session.get(
                f"{HA_URL}{endpoint}",
                timeout=settings.request_timeout,
            )

            response.raise_for_status()

        except requests.exceptions.ConnectionError:
            raise APIError(
                "Unable to connect to Home Assistant."
            )

        except requests.exceptions.HTTPError as exc:
            raise APIError(
                f"Authentication failed ({exc.response.status_code})."
            )

        return response.json()

def post(self, endpoint, data=None):
    """Send data to a Home Assistant API endpoint."""

    response = self.session.post(
        f"{HA_URL}{endpoint}",
        json=data,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def put(self, endpoint, data=None):
    """Update data through a Home Assistant API endpoint."""

    response = self.session.put(
        f"{HA_URL}{endpoint}",
        json=data,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def delete(self, endpoint):
    """Delete data through a Home Assistant API endpoint."""

    response = self.session.delete(
        f"{HA_URL}{endpoint}",
        timeout=30,
    )

    response.raise_for_status()

client = HomeAssistantClient()


def get_config():
    return client.get("/api/config")


def get_states():
    return client.get("/api/states")
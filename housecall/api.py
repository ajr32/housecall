"""
HouseCall - Home Assistant Inventory & Analysis Tool

Communicates with the Home Assistant REST API.
"""

import requests

from .config import HA_TOKEN, HA_URL
from .exceptions import APIError
from .settings import settings


class HomeAssistantClient:
    """Communicate with Home Assistant."""

    API_ROOT = "/api"
    STATES_ENDPOINT = "/api/states"
    CONFIG_ENDPOINT = "/api/config"
    SERVICES_ENDPOINT = "/api/services"

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update(
            {
                "Authorization": f"Bearer {HA_TOKEN}",
                "Content-Type": "application/json",
            }
        )

    def test_connection(self):
        """Verify that Home Assistant is reachable."""

        self.get(self.API_ROOT)

    def get_states(self):
        """Retrieve all Home Assistant entity states."""

        return self.get(self.STATES_ENDPOINT)

    def get(self, endpoint):
        """Retrieve data from a Home Assistant API endpoint."""

        try:
            response = self.session.get(
                f"{HA_URL}{endpoint}",
                timeout=settings.request_timeout,
            )

            response.raise_for_status()

        except requests.exceptions.ConnectionError:
            raise APIError("Unable to connect to Home Assistant.")

        except requests.exceptions.HTTPError as exc:
            raise APIError(f"Authentication failed ({exc.response.status_code}).")

        return response.json()

    def get_config(self):
        """Retrieve Home Assistant configuration."""

        return self.get(self.CONFIG_ENDPOINT)

    def get_services(self):
        """Retrieve Home Assistant services."""

        return self.get(self.SERVICES_ENDPOINT)

    def post(self, endpoint, data=None):
        """Send data to a Home Assistant API endpoint."""

        response = self.session.post(
            f"{HA_URL}{endpoint}",
            json=data,
            timeout=settings.request_timeout,
        )

        response.raise_for_status()

        return response.json()

    def put(self, endpoint, data=None):
        """Update data through a Home Assistant API endpoint."""

        response = self.session.put(
            f"{HA_URL}{endpoint}",
            json=data,
            timeout=settings.request_timeout,
        )

        response.raise_for_status()

        return response.json()

    def delete(self, endpoint):
        """Delete data through a Home Assistant API endpoint."""

        response = self.session.delete(
            f"{HA_URL}{endpoint}",
            timeout=settings.request_timeout,
        )

        response.raise_for_status()

        return response.json()


client = HomeAssistantClient()


def get_config():
    return client.get_config()


def get_states():
    return client.get_states()

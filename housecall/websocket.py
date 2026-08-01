"""
Communicate with the Home Assistant WebSocket API.
"""

import json

from websocket import create_connection

from .config import HA_TOKEN, HA_URL
from .exceptions import APIError

# ============================================================================
# Home Assistant WebSocket Client
# ============================================================================


class HomeAssistantWebSocketClient:
    """Communicate with Home Assistant via WebSocket."""

    def __init__(self):
        ws_url = HA_URL.replace(
            "http://",
            "ws://",
        ).replace(
            "https://",
            "wss://",
        )

        self.url = f"{ws_url}/api/websocket"
        self.ws = None
        self.message_id = 1

    # ------------------------------------------------------------------------
    # Connection Management
    # ------------------------------------------------------------------------

    def connect(self):
        """Connect and authenticate."""

        self.ws = create_connection(self.url)

        # Receive auth_required
        self.ws.recv()

        self.ws.send(
            json.dumps(
                {
                    "type": "auth",
                    "access_token": HA_TOKEN,
                }
            )
        )

        response = json.loads(self.ws.recv())

        if response["type"] != "auth_ok":
            raise APIError("Authentication failed.")

    def close(self):
        """Close the websocket."""

        if self.ws:
            self.ws.close()

    # ------------------------------------------------------------------------
    # Generic Commands
    # ------------------------------------------------------------------------

    def send(self, command):
        """Send a command and return the result."""

        command["id"] = self.message_id
        self.message_id += 1

        self.ws.send(json.dumps(command))

        response = json.loads(self.ws.recv())

        if not response.get("success", False):
            raise APIError(response)

        return response["result"]

    # ------------------------------------------------------------------------
    # Registry Methods
    # ------------------------------------------------------------------------

    def get_entity_registry(self):
        """Retrieve the Home Assistant entity registry."""

        return self.send(
            {
                "type": "config/entity_registry/list",
            }
        )

    def get_device_registry(self):
        """Retrieve the Home Assistant device registry."""

        return self.send(
            {
                "type": "config/device_registry/list",
            }
        )

    def get_area_registry(self):
        """Retrieve the Home Assistant area registry."""

        return self.send(
            {
                "type": "config/area_registry/list",
            }
        )

    def get_label_registry(self):
        """Retrieve the Home Assistant label registry."""

        return self.send(
            {
                "type": "config/label_registry/list",
            }
        )

    def get_floor_registry(self):
        """Retrieve the Home Assistant floor registry."""

        return self.send(
            {
                "type": "config/floor_registry/list",
            }
        )

    # ------------------------------------------------------------------------
    # Future Methods
    # ------------------------------------------------------------------------

    # def get_floor_registry(self):
    #     ...
    #
    # def get_automations(self):
    #     ...

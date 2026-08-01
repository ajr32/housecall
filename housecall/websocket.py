"""
Communicate with the Home Assistant WebSocket API.
"""

import json

from websocket import create_connection

from .config import HA_TOKEN, HA_URL
from .exceptions import APIError


class HomeAssistantWebSocketClient:
    """Communicate with Home Assistant via WebSocket."""

    def __init__(self):
        ws_url = HA_URL.replace("http://", "ws://").replace(
            "https://", "wss://"
        )
        self.url = f"{ws_url}/api/websocket"
        self.ws = None
        self.message_id = 1

    def connect(self):
        """Connect and authenticate."""

        self.ws = create_connection(self.url)

        #
        # Receive auth_required
        #
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

    def send(self, command):
        """Send a command and return the result."""

        command["id"] = self.message_id
        self.message_id += 1

        self.ws.send(json.dumps(command))

        response = json.loads(self.ws.recv())

        if not response.get("success", False):
            raise APIError(response)

        return response["result"]

    def get_device_registry(self):
        """Retrieve the Home Assistant device registry."""

        return self.send(
            {
                "type": "config/device_registry/list",
            }
        )

    def get_entity_registry(self):
        """Retrieve the Home Assistant entity registry."""

        return self.send(
            {
                "type": "config/entity_registry/list",
            }
        )

    def close(self):
        """Close the websocket."""

        if self.ws:
            self.ws.close()
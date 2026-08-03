"""
HouseCall entity inventory.
"""

from ..websocket import HomeAssistantWebSocketClient


def get_entities():
    """Retrieve all Home Assistant entities."""

    ws = HomeAssistantWebSocketClient()

    try:
        ws.connect()
        return ws.get_entity_registry()

    finally:
        ws.close()

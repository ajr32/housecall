"""
HouseCall area inventory.
"""

from ..websocket import HomeAssistantWebSocketClient


def get_areas():
    """Retrieve all Home Assistant areas."""

    ws = HomeAssistantWebSocketClient()

    try:
        ws.connect()
        return ws.get_area_registry()

    finally:
        ws.close()
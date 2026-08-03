"""
HouseCall floors inventory.
"""

from ..websocket import HomeAssistantWebSocketClient


def get_floors():
    """Retrieve all Home Assistant floors."""

    ws = HomeAssistantWebSocketClient()

    try:
        ws.connect()
        return ws.get_floor_registry()

    finally:
        ws.close()

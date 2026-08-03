"""
HouseCall devices inventory.
"""

from ..websocket import HomeAssistantWebSocketClient


def get_devices():
    """Retrieve all Home Assistant devices."""

    ws = HomeAssistantWebSocketClient()

    try:
        ws.connect()
        return ws.get_device_registry()

    finally:
        ws.close()

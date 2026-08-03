"""
HouseCall labels inventory.
"""

from ..websocket import HomeAssistantWebSocketClient


def get_labels():
    """Retrieve all Home Assistant labels."""

    ws = HomeAssistantWebSocketClient()

    try:
        ws.connect()
        return ws.get_label_registry()

    finally:
        ws.close()

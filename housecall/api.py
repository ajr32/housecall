# Talks to Home Assistant

import requests

from .config import HA_TOKEN, HA_URL


def get_config():
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        f"{HA_URL}/api/config",
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()

def get_states():
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        f"{HA_URL}/api/states",
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()
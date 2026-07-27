"""
HouseCall - Home Assistant Inventory & Analysis Tool

Collects inventory from Home Assistant.
"""

from collections import Counter

from .api import get_config, get_states


def scan():
    print("Scanning Home Assistant...")

    config = get_config()
    states = get_states()

    domains = Counter()

    for state in states:
        domain = state["entity_id"].split(".")[0]
        domains[domain] += 1

    return {
        "config": config,
        "states": states,
        "summary": {
            "total_states": len(states),
            "domains": dict(domains),
        },
    }
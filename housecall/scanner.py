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

    available = 0
    unavailable = 0
    unknown = 0

    unavailable_entities = []
    unknown_entities = []

    for state in states:
        domain = state["entity_id"].split(".")[0]
        domains[domain] += 1

        if state["state"] == "unavailable":
            unavailable += 1
            unavailable_entities.append(state["entity_id"])

        elif state["state"] == "unknown":
            unknown += 1
            unknown_entities.append(state["entity_id"])

        else:
            available += 1

    return {
        "config": config,
        "states": states,
        "summary": {
    "total_states": len(states),
    "available": available,
    "unavailable": unavailable,
    "unknown": unknown,
    "domains": dict(domains),
    "unavailable_entities": unavailable_entities,
    "unknown_entities": unknown_entities,
                    },
    }
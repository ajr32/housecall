"""
HouseCall - Home Assistant Inventory & Analysis Tool

Collects inventory from Home Assistant.
"""

from collections import Counter

from .api import get_config, get_states
from .websocket import HomeAssistantWebSocketClient

HELPER_DOMAINS = {
    "input_boolean",
    "input_button",
    "input_datetime",
    "input_number",
    "input_select",
    "input_text",
    "counter",
    "timer",
    "schedule",
}

def scan():
    print("Scanning Home Assistant...")

    config = get_config()
    states = get_states()

    ws = HomeAssistantWebSocketClient()

    ws.connect()

    entity_registry = ws.get_entity_registry()
    device_registry = ws.get_device_registry()

    ws.close()

    device_ids = {device["id"] for device in device_registry}
    
    domains = Counter()

    available = 0
    unavailable = 0
    unknown = 0

    unavailable_entities = []
    unknown_entities = []
    disabled_entities = []
    orphaned_entities = []
    duplicate_helpers = []

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

    helper_names = {}

    for state in states:
        entity_id = state["entity_id"]

        domain = entity_id.split(".", 1)[0]

        if domain not in HELPER_DOMAINS:
            continue

        friendly_name = state.get("attributes", {}).get("friendly_name")

        if not friendly_name:
            continue

        helper_names.setdefault((domain, friendly_name), []).append(entity_id)

    for entities in helper_names.values():
        if len(entities) > 1:
            duplicate_helpers.extend(entities)



    for entity in entity_registry:
        if entity.get("disabled_by") is not None:
            disabled_entities.append(entity["entity_id"])

    for entity in entity_registry:
        device_id = entity.get("device_id")

        if device_id and device_id not in device_ids:
            orphaned_entities.append(entity["entity_id"])

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
            "disabled": len(disabled_entities),
            "disabled_entities": disabled_entities,
            "orphaned": len(orphaned_entities),
            "orphaned_entities": orphaned_entities,
            "duplicate_helpers": duplicate_helpers,
            "duplicate_helper_count": len(duplicate_helpers),
        },
    }

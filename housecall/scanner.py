"""
HouseCall - Home Assistant Inventory & Analysis Tool

Collects inventory from Home Assistant.
"""

from collections import Counter

from .api import get_config, get_states
from .websocket import HomeAssistantWebSocketClient

# ============================================================================
# Constants
# ============================================================================

DUPLICATE_DOMAINS = {
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

# ============================================================================
# Scanner
# ============================================================================


def scan():
    print("Scanning Home Assistant...")

    # ------------------------------------------------------------------------
    # Retrieve Home Assistant data
    # ------------------------------------------------------------------------

    config = get_config()
    states = get_states()

    ws = HomeAssistantWebSocketClient()
    ws.connect()

    entity_registry = ws.get_entity_registry()
    device_registry = ws.get_device_registry()
    area_registry = ws.get_area_registry()
    label_registry = ws.get_label_registry()
    floor_registry = ws.get_floor_registry()

    # automations = ws.get_automations()

    ws.close()

    # ------------------------------------------------------------------------
    # Build lookup tables
    # ------------------------------------------------------------------------

    device_ids = {device["id"] for device in device_registry}

    device_area_ids = {
        device["area_id"] for device in device_registry if device.get("area_id")
    }

    entity_area_ids = {
        entity["area_id"] for entity in entity_registry if entity.get("area_id")
    }

    entity_label_ids = set()

    for entity in entity_registry:
        for label_id in entity.get("labels", []):
            entity_label_ids.add(label_id)

    device_label_ids = set()

    for device in device_registry:
        for label_id in device.get("labels", []):
            device_label_ids.add(label_id)

    used_label_ids = entity_label_ids | device_label_ids

    used_floor_ids = {
        area["floor_id"] for area in area_registry if area.get("floor_id")
    }

    # ------------------------------------------------------------------------
    # Initialize inventory
    # ------------------------------------------------------------------------

    domains = Counter()

    available = 0
    unavailable = 0
    unknown = 0

    unavailable_entities = []
    unknown_entities = []
    disabled_entities = []
    orphaned_entities = []
    duplicate_objects = []
    empty_areas = []
    empty_labels = []
    empty_floors = []

    # ------------------------------------------------------------------------
    # Scan entity states
    # ------------------------------------------------------------------------

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

    # ------------------------------------------------------------------------
    # Detect duplicate helpers
    # ------------------------------------------------------------------------

    object_names = {}

    for state in states:
        entity_id = state["entity_id"]

        domain = entity_id.split(".", 1)[0]

        if domain not in DUPLICATE_DOMAINS:
            continue

        friendly_name = state.get(
            "attributes",
            {},
        ).get("friendly_name")

        if not friendly_name:
            continue

        object_names.setdefault(
            (domain, friendly_name),
            [],
        ).append(entity_id)

    for entities in object_names.values():
        if len(entities) > 1:
            duplicate_objects.extend(entities)

    # ------------------------------------------------------------------------
    # Detect disabled entities
    # ------------------------------------------------------------------------

    for entity in entity_registry:
        if entity.get("disabled_by") is not None:
            disabled_entities.append(entity["entity_id"])

    # ------------------------------------------------------------------------
    # Detect orphaned entities
    # ------------------------------------------------------------------------

    for entity in entity_registry:
        device_id = entity.get("device_id")

        if device_id and device_id not in device_ids:
            orphaned_entities.append(entity["entity_id"])

    # ------------------------------------------------------------------------
    # Detect empty areas
    # ------------------------------------------------------------------------

    for area in area_registry:
        area_id = area["area_id"]

        if area_id not in device_area_ids and area_id not in entity_area_ids:
            empty_areas.append(area["name"])

    # ------------------------------------------------------------------------
    # Detect empty labels
    # ------------------------------------------------------------------------

    for label in label_registry:
        label_id = label["label_id"]

        if label_id not in used_label_ids:
            empty_labels.append(label["name"])

    # ------------------------------------------------------------------------
    # Detect empty floors
    # ------------------------------------------------------------------------

    for floor in floor_registry:
        floor_id = floor["floor_id"]

        if floor_id not in used_floor_ids:
            empty_floors.append(floor["name"])

    # ------------------------------------------------------------------------
    # Detect duplicate objects
    # ------------------------------------------------------------------------

    objects = []

    for area in area_registry:
        objects.append(("Area", area["name"]))

    for label in label_registry:
        objects.append(("Label", label["name"]))

    for floor in floor_registry:
        objects.append(("Floor", floor["name"]))

    object_names = {}

    for object_type, name in objects:
        key = (object_type, name)

        object_names.setdefault(key, 0)
        object_names[key] += 1

    for (object_type, name), count in object_names.items():
        if count > 1:
            duplicate_objects.append(f"{object_type}: {name}")

    # ------------------------------------------------------------------------
    # Return inventory
    # ------------------------------------------------------------------------

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
            "empty_areas": empty_areas,
            "empty_area_count": len(empty_areas),
            "empty_labels": empty_labels,
            "empty_label_count": len(empty_labels),
            "empty_floors": empty_floors,
            "empty_floor_count": len(empty_floors),
            "duplicate_objects": duplicate_objects,
            "duplicate_object_count": len(duplicate_objects),
        },
    }

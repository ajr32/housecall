"""
Assignment detectors.
"""

from ..models import OrganizationIssue


def detect_unassigned_devices(items):
    """
    Detect devices that are not assigned to an Area.

    eg: Kitchen Tablet (no Area)
    """

    issues = []

    for item in items:
        area_id = item.get("area_id")

        if area_id:
            continue

        item_name = item.get("name", "Unknown Device")

        issues.append(
            OrganizationIssue(
                category="Unassigned Devices",
                severity="Medium",
                message="Device is not assigned to an Area.",
                recommendation="Assign the device to a Home Assistant Area.",
                items=[item_name],
            )
        )

    return issues


def detect_unassigned_entities(entities):
    """
    Detect entities that are not assigned to an Area.

    eg: sensor.kitchen_temperature (no Area)
    """

    issues = []

    for entity in entities:
        if entity.get("area_id"):
            continue

        issues.append(
            OrganizationIssue(
                category="Unassigned Entities",
                severity="Medium",
                message="Entity is not assigned to an Area.",
                recommendation="Assign the entity to a Home Assistant Area.",
                items=[entity.get("entity_id", entity.get("name", "Unknown Entity"))],
            )
        )

    return issues

def detect_empty_areas(areas, devices):
    """
    Detect Areas that contain no devices.

    eg: Basement
    """

    assigned_area_ids = {
        device.get("area_id")
        for device in devices
        if device.get("area_id")
    }

    issues = []

    for area in areas:
        area_id = area.get("area_id")

        if area_id in assigned_area_ids:
            continue

        issues.append(
            OrganizationIssue(
                category="Empty Areas",
                severity="Low",
                message="Area contains no devices.",
                recommendation="Assign one or more devices to the Area, or remove the unused Area.",
                items=[area.get("name", "Unknown Area")],
            )
        )

    return issues

def detect_empty_floors(floors, areas):
    """
    Detect Floors that contain no Areas.

    eg: Second Floor
    """

    assigned_floor_ids = {
        area.get("floor_id")
        for area in areas
        if area.get("floor_id")
    }

    issues = []

    for floor in floors:
        floor_id = floor.get("floor_id")

        if floor_id in assigned_floor_ids:
            continue

        issues.append(
            OrganizationIssue(
                category="Empty Floors",
                severity="Low",
                message="Floor contains no Areas.",
                recommendation="Assign one or more Areas to the Floor, or remove the unused Floor.",
                items=[floor.get("name", "Unknown Floor")],
            )
        )

    return issues

def detect_unused_labels(labels, devices, entities):
    """
    Detect Labels that are not assigned to any Device or Entity.

    eg: Holiday
    """

    used_label_ids = set()

    # Labels used by Devices
    for device in devices:
        for label_id in device.get("label_ids", []):
            used_label_ids.add(label_id)

    # Labels used by Entities
    for entity in entities:
        for label_id in entity.get("label_ids", []):
            used_label_ids.add(label_id)

    issues = []

    for label in labels:
        label_id = label.get("label_id")

        if label_id in used_label_ids:
            continue

        issues.append(
            OrganizationIssue(
                category="Unused Labels",
                severity="Low",
                message="Label is not assigned to any Device or Entity.",
                recommendation="Assign the label or remove the unused label.",
                items=[label.get("name", "Unknown Label")],
            )
        )

    return issues
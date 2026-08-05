from .detectors.assignments import (
    detect_empty_areas,
    detect_empty_floors,
    detect_unassigned_devices,
    detect_unassigned_entities,
    detect_unused_labels,
)

DETECTORS = (
    detect_unassigned_devices,
    detect_unassigned_entities,
    detect_empty_areas(),
    detect_empty_floors(),
    detect_unused_labels(),
)


def find_assignment_issues(items):
    """Run all assignment detectors."""

    issues = []

    for detector in DETECTORS:
        issues.extend(detector(items))

    return issues

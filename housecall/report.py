# Writes JSON/HTML reports

import json


def build_health_report(runner, total_time):
    """Build a diagnostic report."""

    report = {
        "checks": [],
        "summary": {},
    }

    for result in runner.results:
        report["checks"].append(
            {
                "name": result.name,
                "passed": result.passed,
                "message": result.message,
                "elapsed": result.elapsed,
            }
        )

    report["summary"] = {
        "checks_run": len(runner.results),
        "passed": runner.passed,
        "failed": runner.failed,
        "runtime": total_time,
        "success": runner.success,
    }
    return report


def build_cleanup_report(runner, total_time):
    """Build a diagnostic report."""

    report = {
        "checks": [],
        "summary": {},
    }

    for result in runner.results:
        report["checks"].append(
            {
                "name": result.name,
                "passed": result.passed,
                "message": result.message,
                "elapsed": result.elapsed,
            }
        )

    report["summary"] = {
        "checks_run": len(runner.results),
        "passed": runner.passed,
        "failed": runner.failed,
        "runtime": total_time,
        "success": runner.success,
    }
    return report

def build_inventory_report():
    from .inventory.areas import get_areas
    from .inventory.floors import get_floors
    from .inventory.labels import get_labels
    from .inventory.devices import get_devices
    from .inventory.entities import get_entities

    areas = get_areas()
    floors = get_floors()
    labels = get_labels()
    devices = get_devices()
    entities = get_entities()

    return {
        "areas": areas,
        "floors": floors,
        "labels": labels,
        "devices": devices,
        "entities": entities,
        "summary": {
            "areas": len(areas),
            "floors": len(floors),
            "labels": len(labels),
            "devices": len(devices),
            "entities": len(entities),
        },
    }

def save_json(data, filename="inventory.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

from ..inventory.areas import get_areas
from ..inventory.devices import get_devices
from ..inventory.entities import get_entities
from ..inventory.floors import get_floors
from ..inventory.labels import get_labels
from .naming import find_naming_issues


def run_naming_report():
    """Generate the naming consistency report."""

    print()
    print("Naming Standards")
    print("================")
    print()

    inventories = (
        ("Areas", get_areas()),
        ("Floors", get_floors()),
        ("Labels", get_labels()),
        ("Devices", get_devices()),
        ("Entities", get_entities()),
    )

    total = 0

    for title, items in inventories:
        issues = find_naming_issues(items)

        if not issues:
            continue

        print(title)
        print("-" * len(title))

        for issue in issues:
            total += 1

            print(f"[{issue.severity}] {issue.category}")
            print(issue.message)

            for item in issue.items:
                print(f"  • {item}")

            print(f"Recommendation: {issue.recommendation}")
            print()

    print("Summary")
    print("-------")
    print(f"Issues Found: {total}")
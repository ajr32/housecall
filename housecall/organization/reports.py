from collections import Counter, defaultdict

from ..inventory.areas import get_areas
from ..inventory.devices import get_devices
from ..inventory.entities import get_entities
from ..inventory.floors import get_floors
from ..inventory.labels import get_labels
from .naming import find_naming_issues


def run_naming_report():
    """Generate the naming consistency report."""

    print()
    print("HouseCall Naming Standards")
    print("==========================")
    print()

    inventories = (
        ("Areas", get_areas()),
        ("Floors", get_floors()),
        ("Labels", get_labels()),
        ("Devices", get_devices()),
        ("Entities", get_entities()),
    )

    total_issues = 0

    for title, items in inventories:
        print(title)
        print("-" * len(title))
        print()

        issues = find_naming_issues(items)

        if not issues:
            print("✓ No naming issues found.")
            print()
            continue

        total_issues += len(issues)

        #
        # Group issues by category
        #
        grouped = defaultdict(list)

        for issue in issues:
            grouped[issue.category].append(issue)

        #
        # Display grouped issues
        #
        for category, category_issues in grouped.items():
            print(f"⚠ {category}")
            print()

            if category == "Duplicate Names":
                counter = Counter()

                for issue in category_issues:
                    for item in issue.items:
                        counter[item] += 1

                for item, count in sorted(counter.items()):
                    print(f"    {item}")
                    print(f"        {count} {'item' if count == 1 else 'items'}")
                    print()

            else:
                for issue in category_issues:
                    for item in issue.items:
                        print(f"    {item}")

                    print()

            print(f"Recommendation: {category_issues[0].recommendation}")
            print()

    print("Summary")
    print("-------")
    print(f"Collections Checked : {len(inventories)}")
    print(f"Issues Found        : {total_issues}")


def run_assignment_report():

    """Generate the assignment analysis report."""

    print()
    print("HouseCall Assignment Analysis")
    print("=============================")
    print()

    from .detectors.assignments import (
        detect_empty_areas,
        detect_empty_floors,
        detect_unassigned_devices,
        detect_unassigned_entities,
        detect_unused_labels,
    )

    areas = get_areas()
    floors = get_floors()
    labels = get_labels()
    devices = get_devices()
    entities = get_entities()

    issues = []

    issues.extend(detect_unassigned_devices(devices))
    issues.extend(detect_unassigned_entities(entities))
    issues.extend(detect_empty_areas(areas, devices))
    issues.extend(detect_empty_floors(floors, areas))
    issues.extend(detect_unused_labels(labels, devices, entities))

    grouped = defaultdict(list)

    for issue in issues:
        grouped[issue.category].append(issue)

    #
    # Display grouped issues
    #
    for category, category_issues in grouped.items():
        print(f"⚠ {category}")
        print()

        if category == "Duplicate Names":
            counter = Counter()

            for issue in category_issues:
                for item in issue.items:
                    counter[item] += 1

            for item, count in sorted(counter.items()):
                print(f"    {item}")
                print(f"        {count} {'item' if count == 1 else 'items'}")
                print()

        else:
            for issue in category_issues:
                for item in issue.items:
                    print(f"    {item}")

                print()

            print(f"Recommendation: {category_issues[0].recommendation}")
            print()

    print("Summary")
    print("-------")
    print(f"Issues Found : {len(issues)}")


def run_organization_report():
    """Generate the complete organization report."""

    print()
    print("HouseCall Organization Report")
    print("============================")
    print()

    run_naming_report()

    print()

    run_assignment_report()

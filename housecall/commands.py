"""
HouseCall command implementations.
"""

from time import perf_counter

from .diagnostics import DiagnosticRunner
from .report import (
    build_cleanup_report,
    build_health_report,
    build_inventory_report,
    save_json,
)


def run_report(
    title,
    checks,
    report_builder,
    verbose=False,
):
    """Run a HouseCall report."""

    if verbose:
        print("Verbose mode enabled.\n")

    runner = DiagnosticRunner()

    print()
    print(title)
    print("=" * len(title))
    print()

    overall_start = perf_counter()

    for check in checks:
        if verbose:
            print(f"Running {check.__class__.__name__}...")

        check_start = perf_counter()
        result = check.run()
        elapsed = perf_counter() - check_start

        # Store the elapsed time on the result
        result.elapsed = elapsed

        runner.add(result)

    print("Diagnostics")
    print("-----------")

    total_time = perf_counter() - overall_start
    report = report_builder(runner, total_time)
    save_json(report)

    # Display results
    for result in report["checks"]:
        status = "✓" if result["passed"] else "✗"

        print(
            f"{status} {result['name']}: {result['message']} ({result['elapsed']:.2f}s)"
        )

    print()
    print("Summary")
    print("-------")
    summary = report["summary"]

    print(f"Checks run : {summary['checks_run']}")
    print(f"Passed     : {summary['passed']}")
    print(f"Failed     : {summary['failed']}")
    print(f"Total time : {summary['runtime']:.2f}s")
    print()

    print()
    print("Overall Health")
    print("--------------")

    if runner.success:
        print("Status : PASS")
    else:
        print("Status : FAIL")


def run_triage(verbose=False):
    from .health import HEALTH_CHECKS

    run_report(
        "HouseCall Health Report",
        HEALTH_CHECKS,
        build_health_report,
        verbose,
    )


def run_housekeeping(verbose=False):
    from .health import HOUSEKEEPING_CHECKS

    run_report(
        "HouseCall Housekeeping",
        HOUSEKEEPING_CHECKS,
        build_cleanup_report,
        verbose,
    )


def run_organization():
    """Display the Organization menu."""

    while True:
        print()
        print("HouseCall Organization")
        print("======================")
        print()
        print("Inventory")
        print("---------")
        print("1. Areas")
        print("2. Floors")
        print("3. Labels")
        print("4. Devices")
        print("5. Entities")
        print("6. Export Inventory")
        print()
        print("Analysis")
        print("---------")
        print("7. Naming Standards")
        print("8. Assignment Analysis")
        print("9. Full Organization Analysis")
        print()
        print("0. Back")
        print()

        choice = input("Selection: ").strip()

        if choice == "1":
            run_inventory_areas()

        elif choice == "2":
            run_inventory_floors()

        elif choice == "3":
            run_inventory_labels()

        elif choice == "4":
            run_inventory_devices()

        elif choice == "5":
            run_inventory_entities()

        elif choice == "6":
            run_export_inventory()

        elif choice == "7":
            run_naming()

        elif choice == "8":
            run_assignments()

        elif choice == "9":
            run_organization_analysis()

        elif choice == "0":
            return

        else:
            print("Invalid selection.")

def run_inventory_areas():
    from .inventory.areas import get_areas

    run_inventory(
        "Home Assistant Areas",
        get_areas(),
    )


def run_inventory_floors():
    """Display Home Assistant"""
    from .inventory.floors import get_floors

    run_inventory(
        "Home Assistant Floors",
        get_floors(),
    )


def run_inventory_labels():
    from .inventory.labels import get_labels

    run_inventory(
        "Home Assistant Labels",
        get_labels(),
    )

def run_inventory_devices():
    from .inventory.devices import get_devices

    run_inventory(
        "Home Assistant Devices",
        get_devices(),
    )


def run_inventory_entities():
    from .inventory.entities import get_entities

    run_inventory(
        "Home Assistant Entities",
        get_entities(),
        key="entity_id",
    )


def run_inventory(title, items, key="name"):
    """Display a Home Assistant inventory."""

    items = sorted(
        items,
        key=lambda item: item.get(key) or item.get("entity_id") or "",
    )

    print()
    print(title)
    print("=" * len(title))
    print()

    for index, item in enumerate(items, start=1):
        print(f"{index:>4}. {item.get(key) or item.get('entity_id')}")

    print()
    print(f"Total {title.replace('Home Assistant ', '')}: {len(items)}")


def run_naming():
    """Run naming analysis."""

    from .organization.reports import run_naming_report

    run_naming_report()

def run_assignments():
    """Run assignment analysis."""

    from .organization.reports import run_assignment_report

    run_assignment_report()

def run_organization_analysis():
    """Run organization analysis."""

    from .organization.reports import run_organization_report

    run_organization_report()

def run_export_inventory():
    """Export Home Assistant inventory."""

    report = build_inventory_report()

    save_json(report, "inventory.json")

    print()
    print("Inventory exported successfully.")
    print(f"Areas   : {report['summary']['areas']}")
    print(f"Floors  : {report['summary']['floors']}")
    print(f"Labels  : {report['summary']['labels']}")
    print(f"Devices : {report['summary']['devices']}")
    print(f"Entities: {report['summary']['entities']}")
    print()
    print("Saved to inventory.json")
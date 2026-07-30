"""
HouseCall command implementations.
"""

from .diagnostics import DiagnosticRunner


def run_doctor():
    """Run HouseCall diagnostics."""

    runner = DiagnosticRunner()

    print("HouseCall Doctor")
    print("-----------------")
    print()

    from .health import HEALTH_CHECKS

    for check in HEALTH_CHECKS:
        runner.add(check.run())

    # Display results
    for result in runner.results:
        status = "✓" if result.passed else "✗"
        print(f"{status} {result.name}: {result.message}")

    print()
    print("Summary")
    print("-------")
    print(f"Checks run : {len(runner.results)}")
    print(f"Passed     : {runner.passed}")
    print(f"Failed     : {runner.failed}")
    print()

    if runner.success:
        print("✓ No problems found.")
    else:
        print("✗ One or more diagnostics failed.")

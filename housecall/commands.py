"""
HouseCall command implementations.
"""

from .diagnostics import DiagnosticRunner


def run_doctor(verbose=False):
    """Run HouseCall diagnostics."""

    if verbose:
        print("Verbose mode enabled.\n")
    runner = DiagnosticRunner()

    print("HouseCall Doctor")
    print("-----------------")
    print()

    from .health import HEALTH_CHECKS

    for check in HEALTH_CHECKS:
        if verbose:
            print(f"Running {check.__class__.__name__}...")
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

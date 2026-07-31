"""
HouseCall command implementations.
"""

from time import perf_counter

from .diagnostics import DiagnosticRunner


def run_doctor(verbose=False):
    """Run HouseCall diagnostics."""

    if verbose:
        print("Verbose mode enabled.\n")

    runner = DiagnosticRunner()

    print()
    print("HouseCall Health Report")
    print("=======================")
    print()

    from .health import HEALTH_CHECKS

    overall_start = perf_counter()

    for check in HEALTH_CHECKS:
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

    # Display results
    for result in runner.results:
        status = "✓" if result.passed else "✗"
        print(f"{status} {result.name}: {result.message} ({result.elapsed:.2f}s)")

    total_time = perf_counter() - overall_start

    print()
    print("Summary")
    print("-------")
    print(f"Checks run : {len(runner.results)}")
    print(f"Passed     : {runner.passed}")
    print(f"Failed     : {runner.failed}")
    print(f"Total time : {total_time:.2f}s")
    print()

    print()
    print("Overall Health")
    print("--------------")

    if runner.success:
        print("Status : PASS")
    else:
        print("Status : FAIL")

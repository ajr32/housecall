"""
HouseCall command implementations.
"""

from time import perf_counter

from .diagnostics import DiagnosticRunner
from .report import build_report, save_json

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

    total_time = perf_counter() - overall_start
    report = build_report(runner, total_time)
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

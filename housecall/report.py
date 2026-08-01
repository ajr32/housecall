# Writes JSON/HTML reports

import json


def build_report(runner, total_time):
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

def save_json(data, filename="inventory.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)



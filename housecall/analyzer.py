"""
HouseCall - Home Assistant Inventory & Analysis Tool

Analyzes collected inventory and identifies potential issues.
"""


def analyze(inventory):
    """Analyze the inventory and return findings."""

    summary = inventory["summary"]

    findings = {
        "warnings": [],
        "info": [],
    }

    if summary["unavailable"] > 0:
        findings["warnings"].append(
            f"{summary['unavailable']} unavailable entities detected."
        )

    if summary["unknown"] > 0:
        findings["warnings"].append(f"{summary['unknown']} unknown entities detected.")

    findings["info"].append(f"{summary['total_states']} total entities found.")

    return findings

"""
HouseCall - Home Assistant Inventory & Analysis Tool

Implements the HouseCall command-line interface.
"""

from .report import save_json
from .scanner import scan
from .analyzer import analyze


def main():
    print("=" * 50)
    print("🏠 HouseCall")
    print("=" * 50)

    from .api import client

    print("Testing connection...")

    client.test_connection()

    print("✓ Connected\n")

    inventory = scan()
    findings = analyze(inventory)

    save_json(inventory)

    summary = inventory["summary"]

    print()
    print("Inventory Summary")
    print("-" * 25)

    print(f"Total States : {summary['total_states']}")
    print(f"Available    : {summary['available']}")
    print(f"Unavailable  : {summary['unavailable']}")
    print(f"Unknown      : {summary['unknown']}")

    if summary["unavailable_entities"]:
        print()
        print("Unavailable Entities")
        print("-" * 25)

        for entity in summary["unavailable_entities"]:
            print(f"  • {entity}")

    print()
    print("Top Domains")
    print("-" * 25)

    for domain, count in sorted(
        summary["domains"].items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(f"{domain:<20} {count}")

    print()
    print("Findings")
    print("-" * 25)

    for warning in findings["warnings"]:
        print(f"⚠ {warning}")

    for info in findings["info"]:
        print(f"ℹ {info}")

    print()
    print("✅ Inventory written to inventory.json")
"""
HouseCall - Home Assistant Inventory & Analysis Tool

Implements the HouseCall command-line interface.
"""

from .report import save_json
from .scanner import scan


def main():
    print("=" * 50)
    print("🏠 HouseCall")
    print("=" * 50)

    inventory = scan()

    save_json(inventory)

    summary = inventory["summary"]

    print()
    print("Inventory Summary")
    print("-" * 25)

    print(f"Total States : {summary['total_states']}")
    print(f"Available    : {summary['available']}")
    print(f"Unavailable  : {summary['unavailable']}")
    print(f"Unknown      : {summary['unknown']}")

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
    print("✅ Inventory written to inventory.json")
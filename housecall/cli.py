"""
HouseCall - Home Assistant Inventory & Analysis Tool

Implements the HouseCall command-line interface.
"""

from .report import save_json
from .scanner import scan
from .analyzer import analyze

import argparse
import logging

from .settings import settings


def main():
    parser = argparse.ArgumentParser(
        prog="housecall",
        description="Analyze a Home Assistant installation."
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {settings.version}",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "test",
        help="Test the Home Assistant connection.",
    )

    args = parser.parse_args()

    if args.command == "test":
        from .api import get_config

        print("Testing connection...")

        config = get_config()

        print("✓ Connected\n")
        print(f"Version : {config['version']}")
        print(f"Location: {config['location_name']}")
        return

    from .logging_config import configure_logging

    configure_logging()

    logger = logging.getLogger(__name__)

    logger.info("HouseCall started.")

    print("=" * 50)
    print(f"🏠 HouseCall v{settings.version}")
    print("=" * 50)

    from .api import client

    print("Testing connection...")
    logger.info("Testing Home Assistant connection.")

    client.test_connection()

    print("✓ Connected\n")
    logger.info("Successfully connected to Home Assistant.")

    logger.info("Starting inventory scan.")
    inventory = scan()

    logger.info("Running analysis.")
    findings = analyze(inventory)

    logger.info("Writing inventory to inventory.json.")
    save_json(inventory)

    summary = inventory["summary"]

    logger.info(
        "Inventory complete: %d states, %d unavailable.",
        summary["total_states"],
        summary["unavailable"],
    )

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
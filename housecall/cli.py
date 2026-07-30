"""
HouseCall - Home Assistant Inventory & Analysis Tool

Implements the HouseCall command-line interface.
"""

from .report import save_json
from .scanner import scan
from .analyzer import analyze
from .console import section
from .diagnostics import Diagnostic, DiagnosticRunner

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

    subparsers.add_parser(
        "doctor",
        help="Check the HouseCall installation.",
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

    if args.command == "doctor":
        from .config import validate_configuration
        from .api import client

        runner = DiagnosticRunner()

        print("HouseCall Doctor")
        print("-----------------")
        print()

        # Configuration
        try:
            validate_configuration()
            runner.add(Diagnostic("Configuration", True, "Configuration OK"))
        except Exception as exc:
            runner.add(Diagnostic("Configuration", False, str(exc)))

        # Home Assistant connection
        try:
            client.test_connection()
            runner.add(Diagnostic("Connection", True, "Home Assistant connection"))
        except Exception as exc:
            runner.add(Diagnostic("Connection", False, str(exc)))

        # Display results
        for result in runner.results:
            status = "✓" if result.passed else "✗"
            print(f"{status} {result.name}: {result.message}")

        print()

        if runner.success:
            print("✓ No problems found.")
        else:
            print("✗ One or more diagnostics failed.")

        return

    from .logging_config import configure_logging

    configure_logging()

    logger = logging.getLogger(__name__)

    logger.info("HouseCall started.")

    print("=" * 50)
    print(f"🏠 HouseCall v{settings.version}")
    print("=" * 50)

    from .config import validate_configuration
    from .api import client

    validate_configuration()
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
    save_json(inventory, settings.output_file)

    summary = inventory["summary"]

    logger.info(
        "Inventory complete: %d states, %d unavailable.",
        summary["total_states"],
        summary["unavailable"],
    )

    section("Inventory Summary")

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

    section("Top Domains")

    for domain, count in sorted(
        summary["domains"].items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(f"{domain:<20} {count}")

    section("Findings")

    for warning in findings["warnings"]:
        print(f"⚠ {warning}")

    for info in findings["info"]:
        print(f"ℹ {info}")

    print()
    print("✅ Inventory written to inventory.json")
"""
HouseCall - Home Assistant Inventory & Analysis Tool

Implements the HouseCall command-line interface.
"""

import argparse
import logging

from .analyzer import analyze
from .commands import (run_housekeeping, run_triage, run_organization)
from .console import section
from .home import show_home
from .report import save_json
from .scanner import scan
from .settings import settings


# ============================================================================
# Menu
# ============================================================================


def show_menu():
    """Display the HouseCall menu."""


# ============================================================================
# Main
# ============================================================================


def main():
    """Run the HouseCall command-line interface."""

    # ------------------------------------------------------------------------
    # Create parser
    # ------------------------------------------------------------------------

    parser = argparse.ArgumentParser(
        prog="housecall",
        description="Analyze a Home Assistant installation.",
    )

    # ------------------------------------------------------------------------
    # Global arguments
    # ------------------------------------------------------------------------

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {settings.version}",
    )

    # ------------------------------------------------------------------------
    # Subcommands
    # ------------------------------------------------------------------------

    subparsers = parser.add_subparsers(dest="command")

    # test_parser = subparsers.add_parser(
    #   "test",
    #   help="Test the Home Assistant connection.",
    # )

    triage_parser = subparsers.add_parser(
        "triage",
        help="Check the HouseCall installation.",
    )

    triage_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed diagnostic output.",
    )

    housekeeping_parser = subparsers.add_parser(
        "housekeeping",
        help="Check for cleanup opportunities.",
    )

    housekeeping_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed diagnostic output.",
    )

    organization_parser = subparsers.add_parser(
        "organization",
        help="Check for cleanup opportunities.",
    )

    organization_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed diagnostic output."
    )

    args = parser.parse_args()

    # ------------------------------------------------------------------------
    # Command dispatch
    # ------------------------------------------------------------------------

    if args.command is None:
        show_home()
        return

    if args.command == "test":
        from .api import get_config

        print("Testing connection...")

        config = get_config()

        print("✓ Connected\n")
        print(f"Version : {config['version']}")
        print(f"Location: {config['location_name']}")
        return

    if args.command == "triage":
        run_triage(args.verbose)
        return

    elif args.command == "housekeeping":
        run_housekeeping(args.verbose)
        return

    elif args.command == "organization":
        run_organization()
        return

    # ------------------------------------------------------------------------
    # Legacy inventory mode
    # ------------------------------------------------------------------------

    from .logging_config import configure_logging

    configure_logging()

    logger = logging.getLogger(__name__)

    logger.info("HouseCall started.")

    print("=" * 50)
    print(f"🏠 HouseCall v{settings.version}")
    print("=" * 50)

    from .api import client
    from .config import validate_configuration

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

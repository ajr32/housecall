"""Interactive Home Screen for HouseCall."""

from .commands import run_triage, run_housekeeping
from .settings import settings


def show_home():
    """Display the HouseCall home screen."""

    while True:
        print("=" * 70)
        print(f"🏠 HouseCall v{settings.version}")
        print("Home Assistant Diagnostic Toolkit")
        print("=" * 70)
        print()

        print("Identification Tools")
        print("--------------------")
        print("1. Clutter - identify unused and redundant items")
        print("2. Triage System - identify issues throughout Home Assistant")
   
        print()

        print("Utilities")
        print("---------")
        print("3. Version")
        print()

        print("0. Exit")
        print()

        choice = input("Select an option: ").strip()

        if choice == "2":
            verbose = input("\nVerbose output? (y/N): ").strip().lower() == "y"

            run_triage(verbose)
            input("\nPress Enter to return to the Home Screen...")
            print()

        if choice == "1":
            #            verbose = input("\nVerbose output? (y/N): ").strip().lower() == "y"

            run_housekeeping()
            input("\nPress Enter to return to the Home Screen...")
            print()

        # if choice == "3":
        #    run_version()
        #     input("\nPress Enter to return to the Home Screen...")
        #     print()

        elif choice == "0":
            return

        else:
            print("\nInvalid selection.")
            input("Press Enter to continue...")
            print()

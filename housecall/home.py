"""Interactive Home Screen for HouseCall."""

from .commands import run_doctor
from .settings import settings


def show_home():
    """Display the HouseCall home screen."""

    while True:
        print("=" * 50)
        print(f"🏠 HouseCall v{settings.version}")
        print("Home Assistant Diagnostic Toolkit")
        print("=" * 50)
        print()

        print("Health")
        print("------")
        print("1. Doctor")
        print()

        print("Utilities")
        print("---------")
        print("2. Version")
        print()

        print("0. Exit")
        print()

        choice = input("Select an option: ").strip()

        if choice == "1":
            run_doctor()
            input("\nPress Enter to return to the Home Screen...")
            print()

        # elif choice == "2":
        #     run_version()
        #     input("\nPress Enter to return to the Home Screen...")
        #     print()

        elif choice == "0":
            return

        else:
            print("\nInvalid selection.")
            input("Press Enter to continue...")
            print()

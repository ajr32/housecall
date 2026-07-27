# user interface/commands

from .api import get_config


def main():
    print("=" * 50)
    print("🏠 HouseCall")
    print("=" * 50)

    print("Connecting to Home Assistant...")

    try:
        config = get_config()

        print("✅ Connected!")
        print()
        print(f"Version: {config['version']}")
        print(f"Location: {config['location_name']}")
        print(f"Time Zone: {config['time_zone']}")

    except Exception as ex:
        print(f"❌ {ex}")
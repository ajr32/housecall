# user interface/commands

from .scanner import scan
from .report import save_json


def main():
    print("=" * 50)
    print("🏠 HouseCall")
    print("=" * 50)

    inventory = scan()

    save_json(inventory)

    print()
    print("✅ Inventory written to inventory.json")
    print()
    print(f"Version : {inventory['config']['version']}")
    print(f"States  : {len(inventory['states'])}")
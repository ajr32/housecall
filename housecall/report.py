# Writes JSON/HTML reports

import json


def save_json(data, filename="inventory.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
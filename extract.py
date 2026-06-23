import json
import csv
from pathlib import Path
import sys

OUTPUT_CSV = "extracted_data.csv"

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

BASE_DIR = get_base_dir()

#Modify this section for each new item record:

INPUT_FOLDER = BASE_DIR / "GameData"
ITEM_PATH = INPUT_FOLDER / "db.aston.en" / "item.bin.json"
SHOP_PATH = INPUT_FOLDER / "db.aston.en" / "shop.bin.json"
TARGET = "aston_s_poppo_ashi"

# ============================================================

with open(ITEM_PATH, "r", encoding="utf-8") as f:
    item_data = json.load(f)

def get_item_info(item_data, item_id):
    row = item_data.get(str(item_id))

    if not isinstance(row, dict):
        return {
            "item_key": None,
            "name": None,
            "category": None,
            "purchase_price": None
        }

    for key, value in row.items():

        if not isinstance(value, dict):
            continue

        return {
            "item_key": key,
            "name": value.get("name"),
            "category": value.get("category"),
            "purchase_price": value.get("purchase_price")
        }

    return {
        "item_key": None,
        "name": None,
        "category": None,
        "purchase_price": None
    }

def find_targets(obj, target, path="root"):
    matches = []

    if isinstance(obj, dict):
        for key, value in obj.items():

            current_path = f"{path}.{key}"

            if key == target:
                matches.append((current_path, value))

            matches.extend(find_targets(value, target, current_path))

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            matches.extend(find_targets(item, target, f"{path}[{i}]"))

    return matches


with open(SHOP_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

matches = find_targets(data, TARGET)

results = []

for match_path, target_data in matches:

    print(f"Found target at: {match_path}")

    table = target_data.get("table")

    if not isinstance(table, dict):
        continue

    for subrow_num, subrow_data in table.items():

        if not subrow_num.isdigit():
            continue

        values = subrow_data.get("", {})

        if not isinstance(values, dict):
            continue

        item_id = values.get("1")

        item_info = get_item_info(item_data, item_id)

        item_info = get_item_info(item_data, item_id)

        results.append({
            "path": match_path,
            "item_key": item_info["item_key"],
            "table_row": subrow_num,
            "item_id": item_id,
            "name": item_info["name"],
            "category": item_info["category"],
            "purchase_price": item_info["purchase_price"]
        })

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "path",
            "item_key",
            "table_row",
            "item_id",
            "name",
            "category",
            "purchase_price"
        ]
    )
    writer.writeheader()
    writer.writerows(results)

print(f"Found {len(matches)} target occurrence(s)")
print(f"Extracted {len(results)} item(s)")
import csv
import json
import sys
from copy import deepcopy
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()

INPUT_FOLDER = BASE_DIR / "GameData"
PATCH_CSV = BASE_DIR / "patch.csv"

ITEM_PATH = INPUT_FOLDER / "db.aston.en" / "item.bin.json"
OUTPUT_PATH = INPUT_FOLDER / "db.aston.en" / "adjusted_item.bin.json"

UPDATE_CSV = BASE_DIR / "updates.csv"


# --------------------------------------------------
# Load files
# --------------------------------------------------

print("Loading item.bin.json...")

with open(ITEM_PATH, encoding="utf-8") as f:
    item_data = json.load(f)

with open(PATCH_CSV, newline="", encoding="utf-8") as f:
    patch_rows = list(csv.DictReader(f))


# --------------------------------------------------
# Build existing item name -> icon lookup
# --------------------------------------------------

name_to_icon = {}
name_to_explanation = {}

for key, value in item_data.items():
    if not key.isdigit():
        continue

    if not isinstance(value, dict):
        continue

    inner_key = next(iter(value.keys()))
    item = value[inner_key]

    existing_name = item.get("name")

    if existing_name:
        name_to_icon[existing_name] = item.get("icon", 5944)
        name_to_explanation[existing_name] = item.get(
            "explanation",
            "Archipelago Generated Item"
        )

print(f"Loaded {len(name_to_icon)} existing item icon mappings")

# --------------------------------------------------
# Find next available row id
# --------------------------------------------------

existing_ids = [
    int(k)
    for k in item_data.keys()
    if k.isdigit()
]

next_row = max(existing_ids) + 1

print(f"Existing rows: {len(existing_ids)}")
print(f"Starting new rows at {next_row}")


# --------------------------------------------------
# Template
# --------------------------------------------------

template = deepcopy(item_data["5848"])
template_key = next(iter(template.keys()))
template_row = template[template_key]


# --------------------------------------------------
# Build new items
# --------------------------------------------------

updated_rows = []

for row in patch_rows:

    item_name = row["item_name"].strip()

    if not item_name:
        updated_rows.append(row)
        continue

    row_id = str(next_row)

    new_entry = deepcopy(template_row)

    new_entry["name"] = item_name
    new_entry["icon"] = name_to_icon.get(item_name, 5944)
    new_entry["reARMP_rowIndex"] = (next_row - 2)
    new_entry["max_count_base"] = 99
    new_entry["reARMP_isValid"] = "1"
    new_entry["hide_on_pause_menu"] = 1
    new_entry["explanation"] = name_to_explanation.get(item_name, "Archipelago Generated Item")
    item_data[row_id] = {
        item_name: new_entry
    }

    row["item_id"] = row_id
    row["new_value"] = row_id
    row["purchase_price"] = row.get("purchase_price") or 1
    row["purchase_points"] = row.get("purchase_points") or 1
    updated_rows.append(row)

    next_row += 1


# --------------------------------------------------
# Update header values
# --------------------------------------------------

item_data["ROW_COUNT"] = next_row
item_data["TEXT_COUNT"] = int(item_data.get("TEXT_COUNT", 0)) + len(updated_rows)


# --------------------------------------------------
# Save adjusted item.bin.json
# --------------------------------------------------

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(item_data, f, indent=2, ensure_ascii=False)

print(f"Wrote {OUTPUT_PATH}")


# --------------------------------------------------
# Save update.csv
# --------------------------------------------------

with open(UPDATE_CSV, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "file_name",
            "table_name",
            "row_id",
            "column_id",
            "item_id",
            "new_value",
            "item_name",
            "purchase_price",
            "purchase_points",
        ],
    )

    writer.writeheader()
    writer.writerows(updated_rows)

print(f"Wrote {UPDATE_CSV}")

print(f"\nCreated {len(updated_rows)} new items.")
print("Done.")
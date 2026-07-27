import csv
import json
import sys
from copy import deepcopy
from pathlib import Path
import zipfile

# --------------------------------------------------
# Paths
# --------------------------------------------------

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = get_base_dir()

INPUT_FOLDER = BASE_DIR / "GameData"
PATCH_FOLDER = BASE_DIR / "AP_PATCH"

patch_files = list(PATCH_FOLDER.glob("*.zip"))

if not patch_files:
    raise FileNotFoundError(f"No patch zip files found in {PATCH_FOLDER}")

PATCH_ZIP = max(
    PATCH_FOLDER.glob("*.zip"),
    key=lambda f: f.stat().st_mtime
)

PATCH_FILENAME = "patch.csv"

ITEM_PATH = INPUT_FOLDER / "db.aston.en" / "item.bin.json"
OUTPUT_PATH = INPUT_FOLDER / "db.aston.en" / "adjusted_item.bin.json"

UPDATE_CSV = BASE_DIR / "updates.csv"
MAPPING_CSV = BASE_DIR/ "Assets" / "item_mapping.csv"


# --------------------------------------------------
# Load files
# --------------------------------------------------

print("Loading item.bin.json...")

with open(ITEM_PATH, encoding="utf-8") as f:
    item_data = json.load(f)

import zipfile

print(f"Loading patch from {PATCH_ZIP.name}")

with zipfile.ZipFile(PATCH_ZIP, "r") as z:

    if PATCH_FILENAME not in z.namelist():
        raise FileNotFoundError(
            f"{PATCH_FILENAME} not found inside {PATCH_ZIP.name}. "
            f"Found: {z.namelist()}"
        )

    with z.open(PATCH_FILENAME) as f:
        patch_rows = list(
            csv.DictReader(
                line.decode("utf-8")
                for line in f
            )
        )


# --------------------------------------------------
# Build existing item name -> icon/explanation lookup
# --------------------------------------------------

name_to_icon = {}
name_to_explanation = {}


# --------------------------------------------------
# AP item quality fallback lookups
# --------------------------------------------------

def get_quality_icon(item_quality):
    if item_quality == "useful":
        return 12174

    if item_quality in ("progression", "trap"):
        return 12173

    return 5926


def get_quality_explanation(item_quality):
    if item_quality == "useful":
        return "From another world, this seems useful."

    if item_quality in ("progression", "trap"):
        return "From another world, this seems important!"

    return "From another world, maybe someone wants this?"


for key, value in item_data.items():

    if not key.isdigit():
        continue

    if not isinstance(value, dict):
        continue

    inner_key = next(iter(value.keys()))
    item = value[inner_key]

    existing_name = item.get("name")

    if existing_name:
        name_to_icon[existing_name] = item.get(
            "icon",
            5944
        )

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
mapping_rows = []


for row in patch_rows:

    item_name = row["item_name"].strip()

    if not item_name:
        updated_rows.append(row)
        continue

    is_junk = row.get("junk_check", "").lower() == "true"

    # --------------------------------------------------
    # Junk checks reuse an existing item.
    # Do NOT create a new item.bin entry.
    # --------------------------------------------------

    if is_junk:

        row["new_value"] = row["item_id"]

        row["purchase_price"] = (
            row.get("purchase_price")
            or 1
        )

        row["purchase_points"] = (
            row.get("purchase_points")
            or 1
        )

        updated_rows.append(row)
        continue

    # --------------------------------------------------
    # Normal AP items create a brand new item entry
    # --------------------------------------------------

    row_id = str(next_row)

    # Preserve original item_id before replacing it
    original_item_id = row.get("item_id", "")

    new_entry = deepcopy(template_row)

    new_entry["name"] = item_name

    new_entry["icon"] = name_to_icon.get(
        item_name,
        get_quality_icon(row.get("item_quality", ""))
    )

    new_entry["reARMP_rowIndex"] = (next_row - 2)
    new_entry["max_count_base"] = 99
    new_entry["reARMP_isValid"] = "1"
    new_entry["hide_on_pause_menu"] = 1

    new_entry["explanation"] = name_to_explanation.get(
        item_name,
        get_quality_explanation(row.get("item_quality", ""))
    )

    item_data[row_id] = {
        item_name: new_entry
    }

    # Update patch row to point at the newly-created item
    row["item_id"] = row_id
    row["new_value"] = row_id

    row["purchase_price"] = (
        row.get("purchase_price")
        or 1
    )

    row["purchase_points"] = (
        row.get("purchase_points")
        or 1
    )

    updated_rows.append(row)

    # Create mapping entry only for generated items
    mapping_rows.append(
        {
            "KEY": row_id,
            "ITEM": original_item_id,
            "LOCATION": row.get(
                "location_id",
                ""
            )
        }
    )

    next_row += 1
# --------------------------------------------------
# Update header values
# --------------------------------------------------

item_data["ROW_COUNT"] = next_row

item_data["TEXT_COUNT"] = (
    int(item_data.get("TEXT_COUNT", 0))
    + len(updated_rows)
)


# --------------------------------------------------
# Save adjusted item.bin.json
# --------------------------------------------------

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(
        item_data,
        f,
        indent=2,
        ensure_ascii=False
    )

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
            "location_id",
        ],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(updated_rows)


print(f"Wrote {UPDATE_CSV}")


# --------------------------------------------------
# Save item_mapping.csv
# --------------------------------------------------

with open(MAPPING_CSV, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "KEY",
            "ITEM",
            "LOCATION",
        ],
    )

    writer.writeheader()
    writer.writerows(mapping_rows)


print(f"Wrote {MAPPING_CSV}")


print(f"\nCreated {len(updated_rows)} new items.")
print(f"Created {len(mapping_rows)} mapping entries.")
print("Done.")
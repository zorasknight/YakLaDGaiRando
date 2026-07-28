import csv
import json
import re

INPUT_CSV = "new_source.csv"
OUTPUT_JSON = "items.json"

CATEGORY_MAP = {
    "5": "important",
    "6": "useful",
    "4": "filler",
    "11": "filler",
}

CATEGORY_ORDER = {
    "IMPORTANT": 1,
    "GEAR": 2,
    "MISC": 3,
    "HEALING": 4,
    "TRAP": 5,
}


def make_key(name):
    """
    Convert item name into lowercase underscore format.
    Example:
    "Fighter's Binding" -> "fighter_s_binding"
    """
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def get_classification(row):
    """
    Determine item classification.
    Trap items override healing/category 11.
    """
    readable_name = row["Human Readable Name"].lower()

    if readable_name.startswith("trap"):
        return "trap"

    return CATEGORY_MAP.get(row["Category"])


items = {}

with open(INPUT_CSV, "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        classification = get_classification(row)

        # Skip unknown categories
        if not classification:
            continue

        item_key = make_key(row["Item Name"])

        # Only keep each item once
        if item_key in items:
            continue

        items[item_key] = {
            "label": row["Item Name"],
            "item_id": row["Item ID"],
            "classification": classification,
            "purchase_price": row["Monetary Cost"] or "0",
            "purchase_points": row["Point Cost"] or "0",
        }


# Sort by classification, then item name
sorted_items = dict(
    sorted(
        items.items(),
        key=lambda x: (
            CATEGORY_ORDER.get(x[1]["classification"], 999),
            x[0]
        )
    )
)


with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
    json.dump(sorted_items, json_file, indent=2, ensure_ascii=False)


print(f"Wrote {len(sorted_items)} unique items to {OUTPUT_JSON}")
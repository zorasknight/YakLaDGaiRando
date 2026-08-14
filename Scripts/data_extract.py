import csv
import json
import re

INPUT_CSV = "new_source.csv"
OUTPUT_JSON = "items.json"


CATEGORY_TAG_MAP = {
    "5": "useful",
    "6": "useful",
    "4": "filler",
    "11": "filler",
}


CATEGORY_ORDER = {
    "important": 1,
    "useful": 2,
    "filler": 3,
    "trap": 4,
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


def normalize_tag(tag):
    """
    Convert tags into consistent format.

    Examples:
    "Pocket Circuit" -> "POCKET_CIRCUIT"
    "Quest" -> "QUEST"
    """
    tag = tag.strip()

    if not tag:
        return None

    tag = tag.upper()
    tag = re.sub(r"[^A-Z0-9]+", "_", tag)

    return tag.strip("_")


def get_item_tags(row):
    """
    Build item tag list.

    Includes:
    - Existing category classification
    - Trap detection
    - Additional Item Tag column values
    """

    tags = []

    readable_name = row["Human Readable Name"].lower()

    # Trap override
    if readable_name.startswith("trap"):
        tags.append("TRAP")

    else:
        category_tag = CATEGORY_TAG_MAP.get(
            row["Category"]
        )

        if category_tag:
            tags.append(
                category_tag.upper()
            )


    # Add custom item tags
    extra_tags = row.get(
        "Item Tag",
        ""
    )

    if extra_tags:

        # Supports:
        # Pocket Circuit
        # Quest, Cartridge
        # QUEST|CARTRIDGE
        split_tags = re.split(
            r"[,|;]",
            extra_tags
        )

        for tag in split_tags:

            normalized = normalize_tag(tag)

            if normalized:
                tags.append(normalized)


    # Remove duplicates while preserving order
        # Remove duplicates while preserving order
    tags = list(
        dict.fromkeys(tags)
    )

    # Promote certain items to IMPORTANT.
    # IMPORTANT replaces USEFUL but leaves other tags intact.
    important_tags = {
        "IMPORTANT",
        "QUEST",
        "POCKET_CIRCUIT",
        "SHOP_KEY",
    }

    if any(tag in important_tags for tag in tags):
        tags = [
            tag
            for tag in tags
            if tag not in {
                "IMPORTANT",
                "USEFUL",
                "FILLER",
            }
        ]

        tags.insert(0, "IMPORTANT")

    return tags


items = {}


with open(INPUT_CSV, "r", encoding="utf-8") as csv_file:

    reader = csv.DictReader(csv_file)

    for row in reader:

        tags = get_item_tags(row)

        # Skip items with no usable tags
        if not tags:
            continue


        item_key = make_key(
            row["Item Name"]
        )


        # Only keep each item once
        if item_key in items:
            continue


        items[item_key] = {

            "label": row["Item Name"],

            "item_id": row["Item ID"],

            "tags": tags,

            "purchase_price": (
                row["Monetary Cost"]
                or "0"
            ),

            "purchase_points": (
                row["Point Cost"]
                or "0"
            ),
        }



# Sort by first tag priority, then item name
sorted_items = dict(
    sorted(
        items.items(),
        key=lambda x: (
            CATEGORY_ORDER.get(
                x[1]["tags"][0].lower(),
                999
            ),
            x[0]
        )
    )
)


with open(
    OUTPUT_JSON,
    "w",
    encoding="utf-8"
) as json_file:

    json.dump(
        sorted_items,
        json_file,
        indent=2,
        ensure_ascii=False
    )


print(
    f"Wrote {len(sorted_items)} unique items to {OUTPUT_JSON}"
)
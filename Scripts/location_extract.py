import csv
import json

INPUT_CSV = "new_source.csv"
OUTPUT_JSON = "locations.json"


REGION_TAGS = {
    "SOTENBORI_4": "SOTENBORI_4",
    "SOTENBORI_3": "SOTENBORI_3",
    "SOTENBORI_2": "SOTENBORI_2",
    "SOTENBORI_1": "SOTENBORI_1",

    "COLOSSEUM_4": "COLOSSEUM_4",
    "COLOSSEUM_3": "COLOSSEUM_3",
    "COLOSSEUM_2": "COLOSSEUM_2",
    "COLOSSEUM_1": "COLOSSEUM_1",

    "POCKET CIRCUIT_4": "POCKET_CIRCUIT_4",
    "POCKET CIRCUIT_3": "POCKET_CIRCUIT_3",
    "POCKET CIRCUIT_2": "POCKET_CIRCUIT_2",
    "POCKET CIRCUIT_1": "POCKET_CIRCUIT_1",

    "YOKOHAMA": "YOKOHAMA",
}


def get_region(row):
    """
    Determine region based on:
    1. Junk flag
    2. Region tag in the Tags column
    """

    # Junk overrides everything
    if row["Junk"].strip().lower() == "true":
        return "JUNK"

    tags = row.get("Tags", "").upper()

    for tag, region in REGION_TAGS.items():
        if tag in tags:
            return region

    return "MISC"


locations = {}

with open(INPUT_CSV, "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        identifier = row["Unique_Location_Identifier"]

        # Keep each location only once
        if identifier in locations:
            continue

        locations[identifier] = {
            "label": row["Human Readable Name"],
            "location": row["Location"],
            "id": row["Unique_Location_Slot_ID"],
            "slot": row["Slot"],
            "source": row["Source"],
            "tags": row.get("Tags", ""),
            "region": get_region(row),
        }


with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
    json.dump(locations, json_file, indent=2, ensure_ascii=False)


print(f"Wrote {len(locations)} locations to {OUTPUT_JSON}")
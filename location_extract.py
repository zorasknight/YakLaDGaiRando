import csv
import json

INPUT_CSV = "new_source.csv"
OUTPUT_JSON = "locations.json"


def get_region(row):
    """
    Determine region based on:
    1. Junk flag
    2. Human readable name
    3. Location identifier fallback
    """

    # Junk overrides everything
    if row["Junk"].strip().lower() == "true":
        return "JUNK"

    name = row["Human Readable Name"].lower()
    location = row["Location"].lower()

    # Check human readable name first
    if "sotenbori" in name:
        return "SOTENBORI"

    if "yokohama" in name:
        return "YOKOHAMA"

    if "pocket circuit" in name:
        return "POCKET_CIRCUIT"

    if "dart" in name:
        return "DARTS"

    if "colosseum" in name:
        return "COLOSSEUM"

    # Fallback to location naming convention
    if "aston_s" in location:
        return "SOTENBORI"

    if "aston_y" in location:
        return "YOKOHAMA"

    if "aston_c" in location:
        return "COLOSSEUM"

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
            "region": get_region(row),
        }


with open(OUTPUT_JSON, "w", encoding="utf-8") as json_file:
    json.dump(locations, json_file, indent=2, ensure_ascii=False)


print(f"Wrote {len(locations)} locations to {OUTPUT_JSON}")
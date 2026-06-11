import csv
import random
from collections import defaultdict

# =========================
# Config
# =========================
INPUT_CSV = "source.csv"
OUTPUT_CSV = "updates.csv"

monetary_min = 100
monetary_max = 1000000

point_min = 10
point_max = 4000

# Categories that may NEVER be placed into Junk slots
NO_JUNK_CATEGORIES = {"5"}

random.seed()

# =========================
# Sphere locks
# =========================
FORCED_SPHERES = {
    "6015": 0,
    "6049": 0,
    "6050": 0,
    "6051": 0,
    "6053": 1,
    "6054": 1,
    "6055": 1,
    "6056": 1,
}

# =========================
# Load CSV
# =========================
def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# =========================
# Spheres
# =========================
def build_pools(rows):
    pools = defaultdict(list)
    for r in rows:
        pools[r["Sphere"]].append(r)
    return pools


# =========================
# Helpers
# =========================
def is_empty(v):
    return v is None or str(v).strip() == ""

def rand_money():
    return random.randint(monetary_min, monetary_max)

def rand_point():
    return random.randint(point_min, point_max)


# =========================
# Shuffle Item IDs
# =========================
def shuffle_all_items(rows):

    # normalize
    for r in rows:
        r["Item ID"] = str(r["Item ID"])

    # Remember each item's category
    item_category = {
        r["Item ID"]: str(r["Category"]).strip()
        for r in rows
    }

    # Build item list
    item_ids = [r["Item ID"] for r in rows]

    # Process constrained categories first
    protected = [
        i for i in item_ids
        if item_category[i] in NO_JUNK_CATEGORIES
    ]

    normal = [
        i for i in item_ids
        if item_category[i] not in NO_JUNK_CATEGORIES
    ]

    random.shuffle(protected)
    random.shuffle(normal)

    item_ids = protected + normal

    pools = build_pools(rows)
    used = set()

    # avoid assigning an item multiple times for costs
    economy_map = {}

    updates = []

    for item_id in item_ids:

        forced_sphere = FORCED_SPHERES.get(item_id)
        category = item_category[item_id]

        def valid_slot(r):
            if category in NO_JUNK_CATEGORIES:
                return str(r.get("Junk", "")).strip().upper() != "TRUE"
            return True

        # handles forced sphere placement
        if forced_sphere is not None:
            candidates = [
                r for r in pools[str(forced_sphere)]
                if id(r) not in used
                and valid_slot(r)
            ]
        else:
            candidates = [
                r for r in rows
                if id(r) not in used
                and valid_slot(r)
            ]

        if not candidates:
            raise Exception(f"No valid slot for item {item_id}")

        slot = random.choice(candidates)
        used.add(id(slot))

        source_file = slot["Source"]
        table_name = slot["Location"]
        row_id = slot["Slot"]

        column = "replacement_item_id"

        # =========================
        # Change Point and Monetary Costs
        # =========================
        if item_id not in economy_map:

            price = slot.get("Monetary Cost")
            points = slot.get("Point Cost")

            if is_empty(price):
                price = rand_money()

            if is_empty(points):
                points = rand_point()

            economy_map[item_id] = {
                "purchase_price": int(price),
                "purchase_points": int(points)
            }

        econ = economy_map[item_id]

        # =========================
        # Create Output
        # =========================
        updates.append({
            "file_name": source_file,
            "table_name": table_name,
            "row_id": row_id,
            "column_id": column,
            "item_id": item_id,
            "new_value": item_id,
            "purchase_price": econ["purchase_price"],
            "purchase_points": econ["purchase_points"],
        })

    return updates


# =========================
# Write Output
# =========================
def write_updates(updates, path):

    with open(path, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "file_name",
                "table_name",
                "row_id",
                "column_id",
                "item_id",
                "new_value",
                "purchase_price",
                "purchase_points"
            ]
        )

        writer.writeheader()
        writer.writerows(updates)


# =========================
# Main
# =========================

def main():
    rows = load_rows(INPUT_CSV)

    updates = shuffle_all_items(rows)

    write_updates(updates, OUTPUT_CSV)

    print(f"Shuffled {len(updates)} item placements -> {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
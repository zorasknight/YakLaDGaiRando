import csv
import random
from collections import defaultdict

# =========================
# CONFIG
# =========================
INPUT_CSV = "source.csv"
OUTPUT_CSV = "updates.csv"

monetary_min = 100
monetary_max = 1000000

point_min = 10
point_max = 4000

random.seed()

# =========================
# HARD CONSTRAINTS
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
# LOAD CSV
# =========================
def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# =========================
# POOLS
# =========================
def build_pools(rows):
    pools = defaultdict(list)
    for r in rows:
        pools[r["Sphere"]].append(r)
    return pools


# =========================
# HELPERS
# =========================
def is_empty(v):
    return v is None or str(v).strip() == ""

def rand_money():
    return random.randint(monetary_min, monetary_max)

def rand_point():
    return random.randint(point_min, point_max)


# =========================
# CORE SHUFFLE
# =========================
def shuffle_all_items(rows):

    # normalize
    for r in rows:
        r["Item ID"] = str(r["Item ID"])

    item_ids = [r["Item ID"] for r in rows]
    random.shuffle(item_ids)

    pools = build_pools(rows)
    used = set()

    # IMPORTANT: same item_id always same economy
    economy_map = {}

    updates = []

    for item_id in item_ids:

        forced_sphere = FORCED_SPHERES.get(item_id)

        # -------------------------
        # SELECT SLOT
        # -------------------------
        if forced_sphere is not None:
            candidates = [
                r for r in pools[str(forced_sphere)]
                if id(r) not in used
            ]
        else:
            candidates = [
                r for r in rows
                if id(r) not in used
            ]

        if not candidates:
            raise Exception(f"No valid slot for item {item_id}")

        slot = random.choice(candidates)
        used.add(id(slot))

        source_file = slot["Source"]
        table_name = slot["Location"]
        row_id = slot["Slot"]

        column = "get_item_id" if source_file == "item_get_by_wire.bin.json" else "1"

        # =========================
        # ECONOMY (CONSISTENT PER ITEM)
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
        # OUTPUT ROW
        # =========================
        updates.append({
            "file_name": source_file,
            "table_name": table_name,
            "row_id": row_id,
            "column_id": column,
            "item_id": item_id,

            # NEW FIELDS (restored)
            "new_value": item_id,
            "purchase_price": econ["purchase_price"],
            "purchase_points": econ["purchase_points"],
        })

    return updates


# =========================
# WRITE OUTPUT
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
# MAIN
# =========================
if __name__ == "__main__":

    rows = load_rows(INPUT_CSV)

    updates = shuffle_all_items(rows)

    write_updates(updates, OUTPUT_CSV)

    print(f"Shuffled {len(updates)} item placements -> {OUTPUT_CSV}")
import csv
import random
from collections import defaultdict

# =========================
# CONFIG
# =========================
INPUT_CSV = "source.csv"
OUTPUT_CSV = "updates.csv"

random.seed()  # set fixed int for reproducible runs if needed


# =========================
# HARD CONSTRAINTS
# =========================
FORCED_SPHERES = {
    #Soccer Ball
    #Shoes
    #Baby Tooth
    #Hat
    "6015": 0,
    "6049": 0,
    "6050": 0,
    "6051": 0,
    #Signed Ball
    #Underwear
    #Crawfish
    #Golden Ball
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
# BUILD POOLS
# =========================
def build_pools(rows):
    """
    Groups available slots by sphere.
    Also tracks junk restriction.
    """

    pools = defaultdict(list)

    for r in rows:
        sphere = r["Sphere"]
        pools[sphere].append(r)

    return pools


# =========================
# SHUFFLE WITH ENFORCEMENT
# =========================
def shuffle_all_items(rows):

    # normalize item ids
    for r in rows:
        r["Item ID"] = int(r["Item ID"])

    item_ids = [r["Item ID"] for r in rows]
    random.shuffle(item_ids)

    pools = build_pools(rows)

    # track used slots so we don't double assign
    used = set()

    updates = []

    for item_id in item_ids:

        forced_sphere = FORCED_SPHERES.get(item_id)

        # -------------------------
        # SELECT VALID POOL
        # -------------------------
        if forced_sphere is not None:
            candidates = [
                r for r in pools[str(forced_sphere)]
                if id(r) not in used
            ]

            if not candidates:
                raise Exception(
                    f"NO VALID SLOT: item {item_id} "
                    f"requires sphere {forced_sphere}"
                )

        else:
            candidates = [
                r for r in rows
                if id(r) not in used
            ]

            if not candidates:
                raise Exception("No valid slots left")

        slot = random.choice(candidates)
        used.add(id(slot))

        # -------------------------
        # APPLY RULES
        # -------------------------
        source_file = slot["Source"]

        # column logic
        if source_file == "item_get_by_wire.bin.json":
            column = "get_item_id"
        else:
            column = "1"

        updates.append({
            "file_name": source_file,
            "table_name": slot["Location"],
            "row_id": slot["Slot"],
            "column_id": column,
            "new_value": item_id
        })

    return updates


# =========================
# WRITE OUTPUT CSV
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
                "new_value"
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

    print(f"Shuffled {len(updates)} items with enforcement -> {OUTPUT_CSV}")
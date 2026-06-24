import csv
import random
from collections import defaultdict
from Scripts.settings import settings

# Config

INPUT_CSV = "source.csv"
OUTPUT_CSV = "updates.csv"


DEFAULT_PRICES = settings.get("remove_default_prices")
SHOP_ITEMS = settings.get("include_shops")
REWARD_ITEMS = settings.get("include_rewards")
COIN_LOCKER_ITEMS = settings.get("include_coin_lockers")
MINIGAME_ITEMS = settings.get("include_minigames")
POOL_ITEMS = settings.get("include_pool")
GOLF_ITEMS = settings.get("include_golf")
CASINOS_ITEMS = settings.get("include_casinos")
SHOGI_ITEMS = settings.get("include_shogi")
DART_ITEMS = settings.get("include_darts")
POCKET_CIRCUIT_ITEMS = settings.get("include_pocket_circuit")
WEIRD_SHOP_ITEMS = settings.get("include_weird_shops")
CONSUMABLE_SHOP_ITEMS = settings.get("include_consumable_shops")




MONETARY_MIN = settings.get("monetary_min")
MONETARY_MAX = settings.get("monetary_max")

POINT_MIN = settings.get("point_min")
POINT_MAX = settings.get("point_max")

# Categories that may NEVER be placed into Junk slots
NO_JUNK_CATEGORIES = {"5"}

random.seed()

# Sphere locks

FORCED_SPHERES = {
    "6049": 0,
    "6050": 0,
    "6051": 0,
    "6053": 0,
    "6015": 1,
    "6054": 1,
    "6055": 1,
    "6056": 1,
}

# Load CSV

def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# Spheres

def build_pools(rows):
    pools = defaultdict(list)
    for r in rows:
        pools[r["Sphere"]].append(r)
    return pools

# Helpers

def is_empty(v):
    return v is None or str(v).strip() == ""

def rand_money():
    return random.randint(MONETARY_MIN, MONETARY_MAX)

def rand_point():
    return random.randint(POINT_MIN, POINT_MAX)

def apply_file_blacklist(rows):
    blacklist = set()

    if not SHOP_ITEMS:
        blacklist.update(["aston_s_ebisuya", "aston_c_loungeshop", "aston_c_boutique_equip", "aston_s_wannpark", "aston_s_akame", "aston_c_boutique", "aston_y_shichiya", "aston_y_lovemagic", "aston_c_boutique_vip", "aston_s_mizorogi_2", "aston_s_mizorogi"])

    if not REWARD_ITEMS:
        blacklist.update(["pokecir"])

    if not COIN_LOCKER_ITEMS:
        blacklist.update(["aston_coinlocker"])
    
    if not MINIGAME_ITEMS:
        blacklist.update(["aston_s_billiards_prize", "darts", "aston_c_casino", "aston_y_shogi", "aston_s_shogi", "aston_s_golf", "aston_s_toba", "aston_y_toba", "aston_c_toba",])
    
    if not POOL_ITEMS:
        blacklist.update(["aston_s_billiards_prize"])
    
    if not DART_ITEMS:
        blacklist.update(["darts"])
    
    if not CASINOS_ITEMS:
        blacklist.update(["aston_c_casino", "aston_s_toba", "aston_y_toba", "aston_c_toba",])
    
    if not SHOGI_ITEMS:
        blacklist.update(["aston_y_shogi", "aston_s_shogi"])
    
    if not GOLF_ITEMS:
        blacklist.update(["aston_s_golf"])
    
    if not POCKET_CIRCUIT_ITEMS:
        blacklist.update(["aston_s_pokecir_parts"])

    if not WEIRD_SHOP_ITEMS:
        blacklist.update(["aston_y_ichibann", "aston_y_smilewagon", "aston_s_shigano", "aston_s_hiratai", "aston_s_kukuru"])

    if not CONSUMABLE_SHOP_ITEMS:
        blacklist.update(["aston_s_poppo_ashi", "aston_s_poppo_sh", "aston_s_poppo_so", "aston_y_poppo02", "aston_s_tsuruha"])

    if not blacklist:
        return rows

    return [
        r for r in rows
        if r.get("Location") not in blacklist
    ]

# Shuffle Item IDs

def shuffle_all_items(rows):

    for r in rows:
        r["Item ID"] = str(r["Item ID"])

    item_category = {
        r["Item ID"]: str(r["Category"]).strip()
        for r in rows
    }

    # Build item list
    item_ids = [r["Item ID"] for r in rows]

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

        # Change Point and Monetary Costs
        if item_id not in economy_map:

            if DEFAULT_PRICES:
                price = rand_money()
                points = rand_point()
            else:
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


        # Create Output
        updates.append({
            "file_name": source_file,
            "table_name": table_name,
            "row_id": row_id,
            "column_id": column,
            "item_id": slot["Item ID"],
            "new_value": item_id,
            "purchase_price": econ["purchase_price"],
            "purchase_points": econ["purchase_points"],
        })

    return updates

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

# MAIN

def main():
    rows = load_rows(INPUT_CSV)

    rows = apply_file_blacklist(rows)

    updates = shuffle_all_items(rows)

    write_updates(updates, OUTPUT_CSV)

    print(f"Shuffled {len(updates)} item placements -> {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
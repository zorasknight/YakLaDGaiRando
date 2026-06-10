import csv
import json
from pathlib import Path

# ============================================================
# Config
# ============================================================

INPUT_FOLDER = Path("GameData")
OUTPUT_FOLDER = Path("GameData_Output")
UPDATES_CSV = "updates.csv"

ITEM_PATH = INPUT_FOLDER / "db.aston.en" / "item.bin.json"

# ============================================================
# Create log files
# ============================================================

CHANGE_LOG_PATH = Path("change_log.txt")
ERROR_LOG_PATH = Path("error_warning_log.txt")


def log_change(msg: str):
    with open(CHANGE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def log_error(msg: str):
    with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


CHANGE_LOG_PATH.write_text("", encoding="utf-8")
ERROR_LOG_PATH.write_text("", encoding="utf-8")

# ============================================================
# Grab required updates
# ============================================================

def load_updates():
    updates = {}

    with open(UPDATES_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            filename = row["file_name"]

            updates.setdefault(filename, []).append({
                "table_name": row["table_name"],
                "row_id": str(row["row_id"]),
                "column_id": row["column_id"],
                "item_id": row["item_id"],
                "new_value": int(row["new_value"]),
                "purchase_price": row["purchase_price"],
                "purchase_points": row.get("purchase_points")
            })

    return updates

# ============================================================
# Shops
# ============================================================

def update_shop(data, updates):

    changes = 0

    for u in updates:

        if u["column_id"] != "replacement_item_id":
            continue

        table_name = u["table_name"]
        row_id = u["row_id"]
        new_value = u["new_value"]

        for root_key, root_value in data.items():

            if not isinstance(root_value, dict):
                continue

            if table_name not in root_value:
                continue

            shop_wrapper = root_value[table_name]

            if "table" not in shop_wrapper:
                msg = f"[WARN] shop | missing table wrapper | {table_name}"
                print(msg)
                log_error(msg)
                break

            table = shop_wrapper["table"]

            if row_id not in table:
                msg = f"[WARN] shop | missing row {row_id} | {table_name}"
                print(msg)
                log_error(msg)
                break

            row_container = table[row_id]

            if "" not in row_container:
                msg = f"[WARN] shop | missing inner dict | {table_name} row={row_id}"
                print(msg)
                log_error(msg)
                break

            row = row_container[""]

            if "1" not in row:
                msg = f"[WARN] shop | missing column '1' | {table_name} row={row_id}"
                print(msg)
                log_error(msg)
                break

            old_value = row["1"]
            row["1"] = new_value

            changes += 1

            msg = f"[SHOP] {table_name} row={row_id} {old_value} -> {new_value}"
            print(msg)
            log_change(msg)

            break

    return changes


# ============================================================
# Rewards
# ============================================================

def update_reward(data, updates):

    changes = 0

    for u in updates:

        if u["column_id"] != "replacement_item_id":
            continue

        table_name = u["table_name"]
        row_id = u["row_id"]
        new_value = u["new_value"]

        for root_key, root_value in data.items():

            if not isinstance(root_value, dict):
                continue

            if table_name not in root_value:
                continue

            reward_wrapper = root_value[table_name]

            if "table" not in reward_wrapper:
                msg = f"[WARN] reward | missing table wrapper | {table_name}"
                print(msg)
                log_error(msg)
                break

            table = reward_wrapper["table"]

            if row_id not in table:
                msg = f"[WARN] reward | missing row {row_id} | {table_name}"
                print(msg)
                log_error(msg)
                break

            row_container = table[row_id]

            if "" not in row_container:
                msg = f"[WARN] reward | missing inner dict | {table_name} row={row_id}"
                print(msg)
                log_error(msg)
                break

            row = row_container[""]

            if "3" not in row:
                msg = f"[WARN] reward | missing column '3' | {table_name} row={row_id}"
                print(msg)
                log_error(msg)
                break

            old_value = row["3"]
            row["3"] = new_value

            changes += 1

            msg = f"[REWARD] {table_name} row={row_id} {old_value} -> {new_value}"
            print(msg)
            log_change(msg)

            break

    return changes


# ============================================================
# Lockers
# ============================================================

def update_coinlocker(data, updates):

    changes = 0

    root = data.get("1")
    if not isinstance(root, dict):
        msg = "[WARN] coinlocker | missing root table '1'"
        print(msg)
        log_error(msg)
        return 0

    region_name = next(iter(root.keys()))
    region = root[region_name]

    if "keys" not in region:
        msg = f"[WARN] coinlocker | missing keys table | {region_name}"
        print(msg)
        log_error(msg)
        return 0

    table = region["keys"]

    for u in updates:

        if u["column_id"] != "replacement_item_id":
            continue

        row_id = str(u["row_id"])
        new_value = u["new_value"]

        if row_id not in table:
            continue

        row = table[row_id][""]

        old_value = row.get("2")
        row["2"] = new_value

        changes += 1

        msg = f"[LOCKER] row={row_id} {old_value} -> {new_value}"
        print(msg)
        log_change(msg)

    return changes


# ============================================================
# Wire
# ============================================================

def update_wire(data, updates):

    changes = 0

    for u in updates:

        if u["column_id"] != "replacement_item_id":
            continue

        row_id = str(u["row_id"])
        new_value = u["new_value"]

        if row_id not in data:
            continue

        row_container = data[row_id]

        if not isinstance(row_container, dict):
            continue

        inner_row = None

        for k, v in row_container.items():
            if isinstance(v, dict) and "get_item_id" in v:
                inner_row = v
                break

        if inner_row is None:
            continue

        old_value = inner_row["get_item_id"]
        inner_row["get_item_id"] = new_value

        changes += 1

        msg = f"[WIRE] row={row_id} {old_value} -> {new_value}"
        print(msg)
        log_change(msg)

    return changes

# ============================================================
# Patch prices in item.bin
# ============================================================

def patch_item_bin_prices(updates_by_file):

    print("\n[ITEM] Processing item.bin.json")

    if not ITEM_PATH.exists():
        msg = f"[ITEM] Missing file: {ITEM_PATH}"
        print(msg)
        log_error(msg)
        return

    with open(ITEM_PATH, encoding="utf-8") as f:
        data = json.load(f)

    changes = 0

    POINT_FIELDS = [
        "buy_syogi_point",
        "buy_casino_point",
        "buy_toba_point",
        "buy_akame_point",
        "buy_billiard_point",
        "buy_golf_point",
        "buy_pokecir_point",
    ]

    for _, updates in updates_by_file.items():

        for u in updates:

            item_id = str(u.get("item_id"))
            new_price = u.get("purchase_price")
            new_points = u.get("purchase_points")

            if not item_id:
                continue

            if item_id not in data:
                continue

            item_block = data[item_id]

            if not isinstance(item_block, dict):
                continue

            inner_key = next(iter(item_block.keys()))
            row = item_block[inner_key]

            # ------------------------
            # purchase price update
            # ------------------------
            if "purchase_price" in row and new_price is not None:
                old_value = row["purchase_price"]
                row["purchase_price"] = int(new_price)

                msg = f"[ITEM PRICE] id={item_id} {old_value} -> {new_price}"
                print(msg)
                log_change(msg)

                changes += 1

            # ------------------------
            # point system update
            # ------------------------
            if new_points is not None:
                try:
                    point_val = int(new_points)

                    for field in POINT_FIELDS:
                        if field in row:
                            row[field] = point_val

                    msg = f"[ITEM POINTS] id={item_id} -> {point_val}"
                    print(msg)
                    log_change(msg)

                except ValueError:
                    msg = f"[WARN] invalid point value for item {item_id}: {new_points}"
                    print(msg)
                    log_error(msg)

    output_path = OUTPUT_FOLDER / "db.aston.en" / "item.bin.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[ITEM] Saved {changes} price changes")


# ============================================================
# Detect File
# ============================================================

def detect_type(filename):

    if filename == "shop.bin.json":
        return "shop"

    if filename == "talk_coinlocker_locker.bin.json":
        return "coinlocker"

    if filename == "item_get_by_wire.bin.json":
        return "wire"
    
    if filename == "reward_table.bin.json":
        return "reward"

    return "unknown"


def apply_updates(json_path, updates):

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    file_type = detect_type(json_path.name)

    if file_type == "shop":
        changes = update_shop(data, updates)

    elif file_type == "coinlocker":
        changes = update_coinlocker(data, updates)

    elif file_type == "wire":
        changes = update_wire(data, updates)

    elif file_type == "reward":
        changes = update_reward(data, updates)

    else:
        return

    if changes == 0:
        return

    output_path = OUTPUT_FOLDER / json_path.relative_to(INPUT_FOLDER)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ============================================================
# MAIN
# ============================================================

def main():

    updates_by_file = load_updates()

    json_files = list(INPUT_FOLDER.rglob("*.json"))

    print(f"Found {len(json_files)} JSON files")

    for json_file in json_files:
        if json_file.name in updates_by_file:
            apply_updates(json_file, updates_by_file[json_file.name])

    patch_item_bin_prices(updates_by_file)


if __name__ == "__main__":
    main()
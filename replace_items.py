import csv
import json
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

INPUT_FOLDER = Path("GameData")
OUTPUT_FOLDER = Path("GameData_Output")
UPDATES_CSV = "updates.csv"

# ============================================================
# ROOT LOG FILES (NEW)
# ============================================================

CHANGE_LOG_PATH = Path("change_log.txt")
ERROR_LOG_PATH = Path("error_warning_log.txt")


def log_change(msg: str):
    with open(CHANGE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def log_error(msg: str):
    with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


# clear logs each run
CHANGE_LOG_PATH.write_text("", encoding="utf-8")
ERROR_LOG_PATH.write_text("", encoding="utf-8")


# ============================================================
# LOAD UPDATES
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
                "new_value": int(row["new_value"])
            })

    return updates


# ============================================================
# SHOP.BIN.JSON
# ============================================================

def update_shop(data, updates):

    changes = 0

    for u in updates:

        table_name = u["table_name"]
        row_id = u["row_id"]
        new_value = u["new_value"]

        found_table = False

        for root_key, root_value in data.items():

            if not isinstance(root_value, dict):
                continue

            if table_name not in root_value:
                continue

            found_table = True

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
                msg = (
                    f"[WARN] shop | missing inner dict | "
                    f"{table_name} row={row_id}"
                )
                print(msg)
                log_error(msg)
                break

            row = row_container[""]

            if "1" not in row:
                msg = (
                    f"[WARN] shop | missing column '1' | "
                    f"{table_name} row={row_id}"
                )
                print(msg)
                log_error(msg)
                break

            old_value = row["1"]
            row["1"] = new_value

            changes += 1

            msg = (
                f"[SHOP] {table_name} "
                f"row={row_id} "
                f"{old_value} -> {new_value}"
            )

            print(msg)
            log_change(msg)

            break

        if not found_table:
            msg = f"[WARN] shop | table not found | {table_name}"
            print(msg)
            log_error(msg)

    return changes


# ============================================================
# TALK_COINLOCKER_LOCKER.BIN.JSON
# ============================================================

def update_coinlocker(data, updates):

    changes = 0

    root = data.get("1")

    if not isinstance(root, dict):
        msg = "[WARN] coinlocker | missing root table '1'"
        print(msg)
        log_error(msg)
        return 0

    if len(root) == 0:
        msg = "[WARN] coinlocker | no regions found"
        print(msg)
        log_error(msg)
        return 0

    region_name = next(iter(root.keys()))

    print(f"Coinlocker region: {region_name}")

    region = root[region_name]

    if "keys" not in region:
        msg = f"[WARN] coinlocker | missing keys table | {region_name}"
        print(msg)
        log_error(msg)
        return 0

    table = region["keys"]

    for u in updates:

        row_id = str(u["row_id"])
        new_value = u["new_value"]

        if row_id not in table:
            msg = f"[WARN] coinlocker | missing row {row_id}"
            print(msg)
            log_error(msg)
            continue

        row_container = table[row_id]

        if "" not in row_container:
            msg = f"[WARN] coinlocker | missing inner dict | row={row_id}"
            print(msg)
            log_error(msg)
            continue

        row = row_container[""]

        old_value = row.get("2")

        row["2"] = new_value

        changes += 1

        msg = f"[LOCKER] row={row_id} {old_value} -> {new_value}"

        print(msg)
        log_change(msg)

    return changes


# ============================================================
# FILE DISPATCH
# ============================================================

def apply_updates(json_path, updates):

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    filename = json_path.name

    print(f"\nProcessing {filename}")

    changes = 0

    if filename == "shop.bin.json":

        print("Detected type: shop")

        changes = update_shop(
            data,
            updates
        )

    elif filename == "talk_coinlocker_locker.bin.json":

        print("Detected type: coinlocker")

        changes = update_coinlocker(
            data,
            updates
        )

    else:

        print("No handler for this file")
        return

    if changes == 0:
        print("No changes")
        return

    output_path = OUTPUT_FOLDER / json_path.relative_to(INPUT_FOLDER)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved {changes} changes")


# ============================================================
# MAIN
# ============================================================

def main():

    updates_by_file = load_updates()

    json_files = list(INPUT_FOLDER.rglob("*.json"))

    print(f"Found {len(json_files)} JSON files")

    for json_file in json_files:

        if json_file.name not in updates_by_file:
            continue

        apply_updates(
            json_file,
            updates_by_file[json_file.name]
        )


if __name__ == "__main__":
    main()
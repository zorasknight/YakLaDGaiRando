import csv
import random


# =========================
# CONFIG
# =========================
INPUT_CSV = "source.csv"
OUTPUT_CSV = "updates.csv"

random.seed()  # optional fixed seed for reproducibility


# =========================
# LOAD CSV
# =========================
def load_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# =========================
# SHUFFLE ALL ITEMS GLOBALLY
# =========================
def shuffle_all_items(rows):

    # extract all item ids globally
    item_ids = [r["Item ID"] for r in rows]

    shuffled = item_ids[:]
    random.shuffle(shuffled)

    updates = []

    for row, new_id in zip(rows, shuffled):

        source_file = row["Source"]

        # =========================
        # COLUMN RULES BY TARGET FILE
        # =========================
        if source_file == "item_get_by_wire.bin.json":
            column = "get_item_id"
        else:
            column = "1"

        updates.append({
            "file_name": source_file,
            "table_name": row["Location"],
            "row_id": row["Slot"],
            "column_id": column,
            "new_value": new_id
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

    print(f"Shuffled {len(updates)} items globally -> {OUTPUT_CSV}")
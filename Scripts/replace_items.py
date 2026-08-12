import csv
import json
import random
from pathlib import Path
from collections import Counter
import sys
import math
import yaml
import zipfile

SCRIPT_DIR = Path(__file__).resolve().parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


# Config

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent  # EXE mode
    return Path(__file__).resolve().parent.parent  # script mode

def get_patch_zip():

    base_dir = get_base_dir()

    patch_folder = base_dir / "AP_PATCH"

    patch_files = list(
        patch_folder.glob("*.zip")
    )

    if not patch_files:
        raise FileNotFoundError(
            f"No patch zip files found in {patch_folder}"
        )

    return max(
        patch_files,
        key=lambda f: f.stat().st_mtime
    )

def load_ap_settings():

    patch_zip = get_patch_zip()

    print(
        f"[CONFIG] Loading settings from {patch_zip.name}"
    )

    PATCH_YAML = "options.yaml"

    with zipfile.ZipFile(patch_zip, "r") as z:

        if PATCH_YAML not in z.namelist():
            raise FileNotFoundError(
                f"{PATCH_YAML} not found in {patch_zip.name}"
            )

        with z.open(PATCH_YAML) as f:
            return yaml.safe_load(
                f.read().decode("utf-8")
            )

SETTINGS = {}

def init_seed(seed=None):
    import random

    if seed is None or str(seed).strip() == "":
        seed = random.SystemRandom().randint(0, 2**32 - 1)

    random.seed(seed)
    return seed

BASE_DIR = get_base_dir()

INPUT_FOLDER = BASE_DIR / "GameData"
OUTPUT_FOLDER = BASE_DIR / "GameData_Output"
UPDATES_CSV = BASE_DIR / "updates.csv"

ITEM_PATH = INPUT_FOLDER / "db.aston.en" / "adjusted_item.bin.json"
NPC_PATH = INPUT_FOLDER / "db.aston.en" / "character_npc_soldier_personal_data.bin.json"

FIRST_ENCOUNTER_ROW = 6317

INTRO_FIGHTS = [
    6509, 6510, 6511, 6512, 6513, 6516, 6517, 6518, 6519, 6520,
    6521, 6522, 6523, 6524, 6525, 6526, 6527, 6528, 6529, 6530,
    6531, 6532, 6533, 6534, 6535, 6536, 6537, 6538, 6539, 6540,
    6541, 6542, 6543, 6544, 6545, 6546, 6547, 6548, 6549, 6550,
    6551, 6552, 6553, 6554, 6555, 6556, 6557, 6558, 6559, 6560,
    6614, 6615, 6621, 6622, 7049, 7050, 7051, 7052, 7053, 7054,
    7055, 7056, 7057, 7058, 7059, 7060, 7162, 7163, 7626, 7627,
    7755, 8166, 8167, 8168, 8169, 8170, 8171, 8321, 8322, 8323,
    8324, 8325, 8326,
]

SPECIAL0_EFFECTS = {
    0: "No Special Effect",
    2: "Makes enemies more likely to confront you.",
    6: "Continually replenishes your Heat when low on health in combat.",
    13: "Your Heat gradually increases while it's equipped.",
    25: "Build heat faster while attacking",
    28: "Deal more damage with charge attacks",
    31: "Longer invulnerability for dodges",
    39: "Your Heat gradually decreases while it's equipped.",
    40: "The less health you have, the greater your attack is boosted.",
    42: "Suppresses the enemy's will to attack during battle.",
    44: "Deal more damage with throws",
    45: "Auto block bullets from the front",
    82: "Reduces the amount of Heat consumed.",
    83: "Gradually recovers health when near death.",
    84: "Nets you more Akame Points.",
    85: "Spot keys on the ground with these on.",
}

SKILL_MONEY_MIN = 0
SKILL_MONEY_MAX = 0

SKILL_AKAME_MIN = 0
SKILL_AKAME_MAX = 0

PART_TIME_MONEY_MIN = 0
PART_TIME_MONEY_MAX = 0

PART_TIME_AKAME_MIN = 0
PART_TIME_AKAME_MAX = 0

ATTACK_AND_DEFENSE_MIN = 0
ATTACK_AND_DEFENSE_MAX = 0

RESIST_MIN = 0
RESIST_MAX = 0

STATUS_RESIST_MIN = 0
STATUS_RESIST_MAX = 1

def load_config():

    global SETTINGS

    global SHOP_KEYS
    global SKILL_MONEY_MIN
    global SKILL_MONEY_MAX
    global SKILL_AKAME_MIN
    global SKILL_AKAME_MAX
    global PART_TIME_MONEY_MIN
    global PART_TIME_MONEY_MAX
    global PART_TIME_AKAME_MIN
    global PART_TIME_AKAME_MAX
    global ATTACK_AND_DEFENSE_MIN
    global ATTACK_AND_DEFENSE_MAX
    global RESIST_MIN
    global RESIST_MAX
    global INTRO_SKIP
    global ENEMY_HP_MULT
    global ENEMY_ATTACK_MULT
    global RANDOMIZE_ENEMY_STATS
    global POOL_MODIFIER
    global GOLF_MODIFIER
    global SHOGI_MODIFIER
    global CASINO_MODIFIER
    global AKAME_SHOP_MODIFIER
    global POCKET_CIRCUIT_MODIFIER
    global MAX_GOLDEN_BALL_COUNT
    global REQUIRED_GOLDEN_BALL_COUNT
    global PROGRESSIVE_GRAPPLE_ITEMS


    SETTINGS = load_ap_settings()

    SHOP_KEYS = SETTINGS["shop_keys"]

    ENEMY_HP_MULT = SETTINGS["enemy_hp_mult"]
    ENEMY_ATTACK_MULT = SETTINGS["enemy_attack_mult"]

    RANDOMIZE_ENEMY_STATS = SETTINGS["randomize_enemy_stats"]

    INTRO_SKIP = SETTINGS["intro_skip"]


    SKILL_MONEY_MIN = SETTINGS["skill_money_min"]
    SKILL_MONEY_MAX = SETTINGS["skill_money_max"]

    # renamed from akame
    SKILL_AKAME_MIN = SETTINGS["skill_akame_min"]
    SKILL_AKAME_MAX = SETTINGS["skill_akame_max"]


    PART_TIME_MONEY_MIN = SETTINGS["part_time_money_min"]
    PART_TIME_MONEY_MAX = SETTINGS["part_time_money_max"]

    # renamed from akame
    PART_TIME_AKAME_MIN = SETTINGS["part_time_akame_min"]
    PART_TIME_AKAME_MAX = SETTINGS["part_time_akame_max"]


    ATTACK_AND_DEFENSE_MIN = SETTINGS["attack_and_defense_min"]
    ATTACK_AND_DEFENSE_MAX = SETTINGS["attack_and_defense_max"]

    RESIST_MIN = SETTINGS["resist_min"]
    RESIST_MAX = SETTINGS["resist_max"]

    POOL_MODIFIER = SETTINGS["pool_modifier"]
    GOLF_MODIFIER = SETTINGS["golf_modifier"]
    SHOGI_MODIFIER = SETTINGS["shogi_modifier"]
    CASINO_MODIFIER = SETTINGS["casino_modifier"]
    AKAME_SHOP_MODIFIER = SETTINGS["akame_shop_modifier"]
    POCKET_CIRCUIT_MODIFIER = SETTINGS["pocket_circuit_modifier"]

    MAX_GOLDEN_BALL_COUNT = SETTINGS["max_golden_ball_count"]
    REQUIRED_GOLDEN_BALL_COUNT = SETTINGS["required_golden_ball_count"]
    PROGRESSIVE_GRAPPLE_ITEMS = SETTINGS["progressive_grapple_items"]

# Create log files

CHANGE_LOG_PATH = Path("change_log.txt")
ERROR_LOG_PATH = Path("error_warning_log.txt")

def log_change(msg: str):
    with open(CHANGE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def log_error(msg: str):
    with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def write_options_file():
    assets_folder = BASE_DIR / "Assets"
    assets_folder.mkdir(parents=True, exist_ok=True)

    options_path = assets_folder / "options.json"

    with open(options_path, "w", encoding="utf-8") as f:
        json.dump(SETTINGS, f, indent=4)

    print(f"[CONFIG] Wrote options to {options_path}")


CHANGE_LOG_PATH.write_text("", encoding="utf-8")
ERROR_LOG_PATH.write_text("", encoding="utf-8")

# Weighted rand

def weighted_rand(min_val, max_val):
    span = max_val - min_val + 1

    cheap_max = min_val + int(span * 0.08) - 1
    average_max = min_val + int(span * 0.35) - 1
    expensive_max = min_val + int(span * 0.65) - 1

    r = random.random()

    if r < 0.50:
        # 50% chance to pull from the bottom 8% of the value range
        return random.randint(min_val, cheap_max)

    elif r < 0.85:
        # 35% chance to pull from the middle 8% to 35% of the value range
        return random.randint(cheap_max + 1, average_max)

    elif r < 0.95:
        # 10% chance to pull from the middle 35% to 65% of the value range
        return random.randint(average_max + 1, expensive_max)

    else:
        # 5% chance to pull from the middle 65% to 100% of the value range
        return random.randint(expensive_max + 1, max_val)

# Grab required updates

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
                "purchase_price": row.get("purchase_price"),
                "purchase_points": row.get("purchase_points")
            })

    return updates

# Encounters

def update_encounters():

    print("\n[NPC] Processing character_npc_soldier_personal_data.bin.json")

    if not NPC_PATH.exists():
        print(f"[NPC] Missing file: {NPC_PATH}")
        return

    with open(NPC_PATH, encoding="utf-8") as f:
        data = json.load(f)

    changes = 0

    for row_id in range(FIRST_ENCOUNTER_ROW, len(data)):

        row_key = str(row_id)

        if row_key not in data:
            continue

        row_block = data[row_key]

        if not isinstance(row_block, dict):
            continue

        inner_key = next(iter(row_block.keys()))
        row = row_block.get(inner_key)

        if not isinstance(row, dict):
            continue

        hp = row.get("hp", 0)
        attack = row.get("power_ratio", 0)

        if hp <= 1:
            continue
        
        if attack <= 0:
            continue

        group = int(row_key)

        # Intro skip
        if INTRO_SKIP and group in INTRO_FIGHTS:
            old_hp = row["hp"]
            row["hp"] = 1

            print(f"Intro fight {group}: hp {old_hp} -> 1")
            log_change(f"Intro fight {group}: hp {old_hp} -> 1")
            changes += 1

        # Randomized Stats
        elif RANDOMIZE_ENEMY_STATS:
            hp_multiplier = random.uniform(0.5, 3.0)
            attack_multiplier = random.uniform(0.5, 3.0)
            
            old_hp = row["hp"]
            row["hp"] = max(1, math.ceil(old_hp * hp_multiplier))
            
            old_attack = row["power_ratio"]
            row["power_ratio"] = max(1.0, round(old_attack * attack_multiplier, 2))

            print(f"{group}: hp {old_hp} -> {row['hp']}, attack {old_attack} -> {row['power_ratio']}")
            log_change(f"{group}: hp {old_hp} -> {row['hp']}, attack {old_attack} -> {row['power_ratio']}")
            changes += 1

        # Scaled Stats
        else:
            hp_multiplier = ENEMY_HP_MULT / 100.0
            attack_multiplier = ENEMY_ATTACK_MULT / 100.0

            old_hp = row["hp"]
            row["hp"] = max(1, math.ceil(old_hp * hp_multiplier))

            old_attack = row["power_ratio"]
            row["power_ratio"] = max(1.0, round(old_attack * attack_multiplier, 2))

            print(f"{group}: hp {old_hp} -> {row['hp']}, attack {old_attack} -> {row['power_ratio']}")
            log_change(f"{group}: hp {old_hp} -> {row['hp']}, attack {old_attack} -> {row['power_ratio']}")
            changes += 1

    output_path = OUTPUT_FOLDER / "db.aston.en" / "character_npc_soldier_personal_data.bin.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {changes} encounter changes")

# Shops

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

    update_shop_item_limits(data, updates)
    return changes


# Shop Counts

def update_shop_item_limits(data, updates):

    shop_category_8_values = {
        "aston_s_ebisuya": 4,
        "aston_s_billiards_prize": 5,
        "aston_s_wannpark": 6,
        "aston_y_shichiya": 7,
        "aston_y_lovemagic": 8,
        "aston_y_shogi": 9,
        "aston_s_shogi": 10,
        "aston_s_golf": 11,
        "aston_s_toba": 12,
        "aston_y_toba": 13,
        "aston_c_toba": 14,
        "aston_c_casino": 15,
        "aston_c_boutique_equip": 16,
        "aston_c_boutique_vip": 17,
        "aston_s_mizorogi_2": 18,
        "aston_s_poppo_ashi": 19,
        "aston_s_poppo_sh": 20,
        "aston_s_poppo_so": 21,
        "aston_y_poppo02": 22,
        "aston_s_kukuru": 23,
        "aston_s_tsuruha": 24,
        "aston_s_hiratai": 25,
        "aston_s_shigano": 26,
        "aston_y_smilewagon": 27,
        "aston_y_ichibann": 28,
    }

    affected_tables = {
        u["table_name"]
        for u in updates
        if u["column_id"] == "replacement_item_id"
    }

    for root_value in data.values():

        if not isinstance(root_value, dict):
            continue

        for table_name, shop_wrapper in root_value.items():

            if table_name not in affected_tables:
                continue

            if not isinstance(shop_wrapper, dict):
                continue

            table = shop_wrapper.get("table")

            if not isinstance(table, dict):
                continue

            item_counts = Counter()

            for row_container in table.values():

                if not isinstance(row_container, dict):
                    continue

                row = row_container.get("")

                if not isinstance(row, dict):
                    continue

                item_id = row.get("1")

                if item_id:
                    item_counts[item_id] += 1

            for row_container in table.values():

                if not isinstance(row_container, dict):
                    continue

                row = row_container.get("")

                if not isinstance(row, dict):
                    continue

                item_id = row.get("1")


                if item_id:
                    row["20"] = item_counts[item_id]

                    if SHOP_KEYS and table_name in shop_category_8_values:
                        row["6"] = 1
                        row["7"] = 12
                        row["8"] = shop_category_8_values[table_name]
# Rewards

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

# Lockers

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

# Wire

def update_wire(data, updates):

    changes = 0

    # =====================================================
    # Normal wire updates
    # =====================================================

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

        for v in row_container.values():

            if isinstance(v, dict) and "get_item_id" in v:
                inner_row = v
                break

        if inner_row is None:
            continue

        old_value = inner_row["get_item_id"]

        if old_value == new_value:
            continue

        inner_row["get_item_id"] = new_value

        changes += 1

        msg = (
            f"[WIRE] row={row_id} "
            f"{old_value} -> {new_value}"
        )

        print(msg)
        log_change(msg)


    # =====================================================
    # Progressive Grapple replacements
    # =====================================================

    if PROGRESSIVE_GRAPPLE_ITEMS:

        GRAPPLE_RANGES = [
            # (start row ID, end row ID, progressive item ID, region)
            (5, 54, 6312, "Sotenbori"),
            (65, 114, 6313, "Colosseum"),
            (115, 164, 6311, "Yokohama"),
        ]

        for row_id, row_container in data.items():

            if not isinstance(row_container, dict):
                continue

            try:
                row_id_int = int(row_id)
            except (ValueError, TypeError):
                continue

            progressive_item = None
            region = None

            for start, end, item_id, range_region in GRAPPLE_RANGES:

                if start <= row_id_int <= end:
                    progressive_item = item_id
                    region = range_region
                    break

            if progressive_item is None:
                continue

            for inner_row in row_container.values():

                if not isinstance(inner_row, dict):
                    continue

                if "get_item_id" not in inner_row:
                    continue

                old_value = inner_row["get_item_id"]

                if old_value == progressive_item:
                    continue

                inner_row["get_item_id"] = progressive_item

                changes += 1

                msg = (
                    f"[WIRE PROGRESSIVE] "
                    f"{region} row={row_id_int} "
                    f"{old_value} -> {progressive_item}"
                )

                print(msg)
                log_change(msg)


    return changes

# Shuffle specific item effect values

def shuffle_healing_items(data):

    SWAP_IDS = [
        "5323", "5324", "5990", "5325", "5992",
        "5326", "5327", "5995", "5996", "6131",
        "6129", "6130", "5991", "5994",
        "6258", "6259", "6260", "6261",
        "6262", "6263", "6264", "6265", 
        "6516", "6517", "6518", "6519", "6520", "6521",
        "6509", "6510", "6511", "6512", "6513",
    ]

    stored_indexes = []

    # Collect current row indexes
    for item_id in SWAP_IDS:

        if item_id not in data:
            print(f"Missing ID {item_id}")
            continue

        item_block = data[item_id]

        if not isinstance(item_block, dict):
            continue

        inner_key = next(iter(item_block.keys()))
        row = item_block[inner_key]

        if "reARMP_rowIndex" not in row:
            print(f"Missing reARMP_rowIndex for {item_id}")
            continue

        stored_indexes.append(row["reARMP_rowIndex"])


    # Shuffle the indexes
    random.shuffle(stored_indexes)


    # Apply shuffled indexes back
    for item_id, new_index in zip(SWAP_IDS, stored_indexes):

        if item_id not in data:
            continue

        item_block = data[item_id]

        inner_key = next(iter(item_block.keys()))
        row = item_block[inner_key]

        old_index = row["reARMP_rowIndex"]
        row["reARMP_rowIndex"] = new_index

        print(
            f"[ITEM SWAP] {item_id} reARMP_rowIndex: "
            f"{old_index} -> {new_index}"
        )

        log_change(
            f"[ITEM SWAP] {item_id} reARMP_rowIndex "
            f"{old_index} -> {new_index}"
        )

# Patch prices in item.bin

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

    shuffle_healing_items(data)

    POINT_FIELDS = {
        "buy_syogi_point": SHOGI_MODIFIER,
        "buy_casino_point": CASINO_MODIFIER,
        "buy_toba_point": CASINO_MODIFIER,
        "buy_akame_point": AKAME_SHOP_MODIFIER,
        "buy_billiard_point": POOL_MODIFIER,
        "buy_golf_point": GOLF_MODIFIER,
        "buy_pokecir_point": POCKET_CIRCUIT_MODIFIER,
    }

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

            if "purchase_price" in row and new_price is not None:
                old_value = row["purchase_price"]
                row["purchase_price"] = int(new_price)

                msg = f"[ITEM PRICE] id={item_id} {old_value} -> {new_price}"
                print(msg)
                log_change(msg)

                changes += 1

            # point system update
            if new_points is not None:
                try:
                    point_val = int(new_points)

                    for field, multiplier in POINT_FIELDS.items():
                        if field in row:
                            row[field] = math.ceil(point_val * (multiplier / 100.0))

                    msg = f"[ITEM POINTS] id={item_id} -> {point_val}"
                    print(msg)
                    log_change(msg)

                except ValueError:
                    msg = f"[WARN] invalid point value for item {item_id}: {new_points}"
                    print(msg)
                    log_error(msg)

    # --------------------------------------------------
    # Randomize generated equipment
    # --------------------------------------------------

    stat_rules = {
        "add_ability_attack": (ATTACK_AND_DEFENSE_MIN, ATTACK_AND_DEFENSE_MAX),
        "add_ability_defense": (ATTACK_AND_DEFENSE_MIN, ATTACK_AND_DEFENSE_MAX),
        "add_ability_resist_gun": (RESIST_MIN, RESIST_MAX),
        "add_ability_resist_sword": (RESIST_MIN, RESIST_MAX),
        "add_ability_resist_bleed": (STATUS_RESIST_MIN, STATUS_RESIST_MAX),
        "add_ability_resist_stun": (STATUS_RESIST_MIN, STATUS_RESIST_MAX),
        "add_ability_resist_burn": (STATUS_RESIST_MIN, STATUS_RESIST_MAX),
        "add_ability_resist_electric": (STATUS_RESIST_MIN, STATUS_RESIST_MAX),
    }

    for item_id, item_block in data.items():

        if not item_id.isdigit():
            continue

        # Only randomize generated AP items
        if int(item_id) <= 4000:
            continue

        if not isinstance(item_block, dict):
            continue

        inner_key = next(iter(item_block.keys()))
        row = item_block[inner_key]

        if int(row.get("category", 0)) != 6:
            continue

        for field, (mn, mx) in stat_rules.items():
            row[field] = random.randint(mn, mx)

        special_id = random.choice(list(SPECIAL0_EFFECTS.keys()))
        row["add_special0"] = special_id
        row["explanation"] = SPECIAL0_EFFECTS[special_id]
        row["max_count_base"] = 99

        msg = f"[ITEM EQUIPMENT] id={item_id} updated equipment stats"
        print(msg)
        log_change(msg)

    output_path = OUTPUT_FOLDER / "db.aston.en" / "item.bin.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[ITEM] Saved {changes} price changes")

def patch_player_skill_bin():
    path = INPUT_FOLDER / "db.aston.en" / "player_skill.bin.json"

    print("\n[SKILL] Processing player_skill.bin.json")

    if not path.exists():
        print(f"[SKILL] Missing file: {path}")
        return

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    for row_id in range(992, 1120):
        row_key = str(row_id)

        if row_key not in data:
            continue

        skill_block = data[row_key]

        if not isinstance(skill_block, dict):
            continue

        inner_key = next(iter(skill_block.keys()))
        row = skill_block.get(inner_key)

        if not isinstance(row, dict):
            continue

        row["need_money"] = weighted_rand(SKILL_MONEY_MIN, SKILL_MONEY_MAX)
        row["need_akame_point"] = weighted_rand(SKILL_AKAME_MIN, SKILL_AKAME_MAX)

    output_path = OUTPUT_FOLDER / "db.aston.en" / "player_skill.bin.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("[SKILL] Done")


def patch_akame_quest_rewards():
    VALID_RANGE = range(1, 148)
    SKIP_IDS = {91, 19, 18, 17, 16, 15, 14, 13, 12}
    path = INPUT_FOLDER / "db.aston.en" / "part_time_job_quest_quest.bin.json"

    print("\nProcessing part_time_job_quest_quest.bin.json")

    if not path.exists():
        print(f"Missing file: {path}")
        return

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    changes = 0

    for row_key, row_block in data.items():
        if not row_key.isdigit():
            continue

        row_id = int(row_key)

        if row_id not in VALID_RANGE:
            continue

        # Skip excluded quest IDs
        if row_id in SKIP_IDS:
            continue

        if not isinstance(row_block, dict):
            continue

        inner_key = next(iter(row_block.keys()))
        row = row_block.get(inner_key)

        if not isinstance(row, dict):
            continue

        old_money = row["reward_money"]
        old_points = row["reward_akame_point"]

        row["reward_money"] = weighted_rand(
            PART_TIME_MONEY_MIN,
            PART_TIME_MONEY_MAX
        )

        row["reward_akame_point"] = weighted_rand(
            PART_TIME_AKAME_MIN,
            PART_TIME_AKAME_MAX
        )

        print(
            f"[PART TIME] {inner_key}: "
            f"money {old_money} -> {row['reward_money']}, "
            f"points {old_points} -> {row['reward_akame_point']}"
        )

        log_change(
            f"Akame Quest {inner_key}: "
            f"money {old_money} -> {row['reward_money']}, "
            f"points {old_points} -> {row['reward_akame_point']}"
        )

        changes += 1

    output_path = OUTPUT_FOLDER / "db.aston.en" / "part_time_job_quest_quest.bin.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {changes} reward changes")

# Detect File

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


# MAIN

def main():
    load_config()

    write_options_file()

    seed = SETTINGS.get("seed")
    used_seed = init_seed(seed)

    print(f"[SEED] {used_seed}")

    CHANGE_LOG_PATH.write_text("", encoding="utf-8")
    ERROR_LOG_PATH.write_text("", encoding="utf-8")
    updates_by_file = load_updates()

    json_files = list(INPUT_FOLDER.rglob("*.json"))

    print(f"Found {len(json_files)} JSON files")

    for json_file in json_files:
        if json_file.name in updates_by_file:
            apply_updates(json_file, updates_by_file[json_file.name])

    patch_item_bin_prices(updates_by_file)
    update_encounters()
    patch_player_skill_bin()
    patch_akame_quest_rewards()

if __name__ == "__main__":
    main()
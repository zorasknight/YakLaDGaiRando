import dearpygui.dearpygui as dpg # type: ignore
from Scripts.settings import settings
from pathlib import Path
import yaml # type: ignore
import time
import sys
import Scripts.shuffle as shuffle
import Scripts.replace_items as replace_items
import Scripts.convert as convert
import threading


def resource_path(relative_path):
    base = (
        Path(sys._MEIPASS)
        if getattr(sys, "frozen", False)
        else BASE_DIR
    )
    return base / relative_path

def get_base_dir():
    # Running as PyInstaller executable
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    # Running as normal .py script
    return Path(__file__).resolve().parent

BASE_DIR = get_base_dir()
CONFIG_DIR = BASE_DIR / "Config"
CONFIG_DIR.mkdir(exist_ok=True)
image_path = resource_path("Assets/background.jpg")
font_path = resource_path("Assets/Pliant.ttf")

DEFAULTS_FILE = CONFIG_DIR / "defaults.yaml"

if not DEFAULTS_FILE.exists():
    bundled = resource_path("Config/defaults.yaml")
    CONFIG_DIR.mkdir(exist_ok=True)
    DEFAULTS_FILE.write_text(bundled.read_text(encoding="utf-8"), encoding="utf-8")


BASE_TOTAL = 631
BASE_REQUIRED = 349
MINIGAME_TOTAL = 106
MINIGAME_REQUIRED = 14

FIELD_SCHEMA = {

    # Ranges (INT)

    "monetary": {
        "type": "range",
        "label": "Shop Money Range",
        "hint": "What random range items shops will be priced at"
    },
    "point": {
        "type": "range",
        "label": "Shop Point Range",
        "hint": "What random range items point cost can be"
    },
    "skill_money": {
        "type": "range",
        "label": "Skill Money Cost",
        "hint": "What random range skills can be priced at"
    },
    "skill_akame": {
        "type": "range",
        "label": "Skill Point Cost",
        "hint": "What random range skills point cost can be"
    },
    "part_time_money": {
        "type": "range",
        "label": "Reward Money",
        "hint": "What random monetary range rewards for Akame quests can give"
    },
    "part_time_akame": {
        "type": "range",
        "label": "Reward Points",
        "hint": "What random point range rewards for Akame quests can give"
    },
    "attack_and_defense": {
        "type": "range",
        "label": "Attack and Defense Stats",
        "hint": "The range an armor's primary stats can be randomized between"
    },
    "resist": {
        "type": "range",
        "label": "Resistance Stats",
        "hint": "The range an armor's resistance stats can be randomized between"
    },
    
    # Float
    
    "enemy_attack_mult": {
        "type": "float",
        "label": "Enemy Attack Multiplier",
        "hint": "Attack multiplier for all enemies"
    },
    "enemy_hp_mult": {
        "type": "float",
        "label": "Enemy Health Multiplier",
        "hint": "Health multiplier for all enemies"
    },

    # Booleans

    "remove_default_prices": {
        "type": "bool",
        "label": "Remove Default Prices",
        "hint": "Ignores vanilla pricing and replaces all costs with randomized values"
    },
    "randomize_enemy_stats": {
        "type": "bool",
        "label": "Randomize Enemy Stats",
        "hint": "(THIS WILL MAKE THE GAME HARDER) Randomize enemy HP and Attack (ignores intro if intro skip is on).",
    },
    "intro_skip": {
        "type": "bool",
        "label": "Intro Speedup",
        "hint": "This sets all tutorial fights pre-sotenbori to 1 HP",
    },
    "include_shops": {
        "type": "bool",
        "label": "Include Shops",
        "hint": "Includes all shops in item pool",
        "required_items": 17,
        "added_items": 114
    },
    "include_consumable_shops": {
        "type": "bool",
        "label": "Include Consumable Shops",
        "hint": "Includes Poppo Marts and the Pharmacy",
        "required_items": 0,
        "added_items": 111
    },
    "include_weird_shops": {
        "type": "bool",
        "label": "Include Weird Shops",
        "hint": "Includes one off stores like ichiban confections",
        "required_items": 0,
        "added_items": 21
    },
    "include_coin_lockers": {
        "type": "bool",
        "label": "Include Coin Lockers",
        "hint": "Includes coin lockers in item pool",
        "required_items": 9,
        "added_items": 50
    },
    "include_pocket_circuit": {
        "type": "bool",
        "label": "Include Pocket Circuit",
        "hint": "Includes the Pocket Circuit shop into the item pool",
        "required_items": 95,
        "added_items": 95
    },
    "include_rewards": {
        "type": "bool",
        "label": "Include PC Rival Rewards",
        "hint": "Includes all Rival Rewards for Pocket Circuit",
        "required_items": 14,
        "added_items": 14
    },
    "include_minigames": {
        "type": "bool",
        "label": "Include Minigames",
        "hint": "Includes all Minigame shops into the item pool",
        "required_items": 14,
        "added_items": 106
    },
    "include_pool": {
        "type": "bool",
        "label": "Include Pool",
        "hint": "Includes Pool Point Shop",
        "required_items": 1,
        "added_items": 11
    },
    "include_golf": {
        "type": "bool",
        "label": "Include Golf",
        "hint": "Includes Golf Point Shop",
        "required_items": 2,
        "added_items": 13
    },
    "include_casinos": {
        "type": "bool",
        "label": "Include Casinos",
        "hint": "Includes both the Casino and Toba Point Shops",
        "required_items": 8,
        "added_items": 52
    },
    "include_shogi": {
        "type": "bool",
        "label": "Include Shogi",
        "hint": "Includes Shogi Point Shop",
        "required_items": 1,
        "added_items": 22
    },
    "include_darts": {
        "type": "bool",
        "label": "Include Darts",
        "hint": "Includes Dart Rival rewards",
        "required_items": 2,
        "added_items": 8
    },

    # Random Seed
    "seed": {
        "type": "int",
        "label": "Random Seed",
        "hint": "Leave blank for a fully random generation. Set a value for consistent results."
    },
}

MINIGAME_KEYS = [
    "include_pool",
    "include_golf",
    "include_casinos",
    "include_shogi",
    "include_darts",
]

# Helper Methods

def field_meta(key):
    return FIELD_SCHEMA.get(key, {})


def field_label(key):
    return field_meta(key).get("label", key.replace("_", " ").title())


def field_hint(key):
    return field_meta(key).get("hint", "")


def field_type(key):
    return field_meta(key).get("type")

def add_tooltip(target, text):
    if text:
        with dpg.tooltip(target):
            dpg.add_text(text)

def make_label(text, hint=None):
    item = dpg.add_text(text)
    if hint:
        add_tooltip(item, hint)
    return item

def log(message):
    current = dpg.get_value("log_text")
    dpg.set_value("log_text", current + message + "\n")
    dpg.set_y_scroll("log_window", 1.0)

def run_randomizer():
    autosave()
    seed = LIVE.get("seed")

    if seed is not None:
        import random
        random.seed(seed)
        log(f"Using seed: {seed}")
    else:
        log("Using random seed (None)")

    def task():
        log("Starting randomizer...")

        pipeline = [
            (shuffle.main, 0),
            (replace_items.main, 0),
            (convert.main, 0),
        ]

        for func, delay in pipeline:
            log(f"Running {func.__module__}...")
            func()
            log(f"Finished {func.__module__}")
            time.sleep(delay)

        log("All scripts completed.")
        log("Enjoy the Rando!")

    threading.Thread(target=task, daemon=True).start()

def set_button_enabled(enabled: bool):
    dpg.configure_item("run_randomizer_btn", enabled=enabled)

    if not enabled:
        dpg.configure_item("run_randomizer_btn",
                           show=True)
        dpg.set_item_label("run_randomizer_btn", "Too Few Locations")
    else:
        dpg.set_item_label("run_randomizer_btn", "Run Randomizer")

def calculate_checks():
    total_checks = BASE_TOTAL
    required_checks = BASE_REQUIRED

    minigames_on = safe_bool(LIVE.get("include_minigames", False))

    for key, meta in FIELD_SCHEMA.items():
        if meta.get("type") != "bool":
            continue

        value = safe_bool(LIVE.get(key, False))

        if key in MINIGAME_KEYS:
            if not minigames_on:
                continue

            if value:
                continue
            else:
                total_checks -= meta.get("added_items", 0)
                required_checks -= meta.get("required_items", 0)

            continue

        if key == "include_minigames":
            if not value:
                total_checks -= MINIGAME_TOTAL
                required_checks -= MINIGAME_REQUIRED
            continue

        if not value:
            total_checks -= meta.get("added_items", 0)
            required_checks -= meta.get("required_items", 0)

    return total_checks, required_checks

def update_check_display():
    total, required = calculate_checks()

    dpg.set_value("total_checks_text", f"Total Checks: {total}")
    dpg.set_value("required_checks_text", f"Required Checks: {required}")

    invalid = required > total

    dpg.configure_item(
        "total_checks_text",
        color=(255, 0, 0, 255) if invalid else (0, 255, 0, 255)
    )
    
    set_button_enabled(not invalid)

settings.reload()
LIVE = dict(settings.data)
LIVE.pop("seed", None)
LIVE["seed"] = None

# Load Defaults

with open(DEFAULTS_FILE, "r", encoding="utf-8") as f:
    DEFAULTS = yaml.safe_load(f) or {}

selected_category = "Shops"


def safe_int(v, fallback=0):
    try:
        return int(v) if v is not None else fallback
    except:
        return fallback
    
def safe_bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("true", "1", "yes", "on")
    return bool(v)

# Rules

FIELD_RULES = {
    "monetary": {"min": 0, "max": 3_000_000},
    "point": {"min": 0, "max": 8000},
    "skill_money": {"min": 0, "max": 3_000_000},
    "skill_akame": {"min": 0, "max": 8000},
    "attack_and_defense": {"min": -2000, "max": 2000},
    "resist": {"min": 0, "max": 1000},
    "enemy_hp_mult": {"min": 0.5, "max": 3.0},
    "enemy_attack_mult": {"min": 0.5, "max": 3.0},
    "part_time_money": {"min": 0, "max": 1000000},
    "part_time_akame": {"min": 0, "max": 5000},
}

def get_rules(base):
    return FIELD_RULES.get(base, {"min": 0, "max": 1_000_000})

# Pairs

def build_pairs():
    pairs = {}
    used = set()

    for k in LIVE.keys():
        if k in used:
            continue

        if k.endswith("_min"):
            base = k[:-4]
            mx = base + "_max"
            if mx in LIVE:
                pairs[base] = (k, mx)
                used.add(k)
                used.add(mx)

    return pairs


pairs = build_pairs()

# Auto Save

def autosave():
    settings.save_user_settings(LIVE)


def set_value(key, value):
    LIVE[key] = value

# Reset Values

def reset_category(cat):

    for base, (mn, mx) in pairs.items():

        if get_category(base) != cat:
            continue

        if mn in DEFAULTS:
            LIVE[mn] = DEFAULTS[mn]
        if mx in DEFAULTS:
            LIVE[mx] = DEFAULTS[mx]

    for key, meta in FIELD_SCHEMA.items():
        if meta.get("type") != "float":
            continue

        if get_category(key) != cat:
            continue

        if key in DEFAULTS:
            LIVE[key] = float(DEFAULTS[key])

    autosave()
    render(cat)
    update_check_display()

# Category

def get_category(base):
    if "monetary" in base or "point" in base:
        return "Shops"
    if "skill" in base:
        return "Skills"
    if "defense" in base or "resist" in base:
        return "Gear"
    if "mult" in base:
        return "Encounters"
    if "part_time" in base:
        return "Quest Rewards"
    return "Other"

# Range + Boolean UI

#Boolean UI
def make_bool(key):
    meta = field_meta(key)

    def update(sender, app_data):
        LIVE[key] = bool(app_data)
        autosave()
        update_check_display()

    cb = dpg.add_checkbox(
    label=field_label(key),
    default_value=safe_bool(LIVE.get(key, False)),
    callback=update
)

    add_tooltip(cb, field_hint(key))

#Range UI
def make_range(base, min_key, max_key, rules):
    meta = field_meta(base)

    # Header
    make_label(
        meta.get("label", base),
        meta.get("hint", "")
    )

    # Values
    min_val = safe_int(LIVE.get(min_key))
    max_val = safe_int(LIVE.get(max_key))

    dpg.add_text("Min")
    min_input = dpg.add_input_int(default_value=min_val, width=160)
    min_slider = dpg.add_slider_int(
        default_value=min_val,
        min_value=rules["min"],
        max_value=rules["max"],
        width=360
    )

    dpg.add_text("Max")
    max_input = dpg.add_input_int(default_value=max_val, width=160)
    max_slider = dpg.add_slider_int(
        default_value=max_val,
        min_value=rules["min"],
        max_value=rules["max"],
        width=360
    )

    lock = {"busy": False}

    def sync():
        if lock["busy"]:
            return

        lock["busy"] = True

        a = safe_int(dpg.get_value(min_input))
        b = safe_int(dpg.get_value(max_input))

        a = max(rules["min"], min(a, rules["max"]))
        b = max(rules["min"], min(b, rules["max"]))

        if a > b:
            b = a

        set_value(min_key, a)
        set_value(max_key, b)

        dpg.set_value(min_input, a)
        dpg.set_value(min_slider, a)
        dpg.set_value(max_input, b)
        dpg.set_value(max_slider, b)

        lock["busy"] = False

    dpg.set_item_callback(min_input, lambda s, a: sync())
    dpg.set_item_callback(max_input, lambda s, a: sync())

    def min_slider_changed(sender, app_data):
        value = int(app_data)

        current_max = safe_int(dpg.get_value(max_input))

        # clamp relationship
        if value > current_max:
            current_max = value
            dpg.set_value(max_input, current_max)
            dpg.set_value(max_slider, current_max)
            set_value(max_key, current_max)

        dpg.set_value(min_input, value)
        dpg.set_value(min_slider, value)
        set_value(min_key, value)


    def max_slider_changed(sender, app_data):
        value = int(app_data)

        current_min = safe_int(dpg.get_value(min_input))

        # clamp relationship
        if value < current_min:
            current_min = value
            dpg.set_value(min_input, current_min)
            dpg.set_value(min_slider, current_min)
            set_value(min_key, current_min)

        dpg.set_value(max_input, value)
        dpg.set_value(max_slider, value)
        set_value(max_key, value)

    dpg.set_item_callback(min_slider, min_slider_changed)
    dpg.set_item_callback(max_slider, max_slider_changed)

# Used for other sliders that do not have min/max
def make_float(base):
    meta = field_meta(base)
    rules = get_rules(base)

    make_label(meta.get("label", base), meta.get("hint", ""))

    key = base

    value = float(LIVE.get(key, rules["min"]))
    value = max(rules["min"], min(value, rules["max"]))

    slider = dpg.add_slider_float(
        default_value=value,
        min_value=rules["min"],
        max_value=rules["max"],
        width=360
    )

    input_box = dpg.add_input_float(
        default_value=value,
        width=160
    )

    def sync_from_slider(sender, app_data):
        v = float(app_data)
        LIVE[key] = v
        dpg.set_value(input_box, v)
        autosave()

    def sync_from_input(sender, app_data):
        try:
            v = float(app_data)
        except:
            return

        v = max(rules["min"], min(v, rules["max"]))
        LIVE[key] = v
        dpg.set_value(slider, v)
        autosave()

    dpg.set_item_callback(slider, sync_from_slider)
    dpg.set_item_callback(input_box, sync_from_input)


# Render

def render(cat):
    dpg.delete_item("content", children_only=True)

    with dpg.group(parent="content"):

        # Boolean Settings
        dpg.add_text("OPTIONS")
        dpg.add_separator()

        bool_keys = [
            key for key, meta in FIELD_SCHEMA.items()
            if meta["type"] == "bool"
        ]

        with dpg.table(
            header_row=False,
            borders_innerH=False,
            borders_innerV=False,
            borders_outerH=False,
            borders_outerV=False
        ):
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()  # 3 columns

            cols = 3

            for i in range(0, len(bool_keys), cols):
                with dpg.table_row():
                    for j in range(cols):
                        if i + j < len(bool_keys):
                            with dpg.table_cell():
                                make_bool(bool_keys[i + j])
                        else:
                            dpg.add_text("")

        dpg.add_spacer(height=10)

        # Range Settings
        dpg.add_text(cat.upper())
        dpg.add_separator()

        for base, (mn, mx) in pairs.items():

            if get_category(base) != cat:
                continue

            meta = field_meta(base)
            rules = get_rules(base)

            with dpg.group():
                make_range(base, mn, mx, rules)

            dpg.add_spacer(height=10)
        
        # Float sliders (single value fields)
        float_keys = [
            k for k, meta in FIELD_SCHEMA.items()
            if meta.get("type") == "float"
        ]

        for key in float_keys:
            if get_category(key) != cat:
                continue

            make_float(key)
            dpg.add_spacer(height=10)

    update_check_display()

# Switch

def switch(sender, app_data, user_data):
    autosave()

    global selected_category
    selected_category = user_data

    render(user_data)
    update_check_display()

# UI

dpg.create_context()


with dpg.font_registry():
    default_font = dpg.add_font(font_path, 18)

dpg.bind_font(default_font)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (100, 100, 100, 255))
        dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (160, 160, 160, 255))
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 3)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (20, 20, 20, 240))
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (20, 20, 20, 240))
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
        dpg.add_theme_style(dpg.mvStyleVar_PopupBorderSize, 3)
        dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 180))
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 8, category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)

width, height, channels, data = dpg.load_image(str(image_path))

with dpg.texture_registry():
    dpg.add_static_texture(
        width=width,
        height=height,
        default_value=data,
        tag="background"
    )

    

dpg.create_viewport(title="Like a Dragon Gaiden Randomizer Settings Editor", width=1280, height=720)
dpg.set_viewport_resizable(False)
with dpg.window(tag="main"):
    dpg.add_text("Randomizer Settings Editor (Auto-Saves on Close)")
    dpg.add_separator()

    with dpg.group(horizontal=True):

        # Side Panel
        with dpg.child_window(width=220):

            dpg.add_text("Actions")
            dpg.add_separator()

            dpg.add_button(
                label="Reset Section",
                width=200,
                callback=lambda: reset_category(selected_category)
            )
            dpg.add_button(
                label="Run Randomizer",
                width=200,
                callback=run_randomizer,
                tag="run_randomizer_btn"
            )

            dpg.add_separator()

            dpg.add_text("Categories")
            dpg.add_separator()

            for c in ["Shops", "Skills", "Gear", "Encounters", "Quest Rewards"]:
                dpg.add_button(label=c, callback=switch, user_data=c, width=200)
            
            dpg.add_separator()
            dpg.add_text("Console")
            dpg.add_separator()

            with dpg.child_window(
                tag="log_window",
                width=200,
                height=200,
                border=True
            ):
                dpg.add_input_text(
                    tag="log_text",
                    multiline=True,
                    readonly=True,
                    width=-1,
                    height=-1,
                    default_value=""
                )
            dpg.add_separator()
            total, required = calculate_checks()

            dpg.add_text(
                f"Total Checks: {total}",
                tag="total_checks_text"
            )

            dpg.add_text(
                f"Required Checks: {required}",
                tag="required_checks_text"
            )
            dpg.add_separator()

            dpg.add_text("Random Seed Value")

            seed_input = dpg.add_input_text(
                width=160,
                default_value=""
            )

            def seed_changed(sender, app_data):
                text = app_data.strip()

                if text == "":
                    LIVE["seed"] = None
                else:
                    try:
                        LIVE["seed"] = int(text)
                    except ValueError:
                        LIVE["seed"] = None

                autosave()

            dpg.set_item_callback(seed_input, seed_changed)

            dpg.add_separator()
        # Main Panel
        with dpg.child_window(tag="content"):
            dpg.add_text("Select category")
    with dpg.draw_layer():
        dpg.draw_image("background", pmin=(0, 0), pmax=(1260, 700))
        dpg.draw_rectangle(
            pmin=(0, 0),
            pmax=(1600, 900),
            color=(0, 0, 0, 0),
            fill=(0, 0, 0, 160)
        )

dpg.setup_dearpygui()
dpg.set_global_font_scale(1.2)
dpg.show_viewport()
dpg.set_primary_window("main", True)

render("Shops")
update_check_display()

dpg.start_dearpygui()
autosave()
dpg.destroy_context()
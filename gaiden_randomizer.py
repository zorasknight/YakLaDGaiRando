import dearpygui.dearpygui as dpg
from settings import settings
from pathlib import Path
import yaml
import time
import sys
import shuffle
import replace_items
import convert
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

    # Booleans

    "remove_default_prices": {
        "type": "bool",
        "label": "Remove Default Prices",
        "hint": "Ignores vanilla pricing and replaces all costs with randomized values"
    },
    "include_coin_lockers": {
        "type": "bool",
        "label": "Include Coin Lockers",
        "hint": "Includes coin lockers in item pool"
    },
    "include_shops": {
        "type": "bool",
        "label": "Include Shops",
        "hint": "Includes all shops in item pool"
    },
    "include_minigames": {
        "type": "bool",
        "label": "Include Minigames",
        "hint": "Includes all Minigame shops into the item pool (NOTE: not pocket circuit)"
    },
    "include_pocket_circuit": {
        "type": "bool",
        "label": "Include Pocket Circuit",
        "hint": "Includes both the Pocket Circuit shop, and reward from beating rivals into the item pool (NOTE: rivals can be turned off from rewards below)"
    },
    "include_rewards": {
        "type": "bool",
        "label": "Include Rewards",
        "hint": "includes all rewards in item pool"
    },
}

# Helper Methods

def field_meta(key):
    return FIELD_SCHEMA.get(key, {})


def field_label(key):
    return field_meta(key).get("label", key.replace("_", " ").title())


def field_hint(key):
    return field_meta(key).get("hint", "")


def field_type(key):
    return field_meta(key).get("type")

def is_bool(key):
    return field_type(key) == "bool"

def is_range_base(base):
    return field_type(base) == "range"

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
    dpg.set_y_scroll("log_window", dpg.get_y_scroll_max("log_window"))

def run_randomizer():
    autosave()
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

        log("All scripts completed. Enjoy the Rando!")

    threading.Thread(target=task, daemon=True).start()

settings.reload()
LIVE = dict(settings.data)

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
    "resist": {"min": 0, "max": 800},
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

    autosave()
    render(cat)

# Category

def get_category(base):
    if "monetary" in base or "point" in base:
        return "Shops"
    if "skill" in base:
        return "Skills"
    if "attack" in base or "resist" in base:
        return "Combat"
    return "Other"

# Range + Boolean UI

#Boolean UI
def make_bool(key):
    meta = field_meta(key)

    def update(sender, app_data):
        LIVE[key] = bool(app_data)
        autosave()

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

# Render

def render_field(key):
    ftype = field_type(key)

    if ftype == "bool":
        make_bool(key)
    else:
        return False

def render(cat):
    dpg.delete_item("content", children_only=True)

    with dpg.group(parent="content"):

        # Boolean Settings
        dpg.add_text("OPTIONS")
        dpg.add_separator()

        for key, meta in FIELD_SCHEMA.items():
            if meta["type"] == "bool":
                make_bool(key)

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

# Switch

def switch(sender, app_data, user_data):
    autosave()

    global selected_category
    selected_category = user_data

    render(user_data)

# UI

dpg.create_context()


with dpg.font_registry():

    with dpg.font(font_path, 18) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)

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

        # LEFT PANEL
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
                callback=run_randomizer
            )

            dpg.add_separator()

            dpg.add_text("Categories")
            dpg.add_separator()

            for c in ["Shops", "Skills", "Combat"]:
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

        # MAIN PANEL
        with dpg.child_window(tag="content"):
            dpg.add_text("Select category")
    with dpg.draw_layer():
        dpg.draw_image("background", pmin=(0, 0), pmax=(1260, 700))
        dpg.draw_rectangle(
            pmin=(0, 0),
            pmax=(1600, 900),
            color=(0, 0, 0, 0),
            fill=(0, 0, 0, 160)  # adjust darkness here
        )

dpg.setup_dearpygui()
dpg.set_global_font_scale(1.2)
dpg.show_viewport()
dpg.set_primary_window("main", True)

render("Shops")

dpg.start_dearpygui()
autosave()
dpg.destroy_context()
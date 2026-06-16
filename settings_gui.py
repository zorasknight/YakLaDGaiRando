import dearpygui.dearpygui as dpg
from settings import settings
from pathlib import Path
import yaml

settings.reload()
LIVE = dict(settings.data)

# LOAD DEFAULTS
DEFAULTS_FILE = Path(__file__).parent / "Config" / "defaults.yaml"

with open(DEFAULTS_FILE, "r", encoding="utf-8") as f:
    DEFAULTS = yaml.safe_load(f) or {}

selected_category = "Shops"


def safe_int(v, fallback=0):
    try:
        return int(v) if v is not None else fallback
    except:
        return fallback


# ============================================================
# RULES
# ============================================================
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


# ============================================================
# PAIRS
# ============================================================
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


# ============================================================
# AUTO SAVE
# ============================================================
def autosave():
    settings.save_user_settings(LIVE)


def set_value(key, value):
    LIVE[key] = value
    autosave()


# ============================================================
# RESET VALUES
# ============================================================
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


# ============================================================
# CATEGORY
# ============================================================
def get_category(base):
    if "monetary" in base or "point" in base:
        return "Shops"
    if "skill" in base:
        return "Skills"
    if "attack" in base or "resist" in base:
        return "Combat"
    return "Other"


# ============================================================
# RANGE UI
# ============================================================
def make_range(min_key, max_key, rules):

    min_val = safe_int(LIVE.get(min_key))
    max_val = safe_int(LIVE.get(max_key))

    dpg.add_text("Min")
    min_input = dpg.add_input_int(default_value=min_val, width=160)
    min_slider = dpg.add_slider_int(default_value=min_val,
                                    min_value=rules["min"],
                                    max_value=rules["max"],
                                    width=360)

    dpg.add_text("Max")
    max_input = dpg.add_input_int(default_value=max_val, width=160)
    max_slider = dpg.add_slider_int(default_value=max_val,
                                    min_value=rules["min"],
                                    max_value=rules["max"],
                                    width=360)

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

    dpg.set_item_callback(min_slider, lambda s, a: set_value(min_key, a))
    dpg.set_item_callback(max_slider, lambda s, a: set_value(max_key, a))


# ============================================================
# RENDER
# ============================================================
def render(cat):

    dpg.delete_item("content", children_only=True)

    with dpg.group(parent="content"):

        for base, (mn, mx) in pairs.items():

            if get_category(base) != cat:
                continue

            rules = get_rules(base)

            dpg.add_text(base.upper())
            dpg.add_separator()

            with dpg.group(horizontal=True):
                dpg.add_spacer(width=20)
                with dpg.group():
                    make_range(mn, mx, rules)

            dpg.add_spacer(height=10)


# ============================================================
# SWITCH
# ============================================================
def switch(sender, app_data, user_data):
    global selected_category
    selected_category = user_data
    render(user_data)


# ============================================================
# UI
# ============================================================
dpg.create_context()
dpg.create_viewport(title="Like a Dragon Gaiden Randomizer Settings Editor", width=1150, height=750)

with dpg.window(tag="main"):

    dpg.add_text("Randomizer Settings Editor (Auto-Saves to YAML!)")
    dpg.add_separator()

    with dpg.group(horizontal=True):

        # LEFT PANEL
        with dpg.child_window(width=220):

            dpg.add_text("ACTIONS")
            dpg.add_separator()

            dpg.add_button(
                label="Reset Section",
                width=200,
                callback=lambda: reset_category(selected_category)
            )

            dpg.add_separator()

            dpg.add_text("Categories")
            dpg.add_separator()

            for c in ["Shops", "Skills", "Combat"]:
                dpg.add_button(label=c, callback=switch, user_data=c, width=200)

        # MAIN PANEL
        with dpg.child_window(tag="content"):
            dpg.add_text("Select category")

dpg.setup_dearpygui()
dpg.set_global_font_scale(1.2)
dpg.show_viewport()
dpg.set_primary_window("main", True)

render("Shops")

dpg.start_dearpygui()
dpg.destroy_context()
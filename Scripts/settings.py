from pathlib import Path
import sys
import yaml # type: ignore
from copy import deepcopy

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parent

BASE_DIR = get_base_dir()

CONFIG_DIR = BASE_DIR / "Config"

DEFAULTS_FILE = CONFIG_DIR / "defaults.yaml"
USER_FILE = CONFIG_DIR / "user_settings.yaml"


def deep_merge(base, override):
    result = deepcopy(base)

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


class Settings:
    def __init__(self):
        self.reload()

    def reload(self):
        # Load defaults
        with open(DEFAULTS_FILE, "r", encoding="utf-8") as f:
            defaults = yaml.safe_load(f) or {}

        # Load user overrides if present
        if USER_FILE.exists():
            with open(USER_FILE, "r", encoding="utf-8") as f:
                user = yaml.safe_load(f) or {}
        else:
            user = {}

        self.data = deep_merge(defaults, user)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def save_user_settings(self, data):
        with open(USER_FILE, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                data,
                f,
                sort_keys=False,
                default_flow_style=False
            )

        self.reload()

    def show_config_files(self):
        print(f"\nConfig Directory: {CONFIG_DIR}")

        if not CONFIG_DIR.exists():
            print("Config folder not found.")
            return

        print("\nFiles found:")
        for file in CONFIG_DIR.iterdir():
            if file.is_file():
                print(f"  - {file.name}")


settings = Settings()

if __name__ == "__main__":
    settings.show_config_files()

    print("\nLoaded settings:")
    print(settings.data)
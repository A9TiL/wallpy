import os
import json

# Application directory (for bundled assets)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_WALLPAPER_DIR = os.path.join(BASE_DIR, "assets", "wallpapers")

# User configuration directory
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "wallpy")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")


DEFAULT_CONFIG = {
    "folder": DEFAULT_WALLPAPER_DIR,
    "interval": 60,
    "mode": "sequential",
    "video": ""
}


def ensure_config_exists():

    os.makedirs(CONFIG_DIR, exist_ok=True)

    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)


def load_config():
    ensure_config_exists()

    with open(CONFIG_PATH) as f:
        return json.load(f)


def save_config(config):

    os.makedirs(CONFIG_DIR, exist_ok=True)

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

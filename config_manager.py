
import yaml
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.yaml"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return yaml.safe_load(f)
    return {}

def save_config(data: dict):
    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(data, f)

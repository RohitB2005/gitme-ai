import tomllib
import tomli_w
from pathlib import Path

CONFIG_PATH = Path.home() / ".gitme.toml"

DEFAULTS = {
    "provider": "ollama",
    "model": "llama3.2",
    "style": "conventional",
}

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return DEFAULTS.copy()
    
    with open(CONFIG_PATH, "rb") as f:
        user_config = tomllib.load(f)
    
    return {**DEFAULTS, **user_config}

def save_config(updates: dict) -> None:
    config = load_config()
    config.update(updates)

    with open(CONFIG_PATH, "wb") as f:
        tomli_w.dump(config, f)


def show_config() -> dict:
    return load_config()
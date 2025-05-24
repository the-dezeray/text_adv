import yaml
import json
from typing import Dict, Any


def load_yaml_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
        return data if data is not None else {}


def load_json_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data


def load_sound():
    pass


def load_art():
    pass

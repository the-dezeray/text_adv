import yaml
import json
from typing import Dict, Any


def write_yaml_file(file_path: str, data: Dict[str, Any]) -> None:
    with open(file_path, "w") as f:
        yaml.dump(data, f)

def load_yaml_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
        return data if data is not None else {}


def load_json_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data


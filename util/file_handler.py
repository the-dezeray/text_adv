import yaml
import json


def load_yaml_file(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
        return data


def load_json_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        return data


def load_sound():
    pass


def load_art():
    pass

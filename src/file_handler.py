import yaml


def load_yaml_file(file_path):
    with open(file_path,"r") as f :
        data = yaml.safe_load(f)
        return data
    
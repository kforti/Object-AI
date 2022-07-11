import yaml


def deserialize_yaml_to_model(path, model):
    with open(path) as f:
        data = yaml.safe_load(f)
    instance = model(**data)
    return instance

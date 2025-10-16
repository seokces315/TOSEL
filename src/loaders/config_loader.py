import yaml


# Load and return the contents of a YAML file from the given file path
def load_config(config_path):

    # Load the specified config file
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config

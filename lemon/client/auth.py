


def key_path() -> str:
    import os
    credential_file = os.environ.get("LEMON_CREDENTIALS")
    if credential_file is not None:
        return credential_file
    else:
        raise ValueError("LEMON_CREDENTIALS not set in ENVIRONMENT_VARIABLES")



def credentials():
    import yaml
    with open(key_path(), "r") as yamlfile:
        return yaml.load(yamlfile, Loader=yaml.FullLoader)["lemon-markets"]['Space']
    

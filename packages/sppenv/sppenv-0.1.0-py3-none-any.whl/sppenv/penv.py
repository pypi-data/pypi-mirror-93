import os


def load_env(overwrite: bool = True):
    """Simple .env Loader"""
    # get current working dir
    env_path = os.path.join(os.getcwd(), ".env")

    with open(env_path, "r") as reader:
        for os_var in reader.readlines():
            # check if there is equals sign in each environment variable set
            if "=" in os_var:
                var, value = os_var.replace("\n", "").split("=")
                os.environ[var] = value

from pathlib import Path


PACKAGE_ROOT = Path(__file__).parent.parent
REPO_ROOT = PACKAGE_ROOT.parent

DATA_PATH = PACKAGE_ROOT.joinpath("data")
MODELS_PATH = DATA_PATH.joinpath("models")

ENV_DIR_PATH = PACKAGE_ROOT.joinpath("env")
ENV_FILE_PATH = PACKAGE_ROOT.joinpath("env", ".env")

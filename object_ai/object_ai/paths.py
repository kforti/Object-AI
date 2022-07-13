import os
from pathlib import Path

REPO_ROOT = os.environ.get('OBJECT_AI_REPO_PATH')
if REPO_ROOT is not None:
    REPO_ROOT = Path(REPO_ROOT)
else:
    REPO_ROOT = Path(__file__).parent.parent.parent
PACKAGE_ROOT = REPO_ROOT.joinpath('object_ai')

DATA_PATH = PACKAGE_ROOT.joinpath("data")
MODELS_PATH = DATA_PATH.joinpath("models")

ENV_DIR_PATH = PACKAGE_ROOT.joinpath("env")
ENV_FILE_PATH = PACKAGE_ROOT.joinpath("env", ".env")

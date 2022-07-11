import pytest

from object_ai.paths import (
    PACKAGE_ROOT,
    REPO_ROOT,
    DATA_PATH,
    MODELS_PATH,
    ENV_DIR_PATH,
    ENV_FILE_PATH,
)


@pytest.mark.parametrize(
    "path,expected",
    [
        (PACKAGE_ROOT, True),
        (REPO_ROOT, True),
        (DATA_PATH, True),
        (MODELS_PATH, True),
        (ENV_DIR_PATH, True),
        (ENV_FILE_PATH, True),
    ],
)
def test_path_exists(path, expected):
    if expected:
        assert path.exists()
    elif not expected:
        assert not path.exists()


@pytest.mark.parametrize(
    "path,expected",
    [
        (PACKAGE_ROOT, "object_ai"),
        (REPO_ROOT, "Object-AI"),
        (DATA_PATH, "data"),
        (MODELS_PATH, "models"),
        (ENV_DIR_PATH, "env"),
        (ENV_FILE_PATH, ".env"),
    ],
)
def test_path_names(path, expected):
    assert path.name == expected

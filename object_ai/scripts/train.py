import os
from pathlib import Path

from object_ai.orchestration.training import run_train


def main():
    DEFAULT_TRAIN_CONFIG = 'example_train_config.yaml'

    config_name = os.environ.get('TRAIN_CONFIG_NAME') or DEFAULT_TRAIN_CONFIG
    # Could allow adding new config path
    config_path = Path(__file__).parent.parent.joinpath('configs', config_name)
    state = run_train(config_path)
    return state

if __name__ == '__main__':
    main()
import os
from pathlib import Path

from object_ai.factories import build_object_detect_dataset


def main():
    DEFAULT_TRAIN_DATA = "PennFudanPed"

    data_name = os.environ.get("DEFAULT_TRAIN_DATA") or DEFAULT_TRAIN_DATA
    # Could allow adding new config path
    config_path = Path(__file__).parent.parent.joinpath("data", data_name)
    dataset = build_object_detect_dataset(config_path)
    print(len(dataset))


if __name__ == "__main__":
    main()

import os
from pathlib import Path
import json

from dotenv import load_dotenv

from labelbox.data.annotation_types import (
    Label,
    LabelList,
    ImageData,
    Point,
    ObjectAnnotation,
    Rectangle,
    Polygon,
)
from labelbox.data.serialization import COCOConverter
import labelbox


ENV_PATH = Path(__file__).parent.parent.joinpath("env", ".env")
load_dotenv(ENV_PATH)


def load_labels(path):
    with open(path) as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    # labels = load_labels(Path(__file__).parent.parent.joinpath('data', 'labelbox', 'export-2022-07-06T20_10_49.972Z.json'))
    LB_API_KEY = os.environ.get("LABELBOX_API_KEY")

    # Create Labelbox client
    client = labelbox.Client(api_key=LB_API_KEY)
    project = client.get_project("cl52t4kln4k1t071p6ospbvto")
    labels = project.label_generator()

    mask_path = "./masks/"
    image_path = (
        "/Users/kevinfortier/bin/Object-AI/object_ai/data/PennFudanPed/PNGImages"
    )

    coco_labels = COCOConverter.serialize_instances(
        labels, image_root=image_path, ignore_existing_data=True
    )
    print(coco_labels)

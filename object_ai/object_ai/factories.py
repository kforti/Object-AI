from pathlib import Path

from object_ai.dataset import ObjectDetectionDataset
from object_ai.repos import LocalImagesRepo, CocoLabelsRepo


def build_object_detect_dataset(dataset_path, transforms=None):
    dataset_path = Path(dataset_path)
    images_repo = LocalImagesRepo(base_path=dataset_path.joinpath('PNGImages'))
    masks_repo = LocalImagesRepo(base_path=dataset_path.joinpath('PedMasks'))
    labels_repo = CocoLabelsRepo()

    dataset = ObjectDetectionDataset(images_repo=images_repo,
                                     masks_repo=masks_repo,
                                     labels_repo=labels_repo,
                                     transforms=transforms)
    return dataset
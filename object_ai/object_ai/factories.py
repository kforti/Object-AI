from pathlib import Path
from typing import Dict, Literal

from object_ai.dataset import ObjectDetectionDataset
from object_ai.repos import LocalImagesRepo, CocoLabelsRepo


class ObjectDatasetConfig:
    images_repo_config: Dict
    labels_repo_config: Dict


class RepoConfig:
    source: str
    kwargs: Dict


def build_images_repo(config):
    if config.source == "local":
        repo = LocalImagesRepo(base_path=config.kwargs["base_path"])
    elif config.source == "s3":
        raise NotImplemented
    else:
        raise KeyError("Image repo source not identified. Check your dataset config")
    return repo


def build_labels_repo(config):
    if config.source == "local":
        masks_repo = LocalImagesRepo(base_path=config.kwargs["masks_base_path"])
        repo = CocoLabelsRepo(masks_repo=masks_repo)
    elif config.source == "labelbox":
        raise NotImplemented
    else:
        raise KeyError("Labels repo source not identified. Check your dataset config")
    return repo


def build_object_detect_dataset(config: ObjectDatasetConfig, transforms=None):
    images_repo = build_images_repo(config=config.images_config)
    labels_repo = build_labels_repo(config=config.labels_config)

    dataset = ObjectDetectionDataset(
        images_repo=images_repo,
        labels_repo=labels_repo,
        transforms=transforms,
    )
    return dataset

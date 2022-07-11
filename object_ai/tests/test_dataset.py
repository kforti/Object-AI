from object_ai.dataset import ObjectDetectionDataset
from object_ai.repos import ImagesRepo, LabelsRepo


class MockedImagesRepo(ImagesRepo):
    images = ["0", "1", "2", "3"]

    def get_image(self, name):
        image = None
        for img in self.images:
            if name == img:
                image = img
                break
        return image

    def list_image_names(self, sort_func=sorted, sort_kwrags=None):
        return self.images


class MockedLabelsRepo(LabelsRepo):
    def get_label(self, name, idx):
        label = {
            "boxes": [],
            "labels": [],
            "masks": None,
            "image_id": idx,
            "area": 12,
            "iscrowd": 0,
        }
        return label


def test_dataset_length():
    images_repo = MockedImagesRepo()
    dataset = ObjectDetectionDataset(
        images_repo=images_repo, labels_repo=None, transforms=None
    )
    assert len(dataset) == len(images_repo.images)


def test_dataset_iteration():
    images_repo = MockedImagesRepo()
    labels_repo = MockedLabelsRepo()
    dataset = ObjectDetectionDataset(
        images_repo=images_repo, labels_repo=labels_repo, transforms=None
    )
    for i, (image, label) in enumerate(dataset):
        assert label["image_id"] == i
        assert image == str(i)

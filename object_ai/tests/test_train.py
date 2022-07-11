from pytest import fixture

from object_ai.factories import ObjectDatasetConfig, RepoConfig
from object_ai.modeling.training import TrainingConfig
from object_ai.train import train


@fixture
def train_config():
    images_repo_config = RepoConfig(source="local", kwargs=None)
    labels_repo_config = RepoConfig(source="local", kwargs=None)
    dataset_config = ObjectDatasetConfig(images_repo_config, labels_repo_config)
    config = TrainingConfig(dataset_config=dataset_config, num_classes=2, num_epochs=1)
    return config


def test_train_returns_results(train_config):
    results = train(train_config)

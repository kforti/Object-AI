
from prefect import flow

from object_ai.train import train
from object_ai.modeling.configs import TrainConfig


@flow
def run_train(config_path):
    config = TrainConfig.from_yaml(config_path)
    result = train(config)
    return result




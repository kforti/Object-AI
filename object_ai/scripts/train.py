import os
from pathlib import Path
import yaml

import torch

from object_ai.utils.engine import train_one_epoch, evaluate
from object_ai.utils import utils
from object_ai.dataset import PennFudanDataset
from object_ai.transforms import get_transform
from object_ai.models import get_model_instance_segmentation
from object_ai.trainers import Trainer


DATASET_PATH = Path(__file__).parent.parent.joinpath('data')


class TrainConfig:

    def __init__(self,
                 num_epochs,
                 num_classes):
        self.num_epochs = num_epochs
        self.num_classes = num_classes

    @classmethod
    def from_yaml(cls, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(num_epochs=data.get('num_epochs'),
                   num_classes=data.get('num_classes'))


def train(config):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    # use our dataset and defined transformations
    dataset = PennFudanDataset(DATASET_PATH.joinpath('PennFudanPed'), get_transform(train=True))
    dataset_test = PennFudanDataset(DATASET_PATH.joinpath('PennFudanPed'), get_transform(train=False))

    # split the dataset in train and test set
    indices = torch.randperm(len(dataset)).tolist()
    dataset = torch.utils.data.Subset(dataset, indices[:-50])
    dataset_test = torch.utils.data.Subset(dataset_test, indices[-50:])

    # define training and validation data loaders
    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=2, shuffle=True, num_workers=4,
        collate_fn=utils.collate_fn)

    data_loader_test = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=False, num_workers=4,
        collate_fn=utils.collate_fn)

    # get the model using our helper function
    model = get_model_instance_segmentation(config.num_classes)

    # move model to the right device
    model.to(device)

    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005,
                                momentum=0.9, weight_decay=0.0005)
    # and a learning rate scheduler
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                   step_size=3,
                                                   gamma=0.1)

    trainer = Trainer(lr_scheduler=lr_scheduler)
    trainer.train(model=model,
                  data_loader=data_loader,
                  eval_data_loader=data_loader_test,
                  device=device,
                  num_epochs=config.num_epochs,
                  optimizer=optimizer)
    print("That's it!")


DEFAULT_TRAIN_CONFIG = 'example_train_config.yaml'

def main():
    config_name = os.environ.get('TRAIN_CONFIG_NAME') or DEFAULT_TRAIN_CONFIG
    # Could allow adding new config path
    config_path = Path(__file__).parent.parent.joinpath('configs', config_name)
    config = TrainConfig.from_yaml(config_path)
    train(config)


if __name__ == '__main__':
    main()
from pathlib import Path

import torch

from object_ai.utils import utils
from object_ai.transforms import get_transforms
from object_ai.models import get_model_instance_segmentation
from object_ai.trainers import Trainer, LocalModelStore
from object_ai.factories import build_object_detect_dataset
from object_ai.paths import DATA_PATH, MODELS_PATH


def train(config, data_path=DATA_PATH):
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    # use our dataset and defined transformations
    dataset_path = data_path.joinpath("PennFudanPed")
    dataset = build_object_detect_dataset(
        dataset_path, transforms=get_transforms(train=True)
    )

    dataset_test = build_object_detect_dataset(
        dataset_path, transforms=get_transforms(train=False)
    )

    # split the dataset in train and test set
    indices = torch.randperm(len(dataset)).tolist()
    dataset = torch.utils.data.Subset(dataset, indices[0:5])
    dataset_test = torch.utils.data.Subset(dataset_test, indices[5:10])

    # define training and validation data loaders
    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=2, shuffle=True, num_workers=4, collate_fn=utils.collate_fn
    )

    data_loader_test = torch.utils.data.DataLoader(
        dataset_test,
        batch_size=1,
        shuffle=False,
        num_workers=4,
        collate_fn=utils.collate_fn,
    )

    # get the model using our helper function
    model = get_model_instance_segmentation(config.num_classes)

    # move model to the right device
    model.to(device)

    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
    # and a learning rate scheduler
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

    model_store = LocalModelStore(base_path=MODELS_PATH)
    trainer = Trainer(lr_scheduler=lr_scheduler, model_store=model_store)
    results = trainer.train(
        model=model,
        model_name="maskrcnn_resnet50",
        data_loader=data_loader,
        eval_data_loader=data_loader_test,
        device=device,
        num_epochs=config.num_epochs,
        optimizer=optimizer,
    )
    return results

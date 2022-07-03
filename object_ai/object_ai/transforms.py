import torch

from .utils import transforms as T

def get_transform(train):
    transforms = []
    transforms.append(T.PILToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    transforms.append(T.ConvertImageDtype(dtype=torch.float))
    return T.Compose(transforms)
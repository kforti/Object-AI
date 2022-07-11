from typing import List, Tuple, Dict, Optional, Union

import torch
from torch import nn, Tensor
from torchvision.transforms import functional as F

from .utils import transforms as T


def get_transforms(train):
    transforms = []
    transforms.append(T.ImageToRGB())
    transforms.append(T.PILToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    transforms.append(T.ConvertImageDtype(dtype=torch.float))
    return T.Compose(transforms)

import os
from pathlib import Path

from PIL import Image
import torch
import numpy as np


class LocalImagesRepo:
    def __init__(self, base_path):
        self.base_path = Path(base_path)

    def get_image(self, name):
        path = self.base_path.joinpath(name)
        image = Image.open(path)
        return image

    def list_image_names(self, sort_func=sorted, sort_kwrags=None):
        names = os.listdir(self.base_path)
        sort_kwrags = sort_kwrags or {}
        sorted_names = sort_func(names, **sort_kwrags)
        return sorted_names


class CocoLabelsRepo:
    def get_label_from_mask(self, mask, idx):
        # instances are encoded as different colors
        obj_ids = np.unique(mask)
        # first id is the background, so remove it
        obj_ids = obj_ids[1:]
        # convert the PIL Image into a numpy array
        mask = np.array(mask)
        # split the color-encoded mask into a set
        # of binary masks
        masks = mask == obj_ids[:, None, None]

        # get bounding box coordinates for each mask
        num_objs = len(obj_ids)
        boxes = []
        for i in range(num_objs):
            pos = np.where(masks[i])
            xmin = np.min(pos[1])
            xmax = np.max(pos[1])
            ymin = np.min(pos[0])
            ymax = np.max(pos[0])
            boxes.append([xmin, ymin, xmax, ymax])

        # convert everything into a torch.Tensor
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class
        labels = torch.ones((num_objs,), dtype=torch.int64)
        masks = torch.as_tensor(masks, dtype=torch.uint8)

        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        label = {}
        label["boxes"] = boxes
        label["labels"] = labels
        label["masks"] = masks
        label["image_id"] = image_id
        label["area"] = area
        label["iscrowd"] = iscrowd

        return label


import os
from pathlib import Path
from io import BytesIO

import PIL.PngImagePlugin
import boto3
import requests
from PIL import Image
import torch
import numpy as np
from botocore.exceptions import ClientError


def get_remote_image(url):
    req = requests.get(url)
    image = Image.open(BytesIO(req.content))

    return image


class ImagesRepo:
    def get_image(self, name):
        raise NotImplemented

    def list_image_names(self, sort_func=sorted, sort_kwrags=None):
        raise NotImplemented


class LocalImagesRepo(ImagesRepo):
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


class S3ImagesRepo:
    def __init__(self, bucket, base_path=None, region="us-east-2"):
        self.bucket = bucket
        self.region = region
        self.base_path = base_path or ""
        if not self.base_path.endswith("/"):
            self.base_path = self.base_path + "/"

    def get_image(self, name):
        client = boto3.client("s3")
        obj = client.get_object(
            Bucket=self.bucket, Key=os.path.join(self.base_path, name)
        )

        image = Image.open(obj["Body"])
        return image

    def list_image_names(self, sort_func=sorted, sort_kwrags=None):
        client = boto3.client("s3")
        continuation_token = ""
        paths = []
        while continuation_token is not None:
            if not continuation_token:
                response = client.list_objects_v2(
                    Bucket=self.bucket,
                    Prefix=self.base_path,
                )
            else:
                response = client.list_objects_v2(
                    Bucket=self.bucket,
                    Prefix=self.base_path,
                    ContinuationToken=continuation_token,
                )
            if "NextContinuationToken" not in response:
                continuation_token = None
            else:
                continuation_token = response["NextContinuationToken"]
            contents = [
                os.path.basename(obj["Key"])
                for obj in response["Contents"]
                if obj["Key"] != self.base_path
            ]
            paths.extend(contents)
        if sort_func is not None:
            sort_kwrags = sort_kwrags or {}
            paths = sort_func(paths, **sort_kwrags)

        return paths

    def get_image_url(self, name):
        base_url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/"
        client = boto3.client("s3")
        try:
            obj = client.head_object(
                Bucket=self.bucket, Key=os.path.join(self.base_path, name)
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "404":
                return None
            raise exc
        url = os.path.join(base_url, self.base_path, name)
        return url


class LabelsRepo:
    def get_label(self, name):
        raise NotImplemented


class CocoLabelsRepo(LabelsRepo):
    def __init__(self, masks_repo: ImagesRepo):
        self.masks_repo = masks_repo

    def get_label(self, name, idx):
        mask = self.masks_repo.get_image(name)
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


class LabelboxLabelsRepo(LabelsRepo):
    def __init__(self, project_id):
        self.project_id = project_id

import yaml
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from ..factories import ObjectDatasetConfig


class TrainingConfig(BaseModel):
    dataset_config: ObjectDatasetConfig
    num_epochs: int
    num_classes: int


class TrainingResults(BaseModel):
    metric: str
    score: float
    model_name: str
    models_path: str

import copy
import json
import os.path
from pathlib import Path
from datetime import datetime

import torch

from object_ai.utils.engine import train_one_epoch, evaluate

def get_current_timestamp():
    timestamp = str(datetime.utcnow().replace(microsecond=0)).replace(' ', '_')
    return timestamp


class LocalModelStore:
    def __init__(self, base_path):
        self.base_path = Path(base_path)

    def save_model(self, model, model_name, meta_data, prefix):
        base_path = self.base_path.joinpath(prefix)
        if not base_path.exists():
            base_path.mkdir(parents=True)
        model_path = base_path.joinpath(model_name)
        meta_path = base_path.joinpath('meta.json')

        # save model
        best_model_wts = copy.deepcopy(model.state_dict())
        torch.save(best_model_wts, model_path)

        # save meta data
        with open(meta_path, 'w') as f:
            json.dump(meta_data, f)

        return None


class Trainer:

    def __init__(self, lr_scheduler, model_store):
        self.lr_scheduler = lr_scheduler
        self.model_store = model_store

    def train(self,
              model,
              model_name,
              optimizer,
              data_loader,
              eval_data_loader,
              device,
              num_epochs):
        start_training_timestamp = get_current_timestamp()
        best_metric_score = None
        for epoch in range(0, num_epochs):
            self.train_one_epoch(model,
                                 optimizer,
                                 data_loader,
                                 device,
                                 epoch)
            self.lr_scheduler.step()
            evaluator = self.evaluate(model, eval_data_loader, device)
            metric_score = evaluator.get_evaluation_metrics()
            if best_metric_score is None or metric_score > best_metric_score:
                best_metric_score = metric_score
                self.model_store.save_model(
                    model=model,
                    model_name=f'{model_name}_{epoch}.pth',
                    meta_data={'metric': 'mean_precision',
                               },
                    prefix=os.path.join(model_name, start_training_timestamp, 'best_model')
                )

    def train_one_epoch(self, model, optimizer, data_loader, device, epoch, print_freq=10):
        return train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=print_freq)

    def evaluate(self, model, data_loader, device):
        return evaluate(model, data_loader, device)
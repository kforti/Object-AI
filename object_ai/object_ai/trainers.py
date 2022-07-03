from object_ai.utils.engine import train_one_epoch, evaluate


class Trainer:

    def __init__(self, lr_scheduler):
        self.lr_scheduler = lr_scheduler

    def train(self,
              model,
              optimizer,
              data_loader,
              eval_data_loader,
              device,
              num_epochs):

        for epoch in range(0, num_epochs):
            self.train_one_epoch(model,
                                 optimizer,
                                 data_loader,
                                 device,
                                 epoch)
            self.lr_scheduler.step()
            self.evaluate(model, eval_data_loader, device)

    def train_one_epoch(self, model, optimizer, data_loader, device, epoch, print_freq=10):
        return train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=10)

    def evaluate(self, model, data_loader, device):
        return evaluate(model, data_loader, device)
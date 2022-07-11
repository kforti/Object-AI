import yaml


class TrainConfig:
    def __init__(self, num_epochs, num_classes):
        self.num_epochs = num_epochs
        self.num_classes = num_classes

    @classmethod
    def from_yaml(cls, path):
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(
            num_epochs=data.get("num_epochs"), num_classes=data.get("num_classes")
        )

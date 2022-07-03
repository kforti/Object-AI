
from object_ai.trainers import Trainer

def test_trainer_run():
    trainer = Trainer()
    run = trainer.run()
    assert run
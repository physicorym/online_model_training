import torch
from torch.optim.optimizer import Optimizer
from dataclasses import dataclass


@dataclass
class Config:
    SEED: int
    IMG_SIZE: int
    CHANNEL: int
    BATCH_SIZE: int
    N_EPOCHS: int
    NUM_ITERATION_ON_EPOCH: int
    IMAGE_DIR: str
    LABELS_FILE: str
    DEVICE: str
    AUGMENTATION: bool
    NUM_WORKER: int
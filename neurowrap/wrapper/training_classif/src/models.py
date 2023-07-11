import torch
import torchmetrics
import torchvision
from torch import nn
from torch.nn import functional as F
import pytorch_lightning as pl

from src.base_config import Config
from config import config

class LitResnet(nn.Module):
    def __init__(self, arch: str, pretrained: bool = True, num_classes: int = 6):
        super().__init__()
        self.arch = arch
        self.num_classes = num_classes
        self.model = torchvision.models.__dict__[arch](pretrained=pretrained)
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, config.NUM_CLASSES)

    def forward(self, x):
        return self.model(x)


class LitPL(pl.LightningModule):

    def __init__(self, model, lr: float = 1e-4):
        super().__init__()
        self.model = model
        self.arch = self.model.arch
        self.num_classes = 3 #self.model.num_classes
        self.train_accuracy = torchmetrics.Accuracy(task='multiclass', num_classes=3)
        self.val_accuracy = torchmetrics.Accuracy(task='multiclass', num_classes=3)
        self.val_f1_score = torchmetrics.F1Score(task='multiclass',num_classes=self.num_classes)
        self.learn_rate = lr
        self.loss = nn.CrossEntropyLoss() #nn.BCEWithLogitsLoss()

    def forward(self, x):
        return F.sigmoid(self.model(x))

    def compute_loss(self, y_hat, y):
        return self.loss(y_hat, y.to(int))

    #.cuda().long()

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.compute_loss(y_hat, y)
        self.log("train_loss", loss, prog_bar=True)
        self.log("train_acc", self.train_accuracy(y_hat, y), prog_bar=False)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.compute_loss(y_hat, y)
        self.log("valid_loss", loss, prog_bar=False)
        self.log("valid_acc", self.val_accuracy(y_hat, y), prog_bar=True)
        self.log("valid_f1", self.val_f1_score(y_hat, y), prog_bar=True)

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.learn_rate)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, self.trainer.max_epochs, 0)
        return [optimizer], [scheduler]
from torch import nn
import torch.optim as optim
import torch

from wrapper.training_classif.src.dataset import get_loaders
from wrapper.training_classif.src.models import *
from wrapper.training_classif.src.losses import FocalLoss
from wrapper.training_classif.config import config
from wrapper.training_classif.src.fit import fit



torch.device('cuda' if torch.cuda.is_available() else 'cpu')

train_data, test_data = get_loaders(config)

net = LitResnet(arch='resnet18', num_classes=config.NUM_CLASSES)
net.to(torch.device(config.DEVICE))

criterion = nn.CrossEntropyLoss()
# criterion = FocalLoss()
optimizer = optim.Adam(net.parameters(), lr=1e-4)
print('начало обучения')
fit(config, net, train_data, optimizer, criterion)
print('конец обучения')

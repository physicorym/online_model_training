from torch import nn
import torch.optim as optim
import torch

from src.dataset import get_loaders
from src.models import LitPL, LitResnet
from src.losses import FocalLoss
from config import config
from src.fit import fit


if __name__ == '__main__':

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
import typing as tp

from torch import nn
import torch.optim as optim
import torch
import numpy as np
import cv2

from src.dataset import get_loaders
from src.models import LitPL, LitResnet
from src.losses import FocalLoss
from src.utils import preprocessing_image
from config import config

class ImageClasification:

    def __init__(self, config: tp.Dict, model: torch.nn.Module):
        self._model_path = config.MODEL
        self._device = config.DEVICE
        self._num_classes = config.NUM_CLASSES

        self._path_img_test = config.IMG_TEST

        self._base_model = model
        
    def predict(self, image: np.ndarray) -> np.ndarray:

        self._base_model.load_state_dict(torch.load(config.MODEL, map_location=torch.device('cpu')))

        self._base_model.eval()

        batch = preprocessing_image(image).to('cpu')

        with torch.no_grad():
            predict = self._base_model(batch)

        return predict

if __name__ == '__main__':

    torch.device('cpu')

    model = LitResnet(arch='resnet18', num_classes=3)
    model.to(torch.device('cpu'))
    model.eval()

    model = ImageClasification(config, model)

    image = cv2.imread(config.IMG_TEST)

    predict = model.predict(image)
    result = torch.argmax(predict)

    print(result.item(), '- class')
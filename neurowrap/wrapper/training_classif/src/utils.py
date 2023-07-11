import os
import numpy as np
import cv2
from torch import nn, max, sum
import torch
from loguru import logger


from .base_config import Config


from wrapper.training_classif.config import config

def preprocessing_image(image):

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (config.IMG_SIZE, config.IMG_SIZE))

    img = torch.tensor(img)
    img = img.permute(2, 0, 1).float()

    img = torch.unsqueeze(img, 0)

    return img

def search_bestmodel():

    name_models = sorted(os.listdir('./weights/'))
    if len(name_models) > 1:
        list_loss = []
        for name_model in name_models:
            name_loss = name_model.split('_')[1]
            list_loss.append(float(name_loss))
        index_min = list_loss.index(min(list_loss))
        os.rename('./weights/' + name_models[index_min], './weights/bestmodel.pth')
    else:
        os.rename('./weights/' + name_models[0], './weights/bestmodel.pth')
        
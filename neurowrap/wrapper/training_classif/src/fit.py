import numpy as np
from torch import nn, max, sum
import torch
from loguru import logger

from src.utils import search_bestmodel
from src.base_config import Config
from config import config

def fit(config: Config, model, dataset, optimizer, criterion):
    n_epochs = config.N_EPOCHS

    val_loss = []
    val_acc = []
    train_loss = []
    train_acc = []
    total_step = len(dataset['train'])
    for epoch in range(n_epochs):

        running_loss = 0.0
        correct = 0
        total = 0

        print(f'Epoch {epoch}\n')
        print(len(dataset['train']), 'train')
        for batch, (data, target) in enumerate(dataset['train']):

            target = target.type(torch.LongTensor)
            data, target = data.to(config.DEVICE), target.to(config.DEVICE)
            optimizer.zero_grad()
            logger.debug('optimizer zero')

            outputs = model(data)
            loss = criterion(outputs, target)
            logger.debug('loss calculate')


            loss.backward()
            optimizer.step()
            logger.debug('update weights')
            running_loss += loss.item()

            _, pred = max(outputs, dim=1)
            correct += sum(pred==target).item()

            total += target.size(0)

            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                  .format(epoch, n_epochs, batch, total_step, loss.item()))

            train_acc.append(100 * correct/ total)
            train_loss.append(running_loss/total_step)

            print(f'\ntrain loss: {np.mean(train_loss):.4f}, '
                  f'train_acc: {(100*correct/total)}:.4f')

            batch_loss=0
            total_t=0
            correct_t=0

        with torch.no_grad():
            model.eval()
            logger.debug('model eval')
            print(len(dataset['valid']), 'validataion')
            for data_v, target_v in dataset['valid']:

                target_v = target_v.type(torch.LongTensor)
                data_v, target_v = data_v.to(config.DEVICE), target_v.to(config.DEVICE)
                # logger.debug('val predict')
                outputs_v = model(data_v)
                loss_t = criterion(outputs_v, target_v)

                batch_loss += loss_t.item()

                _, pred_t = max(outputs_v, dim=1)
                correct_t += sum(pred_t==target_v).item()

                total_t += target_v.size(0)

            val_acc.append(100 * correct_t/ total_t)
            val_loss.append(batch_loss/ len(dataset['train']))

            print(f'validation loss: {np.mean(val_loss):.4f}, '
                    f'validation acc: {(100 * correct_t / total_t):.4f}\n')

        torch.save(model.state_dict(),
                       f"weights/vloss_{np.mean(val_loss)}_vacc_{np.mean(val_acc)}_statemodel.pth")

    search_bestmodel()
    
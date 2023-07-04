from src.dataset import ClassificationDataset, get_loaders

from config import config

from src.utils import search_bestmodel


if __name__ == '__main__':
    search_bestmodel()
    # train, test = get_loaders(config)

    # print(len(train['train']), 'train')
    # print(len(train['valid']), 'valid')

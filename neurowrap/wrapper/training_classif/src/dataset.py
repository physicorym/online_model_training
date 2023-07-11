import os
import torch
import pandas as pd
import cv2
import numpy as np
import typing as tp
from collections import OrderedDict
from sklearn.model_selection import train_test_split

from torch.utils.data import Dataset
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from .base_config import Config


from wrapper.training_classif.config import config

class ClassificationDataset(Dataset):
    def __init__(
        self,
        config: Config,
        df: pd.DataFrame,
    ):

        self.config = config
        self.df_labels = df #pd.read_csv(config.LABELS_FILE)
        self.path_img_dir = os.path.join(config.IMAGE_DIR)
        self.img_names = self.df_labels['filename']#os.listdir(self.path_img_dir)

        self.target = self.df_labels['target']

    def test_getitem(self):
        label = self.target
        # print(label)

    def __getitem__(self, idx: int) -> tuple:
        img_path = os.path.join(self.path_img_dir, str(self.target.iloc[idx]), self.img_names.iloc[idx])
        label = self.target.iloc[idx]

        img = cv2.imread(img_path)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.config.IMG_SIZE, self.config.IMG_SIZE))


        return torch.tensor(img), torch.tensor(label)

    def __len__(self) -> int:
        return len(self.df_labels)

    def collate_fn(self, batch):
        images, labels = [], []

        for (img, label) in batch:
            img = torch.tensor(img)
            img = img.permute(2, 0, 1)
            # if self.transform is not None:
            #     img = self.transform(img)
            images.append(img[None])
            labels.append(np.array(label))

        labels = np.array(labels)

        images = torch.cat(images).float().to(self.config.DEVICE)
        labels = torch.tensor(labels).float().to(self.config.DEVICE)
        return images.to(config.DEVICE), labels.to(config.DEVICE)

def get_transforms(config: Config):
    if config.AUGMENTATION:
        transform_train = transforms.Compose([
            transforms.ToPILImage(),
            transforms.ColorJitter(),
            transforms.RandomCrop(config.IMG_SIZE),
            transforms.RandomHorizontalFlip(),

            transforms.Resize(config.IMG_SIZE),
            transforms.ToTensor(),
        ])
        transform_val = transforms.Compose([
            transforms.ToPILImage(),

            transforms.Resize(config.IMG_SIZE),
            transforms.ToTensor(),
        ])
        return transform_train, transform_val

    transform_train = transforms.Compose([
        transforms.ToPILImage(),

        transforms.Resize(config.IMG_SIZE),
        transforms.ToTensor(),
    ])

    transform_val = transforms.Compose([
        transforms.ToPILImage(),

        transforms.Resize(config.IMG_SIZE),
        transforms.ToTensor(),
    ])

    return transform_train, transform_val

def get_datasets(config: Config) -> tp.Tuple[Dataset, Dataset, Dataset]:
    df = pd.read_csv(config.LABELS_FILE)

    df_train, df_val = train_test_split(df, train_size=0.2)
    df_val, df_test = train_test_split(df_val, train_size=0.2)
    print(len(df_train), len(df_val))
    train_transform, val_transform = get_transforms(config)

    train_dataset = ClassificationDataset(config, df_train)

    valid_dataset = ClassificationDataset(config, df_val)

    test_dataset = ClassificationDataset(config, df_test)

    return train_dataset, valid_dataset, test_dataset


def get_loaders(config: Config) -> tp.Tuple[tp.OrderedDict[str, DataLoader], tp.Dict[str, DataLoader]]:
    train_dataset, valid_dataset, test_dataset = get_datasets(config)

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        num_workers=config.NUM_WORKER,
        collate_fn=train_dataset.collate_fn,
    )

    valid_loader = DataLoader(
        valid_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=config.NUM_WORKER,
        collate_fn=valid_dataset.collate_fn,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=config.NUM_WORKER,
        collate_fn=test_dataset.collate_fn,
    )

    return OrderedDict({'train': train_loader, 'valid': valid_loader}), {'infer': test_loader}

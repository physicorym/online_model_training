
import pytorch_lightning as pl

from src.dataset import get_loaders
from src.models import LitPL, LitResnet
from src.dataset_pl import PLDM
from config import config

#logger = pl.loggers.CSVLogger(save_dir='logs/', name=model.arch)

# ==============================

if __name__ == '__main__':

    train, test = get_loaders(config)

    dm = PLDM()
    dm.setup()
    print(dm.num_classes)

    net = LitResnet(arch='resnet18', num_classes=3)
    # print(net)
    model = LitPL(model=net)

    trainer = pl.Trainer(

        gpus=1,

        logger=None,
        max_epochs=10,
        accumulate_grad_batches=8,
        val_check_interval=0.25,

    )


    trainer.fit(model, train['train'], train['valid'])
import pandas as pd
import os
import sys
sys.path.append('./')
from config import config

#image_directory = 'E:/SHP/classif_train/train/'
image_directory = 'E:/HARNESS_BELT/BENZOL_CLASSIF/train/'
image_directory = config.IMAGE_DIR

list_classes = [folder for folder in os.listdir(image_directory) if folder != '.DS_Store']
print(list_classes)


df = pd.DataFrame({'filename':[], 'target':[],'folder':[]})

df_small = []
for i in range(len(list_classes)):
    list_image = os.listdir(os.path.join(image_directory, str(i)))
    df = pd.DataFrame({'filename': list_image, 'target': str(i)})
    df_small.append(df)

df = pd.concat(df_small, axis=0, ignore_index=True)

df.to_csv('./data/labels.csv')

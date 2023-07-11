
IMAGE_DIR = "C:/Pet_Dev/dataset/train"

SEED = 42
IMG_SIZE = 224
CHANNEL = 3
BATCH_SIZE = 32
N_EPOCHS = 1
NUM_ITERATION_ON_EPOCH = 100

LABELS_FILE = 'C:/Pet_Dev/online_model_training/neurowrap/wrapper/training_classif/data/labels.csv'
MODEL = './weights/bestmodel.pth'

DEVICE = 'cpu'

AUGMENTATION = True

NUM_WORKER = 0
NUM_CLASSES = 17

IMG_TEST = "C:/Pet_Dev/dataset/test.jpeg"

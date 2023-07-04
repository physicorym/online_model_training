
IMAGE_DIR = '/dataset/opensource/fruit/train/'

SEED = 42
IMG_SIZE = 224
CHANNEL = 3
BATCH_SIZE = 32
N_EPOCHS = 3
NUM_ITERATION_ON_EPOCH = 100

LABELS_FILE = './data/labels.csv'
MODEL = './weights/bestmodel.pth'

DEVICE = 'cpu'

AUGMENTATION = True

NUM_WORKER = 0
NUM_CLASSES = 17

IMG_TEST = '/dataset/opensource/fruit/train/0/Apple (18).jpeg'

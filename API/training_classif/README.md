# Обучение классификатора

##### Запуск локально

### Настройка окружения

Сначала создать и активировать venv:

```bash
python3 -m venv venv
. venv/bin/activate
```

1. Установка зависимостей ```pip install -r requirements.txt```
2. Необходимо в файле ```config.py```, расположенного в папке ```config```, указать путь до изображений в поле IMAGE_DIR.

***Пример***

**Config файл**
```
N_EPOCHS = 20 - количество эпох

IMAGE_DIR = '/dataset/opensource/fruit/train/' - путь до изображений

```
Названия папок с изображениями должны называться: 0, 1, 2, 3 и так далее

3. Перед запуском необходимо создать ```labels.csv``` файл с помощью скрипта ```tools/prepare_dataset.py```.

```bash
python tools/prepare_dataset.py
```

(можно создать свой ```labels.csv```)

В папке data создадится файл ```labels.csv```

4. Запуск обучения

```bash
python train.py
```

5. Проверка модели

указать путь до изображения для теста в поле ```IMG_TEST```, в файле ```config.py```.

***Пример***

**Config файл**
```
N_EPOCHS = 20 - количество эпох

IMG_TEST = 'Documents/dataset/test.jpg'
```

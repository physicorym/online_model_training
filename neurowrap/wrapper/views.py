import os

from django.conf import settings
from django.shortcuts import render

# from wrapper.training_classif.train import train


def start_train(request):
    if (request.GET.get('mybtn')):
        train_path = os.path.join(f'{settings.BASE_DIR}'
                                  f'/wrapper/training_classif/train.py')
        with open(train_path) as f:
            exec(f.read())
    return render(request, 'calc.html')

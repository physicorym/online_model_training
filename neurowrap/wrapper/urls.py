from django.urls import path
# from django.contrib import admin
from .views import start_train
urlpatterns = [

    path('', start_train)
]
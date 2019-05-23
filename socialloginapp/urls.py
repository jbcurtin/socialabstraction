from django.contrib import admin
from django.urls import path, include

from socialloginapp import views

urlpatterns = [
    path('index.html', views.index),
]

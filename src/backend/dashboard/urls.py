from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('settings/', views.settings, name='settings'),
]
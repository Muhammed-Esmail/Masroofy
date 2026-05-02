from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.home),
    path('api/auth/', views.Auth, name='Auth'),
    path('api/verify/', views.verifySession, name='verifySession'),
]

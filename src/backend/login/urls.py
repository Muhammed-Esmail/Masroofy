from django.contrib import admin
from django.urls import path, include
from .views import Auth, verifySession

from . import views

app_name='login'
urlpatterns = [
    path('', views.home, name='login'),
    path('api/auth/', Auth),
    path('api/verify/', verifySession),
]

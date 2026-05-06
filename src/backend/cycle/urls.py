from django.urls import path
from . import views

app_name='cycle'
urlpatterns = [
    path('', views.index, name='welcome'),
    path('start_cycle/', views.startCycle, name='start_cycle'),
]
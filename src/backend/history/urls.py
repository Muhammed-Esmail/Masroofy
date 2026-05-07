from django.urls import path
from . import views

app_name='history'
urlpatterns = [
    path('', views.index, name='index'),
    path('full_history/', views.full_history, name='full_history'),
    path('filtered_history/', views.filtered_history, name='filtered_history'),
    path('fetch_cycle_data/', views.fetch_cycle_data, name='fetch_cycle_data'),
    path('get_total_spent/', views.get_total_spent, name='get_total_spent'),
    path('get_active_cycle_id/', views.get_active_cycle_id, name='get_active_cycle_id')
]
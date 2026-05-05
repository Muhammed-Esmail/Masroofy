from django.urls import path
from . import views

app_name='transaction'
urlpatterns = [
    path('', views.index, name='index'),
    path('log_transaction/', views.log_transaction, name='log_transaction'),
    path('update_transaction/', views.update_transaction, name='update_transaction'),
    path('delete_transaction/<int:id>/', views.delete_transaction, name='delete_transaction'),
]
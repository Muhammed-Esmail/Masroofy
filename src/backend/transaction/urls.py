from django.urls import path
from . import views

app_name='transaction'
urlpatterns = [
    path('', views.index, name='index'),
    path('log_transaction/', views.log_transaction, name='log_transaction'),
    path('update_transaction/', views.update_transaction, name='update_transaction'),
    path('delete_transaction/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('category/', views.category_index, name='category_index'),
    path('add_category/', views.add_category, name='add_category'),
    path('update_category/', views.update_category, name='update_category'),
    path('delete_category/<str:name>/', views.delete_category, name='delete_category'),
]
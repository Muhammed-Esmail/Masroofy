from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='expense-list'),
    path('create/', views.create_expense, name='expense-create'),
    path('<int:id>/update/', views.update_expense, name='expense-update'),
    path('<int:id>/delete/', views.delete_expense, name='expense-delete'),
]
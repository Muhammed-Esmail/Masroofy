from django.shortcuts import render
from backend.Controller import Controller
from userSettings.services.SettingsManager import SettingsManager
from history.services import TransactionCRUD, CategoryCRUD
from datetime import datetime
from django.http import JsonResponse
import json
from django.views.decorators.cache import never_cache

controller = Controller()
transaction_crud = TransactionCRUD()
category_manager = controller.getCategoryManager()
transaction_manager = controller.getTransactionManager()
notification_manager = controller.getNotificationManager()
category_crud = CategoryCRUD()

def fetchAndBuildTransactionObject(request):
    data = json.loads(request.body)
    id = data.get('id')
    if (id): id = int(id)
    amount = int(data.get('amount'))
    category_name = data.get('category_name')
    log_date = datetime.strptime(data.get('log_date'), '%Y-%m-%d').date()
    description = data.get('description')
    note = data.get('note')  

    return transaction_crud.createDataObject(
        id=id,
        amount=amount,
        cycle_id=None,
        category_name=category_name,
        log_date=log_date,
        description=description,
        note=note
    )
    
def fetchAndBuildCategoryObject(request):
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    return category_crud.createDataObject(name, description)
    
@never_cache
def index(request):
    categories = category_manager.fetchAllCategories()
    settings = SettingsManager().fetchSettings()
    context = {
        "categories": categories,
        "settings": settings,
    }
    return render(request, 'pages/transaction/transaction.html', context)

def log_transaction(request):
    transaction_obj = fetchAndBuildTransactionObject(request)    
    if transaction_obj.amount <= 0:
        return JsonResponse({'success': False})
    transaction_manager.logTransaction(transaction_obj)
    state = notification_manager.getCurrentState()
    return JsonResponse({'ok': True, 'state': state})

def update_transaction(request):
    transaction_obj = fetchAndBuildTransactionObject(request)
    transaction_manager.updateTransaction(transaction_obj)
    state = notification_manager.getCurrentState()
    return JsonResponse({'ok': True, 'state': state})


def delete_transaction(request, id):
    transaction_manager.deleteTransaction(id)

    state = notification_manager.getCurrentState()
    return JsonResponse({'ok': True, 'state': state})

@never_cache
def category_index(request):
    categories = category_manager.fetchAllCategories()
    settings = SettingsManager().fetchSettings()
    context = {
        "categories": categories,
        "settings": settings,
    }
    return render(request, 'pages/transaction/category.html', context)

def add_category(request):
    category_obj = fetchAndBuildCategoryObject(request)
    
    res = category_manager.addCategory(category_obj)
    
    if res is None:
        print("HERE")
        return JsonResponse({'ok': False, 'description':'Category Name was Not Unique'})

    return JsonResponse({'ok': True})

def update_category(request):
    data = json.loads(request.body)
    previous_category_name = data.get('previous_category_name')
    category_obj = fetchAndBuildCategoryObject(request)
    category_manager.updateCategory(previous_category_name, category_obj)
    return JsonResponse({'ok': True})
    
def delete_category(request, name):
    category_manager.deleteCategory(name)
    return JsonResponse({'ok': True})

from django.shortcuts import render
from backend.Controller import Controller
from transaction.services import TransactionManager, CategoryManager
from history.services import TransactionCRUD
from datetime import datetime
from django.http import JsonResponse
import json

controller = Controller()
transaction_crud = TransactionCRUD()
transaction_manager = controller.getTransactionManager()
category_manager = controller.getCategoryManager()
notification_manager = controller.getNotificationManager()

def index(request):
    categories = category_manager.fetchAllCategories()
    context = {
        "categories": categories
    }
    return render(request, 'pages/transaction/transaction.html', context)

def log_transaction(request):
    data = json.loads(request.body)
    amount = int(data.get('amount'))
    category_name = data.get('category_name')
    log_date = datetime.strptime(data.get('log_date'), '%Y-%m-%d').date()
    description = data.get('description')
    note = data.get('note')  

    transaction_obj = transaction_crud.createDataObject(
        id=None,
        amount=amount,
        cycle_id=None,
        category_name=category_name,
        log_date=log_date,
        description=description,
        note=note
    )
    
    transaction_manager.logTransaction(transaction_obj)
    state = notification_manager.getCurrentState()
    return JsonResponse({'success': True, 'state': state})

def update_transaction(request):
    data = json.loads(request.body)
    id = int(data.get('id', None))
    amount = int(data.get('amount'))
    category_name = data.get('category_name')
    log_date = datetime.strptime(data.get('log_date'), '%Y-%m-%d').date()
    description = data.get('description')
    note = data.get('note')  

    transaction_obj = transaction_crud.createDataObject(
        id=id,
        amount=amount,
        cycle_id=None,
        category_name=category_name,
        log_date=log_date,
        description=description,
        note=note
    )
    
    transaction_manager.updateTransaction(transaction_obj)
    state = notification_manager.getCurrentState()
    return JsonResponse({'success': True, 'state': state})

def delete_transaction(request, id):
    transaction_manager.deleteTransaction(id)
    state = notification_manager.getCurrentState()
    return JsonResponse({'success': True, 'state': state})
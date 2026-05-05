from django.shortcuts import render
from transaction.services import TransactionManager, CategoryManager
from history.services import TransactionCRUD
from datetime import datetime
from django.http import JsonResponse

transaction_crud = TransactionCRUD()
transaction_manager = TransactionManager()
category_manager = CategoryManager()

def index(request):
    categories = category_manager.fetchAllCategories()
    context = {
        "categories": categories
    }
    return render(request, 'pages/transaction/transaction.html', context)

def log_transaction(request):
    amount = int(request.POST.get('amount'))
    category_name = request.POST.get('category_name')
    log_date = datetime.strptime(request.POST.get('log_date'), '%Y-%m-%d').date()
    description = request.POST.get('description')
    note = request.POST.get('note')    

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
    return JsonResponse({'success': True})

def update_transaction(request):
    id=int(request.POST.get('id', None))
    amount = int(request.POST.get('amount'))
    category_name = request.POST.get('category_name')
    log_date = datetime.strptime(request.POST.get('log_date'), '%Y-%m-%d').date()
    description = request.POST.get('description')
    note = request.POST.get('note')    

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
    return JsonResponse({'success': True})

def delete_transaction(request, id):
    transaction_manager.deleteTransaction(id)
    return JsonResponse({'success': True})
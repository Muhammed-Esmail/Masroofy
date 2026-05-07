from django.shortcuts import render
from backend.Controller import Controller
from history.services import HistoryManager
from django.http import HttpResponse, JsonResponse
from transaction.services import CategoryManager
from userSettings.services.SettingsManager import SettingsManager

controller: Controller = Controller()
historyManager: HistoryManager = controller.getHistoryManager()
categoryManager: CategoryManager = controller.getCategoryManager()

def index(request):
    categories = categoryManager.fetchAllCategories()
    context = {
        "categories": categories,
        'settings': SettingsManager().fetchSettings(),
    }
    return render(request, 'pages/history/history.html', context)

def serializeTransaction(data):
    serialized = [
        {
            "id": t.id,
            "amount": t.amount,
            "cycle_id": t.cycle_id,
            "category_name": t.category_name,
            "log_date": str(t.log_date),
            "description": t.description,
            "note": t.note,
        }
        for t in data
    ]
    return serialized

def seralizeCycle(data):
    return {
        "id": data.id,  
        "startDate": data.startDate,
        "endDate": data.endDate,
        "amount": data.amount
    }

def full_history(request):
    data = historyManager.fetchFullHistory()
    return JsonResponse(serializeTransaction(data), safe=False)
    
def filtered_history(request):
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    category_name = request.GET.get('category_name')
    cycle_id = request.GET.get('cycle_id')
    data = historyManager.fetchTransactionData(start_date, end_date, category_name, cycle_id)
    return JsonResponse(serializeTransaction(data), safe=False)

def fetch_cycle_data(request):
    cycle_id = request.GET.get('id')
    data = historyManager.fetchCycleData(cycle_id)
    return JsonResponse(seralizeCycle(data), safe=False)

def get_total_spent(request):
    data = historyManager.getTotalSpentInActiveCycle()
    return HttpResponse(data)

def get_active_cycle_id(reqeust):
    data = historyManager.getActiveCycleID()
    return HttpResponse(data)
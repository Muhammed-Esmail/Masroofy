from django.shortcuts import render
from backend.Controller import Controller
from history.services import HistoryManager
from django.http import HttpResponse

controller: Controller = Controller()
historyManager: HistoryManager = controller.getHistoryManager()

def index(request):
    return render(request, 'pages/history/history.html')

def full_history(request):
    data = historyManager.fetchFullHistory()
    return HttpResponse(data)
    
def filtered_history(request):
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')
    category_id = request.GET.get('category_id')
    cycle_id = request.GET.get('cycle_id')
    
    data = historyManager.fetchTransactionData(start_date, end_date, category_id, cycle_id)
    return HttpResponse(data)

def fetch_cycle_data(request):
    cycle_id = request.GET.get('id')
    data = historyManager.fetchCycleData(cycle_id)
    return HttpResponse(data)

def get_total_spent(request):
    data = historyManager.getTotalSpentInActiveCycle()
    return HttpResponse(data)

def get_active_cycle_id(reqeust):
    data = historyManager.getActiveCycleID()
    return HttpResponse(data)
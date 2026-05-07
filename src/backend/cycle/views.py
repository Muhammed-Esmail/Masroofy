from django.shortcuts import redirect, render
from django.http import HttpResponse
import json

from cycle.services.AllowanceManager import AllowanceManager
from backend.shared_classes.Cycle import Cycle

# Create your views here.
def index(request):
    return render(request, 'pages/onboarding/welcome.html')

def startCycle(request):
    if request.method == 'POST':
        
        amount = request.POST.get('amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        newCycle = Cycle(-1, start_date, end_date, amount)
        allowance_manager = AllowanceManager()
        allowance_manager.initializeCycle(newCycle)

        
        return redirect('/dashboard/')
    
    return HttpResponse('Invalid Method', status=405)

def resetCycle(request):
    if request.method == 'POST': 
        allowanceManager = AllowanceManager()
        allowanceManager.resetCycle()
        return redirect('/dashboard/')
    return HttpResponse('Invalid Method', status=405)
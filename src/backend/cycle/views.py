from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from userSettings.services.SettingsManager import SettingsManager
from django.http import HttpResponse
from cycle.services.AllowanceManager import AllowanceManager
from backend.shared_classes.Cycle import Cycle
from django.http import JsonResponse
import json

@csrf_exempt
# Create your views here.
def index(request):
    context={
        'settings':SettingsManager().fetchSettings()
    }
    return render(request, 'pages/onboarding/welcome.html', context)

@csrf_exempt
def startCycle(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        amount = data.get('amount')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        print(f'[Start Cycle] {start_date}')
        print(f'[Start Cycle] {end_date}')

        if start_date > end_date:
            return JsonResponse({'success' : False, 'description': 'Start date can not exceed end date'}, status=400)

        newCycle = Cycle(-1, start_date, end_date, amount)
        allowance_manager = AllowanceManager()
        allowance_manager.initializeCycle(newCycle)

        
        return JsonResponse({'success' : True, 'description': 'Successfylly created cycle', 'data':'/dashboard/'})
    
    return JsonResponse({'success' : False, 'description': 'Invalid Method'}, status=405)

def resetCycle(request):
    if request.method == 'POST': 
        allowanceManager = AllowanceManager()
        allowanceManager.resetCycle()
        return redirect('/dashboard/')
    return HttpResponse('Invalid Method', status=405)
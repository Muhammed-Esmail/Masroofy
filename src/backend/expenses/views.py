from django.shortcuts import render, redirect, get_object_or_404
from .models import PeriodicExpense
from userSettings.services.SettingsManager import SettingsManager

# 1. READ
def index(request):
    expenses = PeriodicExpense.objects.all().order_by('-created_at')
    context = {
        "expenses": expenses,
        'settings':SettingsManager().fetchSettings()
    }
    return render(request, 'pages/expenses/expenses.html', context)

# 2. CREATE
def create_expense(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        frequency = request.POST.get('frequency')
        
        if frequency == 'MONTHLY':
            days_of_month = [int(day) for day in request.POST.getlist('monthly_days_input')]
            days_of_week = []
        else:
            days_of_month = []
            days_of_week = request.POST.getlist('weekly_days_input')

        PeriodicExpense.objects.create(
            name=name,
            amount=amount,
            frequency=frequency,
            days_of_month=days_of_month,
            days_of_week=days_of_week
        )
        
        return redirect('expense-list')

def update_expense(request, id):
    expense = get_object_or_404(PeriodicExpense, id=id)
    
    if request.method == "POST":
        expense.name = request.POST.get('name')
        expense.amount = request.POST.get('amount')
        expense.frequency = request.POST.get('frequency')
        
        if expense.frequency == 'MONTHLY':
            expense.days_of_month = [int(day) for day in request.POST.getlist('monthly_days_input')]
            expense.days_of_week = []
        else:
            expense.days_of_month = []
            expense.days_of_week = request.POST.getlist('weekly_days_input')
            
        expense.save()
        return redirect('expense-list')
    context={
        'settings':SettingsManager().fetchSettings(),
        'expense': expense,
    }
    return render(request, 'pages/expenses/edit_expense.html', context)

def delete_expense(request, id):
    if request.method == "POST":
        expense = get_object_or_404(PeriodicExpense, id=id)
        expense.delete()
        return redirect('expense-list')
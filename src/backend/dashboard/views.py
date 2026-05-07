from django.shortcuts import render, redirect
from backend.Controller import Controller
from datetime import date
from cycle.services.AllowanceManager import AllowanceManager, NoCycleException

# Create your views here.
def home(request):
    controller = Controller()

    try:
        cycle = controller.getAllowanceManager().getCurrentCycle()
    except NoCycleException:
        return redirect('/cycle/')

    historyManager = controller.getHistoryManager();

    transactions = historyManager.fetchFullHistory(currentOnly=True)
    expenses = controller.getExpenseManager().getAllExpenses()
    categoryNames = controller.getCategoryManager().fetchAllCategories()
    totalSpent = historyManager.getTotalSpentInActiveCycle()
    cycleRemaining = cycle.amount - totalSpent 
    recentTransactions = sorted(transactions, key=lambda t : t.log_date, reverse = True)[:5]
    today = date.today()

    dailyLimit = controller.getDailyLimitCalculator().calculateDailyLimit(today, transactions, cycle, expenses)
    todaySpent = sum(t.amount for t in transactions if t.log_date == today)
    dailyRemaining = max(0, dailyLimit - todaySpent)
    categoryBreakdown = [
        {
            'name': name,
            'spent': sum(t.amount for t in transactions if t.category_name == name)
        }
        for name in categoryNames
    ]

    context={
        'cycle': cycle,
        'dailyLimit': dailyLimit,
        'dailyRemaining': dailyRemaining,
        'totalSpent': totalSpent,
        'cycleRemaining': cycleRemaining,
        'recentTransactions': recentTransactions,
        'categoryBreakdown': categoryBreakdown,
    }
    context['title'] = 'Dashboard'
    return render(request, 'pages/dashboard/dashboard.html',context)


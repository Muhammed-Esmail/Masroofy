from django.shortcuts import render, redirect
from backend.Controller import Controller
from datetime import date
from cycle.services.AllowanceManager import NoCycleException
from userSettings.services.SettingsManager import SettingsManager
import json
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def home(request):
    controller = Controller()

    try:
        cycle = controller.getAllowanceManager().getCurrentCycle()
    except NoCycleException:
        return redirect('/cycle/')

    historyManager = controller.getHistoryManager()

    transactions = historyManager.fetchFullHistory(currentOnly=True)
    expenses = controller.getExpenseManager().getAllExpenses()
    categoryNames = controller.getCategoryManager().fetchAllCategories()
    totalSpent = historyManager.getTotalSpentInActiveCycle()
    cycleRemaining = max(0, cycle.amount - totalSpent)
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

    insightsEngine = controller.insightsEngine
    pieData = json.dumps(insightsEngine.generate_chart('pie', transactions, cycle.amount))
    donutData = json.dumps(insightsEngine.generate_chart('donut', transactions, cycle.amount))
    graphData = json.dumps(insightsEngine.generate_chart('graph', transactions, cycle.amount))

    context={
        'cycle': cycle,
        'dailyLimit': dailyLimit,
        'dailyRemaining': dailyRemaining,
        'totalSpent': totalSpent,
        'cycleRemaining': cycleRemaining,
        'recentTransactions': recentTransactions,
        'categoryBreakdown': categoryBreakdown,

        'pieData': pieData,
        'donutData': donutData,
        'graphData': graphData,
        'settings':SettingsManager().fetchSettings(),
    }
    context['title'] = 'Dashboard'
    return render(request, 'pages/dashboard/dashboard.html',context)


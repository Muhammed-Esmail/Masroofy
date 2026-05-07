from __future__ import annotations 
from typing import Any

from transaction.services import CategoryManager, NotificationManager
from transaction.services import TransactionManager as _TransactionManager 
from history.services import HistoryManager as _HistoryManager
from cycle.services.AllowanceManager import AllowanceManager as _AllowanceManager
from insights.services.InsightsEngine import InsightsEngine 
from dashboard.services import SettingsManager
from dashboard.services.DailyLimitCalculator import DailyLimitCalculator
from expenses.services.expenseManager import ExpenseManager
from userSettings.services import SettingsManager

class Controller:
    _instance = None

    historyManager : _HistoryManager
    allowanceManager: _AllowanceManager
    dailyLimitCalculator: DailyLimitCalculator
    insightsEngine: Any
    categoryManager: CategoryManager
    securityManager: Any
    transactionManager: _TransactionManager
    notificationManager: NotificationManager
    settingsManager: SettingsManager
    expenseManager : ExpenseManager

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.historyManager = _HistoryManager()
        self.allowanceManager = _AllowanceManager()
        self.dailyLimitCalculator = DailyLimitCalculator()
        self.insightsEngine = InsightsEngine()       
        self.categoryManager = CategoryManager()
        self.securityManager = None       # replace with actual class
        self.transactionManager = _TransactionManager()
        self.notificationManager = NotificationManager()
        self.settingsManager = SettingsManager()
        self.expenseManager = ExpenseManager()
        

        self.allowanceManager.setController(self)
        self.transactionManager.setController(self)
        self.notificationManager.setController(self)
        self.transactionManager.subscribe(self.notificationManager)

    def getHistoryManager(self):
        return self.historyManager
    
    def getAllowanceManager(self):
        return self.allowanceManager
    
    def getCategoryManager(self):
        return self.categoryManager
    
    def getTransactionManager(self):
        return self.transactionManager
    
    def getNotificationManager(self):
        return self.notificationManager
    
    def getSettingsManager(self):
        return self.settingsManager
    
    def getExpenseManager(self):
        return self.expenseManager
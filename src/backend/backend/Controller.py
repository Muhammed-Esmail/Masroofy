from __future__ import annotations 
from typing import Any

from transaction.services import CategoryManager, NotificationManager
from transaction.services import TransactionManager as _TransactionManager 
from history.services import HistoryManager as _HistoryManager
from cycle.services.AllowanceManager import AllowanceManager as _AllowanceManager
from insights.services import InsightsEngine 
from dashboard.services import DailyLimitCalculator
from expenses.services import ExpenseManager
from userSettings.services import SettingsManager

class Controller:
    """
    A Singleton Controller that acts as the central hub for financial service management.

    This class orchestrates the interaction between various managers (History, 
    Allowance, Transactions, etc.) and ensures that only one instance of the 
    controller exists throughout the application lifecycle.

    Attributes:
        historyManager (_HistoryManager): Handles record-keeping of past actions.
        allowanceManager (_AllowanceManager): Manages budget cycles and limits.
        dailyLimitCalculator (DailyLimitCalculator): Logic for calculating spending caps.
        categoryManager (CategoryManager): Manages transaction classification.
        securityManager (Any): Placeholder for authentication/authorization logic.
        transactionManager (_TransactionManager): Core logic for processing transactions.
        notificationManager (NotificationManager): Handles user alerts and system messages.
        settingsManager (SettingsManager): Manages user preferences and configurations.
        expenseManager (ExpenseManager): Specialized logic for tracking user expenses.
    """
    _instance = None

    historyManager : _HistoryManager
    allowanceManager: _AllowanceManager
    dailyLimitCalculator: DailyLimitCalculator
    categoryManager: CategoryManager
    transactionManager: _TransactionManager
    notificationManager: NotificationManager
    settingsManager: SettingsManager
    expenseManager : ExpenseManager

    def __new__(cls):
        """
        Implements the Singleton pattern to ensure only one Controller exists.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Internal method to instantiate all sub-managers and establish 
        cross-service dependencies.
        """
        self.historyManager = _HistoryManager()
        self.allowanceManager = _AllowanceManager()
        self.dailyLimitCalculator = DailyLimitCalculator()
        self.categoryManager = CategoryManager()
        self.transactionManager = _TransactionManager()
        self.notificationManager = NotificationManager()
        self.settingsManager = SettingsManager()
        self.expenseManager = ExpenseManager()
        
        # Link managers back to the controller for circular coordination
        self.allowanceManager.setController(self)
        self.transactionManager.setController(self)
        self.notificationManager.setController(self)
        
        # Setup Observer Pattern for notifications
        self.transactionManager.subscribe(self.notificationManager)

    def getHistoryManager(self) -> _HistoryManager:
        """Returns the instance of the HistoryManager."""
        return self.historyManager
    
    def getAllowanceManager(self) -> _AllowanceManager:
        """Returns the instance of the AllowanceManager."""
        return self.allowanceManager
    
    def getCategoryManager(self) -> CategoryManager:
        """Returns the instance of the CategoryManager."""
        return self.categoryManager
    
    def getTransactionManager(self) -> _TransactionManager:
        """Returns the instance of the TransactionManager."""
        return self.transactionManager
    
    def getNotificationManager(self) -> NotificationManager:
        """Returns the instance of the NotificationManager."""
        return self.notificationManager
    
    def getSettingsManager(self) -> SettingsManager:
        """Returns the instance of the SettingsManager."""
        return self.settingsManager
    
    def getExpenseManager(self) -> ExpenseManager:
        """Returns the instance of the ExpenseManager."""
        return self.expenseManager
    
    def getDailyLimitCalculator(self) -> DailyLimitCalculator:
        """Returns the instance of the DailyLimitCalculator"""
        return self.dailyLimitCalculator
from __future__ import annotations 
from typing import Any

from history.services.HistoryManager import HistoryManager as _HistoryManager
from cycle.services.AllowanceManager import AllowanceManager as _AllowanceManager


class Controller:
    _instance = None

    historyManager : _HistoryManager
    allowanceManager: _AllowanceManager
    dailyLimitCalculator: Any
    insightsEngine: Any
    categoryManager: Any
    securityManager: Any

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.historyManager = _HistoryManager()
        self.allowanceManager = _AllowanceManager()
        self.dailyLimitCalculator = None  # replace with actual class
        self.insightsEngine = None        # replace with actual class
        self.categoryManager = None       # replace with actual class
        self.securityManager = None       # replace with actual class

        self.allowanceManager.setController(self)

    def getHistoryManager(self):
        return self.historyManager
    
    def getAllowanceManager(self):
        return self.allowanceManager
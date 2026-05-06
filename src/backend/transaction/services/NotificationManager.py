from typing import override
from history.services import HistoryManager
from transaction.interfaces import Observer
from transaction.constants import BUDGET_THRESHOLD_ALERT, BUDGET_EXHAUSTED_ALERT

class NotificationManager(Observer):
    _instance = None
    _state = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.controller = None
        self.historyManager: HistoryManager = None
            
    def setController(self, controller):
        self.controller = controller
        self.historyManager = self.controller.getHistoryManager()
        
    def getCurrentState(self):
        return self._state
    
    def triggerBudgetAlert(self, message: str):
        self._state = message
        
    @override
    def update(self):
        active_cycle = self.historyManager.getActiveCycle()
        if active_cycle:
            total = active_cycle.amount
            total_spent = self.historyManager.getTotalSpentInActiveCycle()
            if (total_spent >= total):
                self.triggerBudgetAlert(BUDGET_EXHAUSTED_ALERT)
            elif (total_spent/total >= 0.8):
                self.triggerBudgetAlert(BUDGET_THRESHOLD_ALERT)
            else:
                self.triggerBudgetAlert(None)
from typing import override, Optional
from history.services import HistoryManager
from transaction.interfaces import Observer
from transaction.constants import BUDGET_THRESHOLD_ALERT, BUDGET_EXHAUSTED_ALERT

class NotificationManager(Observer):
    """
    A service that monitors financial thresholds and manages alert states.

    As a concrete Observer, this manager reacts to changes in the transaction 
    subsystem. It calculates the current budget usage and sets alert states 
    when spending crosses predefined thresholds.

    Attributes:
        _state (str | None): The current active alert message.
        controller (Controller): Reference to the central mediator.
        historyManager (HistoryManager): Manager used to retrieve cycle and spending data.
    """
    _instance = None
    _state = None
    
    def __new__(cls):
        """Ensures a Singleton instance of NotificationManager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initializes the manager with empty dependencies."""
        self.controller = None
        self.historyManager: HistoryManager = None
            
    def setController(self, controller) -> None:
        """
        Injects the controller and extracts necessary service dependencies.

        Args:
            controller (Controller): The central application controller.
        """
        self.controller = controller
        self.historyManager = self.controller.getHistoryManager()
        
    def getCurrentState(self) -> Optional[str]:
        """
        Retrieves the current alert state.

        Returns:
            Optional[str]: The current budget alert message, or None if no 
                           threshold has been crossed.
        """
        return self._state
    
    def triggerBudgetAlert(self, message: str) -> None:
        """
        Updates the internal state with a specific alert message.

        Args:
            message (str): The alert message to set as the active state.
        """
        self._state = message
        
    @override
    def update(self) -> None:
        """
        Evaluates current spending against the active budget cycle.

        This method is called by the Subject (TransactionManager) whenever 
        transactions change. It calculates the consumption percentage and 
        triggers alerts based on the following logic:
        - 100% or more: BUDGET_EXHAUSTED_ALERT
        - 80% to 99%: BUDGET_THRESHOLD_ALERT
        - Less than 80%: Clears the alert (None)
        """
        active_cycle = self.historyManager.getActiveCycle()
        if active_cycle:
            total = active_cycle.amount
            total_spent = self.historyManager.getTotalSpentInActiveCycle()
            
            # Logic for threshold evaluation
            if (total_spent >= total):
                self.triggerBudgetAlert(BUDGET_EXHAUSTED_ALERT)
            elif (total_spent / total >= 0.8):
                self.triggerBudgetAlert(BUDGET_THRESHOLD_ALERT)
            else:
                self.triggerBudgetAlert(None)
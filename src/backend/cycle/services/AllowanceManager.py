from __future__ import annotations 
from typing import TYPE_CHECKING

from backend.shared_classes import Cycle

if TYPE_CHECKING:
    from backend.Controller import Controller

class NoCycleException(Exception):
    pass

class AllowanceManager:
    _instance = None
    _controller: Controller = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def setController(self, controller: Controller):
        self._controller = controller

    def initializeCycle(self, newCycle: Cycle) -> None:
        '''
        Creates a new cycle given new cycle data.
        '''
        self.resetCycle()

        newCycleID = self._controller.getHistoryManager().createNewCycle(newCycle)

        self._controller.getHistoryManager().setActive(newCycleID)

    def resetCycle(self) -> None:
        '''
        Sets the current cycle (if exists) to inactive.
        '''
        if not self.checkActivityStatus():
            return

        self._controller.getHistoryManager().clearActive()
    

    def getCurrentCycle(self) -> Cycle:
        '''
        Returns a Cycle object of the current active cycle.
        '''
        historyManager = self._controller.getHistoryManager()

        currentCycle  = historyManager.getActiveCycle()

        if currentCycle is None:
            raise NoCycleException("[Allowance Manager] No active Cycle!")

        return currentCycle
        
    def checkActivityStatus(self) -> bool:
        '''
        Checks if there's a current active cycle set.
        
        Returns: boolean
        ''' 
        try: 
            self.getCurrentCycle()
            return True
        
        except NoCycleException:
            return False
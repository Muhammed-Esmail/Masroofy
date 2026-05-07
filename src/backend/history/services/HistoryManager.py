from typing import Optional
from datetime import date

from backend.shared_classes import Cycle
from history.services import TransactionCRUD, CycleCRUD
from cycle.models import CycleModel

class NoActiveCycle(Exception):
    """Exception raised when an operation requires an active cycle, but none is set."""
    pass

class HistoryManager:
    """
    A Facade service that orchestrates cycle and transaction data retrieval.

    HistoryManager provides a high-level API for the rest of the application to 
    interact with historical data, shielding them from the underlying complexities 
    of the specific CRUD services.

    Attributes:
        transaction_queryable (TransactionCRUD): Service for transaction data access.
        cycle_readable (CycleCRUD): Service for cycle data access and state management.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensures a Singleton instance of HistoryManager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    transaction_queryable: TransactionCRUD
    cycle_readable: CycleCRUD

    def __init__(self):
        """Initializes the manager and connects the required service layers."""
        self.transaction_queryable = TransactionCRUD()
        self.cycle_readable = CycleCRUD()

    def fetchCycleData(self, cycle_id: int):
        """
        Retrieves details for a specific cycle.

        Args:
            cycle_id (int): The unique identifier of the cycle.

        Returns:
            Cycle: The cycle data object.
        """
        return self.cycle_readable.fetchById(cycle_id)
    
    def fetchTransactionData(self, startDate: date, endDate: date, category_name: str, cycle_id: int):
        """
        Retrieves transactions based on multiple filtering criteria.

        Args:
            startDate (date): Lower bound for transaction date.
            endDate (date): Upper bound for transaction date.
            category_name (str): Category filter.
            cycle_id (int): Cycle filter.

        Returns:
            list[Transaction]: A list of transactions matching the criteria.
        """
        return self.transaction_queryable.fetchByFilters(startDate, endDate, category_name, cycle_id)
    
    def fetchFullHistory(self, currentOnly: bool = False):
        """
        Retrieves transaction history, optionally restricted to the active cycle.

        Args:
            currentOnly (bool): If True, only fetches transactions for the active cycle. 
                               Defaults to False (all history).

        Returns:
            list[Transaction]: The requested transaction history.

        Raises:
            NoActiveCycle: If currentOnly is True but no cycle is active.
        """
        activeCycleID = self.getActiveCycleID()
        if activeCycleID is None:
            raise NoActiveCycle("[History Manager] No Active Cycle!")
        if currentOnly:
            return self.transaction_queryable.fetchByFilters(cycle_id=activeCycleID)
        else:
            return self.transaction_queryable.fetchByFilters()

    def createNewCycle(self, newCycle: CycleModel) -> int:
        """
        Registers a new budget cycle.

        Args:
            newCycle (CycleModel): The model data for the new cycle.

        Returns:
            int: The ID of the newly created cycle.
        """
        return self.cycle_readable.create(newCycle)

    def getActiveCycle(self) -> Optional[Cycle]:
        """
        Returns the currently active Cycle data object.

        Returns:
            Optional[Cycle]: The active cycle, or None if no cycle is set.
        """
        return self.cycle_readable.fetchActive()

    def getActiveCycleID(self) -> Optional[int]:
        """
        A helper to quickly retrieve the ID of the active cycle.

        Returns:
            Optional[int]: The cycle ID, or None if no cycle is active.
        """
        currentCycle = self.getActiveCycle()
        if currentCycle:
            return currentCycle.id
        return None
    
    def getTotalSpentInActiveCycle(self) -> Optional[int]:
        """
        Aggregates spending for the current active cycle.

        Returns:
            Optional[int]: The total sum spent, or 0 if no cycle is active 
                           or no transactions exist.
        """
        currentCycleId = self.getActiveCycleID()
        if currentCycleId:
            return self.transaction_queryable.getTotalSpentInCycle(currentCycleId)
        return 0

    def setActive(self, id: int) -> None:
        """
        Sets a specific cycle as the active one in the system.

        Args:
            id (int): The ID of the cycle to activate.
        """
        self.cycle_readable.setActive(id)

    def clearActive(self) -> None:
        """Removes the active status from any currently active cycle."""
        self.cycle_readable.clearActive()

    def updateCycleData(self, cycleID: int, newData: CycleModel) -> None:
        """
        Updates the parameters of an existing cycle.

        Args:
            cycleID (int): The ID of the cycle to update.
            newData (CycleModel): The new data values to persist.
        """
        self.cycle_readable.update(cycleID, newData)
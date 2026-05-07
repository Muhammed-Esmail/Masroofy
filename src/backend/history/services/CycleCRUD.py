from typing import Optional
from datetime import date

from history.interfaces import Fetchable, CRUD
from backend.shared_classes import Cycle
from cycle.models import ActiveCycleModel, CycleModel

class CycleCRUD(Fetchable[Cycle], CRUD[Cycle]):
    """
    A service class for managing Cycle entities and the currently active cycle state.

    This class provides standard CRUD operations for CycleModel and manages a 
    single 'active' cycle pointer using ActiveCycleModel.
    """

    def fetchById(self, id: int) -> Cycle:
        """
        Retrieves a specific cycle by its database ID.

        Args:
            id (int): The unique identifier of the cycle.

        Returns:
            Cycle: A data object representing the retrieved cycle.
            
        Raises:
            CycleModel.DoesNotExist: If no cycle matches the provided ID.
        """
        cycle = CycleModel.objects.get(id=id)
        return self.createDataObject(cycle.id, cycle.startDate, cycle.endDate, cycle.amount)

    def create(self, newCycle: Cycle) -> int:
        """
        Persists a new cycle record to the database.

        Args:
            newCycle (Cycle): The cycle data object containing start/end dates and amount.

        Returns:
            int: The ID of the newly created cycle record.
        """
        obj = CycleModel.objects.create(
            startDate=newCycle.startDate,
            endDate=newCycle.endDate,
            amount=newCycle.amount
        )
        return obj.id

    def update(self, id: int, newCycle: Cycle) -> bool:
        """
        Updates an existing cycle record with new data.

        Args:
            id (int): The ID of the cycle to update.
            newCycle (Cycle): The new data to apply.

        Returns:
            bool: True if the update operation was executed.
        """
        CycleModel.objects.filter(id=id).update(
            startDate=newCycle.startDate,
            endDate=newCycle.endDate,
            amount=newCycle.amount
        )
        return True

    def delete(self, id: int) -> bool:
        """
        Deletes a specific cycle record.

        Args:
            id (int): The ID of the cycle to remove.

        Returns:
            bool: True after the deletion attempt.
        """
        CycleModel.objects.filter(id=id).delete()
        return True

    def createDataObject(self, id: int, startDate: date, endDate: date, amount: int) -> Cycle:
        """
        Factory method to convert database values into a Cycle business object.

        Args:
            id (int): Database primary key.
            startDate (date): The start date of the cycle.
            endDate (date): The end date of the cycle.
            amount (int): The total allowance/budget for this cycle.

        Returns:
            Cycle: A populated Cycle data object.
        """
        return Cycle(
            id=id,
            startDate=startDate,
            endDate=endDate,
            amount=amount
        )
    
    def fetchActive(self) -> Optional[Cycle]:
        """
        Retrieves the cycle currently marked as 'active' in the system.

        Returns:
            Optional[Cycle]: The active Cycle object, or None if no cycle 
            is currently active.
        """
        record = ActiveCycleModel.objects.select_related('cycle').first()
        if record is None:
            return None
        c = record.cycle
        return self.createDataObject(c.id, c.startDate, c.endDate, c.amount)

    def setActive(self, cycle_id: int) -> None:
        """
        Sets a specific cycle as the active one.
        
        This method clears any existing active cycle before setting the new one,
        ensuring only one cycle is active at a time.

        Args:
            cycle_id (int): The ID of the cycle to mark as active.
        """
        ActiveCycleModel.objects.all().delete()
        ActiveCycleModel.objects.create(cycle_id=cycle_id)

    def clearActive(self) -> None:
        """
        Removes the active status from all cycles.
        """
        ActiveCycleModel.objects.all().delete()
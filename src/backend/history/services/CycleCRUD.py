from typing import Optional

from history.interfaces import Fetchable, CRUD
from backend.shared_classes import Cycle
from cycle.models import ActiveCycleModel, CycleModel
from datetime import date

class CycleCRUD(Fetchable[Cycle], CRUD[Cycle]):
    def fetchById(self, id) -> Cycle:
        cycle = CycleModel.objects.get(id=id)
        return self.createDataObject(cycle.id, cycle.startDate, cycle.endDate, cycle.amount)

    def create(self, newCycle: Cycle) -> int:
        obj = CycleModel.objects.create(
            startDate=newCycle.startDate,
            endDate=newCycle.endDate,
            amount=newCycle.amount
        )
        return obj.id

    def update(self, id: int, newCycle: Cycle):
        CycleModel.objects.filter(id=id).update(
            startDate=newCycle.startDate,
            endDate=newCycle.endDate,
            amount=newCycle.amount
        )
        return True

    def delete(self, id: int):
        CycleModel.objects.filter(id=id).delete()
        return True

    def createDataObject(self, id: int, startDate: date, endDate: date,  amount: int):
        return Cycle(
            id=id,
            startDate=startDate,
            endDate=endDate,
            amount=amount
        )
    
    def fetchActive(self) -> Optional[Cycle]:
        record = ActiveCycleModel.objects.select_related('cycle').first()
        if record is None:
            return None
        c = record.cycle
        return self.createDataObject(c.id, c.startDate, c.endDate, c.amount)

    def setActive(self, cycle_id: int) -> None:
        ActiveCycleModel.objects.all().delete()
        ActiveCycleModel.objects.create(cycle_id=cycle_id)

    def clearActive(self) -> None:
        ActiveCycleModel.objects.all().delete()
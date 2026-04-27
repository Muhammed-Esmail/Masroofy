from history.interfaces import Fetchable, CRUD
from backend.shared_classes import Cycle
from cycle.models import CycleModel
from datetime import date

class CycleCRUD(Fetchable[Cycle], CRUD[Cycle]):
    def fetchById(self, id):
        cycle = CycleModel.objects.get(id=id)
        return Cycle(
            id=cycle.id,
            startDate=cycle.startDate,
            endDate=cycle.endDate,
            amount=cycle.amount
        )

    def create(self, newCycle: Cycle):
        CycleModel.objects.create(
            startDate=newCycle.startDate,
            endDate=newCycle.endDate,
            amount=newCycle.amount
        )
        return True

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

    def createDataObject(self, id: int, amount: int, startDate: date, endDate: date, description: str, note: str | None):
        return Cycle(
            id=id,
            startDate=startDate,
            endDate=endDate,
            amount=amount
        )
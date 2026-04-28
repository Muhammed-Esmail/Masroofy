from typing import Optional

from history.interfaces import Fetchable, Queryable, CRUD
from backend.shared_classes import Transaction
from transaction.models import TransactionModel
from datetime import date

class TransactionCRUD(Fetchable[Transaction], Queryable[Transaction], CRUD[Transaction]):
    def fetchById(self, id: int) -> Transaction:
        transaction = TransactionModel.objects.get(id=id)
        return self.createDataObject(transaction.id,
                                     transaction.amount,
                                     transaction.cycle_id,
                                     transaction.category_id,
                                     transaction.log_date,
                                     transaction.description,
                                     transaction.note)

    def fetchByFilters(self, startDate: Optional[date] = None, endDate: Optional[date] = None, category_id: Optional[int] = None) -> list[Transaction]:
        transactions = TransactionModel.objects.all()
        if startDate:
            transactions = transactions.filter(log_date__gte=startDate)

        if endDate:
            transactions = transactions.filter(log_date__lte=endDate)

        if category_id:
            transactions = transactions.filter(category_id=category_id)

        return [self.createDataObject(t.id,
                                     t.amount,
                                     t.cycle_id,
                                     t.category_id,
                                     t.log_date,
                                     t.description,
                                     t.note)
                                    for t in transactions
        ]
    
    def create(self, newTransaction: Transaction):
        TransactionModel.objects.create(
            amount=newTransaction.amount,
            cycle_id=newTransaction.cycle_id,
            category_id=newTransaction.category_id,
            log_date=newTransaction.log_date,
            description=newTransaction.description,
            note=newTransaction.note
        )
        return True

    def update(self, id: int, newTransaction: Transaction):
        TransactionModel.objects.filter(id=id).update(
            amount=newTransaction.amount,
            cycle_id=newTransaction.cycle_id,
            category_id=newTransaction.category_id,
            log_date=newTransaction.log_date,
            description=newTransaction.description,
            note=newTransaction.note
        )
        return True

    def delete(self, id: int):
        TransactionModel.objects.filter(id=id).delete()
        return True
    

    def createDataObject(self, id: int, amount: int, cycle_id: int, category_id: int, log_date: date, description: str, note: str | None):
        return Transaction(
            id=id,
            amount=amount,
            cycle_id=cycle_id,
            category_id=category_id,
            log_date=log_date,
            description=description,
            note=note
        )
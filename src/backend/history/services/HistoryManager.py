from services import TransactionCRUD, CycleCRUD
from shared_classes import Category
from datetime import date

class HistoryManager:
    transaction_queryable: TransactionCRUD
    cycle_readable: CycleCRUD

    def __init__(self):
        self.transaction_queryable = TransactionCRUD()
        self.cycle_readable = CycleCRUD()

    def fetchCycleData(self, cycle_id: int):
        return self.cycle_readable.fetchById(cycle_id)
    
    def fetchTransactionData(self, startDate: date, endDate: date, category: Category):
        return self.transaction_queryable.fetchByFilters(startDate, endDate, category)
    
    def fetchFullHistory(self):
        return self.transaction_queryable.fetchByFilters()

from history.services import TransactionCRUD, CycleCRUD
from datetime import date

class HistoryManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    

    transaction_queryable: TransactionCRUD
    cycle_readable: CycleCRUD

    def __init__(self):
        self.transaction_queryable = TransactionCRUD()
        self.cycle_readable = CycleCRUD()

    def fetchCycleData(self, cycle_id: int):
        return self.cycle_readable.fetchById(cycle_id)
    
    def fetchTransactionData(self, startDate: date, endDate: date, category_id: int):
        return self.transaction_queryable.fetchByFilters(startDate, endDate, category_id)
    
    def fetchFullHistory(self):
        return self.transaction_queryable.fetchByFilters()

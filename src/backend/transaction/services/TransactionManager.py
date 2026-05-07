from __future__ import annotations 
from typing import TYPE_CHECKING

from history.services import TransactionCRUD, HistoryManager
from backend.shared_classes import Transaction
from transaction.interfaces import Observer

if TYPE_CHECKING:
    from backend.Controller import Controller


class TransactionManager:
    _instance = None
    _controller: Controller = None
    _transCRUD: TransactionCRUD = None
    _historyManager: HistoryManager = None
    
    def __init__(self):
        if not hasattr(self, 'observers'):
            self.observers = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def setController(self, controller: Controller):
        self._controller = controller
        self._historyManager = self._controller.getHistoryManager()
        self._transCRUD = self._historyManager.transaction_queryable
        
    def subscribe(self, observer: Observer):
        self.observers.append(observer)
        
    def unsubscribe(self, observer: Observer):
        self.observers.remove(observer)
        
    def notify(self):
        for observer in self.observers:
            observer.update()


    def logTransaction(self, transaction: Transaction) -> None:
        '''
        Simply adds the given transaction object as new row in DB.
        ## Parameters:
        - transaction: Transaction
        '''
        transaction.cycle_id = self._historyManager.getActiveCycleID()
        self._transCRUD.create(transaction)
        self.notify()

    def updateTransaction(self, newTransaction: Transaction) -> None:
        '''
        Updates the transaction associated with `newTransaction.id` to the rest of the data inside `newTransaction`
        '''
        newTransaction.cycle_id = self._historyManager.getActiveCycleID()
        self._transCRUD.update(newTransaction.id, newTransaction)
        self.notify()

    def deleteTransaction(self, transactionID: int) -> None:
        '''
        Removes the transaction row associated with `transactionID`.
        '''
        self._transCRUD.delete(transactionID)
        self.notify()

        
from __future__ import annotations 
from typing import TYPE_CHECKING

from history.services import TransactionCRUD
from backend.shared_classes import Transaction

if TYPE_CHECKING:
    from backend.Controller import Controller


class TransactionManager:
    _instance = None
    _controller: Controller = None
    _transCRUD: TransactionCRUD = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def setController(self, controller: Controller):
        self._controller = controller
        self._transCRUD = self._controller.getHistoryManager().transaction_queryable


    def logTransaction(self, transaction: Transaction) -> None:
        '''
        Simply adds the given transaction object as new row in DB.
        ## Parameters:
        - transaction: Transaction
        '''
        self._transCRUD.create(transaction)

    def updateTransaction(self, newTransaction: Transaction) -> None:
        '''
        Updates the transaction associated with `newTransaction.id` to the rest of the data inside `newTransaction`
        '''
        self._transCRUD.update(newTransaction.id, newTransaction)

    def deleteTransaction(self, transactionID: int) -> None:
        '''
        Removes the transaction row associated with `transactionID`.
        '''
        self._transCRUD.delete(transactionID)

        
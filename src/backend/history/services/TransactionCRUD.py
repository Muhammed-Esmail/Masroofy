from typing import Optional
from datetime import date

from history.interfaces import Fetchable, Queryable, CRUD
from backend.shared_classes import Transaction
from transaction.models import TransactionModel

class TransactionCRUD(Fetchable[Transaction], Queryable[Transaction], CRUD[Transaction]):
    """
    A service class for managing financial transactions.

    This class serves as the primary data access layer for Transaction records, 
    combining single-record retrieval, filtered querying, and full CRUD operations.
    It maps Django TransactionModel instances to Transaction business objects.
    """

    def fetchById(self, id: int) -> Transaction:
        """
        Retrieves a single transaction by its database ID.

        Args:
            id (int): The unique identifier for the transaction.

        Returns:
            Transaction: A business object populated with the transaction data.

        Raises:
            TransactionModel.DoesNotExist: If the ID is not found.
        """
        transaction = TransactionModel.objects.get(id=id)
        return self.createDataObject(
            transaction.id,
            transaction.amount,
            transaction.cycle_id,
            transaction.category_id,
            transaction.log_date,
            transaction.description,
            transaction.note
        )

    def fetchByFilters(
        self, 
        startDate: Optional[date] = None, 
        endDate: Optional[date] = None, 
        category_name: Optional[str] = None, 
        cycle_id: Optional[int] = None
    ) -> list[Transaction]:
        """
        Retrieves a list of transactions matching specific criteria.

        This method builds a query dynamically based on the provided filters. 
        If a filter is None, it is excluded from the query constraints.

        Args:
            startDate (date, optional): Only include transactions on or after this date.
            endDate (date, optional): Only include transactions on or before this date.
            category_name (str, optional): Filter by a specific category name.
            cycle_id (int, optional): Filter by a specific budget cycle.

        Returns:
            list[Transaction]: A list of mapped Transaction data objects.
        """
        transactions = TransactionModel.objects.all()
        if startDate:
            transactions = transactions.filter(log_date__gte=startDate)

        if endDate:
            transactions = transactions.filter(log_date__lte=endDate)

        if category_name:
            transactions = transactions.filter(category_id=category_name)
            
        if cycle_id:
            transactions = transactions.filter(cycle_id=cycle_id)

        return [
            self.createDataObject(
                t.id,
                t.amount,
                t.cycle_id,
                t.category_id,
                t.log_date,
                t.description,
                t.note
            ) for t in transactions
        ]
    
    def create(self, newTransaction: Transaction) -> bool:
        """
        Creates a new transaction record in the database.

        Args:
            newTransaction (Transaction): The transaction object to persist.

        Returns:
            bool: True if the operation was successful.
        """
        TransactionModel.objects.create(
            amount=newTransaction.amount,
            cycle_id=newTransaction.cycle_id,
            category_id=newTransaction.category_name,
            log_date=newTransaction.log_date,
            description=newTransaction.description,
            note=newTransaction.note
        )
        return True

    def update(self, id: int, newTransaction: Transaction) -> bool:
        """
        Updates an existing transaction record.

        Args:
            id (int): The ID of the transaction to update.
            newTransaction (Transaction): The updated data.

        Returns:
            bool: True if the update command was executed.
        """
        TransactionModel.objects.filter(id=id).update(
            amount=newTransaction.amount,
            cycle_id=newTransaction.cycle_id,
            category_id=newTransaction.category_name,
            log_date=newTransaction.log_date,
            description=newTransaction.description,
            note=newTransaction.note
        )
        return True

    def delete(self, id: int) -> bool:
        """
        Removes a transaction record from the database.

        Args:
            id (int): The ID of the transaction to delete.

        Returns:
            bool: True if the deletion command was executed.
        """
        TransactionModel.objects.filter(id=id).delete()
        return True
    
    def getTotalSpentInCycle(self, cycle_id: int) -> int:
        """
        Calculates the sum of all transaction amounts within a given cycle.

        Args:
            cycle_id (int): The ID of the cycle to aggregate.

        Returns:
            int: Total amount spent. Returns 0 if no transactions are found.
        """
        transactions = self.fetchByFilters(cycle_id=cycle_id)
        if transactions:
            return sum(t.amount for t in transactions)
        else:
            return 0
    
    def createDataObject(
        self, 
        id: int, 
        amount: int, 
        cycle_id: int, 
        category_name: str, 
        log_date: date, 
        description: str, 
        note: str | None
    ) -> Transaction:
        """
        Factory method to instantiate a Transaction business object.

        Args:
            id (int): Primary key.
            amount (int): Monetary value.
            cycle_id (int): Foreign key to the budget cycle.
            category_name (str): Foreign key to the category.
            log_date (date): Date of the transaction.
            description (str): Short description.
            note (str | None): Additional optional comments.

        Returns:
            Transaction: A populated transaction object.
        """
        return Transaction(
            id=id,
            amount=amount,
            cycle_id=cycle_id,
            category_name=category_name,
            log_date=log_date,
            description=description,
            note=note
        )
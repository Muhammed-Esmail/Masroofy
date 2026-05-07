from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from datetime import date

T = TypeVar('T')

class CRUD(Generic[T], ABC):
    """
    An abstract base interface defining standard Create, Update, and Delete operations.

    This generic interface ensures that service layers maintain a consistent 
    API for modifying data records.

    Type Args:
        T: The entity model type (e.g., Transaction, Category) the service handles.
    """
    @abstractmethod
    def create(self, newObject: T) -> bool:
        """
        Persists a new entity instance to the data store.

        Args:
            newObject (T): The entity instance to be created.

        Returns:
            bool: True if the creation was successful, False otherwise.
        """
        pass

    @abstractmethod
    def update(self, id: int, newObject: T) -> bool:
        """
        Updates an existing entity identified by its unique ID.

        Args:
            id (int): The unique identifier of the entity to update.
            newObject (T): The updated entity instance containing new data.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """
        Removes an entity record from the data store.

        Args:
            id (int): The unique identifier of the entity to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        pass
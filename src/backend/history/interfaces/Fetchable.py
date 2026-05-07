from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Fetchable(Generic[T], ABC):
    """
    An abstract base interface for retrieving individual records.

    Separating Fetchable from CRUD allows for read-only services or 
    specialized retrieval logic.

    Type Args:
        T: The entity model type expected to be returned.
    """
    @abstractmethod
    def fetchById(self, id: int) -> T:
        """
        Retrieves a single entity by its primary key.

        Args:
            id (int): The unique identifier of the entity.

        Returns:
            T: The retrieved entity instance.

        Raises:
            Exception: Implementations should raise an error if the ID is not found.
        """
        pass
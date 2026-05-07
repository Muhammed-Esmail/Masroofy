from abc import ABC, abstractmethod
from datetime import date
from typing import TypeVar, Generic

T = TypeVar('T')

class Queryable(Generic[T], ABC):
    """
    An abstract base interface for advanced data filtering and list retrieval.

    This interface defines the contract for services that need to fetch 
    collections of data based on specific business criteria like dates and categories.

    Type Args:
        T: The entity model type contained within the returned list.
    """
    @abstractmethod
    def fetchByFilters(
        self, 
        startDate: date | None, 
        endDate: date | None, 
        category_name: str | None, 
        cycle_id: int | None
    ) -> list[T]:
        """
        Retrieves a filtered list of entities based on provided criteria.

        All parameters are optional. If a parameter is None, that specific 
        filter should be ignored during the query.

        Args:
            startDate (date | None): The beginning of the date range.
            endDate (date | None): The end of the date range.
            category_name (str | None): Name of the category to filter by.
            cycle_id (int | None): The specific budget cycle ID.

        Returns:
            list[T]: A list of entities matching the combined filter criteria.
        """
        pass
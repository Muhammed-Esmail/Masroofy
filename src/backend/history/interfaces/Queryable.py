from abc import ABC, abstractmethod
from datetime import date
from typing import TypeVar, Generic

T = TypeVar('T')

class Queryable(Generic[T], ABC):
    @abstractmethod
    def fetchByFilters(self, startDate: date, endDate: date, category_id: int) -> list[T]:
        pass
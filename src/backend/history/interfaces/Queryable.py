from abc import ABC, abstractmethod
from datetime import date
from typing import TypeVar, Generic

T = TypeVar('T')

class Queryable(Generic[T], ABC):
    @abstractmethod
    def fetchByFilters(self, startDate: date | None, endDate: date | None, category_id: int | None, cycle_id: int | None) -> list[T]:
        pass
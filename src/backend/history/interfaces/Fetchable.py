from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Fetchable(Generic[T], ABC):
    @abstractmethod
    def fetchById(self, id: int) -> T:
        pass
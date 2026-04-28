from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class CRUD(Generic[T], ABC):
    @abstractmethod
    def create(self, newObject: T) -> bool:
        pass

    @abstractmethod
    def update(self, id: int, newObject: T) -> bool:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
    
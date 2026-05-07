from abc import ABC, abstractmethod

class Observer(ABC):
    """
    An abstract base class that defines the Observer interface.

    This interface is part of the Observer Design Pattern. It allows objects 
    (Subscribers) to receive updates from a Subject (Publisher) when a 
    specific state change or event occurs.
    """

    @abstractmethod
    def update(self) -> None:
        """
        Receive and process an update notification from a Subject.

        This method is invoked by the Subject's notify mechanism. Subclasses 
        should override this to define the specific behavior that should 
        trigger upon notification (e.g., refreshing data, logging, or 
        triggering alerts).
        """
        pass
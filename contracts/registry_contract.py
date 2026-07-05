from abc import ABC, abstractmethod
from typing import Any, List, Optional


class RegistryContract(ABC):
    """
    Base contract for all registries.

    Registries are responsible for storing and retrieving
    research objects.

    Registries do not perform domain reasoning.
    """

    @abstractmethod
    def get_all(self) -> List[Any]:
        """Return all registered objects."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, object_id: str) -> Optional[Any]:
        """Return an object by its unique identifier."""
        raise NotImplementedError

    @abstractmethod
    def add(self, obj: Any) -> None:
        """Add a new object to the registry."""
        raise NotImplementedError

    @abstractmethod
    def update(self, obj: Any) -> None:
        """Update an existing object."""
        raise NotImplementedError

    @abstractmethod
    def remove(self, object_id: str) -> None:
        """Remove an object from the registry."""
        raise NotImplementedError
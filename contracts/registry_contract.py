from abc import ABC, abstractmethod
from typing import Any, List, Optional


class ReadRegistryContract(ABC):
    """
    Contract for registries that provide read-only access.
    """

    @abstractmethod
    def get_all(self) -> List[Any]:
        """Return all registered objects."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, object_id: str) -> Optional[Any]:
        """Return an object by its unique identifier."""
        raise NotImplementedError


class MutableRegistryContract(ReadRegistryContract):
    """
    Contract for registries that support mutation.
    """

    @abstractmethod
    def add(self, obj: Any) -> None:
        """Add an object."""
        raise NotImplementedError

    @abstractmethod
    def update(self, obj: Any) -> None:
        """Update an existing object."""
        raise NotImplementedError

    @abstractmethod
    def remove(self, object_id: str) -> None:
        """Remove an object by identifier."""
        raise NotImplementedError


# Compatibility alias for earlier imports.
RegistryContract = MutableRegistryContract
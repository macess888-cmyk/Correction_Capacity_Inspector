"""
Contracts package.

Defines architectural interfaces shared across the platform.
Contracts describe expected behavior and contain no implementation.
"""

from .registry_contract import (
    MutableRegistryContract,
    ReadRegistryContract,
    RegistryContract,
)

__all__ = [
    "ReadRegistryContract",
    "MutableRegistryContract",
    "RegistryContract",
]
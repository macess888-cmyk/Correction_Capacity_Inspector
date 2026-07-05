"""
Contracts package.

Defines architectural interfaces shared across the platform.

Contracts describe expected behavior.

They do not contain implementation.
"""

from .registry_contract import RegistryContract

__all__ = [
    "RegistryContract",
]
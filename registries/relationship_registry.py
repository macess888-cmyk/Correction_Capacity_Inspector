from typing import List, Optional

from contracts import MutableRegistryContract
from models.relationship import Relationship


class RelationshipRegistry(MutableRegistryContract):
    """
    Stores and retrieves Relationship objects.

    The registry performs storage and retrieval only.
    It does not perform graph reasoning.
    """

    def __init__(self) -> None:
        self._relationships: List[Relationship] = []

    def get_all(self) -> List[Relationship]:
        return list(self._relationships)

    def get_by_id(
        self,
        relationship_id: str,
    ) -> Optional[Relationship]:
        for relationship in self._relationships:
            if relationship.relationship_id == relationship_id:
                return relationship

        return None

    def add(
        self,
        relationship: Relationship,
    ) -> None:
        self._relationships.append(relationship)

    def update(
        self,
        relationship: Relationship,
    ) -> None:
        for index, existing in enumerate(self._relationships):
            if existing.relationship_id == relationship.relationship_id:
                self._relationships[index] = relationship
                return

        raise KeyError(
            f"Relationship not found: {relationship.relationship_id}"
        )

    def remove(
        self,
        relationship_id: str,
    ) -> None:
        for index, relationship in enumerate(self._relationships):
            if relationship.relationship_id == relationship_id:
                del self._relationships[index]
                return

        raise KeyError(
            f"Relationship not found: {relationship_id}"
        )

    def by_source(
        self,
        source_id: str,
    ) -> List[Relationship]:
        return [
            relationship
            for relationship in self._relationships
            if relationship.source_id == source_id
        ]

    def by_target(
        self,
        target_id: str,
    ) -> List[Relationship]:
        return [
            relationship
            for relationship in self._relationships
            if relationship.target_id == target_id
        ]

    def by_type(
        self,
        relationship_type: str,
    ) -> List[Relationship]:
        return [
            relationship
            for relationship in self._relationships
            if relationship.relationship_type == relationship_type
        ]
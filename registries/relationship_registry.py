from typing import List, Optional

from models.relationship import Relationship


class RelationshipRegistry:
    """
    Registry responsible for storing Relationship objects.

    The registry performs storage and retrieval only.

    It does not perform graph reasoning.
    """

    def __init__(self):
        self._relationships: List[Relationship] = []

    def get_all(self) -> List[Relationship]:
        return self._relationships

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
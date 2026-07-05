from typing import List, Optional

from models.relationship import Relationship
from registries.relationship_registry import RelationshipRegistry


class RelationshipService:
    """
    Coordinates relationship operations.

    Business logic belongs here.

    Storage belongs in the registry.

    Representation belongs in the model.
    """

    def __init__(self, registry: RelationshipRegistry):
        self._registry = registry

    def add_relationship(
        self,
        relationship: Relationship,
    ) -> None:
        self._registry.add(relationship)

    def get_relationship(
        self,
        relationship_id: str,
    ) -> Optional[Relationship]:
        return self._registry.get_by_id(relationship_id)

    def get_all_relationships(self) -> List[Relationship]:
        return self._registry.get_all()

    def relationships_from(
        self,
        source_id: str,
    ) -> List[Relationship]:
        return self._registry.by_source(source_id)

    def relationships_to(
        self,
        target_id: str,
    ) -> List[Relationship]:
        return self._registry.by_target(target_id)

    def relationships_of_type(
        self,
        relationship_type: str,
    ) -> List[Relationship]:
        return self._registry.by_type(relationship_type)
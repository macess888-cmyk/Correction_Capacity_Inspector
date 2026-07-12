from enum import Enum


class ExecutionProvenanceRelationship(str, Enum):
    DERIVED_FROM = "DERIVED_FROM"
    PRODUCED_BY = "PRODUCED_BY"
    EVALUATED_FROM = "EVALUATED_FROM"
    RECORDED_FROM = "RECORDED_FROM"
    REPLAYED_FROM = "REPLAYED_FROM"
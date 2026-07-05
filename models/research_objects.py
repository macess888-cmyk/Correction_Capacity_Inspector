from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


DEFAULT_AUTHOR = "Correction Capacity Inspector"


@dataclass
class ResearchObject:
    id: str
    name: str
    description: str
    status: str = "Candidate"
    created: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    modified: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    author: str = DEFAULT_AUTHOR
    version: str = "0.1"
    references: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


@dataclass
class Stage(ResearchObject):
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    inspection_questions: List[str] = field(default_factory=list)


@dataclass
class Transition(ResearchObject):
    source: str = ""
    destination: str = ""
    assumptions: List[str] = field(default_factory=list)
    break_surfaces: List[str] = field(default_factory=list)
    counterexamples: List[str] = field(default_factory=list)
    survivor_conditions: List[str] = field(default_factory=list)
    inspection_questions: List[str] = field(default_factory=list)


@dataclass
class BreakSurface(ResearchObject):
    between: List[str] = field(default_factory=list)
    failure_modes: List[str] = field(default_factory=list)
    observable_symptoms: List[str] = field(default_factory=list)
    survivors: List[str] = field(default_factory=list)
    recovery_options: List[str] = field(default_factory=list)
    counterexamples: List[str] = field(default_factory=list)


@dataclass
class CounterExample(ResearchObject):
    claim: str = ""
    observation: str = ""
    evidence: str = "Pending"
    impact: str = "Unknown"
    resolution: str = "Unknown"


@dataclass
class Observation(ResearchObject):
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    source: str = "Unknown"
    confidence: str = "Unknown"
    attachments: List[str] = field(default_factory=list)


@dataclass
class Hypothesis(ResearchObject):
    statement: str = ""
    supports: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)
    confidence: str = "Unknown"


@dataclass
class Survivor(ResearchObject):
    remaining_capacity: str = "Unknown"
    limitations: List[str] = field(default_factory=list)


@dataclass
class RecoveryCorridor(ResearchObject):
    origin: str = ""
    destination: str = ""
    conditions: List[str] = field(default_factory=list)
    remaining_optionality: str = "Unknown"
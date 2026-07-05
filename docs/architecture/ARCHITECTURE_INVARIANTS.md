# Correction Capacity Inspector — Architecture Invariants

Version: 1.0  
Status: FROZEN  
Date: 2026-07-05

---

## Core Position

The Correction Capacity Inspector is a modular research platform for modeling, inspecting, and analyzing candidate correction topologies.

The software supports structured inspection.

It does not establish theory.

---

## Foundational Distinctions

Observed ≠ Explained

Explained ≠ Established

Established ≠ Universal

Software ≠ Theory

Implementation ≠ Proof

Visualization ≠ Evidence

Evidence ≠ Conclusion

Conclusion ≠ Authority

UNKNOWN → HOLD

---

## Layer Ownership

### Models

Define research objects.

Models do not contain UI logic.

Models do not perform orchestration.

---

### Registries

Store and retrieve research objects.

Registries do not perform reasoning.

Registries do not render UI.

---

### Services

Coordinate registries.

Perform domain reasoning.

Services do not render UI.

---

### Orchestrators

Coordinate multiple services.

Manage workflows.

Orchestrators do not store data.

---

### Components

Render reusable UI elements.

Components do not own research logic.

---

### Pages

Compose components.

Manage navigation.

Pages do not define research logic.

---

## Dependency Direction

Allowed dependency direction:

Pages
↓
Components
↓
Orchestrators
↓
Services
↓
Registries
↓
Models

Lower layers must not import higher layers.

---

## Frozen Architecture v1

Research Artifacts
↓
Models
↓
Registries
↓
Services
↓
Orchestrators
↓
Components
↓
Pages

---

## Status Vocabulary

Observed

Recorded

Candidate

Hypothesis

Supported

Competing

Needs Investigation

Counterexample Found

Deprecated

Rejected

Frozen

---

## Development Rule

Every new capability must identify which architectural layer owns it.

Every new capability must preserve the distinction between implementation and proof.
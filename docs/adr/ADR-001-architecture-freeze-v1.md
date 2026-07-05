# ADR-001 — Architecture Freeze v1

Date: 2026-07-05  
Status: Accepted

---

## Context

The Correction Capacity Inspector has evolved from a simulator into a layered research platform.

The project now includes:

- research object models
- registries
- service layer
- topology explorer
- documentation artifacts

A freeze point is required before adding kernel, relationship, inspection, or graph capabilities.

---

## Decision

Freeze Architecture v1 around the following layers:

Research Artifacts  
Models  
Registries  
Services  
Orchestrators  
Components  
Pages

The dependency direction is downward only.

Lower layers must not import higher layers.

---

## Consequences

Future features must extend the architecture rather than redefine it.

Models remain independent of UI.

Registries store and retrieve.

Services reason.

Orchestrators coordinate.

Components render.

Pages compose.

---

## Boundary

This architecture freeze does not establish correction topology as theory.

It only freezes the current software architecture.

UNKNOWN → HOLD
# Registry Convergence Plan

**Date:** 2026-07-05

**Capability:** 008

**Status:** ACTIVE

---

# Purpose

Establish a consistent public contract across platform registries without changing their current behavior.

---

# Motivation

Multiple registries now perform related storage and retrieval responsibilities.

Current registry implementations include:

- Stage Registry
- Transition Registry
- Relationship Registry
- Evidence Registry
- Inspection Report Registry

Their interfaces are not yet fully aligned.

---

# Current Contract

RegistryContract currently defines:

- get_all()
- get_by_id()
- add()
- update()
- remove()

Before adoption, each registry must be inspected against this interface.

---

# Migration Strategy

## Phase 1 — Inspect

Review every registry’s current:

- implementation style
- method names
- identifiers
- return types
- mutation behavior
- callers

No code changes during inspection.

---

## Phase 2 — Compare

Create a compatibility matrix showing:

- methods already compatible
- methods requiring aliases
- methods requiring implementation
- behavior that must remain unchanged

---

## Phase 3 — Align

Apply the smallest safe changes required for consistency.

Prefer incremental migration.

Do not rewrite working registries unnecessarily.

---

## Phase 4 — Adopt

Registries may adopt RegistryContract only after all required methods are meaningfully supported.

Abstract methods must not be implemented as misleading placeholders.

---

## Phase 5 — Verify

Run:

- syntax compilation
- registry-specific tests
- full architecture test suite

Existing behavior must remain stable.

---

# Success Criteria

- Registry interfaces become consistent.
- Existing callers remain operational.
- No storage behavior changes unintentionally.
- No UI dependencies are introduced.
- No domain reasoning moves into registries.
- Full architecture test suite passes.
- Migration remains reversible.

---

# Boundaries

Registry convergence does not introduce:

- persistence
- database integration
- graph reasoning
- domain interpretation
- UI behavior
- research claims

---

# Current Standing

Registry convergence is approved for inspection.

Implementation remains pending examination of the existing registries.

UNKNOWN → HOLD
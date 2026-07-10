from contracts import ReadRegistryContract
from registries.transition_registry import (
    TransitionRegistry,
    get_all_transitions,
    get_transition_by_name,
    get_transition_registry,
    get_transitions_from_stage,
    get_transitions_to_stage,
)


def test_transition_registry_contract():

    registry = TransitionRegistry()

    assert isinstance(registry, ReadRegistryContract)


def test_transition_registry_read_operations():

    registry = TransitionRegistry()

    transitions = registry.get_all()

    assert len(transitions) == 2

    assert registry.get_by_id(
        "transition_reality_to_signals"
    ) is not None

    assert registry.get_by_name(
        "Signal Formation"
    ) is not None

    assert registry.get_by_id("missing") is None
    assert registry.get_by_name("missing") is None


def test_transition_queries():

    registry = TransitionRegistry()

    assert len(
        registry.from_stage("Reality")
    ) == 1

    assert len(
        registry.to_stage("Signals")
    ) == 1


def test_transition_registry_returns_copy():

    registry = TransitionRegistry()

    transitions = registry.get_all()

    transitions.clear()

    assert len(
        registry.get_all()
    ) == 2


def test_transition_compatibility_helpers():

    assert len(get_transition_registry()) == 2

    assert len(get_all_transitions()) == 2

    assert get_transition_by_name(
        "Signal Formation"
    ) is not None

    assert len(
        get_transitions_from_stage("Reality")
    ) == 1

    assert len(
        get_transitions_to_stage("Signals")
    ) == 1
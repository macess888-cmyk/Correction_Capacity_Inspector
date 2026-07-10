from contracts import ReadRegistryContract
from registries.stage_registry import (
    StageRegistry,
    get_all_stages,
    get_stage_by_name,
    get_stage_registry,
)


def test_stage_registry_contract():

    registry = StageRegistry()

    assert isinstance(registry, ReadRegistryContract)


def test_stage_registry_read_operations():

    registry = StageRegistry()

    stages = registry.get_all()

    assert len(stages) == 2
    assert registry.get_by_id("stage_reality") is not None
    assert registry.get_by_name("Reality") is not None
    assert registry.get_by_id("missing") is None
    assert registry.get_by_name("Missing") is None


def test_stage_registry_returns_copy():

    registry = StageRegistry()

    stages = registry.get_all()
    stages.clear()

    assert len(registry.get_all()) == 2


def test_stage_registry_compatibility_helpers():

    assert len(get_stage_registry()) == 2
    assert len(get_all_stages()) == 2
    assert get_stage_by_name("Reality") is not None
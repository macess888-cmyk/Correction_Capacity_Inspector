from contracts import RegistryContract


def test_registry_contract_exists():
    assert RegistryContract is not None


def test_registry_contract_required_methods():
    required_methods = [
        "get_all",
        "get_by_id",
        "add",
        "update",
        "remove",
    ]

    for method in required_methods:
        assert hasattr(RegistryContract, method)
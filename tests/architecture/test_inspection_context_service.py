from datetime import UTC

from models.inspection_context import InspectionContext
from registries.inspection_context_registry import (
    InspectionContextRegistry,
)
from services.inspection_context_service import (
    InspectionContextService,
)


def make_context(
    inspection_id: str = "inspection-001",
    status: str = "CREATED",
) -> InspectionContext:
    return InspectionContext(
        inspection_id=inspection_id,
        subject="Example subject",
        scope="Example scope",
        objective="Example objective",
        operator="Example operator",
        status=status,
    )


def make_service() -> InspectionContextService:
    registry = InspectionContextRegistry()
    return InspectionContextService(registry)


def test_service_creates_and_gets_context() -> None:
    service = make_service()
    context = make_context()

    service.create_context(context)

    assert service.get_context("inspection-001") is context


def test_service_updates_context() -> None:
    service = make_service()
    context = make_context()

    service.create_context(context)

    context.status = "ACTIVE"
    service.update_context(context)

    assert service.get_context("inspection-001").status == "ACTIVE"


def test_service_completes_context() -> None:
    service = make_service()
    context = make_context()

    service.create_context(context)

    completed = service.complete_context("inspection-001")

    assert completed.status == "COMPLETED"
    assert completed.completed is not None
    assert completed.completed.tzinfo == UTC


def test_service_pauses_context() -> None:
    service = make_service()
    context = make_context()

    service.create_context(context)

    paused = service.pause_context("inspection-001")

    assert paused.status == "PAUSED"


def test_service_resumes_context() -> None:
    service = make_service()
    context = make_context(status="PAUSED")

    service.create_context(context)

    resumed = service.resume_context("inspection-001")

    assert resumed.status == "ACTIVE"


def test_service_archives_context() -> None:
    service = make_service()
    context = make_context()

    service.create_context(context)

    archived = service.archive_context("inspection-001")

    assert archived.status == "ARCHIVED"


def test_service_lists_and_counts_contexts() -> None:
    service = make_service()

    first = make_context("inspection-001")
    second = make_context("inspection-002")

    service.create_context(first)
    service.create_context(second)

    assert service.list_contexts() == [first, second]
    assert service.count_contexts() == 2


def test_service_reports_context_existence() -> None:
    service = make_service()
    context = make_context()

    service.create_context(context)

    assert service.context_exists("inspection-001") is True
    assert service.context_exists("missing") is False
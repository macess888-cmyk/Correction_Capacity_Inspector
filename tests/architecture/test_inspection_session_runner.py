from orchestrators import InspectionSessionRunner
from orchestrators.inspection_session_runner import InspectionSessionResult


def test_inspection_session_runner_returns_result():

    runner = InspectionSessionRunner()

    result = runner.run()

    assert isinstance(result, InspectionSessionResult)
    assert result.completed_stages == ["Inspection Started"]
    assert result.observations == []
    assert result.unknowns == []
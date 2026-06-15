from workflow_automation.cli import print_run_result
from workflow_automation.runner import WorkflowRunResult


def test_print_run_result(capsys):
    result = WorkflowRunResult(
        name="sample-workflow",
        status="ok",
        message="Workflow placeholder executed: sample-workflow",
        target="data/input_docs",
    )

    print_run_result(result)

    captured = capsys.readouterr()

    assert "WORKFLOW AUTOMATION MVP" in captured.out
    assert "sample-workflow" in captured.out
    assert "ok" in captured.out
    assert "data/input_docs" in captured.out

from workflow_automation.cli import print_run_result
from workflow_automation.runner import WorkflowRunResult


def test_print_run_result(capsys):
    result = WorkflowRunResult(
        name="sample-document-workflow",
        status="ok",
        message="Workflow contract loaded: sample-document-workflow",
        target="data/input_docs",
        total_steps=3,
        enabled_steps=2,
    )

    print_run_result(result)

    captured = capsys.readouterr()

    assert "WORKFLOW AUTOMATION MVP" in captured.out
    assert "sample-document-workflow" in captured.out
    assert "ok" in captured.out
    assert "data/input_docs" in captured.out
    assert "Steps: 2/3 enabled" in captured.out

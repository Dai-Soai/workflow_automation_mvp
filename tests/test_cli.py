from workflow_automation.cli import print_run_result
from workflow_automation.executor import StepExecutionResult
from workflow_automation.runner import WorkflowRunResult


def test_print_run_result(capsys):
    result = WorkflowRunResult(
        name="sample-document-workflow",
        status="ok",
        message="Workflow executed locally: sample-document-workflow",
        target="data/input_docs",
        total_steps=3,
        enabled_steps=2,
        task_types=["detect", "pipeline"],
        step_results=[
            StepExecutionResult(
                step_name="detect_documents",
                task_type="detect",
                status="ok",
                message="Executed Detect Documents for target: data/input_docs",
            ),
            StepExecutionResult(
                step_name="run_document_pipeline",
                task_type="pipeline",
                status="ok",
                message="Document pipeline executed successfully.",
            ),
        ],
    )

    print_run_result(result)

    captured = capsys.readouterr()

    assert "WORKFLOW AUTOMATION MVP" in captured.out
    assert "sample-document-workflow" in captured.out
    assert "ok" in captured.out
    assert "data/input_docs" in captured.out
    assert "Steps: 2/3 enabled" in captured.out
    assert "Tasks: detect, pipeline" in captured.out
    assert "Step Results:" in captured.out
    assert "detect_documents" in captured.out
    assert "run_document_pipeline" in captured.out


def test_print_dry_run_result(capsys):
    result = WorkflowRunResult(
        name="sample-document-workflow",
        status="ok",
        message="Workflow dry run completed: sample-document-workflow",
        target="data/input_docs",
        total_steps=3,
        enabled_steps=3,
        task_types=["detect", "pipeline", "publish"],
        step_results=[],
        dry_run=True,
    )

    print_run_result(result)

    captured = capsys.readouterr()

    assert "WORKFLOW AUTOMATION MVP" in captured.out
    assert "Mode: dry-run" in captured.out
    assert "Workflow dry run completed" in captured.out

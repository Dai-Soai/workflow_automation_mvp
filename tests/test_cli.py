from workflow_automation.cli import print_run_result
from workflow_automation.executor import StepExecutionResult
from workflow_automation.knowledge_executor import KnowledgeSearchResult
from workflow_automation.runner import WorkflowRunResult


def test_print_run_result(capsys):
    result = WorkflowRunResult(
        name="sample-document-workflow",
        status="ok",
        message="Workflow executed locally: sample-document-workflow",
        target="data/input_docs",
        total_steps=4,
        enabled_steps=3,
        task_types=["detect", "pipeline", "index"],
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
            StepExecutionResult(
                step_name="index_knowledge_search",
                task_type="index",
                status="ok",
                message="Knowledge Search index completed. Indexed 3 document(s).",
            ),
        ],
    )

    print_run_result(result)

    captured = capsys.readouterr()

    assert "WORKFLOW AUTOMATION MVP" in captured.out
    assert "sample-document-workflow" in captured.out
    assert "ok" in captured.out
    assert "data/input_docs" in captured.out
    assert "Steps: 3/4 enabled" in captured.out
    assert "Tasks: detect, pipeline, index" in captured.out
    assert "Step Results:" in captured.out
    assert "index_knowledge_search" in captured.out


def test_print_dry_run_result(capsys):
    result = WorkflowRunResult(
        name="sample-document-workflow",
        status="ok",
        message="Workflow dry run completed: sample-document-workflow",
        target="data/input_docs",
        total_steps=4,
        enabled_steps=4,
        task_types=["detect", "pipeline", "publish", "index"],
        step_results=[],
        dry_run=True,
    )

    print_run_result(result)

    captured = capsys.readouterr()

    assert "WORKFLOW AUTOMATION MVP" in captured.out
    assert "Mode: dry-run" in captured.out
    assert "Workflow dry run completed" in captured.out


def test_print_search_result(capsys):
    search_result = KnowledgeSearchResult(
        status="ok",
        command=["radar-search", "search", "Workflow"],
        stdout="Found 1 result(s).",
        stderr="",
        returncode=0,
    )

    result = WorkflowRunResult(
        name="sample-document-workflow",
        status="ok",
        message="Workflow executed locally: sample-document-workflow",
        target="data/input_docs",
        total_steps=4,
        enabled_steps=4,
        task_types=["detect", "pipeline", "publish", "index"],
        step_results=[],
        search_query="Workflow",
        search_result=search_result,
    )

    print_run_result(result)

    captured = capsys.readouterr()

    assert "Knowledge Search:" in captured.out
    assert "Query: Workflow" in captured.out
    assert "Found 1 result(s)." in captured.out

import pytest

from workflow_automation.runner import WorkflowRunResult
from workflow_automation.telegram import (
    TelegramWorkflowRequest,
    format_workflow_response,
    parse_telegram_command,
)


def test_parse_telegram_command_basic():
    request = parse_telegram_command("/run workflows/sample.workflow.json")

    assert request.workflow == "workflows/sample.workflow.json"
    assert request.target is None
    assert request.publish is False
    assert request.search is None
    assert request.dry_run is False


def test_parse_telegram_command_with_options():
    request = parse_telegram_command(
        "/run workflows/sample.workflow.json "
        "--target data/custom_docs "
        "--export-json "
        "--export-markdown "
        "--publish "
        "--search Workflow "
        "--dry-run"
    )

    assert request.workflow == "workflows/sample.workflow.json"
    assert request.target == "data/custom_docs"
    assert request.export_json is True
    assert request.export_markdown is True
    assert request.publish is True
    assert request.search == "Workflow"
    assert request.dry_run is True


def test_parse_telegram_command_rejects_empty_command():
    with pytest.raises(ValueError, match="Empty Telegram command"):
        parse_telegram_command("")


def test_parse_telegram_command_rejects_unsupported_command():
    with pytest.raises(ValueError, match="Unsupported Telegram command"):
        parse_telegram_command("/unknown workflows/sample.workflow.json")


def test_parse_telegram_command_rejects_missing_workflow():
    with pytest.raises(ValueError, match="Missing workflow path"):
        parse_telegram_command("/run")


def test_parse_telegram_command_rejects_missing_target_value():
    with pytest.raises(ValueError, match="Missing value for --target"):
        parse_telegram_command("/run workflows/sample.workflow.json --target")


def test_parse_telegram_command_rejects_missing_search_value():
    with pytest.raises(ValueError, match="Missing value for --search"):
        parse_telegram_command("/run workflows/sample.workflow.json --search")


def test_parse_telegram_command_rejects_unknown_option():
    with pytest.raises(ValueError, match="Unsupported Telegram option"):
        parse_telegram_command("/run workflows/sample.workflow.json --unknown")


def test_format_workflow_response_basic():
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

    response = format_workflow_response(result)

    assert "WORKFLOW AUTOMATION" in response
    assert "sample-document-workflow" in response
    assert "Status: ok" in response
    assert "Target: data/input_docs" in response
    assert "Steps: 4/4 enabled" in response
    assert "Mode: dry-run" in response

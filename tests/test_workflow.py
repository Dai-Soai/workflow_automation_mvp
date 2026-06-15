import pytest

from workflow_automation.runner import run_workflow
from workflow_automation.workflow import load_workflow_spec


def test_load_workflow_spec(tmp_path):
    workflow = tmp_path / "sample.workflow"
    workflow.write_text(
        "sample-workflow\n" "Process a document folder\n" "data/input_docs\n",
        encoding="utf-8",
    )

    spec = load_workflow_spec(str(workflow))

    assert spec.name == "sample-workflow"
    assert spec.description == "Process a document folder"
    assert spec.target == "data/input_docs"


def test_load_workflow_spec_rejects_missing_file(tmp_path):
    missing = tmp_path / "missing.workflow"

    with pytest.raises(FileNotFoundError):
        load_workflow_spec(str(missing))


def test_run_workflow(tmp_path):
    workflow = tmp_path / "sample.workflow"
    workflow.write_text(
        "sample-workflow\n" "Process a document folder\n" "data/input_docs\n",
        encoding="utf-8",
    )

    result = run_workflow(str(workflow))

    assert result.status == "ok"
    assert result.name == "sample-workflow"
    assert result.target == "data/input_docs"

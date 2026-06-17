import pytest

from workflow_automation.runner import run_workflow
from workflow_automation.workflow import load_workflow_spec


def write_sample_workflow(path):
    path.write_text(
        """
{
  "name": "sample-document-workflow",
  "description": "Process a document folder through RADAR automation.",
  "target": "data/input_docs",
  "steps": [
    {
      "name": "detect_documents",
      "type": "detect",
      "enabled": true
    },
    {
      "name": "run_document_pipeline",
      "type": "pipeline",
      "enabled": true
    },
    {
      "name": "publish_to_knowledge_search",
      "type": "publish",
      "enabled": false
    }
  ],
  "options": {
    "export_json": true,
    "export_markdown": true,
    "publish": false
  }
}
""",
        encoding="utf-8",
    )


def test_load_workflow_spec(tmp_path):
    workflow = tmp_path / "sample.workflow.json"
    write_sample_workflow(workflow)

    spec = load_workflow_spec(str(workflow))

    assert spec.name == "sample-document-workflow"
    assert spec.description == "Process a document folder through RADAR automation."
    assert spec.target == "data/input_docs"
    assert len(spec.steps) == 3
    assert spec.steps[0].name == "detect_documents"
    assert spec.steps[0].type == "detect"
    assert spec.steps[0].enabled is True
    assert spec.steps[2].enabled is False
    assert spec.options.export_json is True
    assert spec.options.export_markdown is True
    assert spec.options.publish is False


def test_load_workflow_spec_rejects_missing_file(tmp_path):
    missing = tmp_path / "missing.workflow.json"

    with pytest.raises(FileNotFoundError):
        load_workflow_spec(str(missing))


def test_load_workflow_spec_rejects_invalid_json(tmp_path):
    workflow = tmp_path / "invalid.workflow.json"
    workflow.write_text("{ invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid workflow JSON"):
        load_workflow_spec(str(workflow))


def test_load_workflow_spec_rejects_missing_required_field(tmp_path):
    workflow = tmp_path / "missing-field.workflow.json"
    workflow.write_text(
        """
{
  "name": "broken-workflow",
  "description": "Missing target and steps"
}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Workflow missing required field"):
        load_workflow_spec(str(workflow))


def test_load_workflow_spec_rejects_step_missing_name(tmp_path):
    workflow = tmp_path / "missing-step-name.workflow.json"
    workflow.write_text(
        """
{
  "name": "broken-workflow",
  "description": "Broken step",
  "target": "data/input_docs",
  "steps": [
    {
      "type": "pipeline",
      "enabled": true
    }
  ]
}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Workflow step missing required field: name"):
        load_workflow_spec(str(workflow))


def test_run_workflow(tmp_path):
    workflow = tmp_path / "sample.workflow.json"
    write_sample_workflow(workflow)

    result = run_workflow(str(workflow))

    assert result.status == "ok"
    assert result.name == "sample-document-workflow"
    assert result.target == "data/input_docs"
    assert result.total_steps == 3
    assert result.enabled_steps == 2
    assert "Workflow contract loaded" in result.message

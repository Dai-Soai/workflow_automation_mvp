import pytest

from workflow_automation.runner import run_workflow
from workflow_automation.workflow import load_workflow_spec, override_workflow_spec


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
        "enabled": false
      },
      {
        "name": "publish_to_knowledge_search",
        "type": "publish",
        "enabled": false
      },
      {
        "name": "index_knowledge_search",
        "type": "index",
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
    assert len(spec.steps) == 4
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
    assert result.total_steps == 4
    assert result.enabled_steps == 1
    assert result.task_types == ["detect"]
    assert len(result.step_results) == 1
    assert result.step_results[0].step_name == "detect_documents"
    assert result.step_results[0].status == "ok"
    assert "Workflow executed locally" in result.message


def test_load_workflow_spec_rejects_unsupported_step_type(tmp_path):
    workflow = tmp_path / "unsupported-step.workflow.json"
    workflow.write_text(
        """
{
  "name": "broken-workflow",
  "description": "Unsupported step type",
  "target": "data/input_docs",
  "steps": [
    {
      "name": "unknown_step",
      "type": "unknown",
      "enabled": true
    }
  ]
}
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported workflow step type"):
        load_workflow_spec(str(workflow))


def test_override_workflow_spec(tmp_path):
    workflow = tmp_path / "sample.workflow.json"
    write_sample_workflow(workflow)

    spec = load_workflow_spec(str(workflow))

    overridden = override_workflow_spec(
        spec,
        target="data/custom_docs",
        export_json=True,
        export_markdown=True,
        publish=True,
    )

    assert overridden.target == "data/custom_docs"
    assert overridden.options.export_json is True
    assert overridden.options.export_markdown is True
    assert overridden.options.publish is True
    assert overridden.name == spec.name
    assert overridden.steps == spec.steps


def test_run_workflow_dry_run(tmp_path):
    workflow = tmp_path / "sample.workflow.json"
    write_sample_workflow(workflow)

    result = run_workflow(str(workflow), dry_run=True)

    assert result.status == "ok"
    assert result.dry_run is True
    assert result.step_results == []
    assert "Workflow dry run completed" in result.message

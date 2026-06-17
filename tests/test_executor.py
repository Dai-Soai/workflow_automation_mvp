from workflow_automation.executor import execute_step, execute_steps
from workflow_automation.workflow import WorkflowStep


def test_execute_step():
    step = WorkflowStep(
        name="detect_documents",
        type="detect",
        enabled=True,
    )

    result = execute_step(step, target="data/input_docs")

    assert result.status == "ok"
    assert result.step_name == "detect_documents"
    assert result.task_type == "detect"
    assert "Detect Documents" in result.message
    assert "data/input_docs" in result.message


def test_execute_steps_skips_disabled_steps():
    steps = [
        WorkflowStep(
            name="detect_documents",
            type="detect",
            enabled=True,
        ),
        WorkflowStep(
            name="publish_to_knowledge_search",
            type="publish",
            enabled=False,
        ),
    ]

    results = execute_steps(steps, target="data/input_docs")

    assert len(results) == 1
    assert results[0].step_name == "detect_documents"

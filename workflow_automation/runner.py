from dataclasses import dataclass

from workflow_automation.workflow import WorkflowSpec, load_workflow_spec


@dataclass
class WorkflowRunResult:
    name: str
    status: str
    message: str
    target: str
    total_steps: int
    enabled_steps: int


def run_workflow(workflow_path: str) -> WorkflowRunResult:
    spec: WorkflowSpec = load_workflow_spec(workflow_path)

    enabled_steps = [step for step in spec.steps if step.enabled]

    return WorkflowRunResult(
        name=spec.name,
        status="ok",
        message=f"Workflow contract loaded: {spec.name}",
        target=spec.target,
        total_steps=len(spec.steps),
        enabled_steps=len(enabled_steps),
    )

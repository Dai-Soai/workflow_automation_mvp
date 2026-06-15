from dataclasses import dataclass

from workflow_automation.workflow import WorkflowSpec, load_workflow_spec


@dataclass
class WorkflowRunResult:
    name: str
    status: str
    message: str
    target: str


def run_workflow(workflow_path: str) -> WorkflowRunResult:
    spec: WorkflowSpec = load_workflow_spec(workflow_path)

    return WorkflowRunResult(
        name=spec.name,
        status="ok",
        message=f"Workflow placeholder executed: {spec.name}",
        target=spec.target,
    )

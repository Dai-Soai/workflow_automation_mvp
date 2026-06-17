from dataclasses import dataclass

from workflow_automation.executor import StepExecutionResult, execute_steps
from workflow_automation.workflow import WorkflowSpec, load_workflow_spec


@dataclass
class WorkflowRunResult:
    name: str
    status: str
    message: str
    target: str
    total_steps: int
    enabled_steps: int
    task_types: list[str]
    step_results: list[StepExecutionResult]


def run_workflow(workflow_path: str) -> WorkflowRunResult:
    spec: WorkflowSpec = load_workflow_spec(workflow_path)

    enabled_steps = [step for step in spec.steps if step.enabled]
    step_results = execute_steps(enabled_steps, spec.target)
    task_types = [result.task_type for result in step_results]

    return WorkflowRunResult(
        name=spec.name,
        status="ok",
        message=f"Workflow executed locally: {spec.name}",
        target=spec.target,
        total_steps=len(spec.steps),
        enabled_steps=len(enabled_steps),
        task_types=task_types,
        step_results=step_results,
    )

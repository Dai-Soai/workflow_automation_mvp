from dataclasses import dataclass

from workflow_automation.registry import get_task_definition
from workflow_automation.workflow import WorkflowStep


@dataclass
class StepExecutionResult:
    step_name: str
    task_type: str
    status: str
    message: str


def execute_step(step: WorkflowStep, target: str) -> StepExecutionResult:
    task_definition = get_task_definition(step.type)

    return StepExecutionResult(
        step_name=step.name,
        task_type=step.type,
        status="ok",
        message=f"Executed {task_definition.name} for target: {target}",
    )


def execute_steps(
    steps: list[WorkflowStep],
    target: str,
) -> list[StepExecutionResult]:
    results: list[StepExecutionResult] = []

    for step in steps:
        if not step.enabled:
            continue

        results.append(execute_step(step, target))

    return results

from dataclasses import dataclass

from workflow_automation.pipeline_executor import run_document_pipeline
from workflow_automation.registry import get_task_definition
from workflow_automation.workflow import WorkflowOptions, WorkflowStep


@dataclass
class StepExecutionResult:
    step_name: str
    task_type: str
    status: str
    message: str


def execute_pipeline_step(
    step: WorkflowStep,
    target: str,
    options: WorkflowOptions,
) -> StepExecutionResult:
    result = run_document_pipeline(
        target=target,
        json_dir="outputs/workflow_json" if options.export_json else None,
        md_dir="outputs/workflow_md" if options.export_markdown else None,
        publish=options.publish,
    )

    if result.status == "ok":
        return StepExecutionResult(
            step_name=step.name,
            task_type=step.type,
            status="ok",
            message="Document pipeline executed successfully.",
        )

    return StepExecutionResult(
        step_name=step.name,
        task_type=step.type,
        status="failed",
        message=result.stderr or result.stdout or "Document pipeline failed.",
    )


def execute_step(
    step: WorkflowStep,
    target: str,
    options: WorkflowOptions,
) -> StepExecutionResult:
    if step.type == "pipeline":
        return execute_pipeline_step(step, target, options)

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
    options: WorkflowOptions,
) -> list[StepExecutionResult]:
    results: list[StepExecutionResult] = []

    for step in steps:
        if not step.enabled:
            continue

        results.append(execute_step(step, target, options))

    return results

from dataclasses import dataclass

from workflow_automation.executor import StepExecutionResult, execute_steps
from workflow_automation.knowledge_executor import (
    KnowledgeSearchResult,
    search_documents,
)
from workflow_automation.workflow import (
    WorkflowSpec,
    load_workflow_spec,
    override_workflow_spec,
)


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
    dry_run: bool = False
    search_query: str | None = None
    search_result: KnowledgeSearchResult | None = None


def run_workflow(
    workflow_path: str,
    target: str | None = None,
    export_json: bool | None = None,
    export_markdown: bool | None = None,
    publish: bool | None = None,
    dry_run: bool = False,
    search_query: str | None = None,
) -> WorkflowRunResult:
    spec: WorkflowSpec = load_workflow_spec(workflow_path)

    spec = override_workflow_spec(
        spec,
        target=target,
        export_json=export_json,
        export_markdown=export_markdown,
        publish=publish,
    )

    enabled_steps = [step for step in spec.steps if step.enabled]

    if dry_run:
        task_types = [step.type for step in enabled_steps]

        return WorkflowRunResult(
            name=spec.name,
            status="ok",
            message=f"Workflow dry run completed: {spec.name}",
            target=spec.target,
            total_steps=len(spec.steps),
            enabled_steps=len(enabled_steps),
            task_types=task_types,
            step_results=[],
            dry_run=True,
            search_query=search_query,
        )

    step_results = execute_steps(enabled_steps, spec.target, spec.options)
    task_types = [result.task_type for result in step_results]

    search_result = None

    if search_query:
        search_result = search_documents(search_query)

    overall_status = "ok"

    if any(result.status == "failed" for result in step_results):
        overall_status = "failed"

    if search_result and search_result.status == "failed":
        overall_status = "failed"

    return WorkflowRunResult(
        name=spec.name,
        status=overall_status,
        message=f"Workflow executed locally: {spec.name}",
        target=spec.target,
        total_steps=len(spec.steps),
        enabled_steps=len(enabled_steps),
        task_types=task_types,
        step_results=step_results,
        search_query=search_query,
        search_result=search_result,
    )

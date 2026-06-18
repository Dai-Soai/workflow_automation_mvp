from dataclasses import dataclass


@dataclass(frozen=True)
class TaskDefinition:
    task_type: str
    name: str
    description: str


DEFAULT_TASKS = {
    "detect": TaskDefinition(
        task_type="detect",
        name="Detect Documents",
        description="Detect supported documents in the workflow target.",
    ),
    "pipeline": TaskDefinition(
        task_type="pipeline",
        name="Run Document Pipeline",
        description="Run the document pipeline on supported input files.",
    ),
    "publish": TaskDefinition(
        task_type="publish",
        name="Publish to Knowledge Search",
        description="Publish processed output to Knowledge Search input.",
    ),
    "index": TaskDefinition(
        task_type="index",
        name="Index Knowledge Search",
        description="Index published documents into Knowledge Search.",
    ),
}


def get_task_registry() -> dict[str, TaskDefinition]:
    return dict(DEFAULT_TASKS)


def is_supported_task(task_type: str) -> bool:
    return task_type in DEFAULT_TASKS


def get_task_definition(task_type: str) -> TaskDefinition:
    if task_type not in DEFAULT_TASKS:
        raise ValueError(f"Unsupported task type: {task_type}")

    return DEFAULT_TASKS[task_type]


def list_task_types() -> list[str]:
    return sorted(DEFAULT_TASKS.keys())

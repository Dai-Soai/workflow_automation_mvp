import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from workflow_automation.registry import is_supported_task


@dataclass
class WorkflowStep:
    name: str
    type: str
    enabled: bool = True


@dataclass
class WorkflowOptions:
    export_json: bool = False
    export_markdown: bool = False
    publish: bool = False


@dataclass
class WorkflowSpec:
    name: str
    description: str
    target: str
    steps: list[WorkflowStep]
    options: WorkflowOptions


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid workflow JSON: {path}") from exc


def _parse_steps(raw_steps: list[dict[str, Any]]) -> list[WorkflowStep]:
    steps: list[WorkflowStep] = []

    for raw_step in raw_steps:
        if "name" not in raw_step:
            raise ValueError("Workflow step missing required field: name")

        if "type" not in raw_step:
            raise ValueError("Workflow step missing required field: type")

        task_type = str(raw_step["type"])

        if not is_supported_task(task_type):
            raise ValueError(f"Unsupported workflow step type: {task_type}")

        steps.append(
            WorkflowStep(
                name=str(raw_step["name"]),
                type=task_type,
                enabled=bool(raw_step.get("enabled", True)),
            )
        )

    return steps


def _parse_options(raw_options: dict[str, Any] | None) -> WorkflowOptions:
    raw_options = raw_options or {}

    return WorkflowOptions(
        export_json=bool(raw_options.get("export_json", False)),
        export_markdown=bool(raw_options.get("export_markdown", False)),
        publish=bool(raw_options.get("publish", False)),
    )


def load_workflow_spec(workflow_path: str) -> WorkflowSpec:
    path = Path(workflow_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Workflow file not found: {path}")

    payload = _load_json(path)

    required_fields = ["name", "description", "target", "steps"]

    for field in required_fields:
        if field not in payload:
            raise ValueError(f"Workflow missing required field: {field}")

    steps = _parse_steps(payload["steps"])

    return WorkflowSpec(
        name=str(payload["name"]),
        description=str(payload["description"]),
        target=str(payload["target"]),
        steps=steps,
        options=_parse_options(payload.get("options")),
    )


def override_workflow_spec(
    spec: WorkflowSpec,
    target: str | None = None,
    export_json: bool | None = None,
    export_markdown: bool | None = None,
    publish: bool | None = None,
) -> WorkflowSpec:
    options = WorkflowOptions(
        export_json=spec.options.export_json if export_json is None else export_json,
        export_markdown=(
            spec.options.export_markdown if export_markdown is None else export_markdown
        ),
        publish=spec.options.publish if publish is None else publish,
    )

    return WorkflowSpec(
        name=spec.name,
        description=spec.description,
        target=spec.target if target is None else target,
        steps=spec.steps,
        options=options,
    )

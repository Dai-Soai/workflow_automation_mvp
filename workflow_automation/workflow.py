from dataclasses import dataclass
from pathlib import Path


@dataclass
class WorkflowSpec:
    name: str
    description: str
    target: str


def load_workflow_spec(workflow_path: str) -> WorkflowSpec:
    path = Path(workflow_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Workflow file not found: {path}")

    text = path.read_text(encoding="utf-8")

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    name = lines[0] if lines else "unnamed-workflow"
    description = lines[1] if len(lines) > 1 else "No description"
    target = lines[2] if len(lines) > 2 else "No target"

    return WorkflowSpec(
        name=name,
        description=description,
        target=target,
    )

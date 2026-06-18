import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PipelineExecutionResult:
    status: str
    command: list[str]
    stdout: str
    stderr: str
    returncode: int


def run_document_pipeline(
    target: str,
    json_dir: str | None = None,
    md_dir: str | None = None,
    publish: bool = False,
) -> PipelineExecutionResult:
    target_path = Path(target).expanduser().resolve()

    command = [
        "doc-pipe",
        "--batch",
        str(target_path),
    ]

    if json_dir:
        command.extend(["--json-dir", json_dir])

    if md_dir:
        command.extend(["--md-dir", md_dir])

    if publish:
        command.append("--publish")

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    status = "ok" if completed.returncode == 0 else "failed"

    return PipelineExecutionResult(
        status=status,
        command=command,
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
    )

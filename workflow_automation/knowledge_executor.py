import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class KnowledgeIndexResult:
    status: str
    command: list[str]
    stdout: str
    stderr: str
    returncode: int


@dataclass
class KnowledgeSearchResult:
    status: str
    command: list[str]
    stdout: str
    stderr: str
    returncode: int


def index_documents(index_dir: str) -> KnowledgeIndexResult:
    path = Path(index_dir).expanduser().resolve()

    command = [
        "radar-search",
        "index",
        str(path),
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    status = "ok" if completed.returncode == 0 else "failed"

    return KnowledgeIndexResult(
        status=status,
        command=command,
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
    )


def search_documents(query: str) -> KnowledgeSearchResult:
    command = [
        "radar-search",
        "search",
        query,
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    status = "ok" if completed.returncode == 0 else "failed"

    return KnowledgeSearchResult(
        status=status,
        command=command,
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
    )

from dataclasses import dataclass

from workflow_automation.runner import WorkflowRunResult, run_workflow


@dataclass
class TelegramWorkflowRequest:
    workflow: str
    target: str | None = None
    export_json: bool = False
    export_markdown: bool = False
    publish: bool = False
    search: str | None = None
    dry_run: bool = False


def parse_telegram_command(command: str) -> TelegramWorkflowRequest:
    parts = command.strip().split()

    if not parts:
        raise ValueError("Empty Telegram command")

    if parts[0] != "/run":
        raise ValueError(f"Unsupported Telegram command: {parts[0]}")

    if len(parts) < 2:
        raise ValueError("Missing workflow path")

    workflow = parts[1]

    target = None
    export_json = False
    export_markdown = False
    publish = False
    search = None
    dry_run = False

    index = 2

    while index < len(parts):
        token = parts[index]

        if token == "--target":
            if index + 1 >= len(parts):
                raise ValueError("Missing value for --target")
            target = parts[index + 1]
            index += 2
            continue

        if token == "--export-json":
            export_json = True
            index += 1
            continue

        if token == "--export-markdown":
            export_markdown = True
            index += 1
            continue

        if token == "--publish":
            publish = True
            index += 1
            continue

        if token == "--search":
            if index + 1 >= len(parts):
                raise ValueError("Missing value for --search")
            search = parts[index + 1]
            index += 2
            continue

        if token == "--dry-run":
            dry_run = True
            index += 1
            continue

        raise ValueError(f"Unsupported Telegram option: {token}")

    return TelegramWorkflowRequest(
        workflow=workflow,
        target=target,
        export_json=export_json,
        export_markdown=export_markdown,
        publish=publish,
        search=search,
        dry_run=dry_run,
    )


def format_workflow_response(result: WorkflowRunResult) -> str:
    lines = [
        "WORKFLOW AUTOMATION",
        "",
        f"Workflow: {result.name}",
        f"Status: {result.status}",
        f"Target: {result.target}",
        f"Steps: {result.enabled_steps}/{result.total_steps} enabled",
    ]

    if result.task_types:
        lines.append(f"Tasks: {', '.join(result.task_types)}")

    if result.dry_run:
        lines.append("Mode: dry-run")

    if result.step_results:
        lines.append("")
        lines.append("Step Results:")

        for step_result in result.step_results:
            lines.append(
                f"- [{step_result.status}] "
                f"{step_result.step_name} "
                f"({step_result.task_type})"
            )

    if result.search_result is not None:
        lines.append("")
        lines.append("Knowledge Search:")
        lines.append(f"Query: {result.search_query}")
        lines.append(f"Status: {result.search_result.status}")

        stdout = result.search_result.stdout.strip()

        if stdout:
            lines.append("")
            lines.append(stdout)

    lines.append("")
    lines.append(result.message)

    return "\n".join(lines)


def _status_icon(status: str) -> str:
    if status == "ok":
        return "✅"

    if status == "failed":
        return "❌"

    return "ℹ️"


def _extract_search_result_count(stdout: str) -> str | None:
    for line in stdout.splitlines():
        stripped = line.strip()

        if stripped.startswith("Found ") and " result" in stripped:
            return stripped

    return None


def format_compact_workflow_response(result: WorkflowRunResult) -> str:
    icon = _status_icon(result.status)

    lines = [
        f"{icon} Workflow completed",
        "",
        f"Workflow: {result.name}",
        f"Status: {result.status}",
        f"Target: {result.target}",
        f"Steps: {result.enabled_steps}/{result.total_steps}",
    ]

    if result.task_types:
        lines.append(f"Tasks: {', '.join(result.task_types)}")

    if result.dry_run:
        lines.append("Mode: dry-run")

    if result.step_results:
        lines.append("")
        lines.append("Results:")

        for step_result in result.step_results:
            step_icon = _status_icon(step_result.status)
            lines.append(
                f"{step_icon} {step_result.step_name} ({step_result.task_type})"
            )

    if result.search_result is not None:
        lines.append("")
        lines.append("Knowledge Search:")
        lines.append(f"Query: {result.search_query}")
        lines.append(f"Status: {result.search_result.status}")

        count_line = _extract_search_result_count(result.search_result.stdout)

        if count_line:
            lines.append(count_line)

    lines.append("")
    lines.append(result.message)

    return "\n".join(lines)


def handle_workflow_request(
    request: TelegramWorkflowRequest,
    compact: bool = False,
) -> str:
    result = run_workflow(
        request.workflow,
        target=request.target,
        export_json=True if request.export_json else None,
        export_markdown=True if request.export_markdown else None,
        publish=True if request.publish else None,
        dry_run=request.dry_run,
        search_query=request.search,
    )

    if compact:
        return format_compact_workflow_response(result)

    return format_workflow_response(result)


def handle_telegram_command(command: str, compact: bool = False) -> str:
    request = parse_telegram_command(command)

    return handle_workflow_request(request, compact=compact)


def format_workflow_help() -> str:
    return "\n".join(
        [
            "WORKFLOW AUTOMATION HELP",
            "",
            "Commands:",
            "",
            "/workflow help",
            "Show available workflow commands.",
            "",
            "/workflow status",
            "Show workflow automation status.",
            "",
            "/run <workflow_path>",
            "Run a workflow contract.",
            "",
            "Examples:",
            "",
            "/run workflows/sample.workflow.json --dry-run",
            "/run workflows/sample.workflow.json --publish --search Workflow",
            "/run workflows/sample.workflow.json --target data/custom_docs --export-json --export-markdown --publish",
        ]
    )


def format_workflow_status() -> str:
    return "\n".join(
        [
            "WORKFLOW AUTOMATION STATUS",
            "",
            "Status: ok",
            "Mode: mock-telegram-command",
            "Supported commands: /workflow help, /workflow status, /run",
            "Workflow engine: available",
        ]
    )


def handle_mock_telegram_command(command: str, compact: bool = False) -> str:
    normalized = command.strip()

    if not normalized:
        raise ValueError("Empty Telegram command")

    if normalized == "/workflow help":
        return format_workflow_help()

    if normalized == "/workflow status":
        return format_workflow_status()

    if normalized.startswith("/run"):
        return handle_telegram_command(normalized, compact=compact)

    raise ValueError(f"Unsupported Telegram command: {normalized}")

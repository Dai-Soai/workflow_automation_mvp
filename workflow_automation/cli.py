from typing import Any
import argparse

from workflow_automation.runner import run_workflow


def print_run_result(result: Any) -> None:
    print("=" * 60)
    print("WORKFLOW AUTOMATION MVP")
    print("=" * 60)
    print(f"Workflow: {result.name}")
    print(f"Status: {result.status}")
    print(f"Target: {result.target}")
    print(f"Steps: {result.enabled_steps}/{result.total_steps} enabled")

    if result.task_types:
        print(f"Tasks: {', '.join(result.task_types)}")

    if result.dry_run:
        print("Mode: dry-run")

    print()

    if result.step_results:
        print("Step Results:")
        for step_result in result.step_results:
            print(
                f"- [{step_result.status}] "
                f"{step_result.step_name} "
                f"({step_result.task_type})"
            )
            print(f"  {step_result.message}")
        print()

    if result.search_result is not None:
        print("Knowledge Search:")
        print(f"Query: {result.search_query}")
        print(f"Status: {result.search_result.status}")

        if result.search_result.stdout.strip():
            print(result.search_result.stdout.strip())

        if result.search_result.stderr.strip():
            print(result.search_result.stderr.strip())

        print()

    print(result.message)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="auto-run",
        description="Workflow Automation MVP",
    )

    parser.add_argument("workflow", help="Path to workflow JSON contract")

    parser.add_argument(
        "--target",
        help="Override workflow target directory",
    )

    parser.add_argument(
        "--export-json",
        action="store_true",
        help="Override workflow option: export JSON reports",
    )

    parser.add_argument(
        "--export-markdown",
        action="store_true",
        help="Override workflow option: export Markdown reports",
    )

    parser.add_argument(
        "--publish",
        action="store_true",
        help="Override workflow option: publish processed documents",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load and validate workflow without executing steps",
    )

    parser.add_argument(
        "--search",
        help="Run Knowledge Search query after workflow execution",
    )

    args = parser.parse_args()

    result = run_workflow(
        args.workflow,
        target=args.target,
        export_json=True if args.export_json else None,
        export_markdown=True if args.export_markdown else None,
        publish=True if args.publish else None,
        dry_run=args.dry_run,
        search_query=args.search,
    )

    print_run_result(result)


if __name__ == "__main__":
    main()

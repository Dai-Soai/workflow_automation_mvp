import argparse

from workflow_automation.runner import run_workflow


def print_run_result(result):
    print("=" * 60)
    print("WORKFLOW AUTOMATION MVP")
    print("=" * 60)
    print(f"Workflow: {result.name}")
    print(f"Status: {result.status}")
    print(f"Target: {result.target}")
    print(f"Steps: {result.enabled_steps}/{result.total_steps} enabled")

    if result.task_types:
        print(f"Tasks: {', '.join(result.task_types)}")

    print()
    print(result.message)


def main():
    parser = argparse.ArgumentParser(
        prog="auto-run",
        description="Workflow Automation MVP",
    )

    parser.add_argument("workflow", help="Path to workflow JSON contract")

    args = parser.parse_args()

    result = run_workflow(args.workflow)

    print_run_result(result)


if __name__ == "__main__":
    main()

# Workflow Automation MVP

A lightweight workflow automation layer for orchestrating reusable RADAR utility pipelines.

## Current Status

M1 Bootstrap                    ✅
M2 Workflow Contract            ✅
M3 Task Registry                ✅
M4 Local Workflow Runner        ✅
M5 Document Pipeline Executor   ✅
M6 CLI Layer Expansion          ✅
M7 Knowledge Search Integration ✅
M8A Telegram Contract ✅
M8C Telegram Response Integration ✅

## Purpose

This utility will become the automation layer for the RADAR AI Utility Ecosystem.

It is designed to coordinate:

- Document Pipeline
- OCR
- Summary
- Knowledge Search
- Telegram Bot
- Future workflow runners

## Usage

```bash
auto-run workflows/sample.workflow.json
```
### Dry Run

```bash
auto-run workflows/sample.workflow.json --dry-run
```
### Run Workflow and Search

```bash
auto-run workflows/sample.workflow.json \
  --publish \
  --search "Workflow"
```

### Mock Telegram Commands

```bash
python - <<'PY'
from workflow_automation.telegram import handle_mock_telegram_command

print(handle_mock_telegram_command("/workflow help"))
PY
```

```bash
python - <<'PY'
from workflow_automation.telegram import handle_mock_telegram_command

print(
    handle_mock_telegram_command(
        "/run workflows/sample.workflow.json --dry-run"
    )
)
PY
```
### Compact Telegram Response

```bash
python - <<'PY'
from workflow_automation.telegram import handle_mock_telegram_command

print(
    handle_mock_telegram_command(
        "/run workflows/sample.workflow.json --dry-run",
        compact=True,
    )
)
PY
```

## Features

- CLI command: `auto-run`
- JSON workflow contract loading
- Workflow step validation
- Workflow options parsing
- Task registry
- Supported task type validation
- Workflow execution placeholder
- Pytest foundation
- Document Pipeline executor
- Executes `doc-pipe --batch` from workflow steps
- Workflow JSON/Markdown export options
- Workflow publish option
- CLI target override
- CLI export JSON override
- CLI export Markdown override
- CLI publish override
- Dry-run workflow validation
- Telegram workflow request contract
- Telegram-style `/run` command parser
- Workflow response formatter for chat interfaces
- Mock Telegram command router
- `/workflow help` command
- `/workflow status` command
- `/run` command routing
- Compact Telegram workflow response
- Status icons for chat output
- Search result summary formatting
- Compact mode for mock Telegram command handler

## Roadmap

* [x] M1 Bootstrap
* [x] M2 Workflow Contract
* [x] M3 Task Registry
* [x] M4 Local Workflow Runner
* [x] M5 Document Pipeline Executor
* [x] M6 CLI Layer Expansion
* [x] M7 Knowledge Search Integration
- [x] M8 Telegram Trigger
- [x] M8B Mock Telegram Command
- [x] M8C Telegram Response Integration
* [ ] M9 Packaging & README
* [ ] M10 v0.1.0 Release

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Workflow Automation MVP

A lightweight workflow automation layer for orchestrating reusable RADAR utility pipelines.

## Current Status

M9 Packaging & README Finalization.

## Purpose

This utility is the automation layer for the RADAR AI Utility Ecosystem.

It coordinates reusable local utilities such as:

- Document Pipeline
- OCR
- Summary
- Knowledge Search
- Telegram-facing command handlers
- Future workflow runners

## Features

- CLI command: `auto-run`
- JSON workflow contract loading
- Workflow step validation
- Workflow options parsing
- Task registry
- Supported task type validation
- Local workflow runner
- Step execution results
- Document Pipeline executor
- Executes `doc-pipe --batch` from workflow steps
- Workflow JSON export option
- Workflow Markdown export option
- Workflow publish option
- Knowledge Search index step
- Post-workflow search query
- `radar-search index` integration
- `radar-search search` integration
- Telegram workflow request contract
- Telegram-style `/run` command parser
- Mock Telegram command router
- `/workflow help` command
- `/workflow status` command
- Compact Telegram workflow response
- Status icons for chat output
- Search result summary formatting
- Pytest coverage

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

## Local Utility Dependencies

This MVP can orchestrate other local RADAR utilities.

Install Document Pipeline:

```bash
pip install -e ../document_pipeline_mvp
```

Install Knowledge Search:

```bash
pip install -e ../radar_knowledge_search
```

Verify CLI commands:

```bash
which auto-run
which doc-pipe
which radar-search
```

## Usage

### Run Workflow

```bash
auto-run workflows/sample.workflow.json
```

### Dry Run

```bash
auto-run workflows/sample.workflow.json --dry-run
```

### Override Target and Options

```bash
auto-run workflows/sample.workflow.json \
  --target data/custom_docs \
  --export-json \
  --export-markdown \
  --publish
```

### Run Workflow and Search

```bash
auto-run workflows/sample.workflow.json \
  --publish \
  --search "Workflow"
```

## Mock Telegram Commands

### Help

```bash
python - <<'PY'
from workflow_automation.telegram import handle_mock_telegram_command

print(handle_mock_telegram_command("/workflow help"))
PY
```

### Status

```bash
python - <<'PY'
from workflow_automation.telegram import handle_mock_telegram_command

print(handle_mock_telegram_command("/workflow status"))
PY
```

### Dry Run from Mock Telegram Command

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
        "/run workflows/sample.workflow.json --publish --search Workflow",
        compact=True,
    )
)
PY
```

## Workflow Contract Example

```json
{
  "name": "sample-document-workflow",
  "description": "Process a document folder through RADAR automation.",
  "target": "data/input_docs",
  "steps": [
    {
      "name": "detect_documents",
      "type": "detect",
      "enabled": true
    },
    {
      "name": "run_document_pipeline",
      "type": "pipeline",
      "enabled": true
    },
    {
      "name": "publish_to_knowledge_search",
      "type": "publish",
      "enabled": true
    },
    {
      "name": "index_knowledge_search",
      "type": "index",
      "enabled": true
    }
  ],
  "options": {
    "export_json": true,
    "export_markdown": true,
    "publish": true
  }
}
```

## Supported Task Types

| Task Type | Purpose |
|---|---|
| `detect` | Validate and acknowledge workflow target |
| `pipeline` | Run Document Pipeline |
| `publish` | Publish processed documents |
| `index` | Index published documents with Knowledge Search |

## Architecture

```text
Telegram / CLI
    ↓
Command Parser
    ↓
Workflow Contract
    ↓
Task Registry
    ↓
Local Workflow Runner
    ↓
Document Pipeline
    ↓
Published Documents
    ↓
Knowledge Search Index
    ↓
Knowledge Search Query
```

## Project Structure

```text
workflow_automation_mvp/
├── data/
├── outputs/
├── tests/
├── workflow_automation/
│   ├── cli.py
│   ├── executor.py
│   ├── knowledge_executor.py
│   ├── pipeline_executor.py
│   ├── registry.py
│   ├── runner.py
│   ├── telegram.py
│   └── workflow.py
├── workflows/
│   └── sample.workflow.json
├── pyproject.toml
└── README.md
```

## Tests

```bash
pytest
```

Current expected status:

```text
41 passed
```

## Roadmap

- [x] M1 Bootstrap
- [x] M2 Workflow Contract
- [x] M3 Task Registry
- [x] M4 Local Workflow Runner
- [x] M5 Document Pipeline Executor
- [x] M6 CLI Layer Expansion
- [x] M7 Knowledge Search Integration
- [x] M8A Telegram Contract
- [x] M8B Mock Telegram Command
- [x] M8C Telegram Response Integration
- [x] M9 Packaging & README Finalization
- [ ] M10 v0.1.0 Release

## Release Status

Current release candidate:

```text
v0.1.0-rc
```

## License

MIT optional.

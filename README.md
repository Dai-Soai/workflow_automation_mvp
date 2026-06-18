# Workflow Automation MVP

A lightweight workflow automation layer for orchestrating reusable RADAR utility pipelines.

## Current Status

M6 CLI Layer Expansion.

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

## Roadmap

* [x] M1 Bootstrap
* [x] M2 Workflow Contract
* [x] M3 Task Registry
* [x] M4 Local Workflow Runner
* [x] M5 Document Pipeline Executor
* [x] M6 CLI Layer Expansion
* [ ] M7 Knowledge Search Integration
* [ ] M8 Telegram Trigger
* [ ] M9 Packaging & README
* [ ] M10 v0.1.0 Release

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

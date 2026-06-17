# Workflow Automation MVP

A lightweight workflow automation layer for orchestrating reusable RADAR utility pipelines.

## Current Status

M2 Workflow Contract.

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

## Features

- CLI command: auto-run
- JSON workflow contract loading
- Workflow step validation
- Workflow options parsing
- Workflow execution placeholder
- Pytest foundation

## Roadmap

* [x] M1 Bootstrap
* [x] M2 Workflow Contract
* [ ] M3 Task Registry
* [ ] M4 Local Workflow Runner
* [ ] M5 Document Pipeline Executor
* [ ] M6 CLI Layer Expansion
* [ ] M7 Knowledge Search Integration
* [ ] M8 Telegram Trigger
* [ ] M9 Packaging & README
* [ ] M10 v0.1.0 Release

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

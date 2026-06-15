# Workflow Automation MVP

A lightweight workflow automation layer for orchestrating reusable RADAR utility pipelines.

## Current Status

M1 Bootstrap.

## Purpose

This utility will become the automation layer for the RADAR AI Utility Ecosystem.

It is designed to coordinate:

- Document Pipeline
- OCR
- Summary
- Knowledge Search
- Telegram Bot
- Future workflow runners

## Features

- CLI command: `auto-run`
- Basic workflow spec loading
- Workflow placeholder execution
- Pytest foundation

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

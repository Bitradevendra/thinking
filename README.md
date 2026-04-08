# Thinking

A long-form reasoning engine that treats difficult problems like exploration tasks, not one-shot prompts.

## Why This Repo Feels Different

`thinking` is built around depth. Instead of asking an LLM for a single answer and stopping there, it uses branching search, logging, symbolic checks, and session artifacts to make reasoning feel like a process you can inspect.

## What It Does

- runs multi-branch Tree of Thoughts style exploration
- uses DeepSeek-backed reasoning calls
- supports file attachments as extra context
- logs session details, outputs, and reasoning artifacts for later review

## Project Structure

```text
thinking/
|-- main.py
|-- tree_of_thoughts.py
|-- llm_client.py
|-- cas_solver.py
|-- logger.py
|-- config.py
|-- web_server.py
|-- requirements.txt
`-- README.md
```

## Requirements

- Python 3.8+
- a valid `DEEPSEEK_API_KEY`

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Set the API key in PowerShell:

```bash
$env:DEEPSEEK_API_KEY="your-api-key"
```

## Run Locally

Basic reasoning session:

```bash
python main.py "Solve x^2 + 5x + 6 = 0"
```

Use files as context:

```bash
python main.py "Analyze this code" --files main.py config.py
```

## How It Works

- `main.py` creates and runs a reasoning session
- `tree_of_thoughts.py` grows and prunes the search tree
- `llm_client.py` handles model calls
- `cas_solver.py` verifies symbolic reasoning when needed
- `logger.py` stores the full session trail in `logs/`

## Best Fit

This is for people who want the reasoning trail, not just the final answer.

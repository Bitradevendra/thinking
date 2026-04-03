# thinking

`thinking` is an advanced Python reasoning system that combines Tree of Thoughts search, DeepSeek-based evaluation, file attachments, and structured session logging.

## Overview

The project is designed for long-form reasoning sessions with branching search, external LLM calls, and saved outputs for review.

## Project Structure

```text
thinking/
|-- main.py
|-- tree_of_thoughts.py
|-- llm_client.py
|-- cas_solver.py
|-- logger.py
|-- config.py
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

## Running The Project

Basic usage:

```bash
python main.py "Solve x^2 + 5x + 6 = 0"
```

With files:

```bash
python main.py "Analyze this code" --files main.py config.py
```

## How It Works

- `main.py` starts a reasoning session
- `tree_of_thoughts.py` expands and prunes reasoning branches
- `llm_client.py` handles LLM calls
- `cas_solver.py` verifies symbolic math where needed
- `logger.py` writes session artifacts to `logs/`

# thinking

`thinking` is an advanced Python reasoning system that combines Tree of Thoughts search, DeepSeek-based evaluation, file attachments, and structured session logging.

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Set the API key in PowerShell:

```bash
$env:DEEPSEEK_API_KEY="your-api-key"
```

## Use

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
- logs are written to `logs/`

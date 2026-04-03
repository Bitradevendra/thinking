# Quick Start Guide

## 1. Installation (First Time Only)

```bash
# Install dependencies
pip install -r requirements.txt
```

## 2. Set API Key

**Windows PowerShell:**
```powershell
$env:DEEPSEEK_API_KEY = "your-deepseek-api-key"
```

**Windows CMD:**
```cmd
set DEEPSEEK_API_KEY=your-deepseek-api-key
```

**Linux/Mac:**
```bash
export DEEPSEEK_API_KEY=your-deepseek-api-key
```

Or create a `.env` file (copy from `.env.example`).

## 3. Run Your First Problem

```bash
python main.py "What is 2 + 2?" --iterations 10
```

## Common Usage Patterns

### Simple Math Problem
```bash
python main.py "Solve: 2x + 5 = 15"
```

### Complex Problem with Extended Thinking
```bash
python main.py "Prove that sqrt(2) is irrational" --time 1800
```

### Code Analysis with File
```bash
python main.py "Review this code for bugs and optimization opportunities" --files examples/example_code.py
```

### Multiple Files
```bash
python main.py "Analyze the relationship between these files" --files file1.py file2.py data.json
```

### Custom Iterations
```bash
python main.py "Optimize this algorithm" --iterations 100
```

## Understanding the Output

During execution you'll see:
- **Progress bar** showing iterations completed
- **Real-time stats** (nodes explored, iteration rate)
- **Final summary** with statistics

After completion, check:
- `logs/session_YYYYMMDD_HHMMSS/final_result.txt` - Best solution
- `logs/session_YYYYMMDD_HHMMSS/summary.txt` - Session summary
- `logs/session_YYYYMMDD_HHMMSS/thought_tree.json` - Complete reasoning tree

## Tips

1. **Start small** - Test with `--iterations 10` first
2. **Use files wisely** - Only attach relevant context files
3. **Monitor progress** - Watch the iteration rate (should be ~2 iter/s)
4. **Check logs** - If results are unexpected, review the log files

## Troubleshooting

**"API key not set" error:**
- Set the environment variable as shown above
- Or edit `config.py` directly

**Slow performance:**
- Reduce number of iterations
- Reduce `TOT_BRANCHES_PER_NODE` in config.py
- Check internet connection (API calls)

**No mathematical verification:**
- Problem may not contain extractable math expressions
- Check `cas_computations.log` to see what was attempted

## Need Help?

1. Read the full `README.md`
2. Run `python setup.py` for guided setup
3. Check example problems in `examples/` directory
4. Review log files for detailed debugging info

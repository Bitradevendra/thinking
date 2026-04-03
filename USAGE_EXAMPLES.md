# Usage Examples and Command Reference

## Basic Commands

### Simple Problems

**Basic math:**
```bash
python main.py "What is 2 + 2?"
```

**Equation solving:**
```bash
python main.py "Solve: x^2 + 5x + 6 = 0"
```

**Simplification:**
```bash
python main.py "Simplify: (x^2 - 4)/(x - 2)"
```

---

## Control Options

### Iteration-Based (Recommended)

**Quick test (10 iterations, ~10 seconds):**
```bash
python main.py "Test problem" --iterations 10
```

**Medium depth (50 iterations, ~30 seconds):**
```bash
python main.py "Solve x^3 - 6x^2 + 11x - 6 = 0" --iterations 50
```

**Deep analysis (100 iterations, ~1 minute):**
```bash
python main.py "Prove the Pythagorean theorem" --iterations 100
```

### Time-Based

**30 minutes thinking:**
```bash
python main.py "Complex problem" --time 1800
```

**60 minutes thinking:**
```bash
python main.py "Very complex problem" --time 3600
```

---

## File Attachments

### Single File

**Text file:**
```bash
python main.py "Analyze this document" --files document.txt
```

**Python code:**
```bash
python main.py "Review this code" --files script.py
```

**PDF document:**
```bash
python main.py "Summarize this paper" --files research.pdf
```

### Multiple Files

**Multiple code files:**
```bash
python main.py "Review this project" --files main.py utils.py config.py
```

**Mixed file types:**
```bash
python main.py "Analyze this project" --files README.md code.py data.json
```

**Using examples:**
```bash
python main.py "Find bugs in this code" --files examples\example_code.py
```

---

## Problem Types

### Mathematics

**Algebra:**
```bash
python main.py "Factor: x^3 + 6x^2 + 11x + 6"
python main.py "Solve the system: x + y = 5, 2x - y = 1"
python main.py "Find all real solutions: x^4 - 5x^2 + 4 = 0"
```

**Calculus:**
```bash
python main.py "Find the derivative of x^3 * sin(x)"
python main.py "Integrate: x^2 * e^x"
python main.py "Find the limit as x approaches 0 of sin(x)/x"
```

**Proofs:**
```bash
python main.py "Prove that sqrt(2) is irrational" --iterations 100
python main.py "Prove the fundamental theorem of calculus" --time 1800
```

### Code Analysis

**Bug finding:**
```bash
python main.py "Find potential bugs in this code" --files buggy_code.py
```

**Optimization:**
```bash
python main.py "Suggest optimizations for this algorithm" --files slow_algorithm.py --iterations 50
```

**Code review:**
```bash
python main.py "Perform a code review" --files main.py utils.py --iterations 80
```

**Refactoring suggestions:**
```bash
python main.py "Suggest refactoring improvements" --files legacy_code.py --time 1800
```

### Document Analysis

**Summarization:**
```bash
python main.py "Provide a detailed summary of this document" --files report.pdf
```

**Multiple documents:**
```bash
python main.py "Compare and contrast these documents" --files doc1.txt doc2.txt doc3.txt
```

---

## Advanced Examples

### Complex Mathematical Problem

```bash
python main.py "Solve the differential equation: dy/dx = x*y, with initial condition y(0) = 1. Verify the solution." --iterations 80
```

### Multi-File Code Analysis

```bash
python main.py "Analyze the architecture of this project. Identify design patterns, potential issues, and improvement opportunities." --files main.py config.py utils.py database.py --iterations 100
```

### Research Paper Analysis

```bash
python main.py "Analyze this research paper. Identify the main contributions, methodology, and potential limitations." --files research_paper.pdf --time 2400
```

### Algorithm Design

```bash
python main.py "Design an efficient algorithm to find the longest palindromic substring in a string. Provide time and space complexity analysis." --iterations 60
```

### Proof Verification

```bash
python main.py "Verify this mathematical proof and identify any logical gaps: [paste proof here]" --iterations 50
```

---

## Combining Options

**Complex problem with files and extended thinking:**
```bash
python main.py "Analyze this codebase for security vulnerabilities" --files api.py auth.py database.py --time 3600
```

**Math problem with deep analysis:**
```bash
python main.py "Prove that there are infinitely many prime numbers" --iterations 100
```

**Quick file review:**
```bash
python main.py "Quick review of this code" --files script.py --iterations 20
```

---

## Getting Help

**Show help:**
```bash
python main.py --help
```

**View version/info:**
```bash
python main.py
```

---

## Output Examples

### Terminal Output (During Execution)

```
================================================================================
Advanced Reasoning System - Session Started
================================================================================
Session logs will be saved to: c:\Users\iamir\Downloads\thinking\logs\session_20260216_112000

Starting deep reasoning process...
Target: 50 iterations
Estimated time: 0.4 minutes

Reasoning |████████████████░░░░| 40/50 [00:20<00:05] {nodes: 120, rate: 2.0 it/s}
```

### Terminal Output (After Completion)

```
================================================================================
Reasoning Complete!
================================================================================
Time elapsed: 0.5 minutes
Total nodes explored: 150
Branches pruned: 45
Best solution score: 0.87

Results saved to: c:\Users\iamir\Downloads\thinking\logs\session_20260216_112000
================================================================================

Final Result Preview:
================================================================================
Step 0 (Score: 1.00):
Initial Problem Analysis: Solve: x^2 - 4 = 0

================================================================================Step 1 (Score: 0.92):
Factor the equation: (x-2)(x+2) = 0

================================================================================Step 2 (Score: 0.95):
Apply zero product property: x-2=0 or x+2=0

================================================================================Step 3 (Score: 0.98):
Solutions: x = 2 or x = -2

[CAS Verified: Both solutions check out]
================================================================================
```

---

## Log File Contents

After running, check these files in `logs/session_YYYYMMDD_HHMMSS/`:

### final_result.txt
```
Step 0 (Score: 1.00):
Initial Problem Analysis: Solve: x^2 - 4 = 0

Step 1 (Score: 0.92):
Factor the equation using difference of squares: (x-2)(x+2) = 0
...
```

### summary.txt
```
Advanced Reasoning System - Session Summary
================================================================================

Problem: Solve: x^2 - 4 = 0

Time Elapsed: 0.5 minutes
Total Iterations: 50
Total Nodes: 150
Branches Explored: 105
Branches Pruned: 45
Best Score: 0.87
...
```

### thought_tree.json
```json
{
  "session_start": "2026-02-16T11:20:00",
  "nodes": [
    {
      "node_id": 0,
      "parent_id": null,
      "depth": 0,
      "content": "Initial Problem Analysis...",
      "score": 1.0,
      "pruned": false
    },
    ...
  ]
}
```

---

## Tips for Best Results

### 1. Problem Clarity
❌ **Vague:** "Help me with math"
✅ **Clear:** "Solve the quadratic equation x^2 + 5x + 6 = 0 and verify all solutions"

### 2. Iteration Guidelines
- **Quick test:** 10 iterations
- **Simple problems:** 20-30 iterations
- **Medium complexity:** 50-80 iterations
- **Complex problems:** 100+ iterations or use time-based

### 3. File Attachments
- ✅ Attach only relevant files
- ✅ Keep files under 10MB each
- ✅ Use supported formats (.txt, .md, .py, .pdf, .json, .csv)
- ❌ Don't attach unnecessary files (slows processing)

### 4. Time vs Iterations
- **Iterations:** More predictable, consistent results
- **Time:** Better for very complex problems, less predictable

### 5. Review Logs
Always check the log files for:
- Complete reasoning path
- Why certain branches were pruned
- CAS verification results
- API responses

---

## Troubleshooting Common Issues

### Problem: API Key Error
```bash
# Error message
ValueError: Please set DEEPSEEK_API_KEY environment variable

# Solution
$env:DEEPSEEK_API_KEY = "your-actual-api-key"
```

### Problem: File Not Found
```bash
# Error message
Error: File not found: example.txt

# Solution - Use correct path
python main.py "Problem" --files examples\example_math.txt  # Windows
python main.py "Problem" --files examples/example_math.txt  # Linux/Mac
```

### Problem: Slow Performance
```bash
# Reduce iterations
python main.py "Problem" --iterations 20  # Instead of 100

# Or reduce branches in config.py
TOT_BRANCHES_PER_NODE = 2  # Instead of 3
```

### Problem: Low Quality Results
```bash
# Increase iterations
python main.py "Problem" --iterations 100

# Or increase thinking time
python main.py "Problem" --time 3600
```

---

## Windows-Specific Commands

### Using PowerShell Menu
```powershell
powershell -ExecutionPolicy Bypass -File run.ps1
```

### Setting API Key (PowerShell)
```powershell
$env:DEEPSEEK_API_KEY = "your-key-here"
```

### Setting API Key (CMD)  
```cmd
set DEEPSEEK_API_KEY=your-key-here
```

### File Paths (Windows)
```bash
# Use backslashes or forward slashes
python main.py "Problem" --files examples\example_code.py
python main.py "Problem" --files examples/example_code.py  # Also works
```

---

## Quick Reference Card

```
BASIC USAGE:
  python main.py "your problem here"

WITH FILES:
  python main.py "problem" --files file1.txt file2.py

SET ITERATIONS:
  python main.py "problem" --iterations 50

SET TIME:
  python main.py "problem" --time 1800

COMBINE:
  python main.py "problem" --files data.txt --iterations 100

HELP:
  python main.py --help

SETUP:
  python setup.py

INTERACTIVE (Windows):
  powershell -ExecutionPolicy Bypass -File run.ps1
```

---

**For more examples, see the `examples/` directory!**

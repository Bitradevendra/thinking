# Project Overview: Advanced Reasoning System

## 📁 Project Structure

```
thinking/
├── main.py                  # Entry point - CLI interface with progress bar
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── setup.py                 # Setup and testing script
│
├── Core Components/
│   ├── tree_of_thoughts.py # Tree-of-Thoughts controller (main algorithm)
│   ├── llm_client.py        # DeepSeek API client
│   ├── cas_solver.py        # SymPy Computer Algebra System
│   ├── logger.py            # Comprehensive logging system
│   ├── file_handler.py      # Multi-file input processing
│   └── formal_verifier.py   # Lean/Coq stub (future)
│
├── Documentation/
│   ├── README.md            # Full documentation
│   ├── QUICKSTART.md        # Quick start guide
│   └── .env.example         # Environment variable template
│
├── Examples/
│   └── examples/
│       ├── example_math.txt    # Sample math problem
│       ├── example_code.py     # Sample code for analysis
│       └── README.md           # Examples documentation
│
└── Logs/
    └── logs/                # Session logs (auto-created)
        └── session_YYYYMMDD_HHMMSS/
            ├── thought_tree.json      # Complete reasoning tree
            ├── api_responses.log      # All API calls
            ├── cas_computations.log   # Math verifications
            ├── summary.txt            # Session summary
            └── final_result.txt       # Best solution
```

## 🔧 Component Details

### 1. main.py (Entry Point)
- **Purpose:** CLI interface with clean progress bar
- **Features:**
  - Argument parsing (problem, files, time, iterations)
  - Session initialization
  - Progress tracking with tqdm
  - Result display and saving
- **Key Functions:**
  - `AdvancedReasoningSystem`: Main orchestrator class
  - `solve()`: Core solving method
  - `main()`: CLI entry point

### 2. tree_of_thoughts.py (Core Algorithm)
- **Purpose:** Implements Tree-of-Thoughts search
- **Features:**
  - Node creation and expansion
  - Branch scoring and pruning
  - CAS integration for verification
  - Best-first search algorithm
- **Key Classes:**
  - `ThoughtNode`: Represents a reasoning node
  - `TreeOfThoughts`: Main ToT controller
- **Key Methods:**
  - `create_node()`: Create reasoning nodes
  - `expand_node()`: Generate child branches
  - `score_node()`: Evaluate solutions
  - `search()`: Main search algorithm

### 3. llm_client.py (API Client)
- **Purpose:** DeepSeek API integration
- **Features:**
  - API request handling
  - Response parsing
  - Solution scoring
  - Branch generation
- **Key Methods:**
  - `generate_response()`: Get LLM responses
  - `score_solution()`: Score a solution path
  - `generate_branches()`: Create alternative approaches

### 4. cas_solver.py (Mathematical Verification)
- **Purpose:** SymPy integration for math operations
- **Features:**
  - Equation solving
  - Expression simplification
  - Step verification
  - Integration/differentiation
- **Key Methods:**
  - `solve_equation()`: Solve equations
  - `simplify_expression()`: Simplify expressions
  - `verify_step()`: Verify mathematical claims
  - `integrate()` / `differentiate()`: Calculus operations

### 5. logger.py (Logging System)
- **Purpose:** Comprehensive logging of all operations
- **Features:**
  - Structured log files
  - Tree structure tracking
  - API call logging
  - CAS computation logging
- **Output Files:**
  - `thought_tree.json`: Complete tree with all nodes
  - `api_responses.log`: All API requests/responses
  - `cas_computations.log`: All math verifications
  - `summary.txt`: Session statistics
  - `final_result.txt`: Best solution found

### 6. file_handler.py (File Input)
- **Purpose:** Handle multiple file inputs
- **Features:**
  - File validation
  - Multiple format support (txt, md, py, pdf, json, csv)
  - Size limits
  - Content extraction
- **Key Methods:**
  - `validate_file()`: Check file validity
  - `read_file()`: Read single file
  - `read_multiple_files()`: Read and combine multiple files

### 7. formal_verifier.py (Future Enhancement)
- **Purpose:** Formal verification with Lean/Coq
- **Status:** Stub implementation (planned feature)
- **Future Capabilities:**
  - Natural language to formal syntax translation
  - Proof verification
  - Syntax checking

### 8. config.py (Configuration)
- **Purpose:** System configuration
- **Settings:**
  - API credentials
  - ToT parameters (depth, branches, scoring)
  - Timing settings
  - File handling limits
  - CAS and formal verification options

## 🔄 Data Flow

```
User Input (CLI)
    ↓
main.py (Parse arguments, initialize system)
    ↓
file_handler.py (Process attached files)
    ↓
tree_of_thoughts.py (Create root node)
    ↓
┌─────────────────────────────────────────────┐
│ Main Search Loop (Tree of Thoughts)        │
│                                             │
│  1. Select highest-priority node           │
│      ↓                                      │
│  2. llm_client.py (Score current node)     │
│      ↓                                      │
│  3. cas_solver.py (Verify math steps)      │
│      ↓                                      │
│  4. Pruning decision                        │
│      ↓                                      │
│  5. llm_client.py (Generate branches)      │
│      ↓                                      │
│  6. Add branches to frontier               │
│      ↓                                      │
│  7. logger.py (Log all operations)         │
│      ↓                                      │
│  Repeat until time/iteration limit         │
└─────────────────────────────────────────────┘
    ↓
Return best solution path
    ↓
logger.py (Save final results)
    ↓
Display results to user
```

## 🧮 Algorithm: Tree of Thoughts

### Phase 1: Initialization
1. Parse problem and attached files
2. Create root node with initial analysis
3. Initialize priority queue (frontier)

### Phase 2: Search Loop
For each iteration:
1. **Select Node:** Pick highest-scored node from frontier
2. **Score Node:**
   - Extract mathematical expressions
   - Verify with CAS (SymPy)
   - Get LLM evaluation
   - Combine scores (LLM + CAS bonus/penalty)
3. **Prune Check:**
   - Score too low? Prune
   - Math verification failed? Prune
4. **Update Best Path:**
   - If current path better than best, update
5. **Expand Node:**
   - Generate N alternative branches (LLM)
   - Create child nodes
   - Add to frontier with priority scores

### Phase 3: Result Extraction
1. Retrieve best-scoring complete path
2. Format solution with step-by-step reasoning
3. Save to log files

## 📊 Scoring System

Each node receives a score from 0.0 to 1.0:

```python
Final Score = LLM Score + CAS Bonus/Penalty

Where:
- LLM Score: 0.0 - 1.0 (from DeepSeek evaluation)
- CAS Bonus: +0.2 if math verified correctly
- CAS Penalty: -0.3 if math verification failed
- Final Score: Clamped to [0.0, 1.0]
```

## 🎯 Key Features Implemented

✅ **Tree-of-Thoughts Search**
- Multi-branch exploration
- Best-first search
- Intelligent pruning

✅ **CAS Integration**
- Automatic math extraction
- SymPy verification
- Equation solving, simplification, calculus

✅ **LLM Integration**
- DeepSeek API for reasoning
- Branch generation
- Solution evaluation

✅ **File Attachments**
- Multiple file support
- PDF, code, text, JSON, CSV
- Context integration

✅ **Extended Thinking**
- 30-60 minute sessions
- Configurable iterations
- Time-based or iteration-based

✅ **Clean Interface**
- Progress bar (no verbose output)
- Real-time statistics
- Session summaries

✅ **Comprehensive Logging**
- All API calls logged
- Complete tree structure saved
- Math verifications tracked
- Final results preserved

## 🚀 Usage Patterns

### 1. Mathematical Problem Solving
```bash
python main.py "Solve x^3 - 6x^2 + 11x - 6 = 0" --iterations 50
```
- CAS verifies each step
- Multiple solution approaches explored
- Final answer mathematically verified

### 2. Code Analysis
```bash
python main.py "Find bugs in this code" --files buggy_code.py --time 1800
```
- Code context loaded
- Multiple analysis branches
- 30 minutes thinking time

### 3. Proof Verification
```bash
python main.py "Prove sqrt(2) is irrational" --iterations 100
```
- Mathematical proof steps
- CAS verification of claims
- Multiple proof strategies

### 4. Multi-File Analysis
```bash
python main.py "Analyze system architecture" --files main.py utils.py config.py
```
- All files loaded as context
- Cross-file analysis
- Comprehensive review

## 📝 Configuration Options

Edit `config.py` to customize:

```python
# Tree Structure
TOT_MAX_DEPTH = 5              # How deep the tree can grow
TOT_BRANCHES_PER_NODE = 3      # Alternatives per expansion
TOT_MIN_SCORE = 0.3            # Minimum score to survive

# Search Control
TOT_MAX_ITERATIONS = 100       # Hard limit on iterations

# Timing
MIN_THINKING_TIME = 1800       # Default: 30 minutes
MAX_THINKING_TIME = 3600       # Maximum: 60 minutes

# File Handling
MAX_FILE_SIZE = 10 * 1024 * 1024    # 10MB per file
SUPPORTED_FILE_TYPES = ['.txt', '.md', '.py', '.pdf', ...]
```

## 🔮 Future Enhancements

### Planned Features
1. **Formal Verification**
   - Lean 4 integration
   - Coq integration
   - Automated proof generation

2. **Additional CAS Engines**
   - Wolfram Alpha API
   - Mathematica integration
   - SageMath support

3. **Enhanced Interface**
   - Web UI
   - Interactive mode
   - Real-time visualization

4. **Advanced Features**
   - Multi-model ensemble
   - Adaptive branching
   - Learn from past sessions

## 🐛 Debugging

### Log File Locations
All logs in: `logs/session_YYYYMMDD_HHMMSS/`

**Quick Debug Checklist:**
1. Check `final_result.txt` for the answer
2. Check `summary.txt` for statistics
3. Check `api_responses.log` for API issues
4. Check `cas_computations.log` for math errors
5. Check `thought_tree.json` for full tree structure

### Common Issues
- **Low-quality results:** Increase iterations or thinking time
- **Too slow:** Reduce branches per node
- **Math not verified:** Check CAS log for errors
- **API errors:** Check API key and internet connection

## 📚 Dependencies

```
requests>=2.31.0   # HTTP requests for API
sympy>=1.12        # Computer Algebra System
tqdm>=4.66.0       # Progress bars
PyPDF2>=3.0.0      # PDF file support
```

## 🎓 Technical Notes

### Performance
- **Iteration rate:** ~2 iterations/second (depends on API latency)
- **Memory usage:** ~100-500MB (depends on tree size)
- **Disk usage:** ~1-10MB per session (logs)

### Scalability
- Horizontal: Can be parallelized (multiple branches)
- Vertical: Limited by API rate limits
- Storage: Log files grow linearly with iterations

---

**Last Updated:** 2026-02-16  
**Version:** 1.0  
**Status:** Production Ready

"""
Configuration settings for the Advanced Reasoning System
"""
import os
from datetime import datetime

# API Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

# Local LLM Configuration (llama.cpp)
ENABLE_LOCAL_LLM = True  # Set to True to auto-detect and use local model
LOCAL_LLM_URL = "http://localhost:8080/v1/chat/completions"  # Standard llama.cpp server URL
LOCAL_LLM_MODEL = "local-model"  # Name doesn't matter for local usually


# Tree of Thoughts Configuration - DEEP THINKING MODE
# Configured for 30+ minutes of intensive, edge-to-edge reasoning
TOT_MAX_DEPTH = 8  # Maximum depth of thought tree (deeper exploration)
TOT_BRANCHES_PER_NODE = 5  # Number of alternative branches to explore per node (more paths)
TOT_MIN_SCORE = 0.2  # Minimum score to keep a branch alive (lower threshold = more exploration)
TOT_MAX_ITERATIONS = 3600  # Maximum total iterations (~30 minutes at 2 iter/sec)

# Timing Configuration
MIN_THINKING_TIME = 30 * 60  # 30 minutes in seconds (1800 seconds)
MAX_THINKING_TIME = 60 * 60  # 60 minutes in seconds (3600 seconds)


# Logging Configuration
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def get_session_log_dir():
    """Create a new log directory for this session"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = os.path.join(LOG_DIR, f"session_{timestamp}")
    os.makedirs(session_dir, exist_ok=True)
    return session_dir

# File Input Configuration
SUPPORTED_FILE_TYPES = ['.txt', '.md', '.py', '.pdf', '.json', '.csv']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB per file

# CAS Configuration
CAS_ENGINE = "sympy"  # or "wolfram" if you have Wolfram API

# Formal Verification Configuration
FORMAL_VERIFIER = "lean"  # or "coq"
ENABLE_FORMAL_VERIFICATION = False  # Set to True when ready

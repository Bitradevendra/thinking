"""
Quick setup and test script for the Advanced Reasoning System
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    return result.returncode == 0


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   Advanced Reasoning System - Setup & Test Script       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ ERROR: Python 3.8 or higher is required")
        return
    
    print("✅ Python version OK")
    
    # Install requirements
    print("\n" + "="*60)
    choice = input("Install/update requirements? (y/n): ").strip().lower()
    if choice == 'y':
        success = run_command(
            f"{sys.executable} -m pip install -r requirements.txt",
            "Installing dependencies..."
        )
        if success:
            print("✅ Dependencies installed successfully")
        else:
            print("❌ Failed to install dependencies")
            return
    
    # Check API key
    print("\n" + "="*60)
    print("Checking DeepSeek API key...")
    print("="*60)
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        print("⚠️  WARNING: DEEPSEEK_API_KEY not set!")
        print("\nPlease set your API key:")
        print("  Windows PowerShell: $env:DEEPSEEK_API_KEY = 'your-key-here'")
        print("  Windows CMD: set DEEPSEEK_API_KEY=your-key-here")
        print("  Or edit config.py")
        
        choice = input("\nContinue anyway? (y/n): ").strip().lower()
        if choice != 'y':
            return
    else:
        print(f"✅ API key found: {api_key[:10]}...")
    
    # Run a simple test
    print("\n" + "="*60)
    choice = input("Run a quick test? (y/n): ").strip().lower()
    if choice == 'y':
        print("\nRunning test with 10 iterations (should take ~10-20 seconds)...")
        test_problem = "What is 2 + 2? Verify using basic arithmetic."
        
        success = run_command(
            f'{sys.executable} main.py "{test_problem}" --iterations 10',
            "Test Run"
        )
        
        if success:
            print("\n✅ Test completed!")
        else:
            print("\n❌ Test failed")
    
    # Show usage
    print("\n" + "="*60)
    print("Setup complete!")
    print("="*60)
    print("\nExample usage:")
    print("  python main.py \"Solve x^2 - 4 = 0\"")
    print("  python main.py \"Analyze this code\" --files example_code.py")
    print("  python main.py \"Your problem\" --time 1800 --files file1.txt file2.py")
    print("\nFor more examples, see README.md")
    print("For sample problems, check the examples/ directory")
    print("\nLogs will be saved to: logs/session_YYYYMMDD_HHMMSS/")
    print("")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

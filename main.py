"""
Main entry point for the Advanced Reasoning System
Provides a clean interface with progress bar
"""
import sys
import time
import argparse
from pathlib import Path
from typing import List
from tqdm import tqdm

from config import (
    get_session_log_dir, 
    MIN_THINKING_TIME, 
    MAX_THINKING_TIME,
    TOT_MAX_ITERATIONS
)
from logger import ReasoningLogger
from llm_client import DeepSeekClient
from cas_solver import CASSolver
from tree_of_thoughts import TreeOfThoughts
from file_handler import FileInputHandler
from formal_verifier import FormalVerifier


class AdvancedReasoningSystem:
    """Main system orchestrator"""
    
    def __init__(self):
        self.session_dir = get_session_log_dir()
        self.logger = ReasoningLogger(self.session_dir)
        
        print(f"\n{'='*80}")
        print(f"Advanced Reasoning System - Session Started")
        print(f"{'='*80}")
        print(f"Session logs will be saved to: {self.session_dir}\n")
        
        # Initialize components
        self.llm = DeepSeekClient(logger=self.logger)
        self.cas = CASSolver(logger=self.logger)
        self.file_handler = FileInputHandler()
        self.verifier = FormalVerifier(logger=self.logger)
        self.tot = TreeOfThoughts(self.llm, self.cas, self.logger)
        
    def solve(self, problem: str, file_paths: List[str] = None, 
             thinking_time: int = None, max_iterations: int = None):
        """
        Main solving method
        
        Args:
            problem: The problem to solve
            file_paths: Optional list of file paths to attach
            thinking_time: Target thinking time in seconds
            max_iterations: Maximum iterations (overrides thinking_time)
        """
        
        # Process attached files if any
        if file_paths:
            print(f"Processing {len(file_paths)} attached file(s)...")
            file_context = self.file_handler.create_context_from_files(file_paths)
            problem = file_context + "\n\nPROBLEM:\n" + problem
        
        # Determine iterations
        if max_iterations is None:
            if thinking_time is None:
                thinking_time = MIN_THINKING_TIME
            
            # Estimate iterations based on time (rough estimate: ~2 iterations per second)
            max_iterations = min(TOT_MAX_ITERATIONS, thinking_time * 2)
        
        print(f"\nStarting deep reasoning process...")
        print(f"Target: {max_iterations} iterations")
        print(f"Estimated time: {max_iterations / 2 / 60:.1f} minutes\n")
        
        # Progress tracking
        start_time = time.time()
        progress_data = {
            'iterations': 0,
            'nodes': 0,
            'last_update': start_time
        }
        
        # Create progress bar
        pbar = tqdm(
            total=max_iterations,
            desc="Reasoning",
            unit="iter",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            ncols=100
        )
        
        def progress_callback(iteration, total, num_nodes):
            """Update progress bar"""
            progress_data['iterations'] = iteration
            progress_data['nodes'] = num_nodes
            progress_data['last_update'] = time.time()
            
            # Update progress bar
            pbar.n = iteration
            pbar.set_postfix({
                'nodes': num_nodes,
                'rate': f"{iteration / (time.time() - start_time):.1f} it/s"
            })
            pbar.refresh()
        
        # Run Tree of Thoughts search
        try:
            result = self.tot.search(
                problem=problem,
                max_iterations=max_iterations,
                progress_callback=progress_callback
            )
        finally:
            pbar.close()
        
        # Calculate stats
        elapsed_time = time.time() - start_time
        stats = self.logger.get_stats()
        
        print(f"\n{'='*80}")
        print(f"Reasoning Complete!")
        print(f"{'='*80}")
        print(f"Time elapsed: {elapsed_time / 60:.1f} minutes")
        print(f"Total nodes explored: {stats['total_nodes']}")
        print(f"Branches pruned: {stats['branches_pruned']}")
        print(f"Best solution score: {self.tot.best_score:.2f}")
        print(f"\nResults saved to: {self.session_dir}")
        print(f"{'='*80}\n")
        
        # Save final results
        self.logger.log_final_result(result)
        
        summary = f"""
Advanced Reasoning System - Session Summary
{'='*80}

Problem:
{problem[:500]}{'...' if len(problem) > 500 else ''}

Time Elapsed: {elapsed_time / 60:.1f} minutes
Total Iterations: {progress_data['iterations']}
Total Nodes: {stats['total_nodes']}
Branches Explored: {stats['branches_explored']}
Branches Pruned: {stats['branches_pruned']}
Best Score: {self.tot.best_score:.2f}

Best Solution Path:
{result}

Log files:
- Thought Tree: {self.logger.tree_log_path}
- API Responses: {self.logger.api_log_path}
- CAS Computations: {self.logger.cas_log_path}
- Final Result: {self.logger.final_result_path}
"""
        
        self.logger.log_summary(summary)
        
        # Print result preview
        print("Final Result Preview:")
        print("="*80)
        preview_lines = result.split('\n')[:20]
        print('\n'.join(preview_lines))
        if len(result.split('\n')) > 20:
            print("...")
            print(f"\n(Full result saved to {self.logger.final_result_path})")
        print("="*80)
        
        return result


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Advanced Reasoning System with Tree of Thoughts, CAS verification, and formal methods",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple problem
  python main.py "Solve: x^2 + 5x + 6 = 0"
  
  # With file attachments
  python main.py "Analyze this code" --files code.py utils.py
  
  # Extended thinking time
  python main.py "Prove the Pythagorean theorem" --time 3600
  
  # Custom iterations
  python main.py "Optimize this algorithm" --iterations 200
        """
    )
    
    parser.add_argument(
        "problem",
        type=str,
        help="The problem or question to solve"
    )
    
    parser.add_argument(
        "-f", "--files",
        nargs="+",
        help="Files to attach as context (supports .txt, .md, .py, .pdf, .json, .csv)"
    )
    
    parser.add_argument(
        "-t", "--time",
        type=int,
        help=f"Target thinking time in seconds (default: {MIN_THINKING_TIME}, max: {MAX_THINKING_TIME})"
    )
    
    parser.add_argument(
        "-i", "--iterations",
        type=int,
        help=f"Maximum iterations (overrides --time, max: {TOT_MAX_ITERATIONS})"
    )
    
    args = parser.parse_args()
    
    # Validate file paths if provided
    if args.files:
        for file_path in args.files:
            if not Path(file_path).exists():
                print(f"Error: File not found: {file_path}")
                sys.exit(1)
    
    # Create and run system
    try:
        system = AdvancedReasoningSystem()
        system.solve(
            problem=args.problem,
            file_paths=args.files,
            thinking_time=args.time,
            max_iterations=args.iterations
        )
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

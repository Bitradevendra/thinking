"""
Logging system for the Advanced Reasoning System
All responses and intermediate steps are logged to files
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List


class ReasoningLogger:
    """Handles all logging for the reasoning process"""
    
    def __init__(self, session_dir: str):
        self.session_dir = session_dir
        self.tree_log_path = os.path.join(session_dir, "thought_tree.json")
        self.api_log_path = os.path.join(session_dir, "api_responses.log")
        self.cas_log_path = os.path.join(session_dir, "cas_computations.log")
        self.summary_path = os.path.join(session_dir, "summary.txt")
        self.final_result_path = os.path.join(session_dir, "final_result.txt")
        
        # Initialize tree structure
        self.tree_data = {
            "session_start": datetime.now().isoformat(),
            "nodes": [],
            "branches_explored": 0,
            "branches_pruned": 0
        }
        
    def log_api_request(self, request_data: Dict[str, Any], response_data: Dict[str, Any]):
        """Log API request and response"""
        with open(self.api_log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"REQUEST:\n{json.dumps(request_data, indent=2)}\n")
            f.write(f"RESPONSE:\n{json.dumps(response_data, indent=2)}\n")
    
    def log_cas_computation(self, problem: str, solution: str, verified: bool):
        """Log CAS computation"""
        with open(self.cas_log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Problem: {problem}\n")
            f.write(f"Solution: {solution}\n")
            f.write(f"Verified: {verified}\n")
    
    def log_tree_node(self, node_id: int, parent_id: int = None, 
                     content: str = "", score: float = 0.0, 
                     depth: int = 0, pruned: bool = False):
        """Log a node in the thought tree"""
        node = {
            "node_id": node_id,
            "parent_id": parent_id,
            "timestamp": datetime.now().isoformat(),
            "depth": depth,
            "content": content,
            "score": score,
            "pruned": pruned
        }
        self.tree_data["nodes"].append(node)
        
        if pruned:
            self.tree_data["branches_pruned"] += 1
        else:
            self.tree_data["branches_explored"] += 1
        
        # Save tree state
        self._save_tree()
    
    def _save_tree(self):
        """Save current tree state to file"""
        with open(self.tree_log_path, 'w', encoding='utf-8') as f:
            json.dump(self.tree_data, f, indent=2)
    
    def log_summary(self, summary: str):
        """Log session summary"""
        with open(self.summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
    
    def log_final_result(self, result: str):
        """Log final result"""
        with open(self.final_result_path, 'w', encoding='utf-8') as f:
            f.write(result)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics"""
        return {
            "total_nodes": len(self.tree_data["nodes"]),
            "branches_explored": self.tree_data["branches_explored"],
            "branches_pruned": self.tree_data["branches_pruned"],
            "session_dir": self.session_dir
        }

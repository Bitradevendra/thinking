"""
Tree of Thoughts Controller
Implements branching, scoring, and pruning of solution paths
"""
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from llm_client import DeepSeekClient
from cas_solver import CASSolver
from config import TOT_MAX_DEPTH, TOT_BRANCHES_PER_NODE, TOT_MIN_SCORE
import re


@dataclass
class ThoughtNode:
    """Represents a node in the thought tree"""
    node_id: int
    parent_id: Optional[int]
    depth: int
    content: str
    score: float
    pruned: bool = False
    cas_verified: bool = False
    children: List[int] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class TreeOfThoughts:
    """Tree of Thoughts controller for strategic reasoning"""
    
    def __init__(self, llm_client: DeepSeekClient, cas_solver: CASSolver, logger):
        self.llm = llm_client
        self.cas = cas_solver
        self.logger = logger
        
        self.nodes: Dict[int, ThoughtNode] = {}
        self.next_node_id = 0
        self.best_path: List[int] = []
        self.best_score: float = 0.0
        
    def create_node(self, content: str, parent_id: Optional[int] = None, 
                   score: float = 0.0, depth: int = 0) -> int:
        """Create a new thought node"""
        node_id = self.next_node_id
        self.next_node_id += 1
        
        node = ThoughtNode(
            node_id=node_id,
            parent_id=parent_id,
            depth=depth,
            content=content,
            score=score,
            children=[]
        )
        
        self.nodes[node_id] = node
        
        if parent_id is not None and parent_id in self.nodes:
            self.nodes[parent_id].children.append(node_id)
        
        # Log to file
        self.logger.log_tree_node(
            node_id=node_id,
            parent_id=parent_id,
            content=content,
            score=score,
            depth=depth,
            pruned=False
        )
        
        return node_id
    
    def extract_mathematical_expressions(self, text: str) -> List[str]:
        """Extract mathematical expressions from text for CAS verification"""
        expressions = []
        
        # Look for equations
        equation_pattern = r'([a-zA-Z0-9\s\+\-\*/\(\)\^]+=[a-zA-Z0-9\s\+\-\*/\(\)\^]+)'
        equations = re.findall(equation_pattern, text)
        expressions.extend(equations)
        
        # Look for expressions in common math notation
        # This is simplified - could be much more sophisticated
        expr_patterns = [
            r'∫\s*(.+?)\s*d[a-z]',  # Integrals
            r'd/d[a-z]\s*\((.+?)\)',  # Derivatives
            r'lim\s+.+?→.+?\s+(.+)',  # Limits
        ]
        
        for pattern in expr_patterns:
            matches = re.findall(pattern, text)
            expressions.extend(matches)
        
        return expressions
    
    def verify_with_cas(self, content: str) -> Dict[str, Any]:
        """Verify mathematical content with CAS"""
        expressions = self.extract_mathematical_expressions(content)
        
        if not expressions:
            return {"verified": True, "no_math": True}
        
        results = []
        all_verified = True
        
        for expr in expressions:
            # Try different CAS operations
            result = None
            
            if '=' in expr:
                result = self.cas.solve_equation(expr)
            else:
                result = self.cas.simplify_expression(expr)
            
            if result and result.get("success"):
                results.append(result)
            else:
                all_verified = False
        
        return {
            "verified": all_verified,
            "results": results,
            "no_math": False
        }
    
    def score_node(self, node_id: int, problem: str) -> float:
        """Score a node using LLM and CAS verification"""
        node = self.nodes[node_id]
        
        # First, try CAS verification
        cas_result = self.verify_with_cas(node.content)
        
        # If CAS verification failed, lower the score
        cas_bonus = 0.0
        if cas_result.get("verified"):
            cas_bonus = 0.2
        elif not cas_result.get("no_math"):
            cas_bonus = -0.3  # Penalty for failed math verification
        
        node.cas_verified = cas_result.get("verified", False)
        
        # Get LLM score
        cas_summary = ""
        if cas_result.get("results"):
            cas_summary = f"CAS Results: {cas_result['results']}"
        
        llm_score = self.llm.score_solution(problem, node.content, cas_summary)
        
        # Combine scores
        final_score = min(1.0, max(0.0, llm_score + cas_bonus))
        
        node.score = final_score
        return final_score
    
    def should_prune(self, node_id: int) -> bool:
        """Determine if a branch should be pruned"""
        node = self.nodes[node_id]
        
        # Prune if score too low
        if node.score < TOT_MIN_SCORE:
            return True
        
        # Prune if CAS verification explicitly failed
        if not node.cas_verified and not self.verify_with_cas(node.content).get("no_math"):
            return True
        
        return False
    
    def expand_node(self, node_id: int, problem: str, num_branches: int = None) -> List[int]:
        """Expand a node by generating child branches"""
        node = self.nodes[node_id]
        
        if num_branches is None:
            num_branches = TOT_BRANCHES_PER_NODE
        
        # Don't expand if too deep
        if node.depth >= TOT_MAX_DEPTH:
            return []
        
        # Don't expand pruned nodes
        if node.pruned:
            return []
        
        # Build current path context
        path_context = self.get_path_to_node(node_id)
        
        # Generate branches
        branches = self.llm.generate_branches(problem, path_context, num_branches)
        
        # Create child nodes
        child_ids = []
        for branch_content in branches:
            child_id = self.create_node(
                content=branch_content,
                parent_id=node_id,
                depth=node.depth + 1
            )
            child_ids.append(child_id)
        
        return child_ids
    
    def get_path_to_node(self, node_id: int) -> str:
        """Get the reasoning path from root to this node"""
        path = []
        current_id = node_id
        
        while current_id is not None:
            node = self.nodes[current_id]
            path.insert(0, f"[Step {node.depth}] {node.content}")
            current_id = node.parent_id
        
        return "\n\n".join(path)
    
    def get_best_path(self) -> str:
        """Get the best reasoning path found"""
        if not self.best_path:
            # Fallback to root node if available
            if 0 in self.nodes:
                return f"Initial Analysis Only (Tree search did not expand - likely API error):\n\n{self.nodes[0].content}"
            return "No solution found"
        
        path_parts = []
        for node_id in self.best_path:
            node = self.nodes[node_id]
            path_parts.append(f"Step {node.depth} (Score: {node.score:.2f}):\n{node.content}")
        
        return "\n\n" + "="*80 + "\n\n".join(path_parts)
    
    def update_best_path(self, node_id: int):
        """Update the best path if this node's path is better"""
        node = self.nodes[node_id]
        
        # Build path to this node
        path = []
        current_id = node_id
        total_score = 0.0
        
        while current_id is not None:
            path.insert(0, current_id)
            node_score = self.nodes[current_id].score
            total_score += node_score
            current_id = self.nodes[current_id].parent_id
        
        # USE TOTAL SCORE to encourage deeper chains of thought!
        # Previously used average, which penalized depth.
        if total_score > self.best_score:
            self.best_score = total_score
            self.best_path = path
    
    def search(self, problem: str, max_iterations: int, progress_callback=None) -> str:
        """
        Main search algorithm using Tree of Thoughts
        Returns the best solution found
        """
        if max_iterations is None:
            max_iterations = TOT_MAX_ITERATIONS
        
        # GENERATE INITIAL ANALYSIS using LLM instead of echoing text
        # Only use first 10k chars for initial prompt to be fast
        try:
            print("Generating initial analysis...")
            initial_prompt = f"Analyze this problem and outline a high-level approach:\n\n{problem[:10000]}..."
            initial_analysis_resp = self.llm.generate_response(initial_prompt, max_tokens=1000)
            
            if initial_analysis_resp["success"]:
                root_content = f"Initial Analysis:\n{initial_analysis_resp['content']}"
            else:
                error_msg = initial_analysis_resp.get('error', 'Unknown Error')
                root_content = f"Initial Problem Setup (Analysis Failed - Error: {error_msg}): {problem[:500]}..."
        except Exception as e:
            root_content = f"Initial Problem Setup (Exception: {str(e)}): {problem[:500]}..."

        # Create root node with LOW SCORE to ensure children are preferred
        root_id = self.create_node(
            content=root_content,
            depth=0,
            score=0.1  # Low score so any valid thought improves it
        )
        
        # Priority queue of nodes to explore (node_id, priority_score)
        frontier = [(root_id, 1.0)]
        iterations = 0
        
        print(f"DEBUG: Starting search with {len(frontier)} nodes and {max_iterations} max iterations")
        
        while frontier and iterations < max_iterations:
            iterations += 1
            if iterations % 10 == 0:
                print(f"Iteration {iterations}/{max_iterations}")
            
            # Get highest priority node
            frontier.sort(key=lambda x: x[1], reverse=True)
            current_id, _ = frontier.pop(0)
            current_node = self.nodes[current_id]
            
            # Skip if pruned
            if current_node.pruned:
                continue
            
            # Score the current node
            score = self.score_node(current_id, problem)
            
            # Check if should prune
            if self.should_prune(current_id):
                current_node.pruned = True
                self.logger.log_tree_node(
                    node_id=current_id,
                    parent_id=current_node.parent_id,
                    content=current_node.content,
                    score=score,
                    depth=current_node.depth,
                    pruned=True
                )
                continue
            
            # Update best path
            self.update_best_path(current_id)
            
            # Expand node
            child_ids = self.expand_node(current_id, problem)
            
            # Add children to frontier
            for child_id in child_ids:
                # Initial priority is parent's score (will be refined when evaluated)
                frontier.append((child_id, score * 0.9))
            
            # Progress callback
            if progress_callback:
                progress_callback(iterations, max_iterations, len(self.nodes))
        
        # Return best solution
        return self.get_best_path()

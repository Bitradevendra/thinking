"""
DeepSeek API Client for LLM interactions (with Local LLM Support)
"""
import requests
import json
from typing import Dict, Any, List, Optional
from config import (DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL, 
                   ENABLE_LOCAL_LLM, LOCAL_LLM_URL, LOCAL_LLM_MODEL)


class DeepSeekClient:
    """Client for interacting with DeepSeek API or Local LLM"""
    
    def __init__(self, api_key: str = None, logger = None):
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
        self.model = DEEPSEEK_MODEL
        self.logger = logger
        self.use_local = False
        
        # Check Local LLM availability if enabled
        if ENABLE_LOCAL_LLM:
            if self.check_local_availability():
                print(f"\n✅ LOCAL LLM DETECTED at {LOCAL_LLM_URL}")
                print(f"   Switching to Local Mode (No API costs!)")
                self.use_local = True
                self.api_url = LOCAL_LLM_URL
                self.model = LOCAL_LLM_MODEL
                self.api_key = "local-key"  # Dummy key required by some local servers
            else:
                print(f"\n⚠️ Local LLM not found at {LOCAL_LLM_URL}")
                print(f"   Falling back to DeepSeek API ({self.api_url})")
        
        # Only validate API key if NOT using local
        if not self.use_local:
            if not self.api_key or self.api_key == "your-api-key-here":
                raise ValueError("Please set DEEPSEEK_API_KEY environment variable or in config.py")
    
    def check_local_availability(self) -> bool:
        """Check if the local LLM server is reachable"""
        try:
            # Try a simple models list request to check connectivity
            # Note: standardized to /v1/models usually
            base_url = self.get_base_url(LOCAL_LLM_URL)
            test_url = f"{base_url}/models"
            
            response = requests.get(test_url, timeout=2)
            if response.status_code == 200:
                print(f"   Connected to Local LLM: {response.json()}")
                return True
            # Fallback: try chatting directly
            return self.test_chat_connection()
        except Exception as e:
            # print(f"   Local LLM Check Failed: {str(e)}")
            return False

    def get_base_url(self, url):
        """Extract base url from chat completion url"""
        if "/chat/completions" in url:
            return url.replace("/chat/completions", "")
        return url

    def test_chat_connection(self) -> bool:
        """Test if chat completion endpoint works"""
        try:
            requests.post(
                LOCAL_LLM_URL, 
                json={"messages": [{"role": "user", "content": "ping"}], "max_tokens": 1},
                timeout=2
            )
            return True # Even if 400 or error, server is there
        except:
            return False

    def generate_response(self, prompt: str, system_prompt: str = None, 
                         temperature: float = 0.7, max_tokens: int = 4000) -> Dict[str, Any]:
        """Generate a response from LLM"""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        request_data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if self.use_local:
            # Local models often need lower temp for reasoning
            request_data["temperature"] = 0.7 
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Increase timeout for local models as they can be slow
            timeout = 300 if self.use_local else 120
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=request_data,
                timeout=timeout
            )
            response.raise_for_status()
            response_data = response.json()
            
            # Log if logger is available
            if self.logger:
                self.logger.log_api_request(request_data, response_data)
            
            return {
                "success": True,
                "content": response_data["choices"][0]["message"]["content"],
                "usage": response_data.get("usage", {}),
                "raw_response": response_data
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg = f"{e} - Detail: {error_detail}"
                except:
                    pass
            
            error_response = {
                "success": False,
                "error": error_msg,
                "content": ""
            }
            
            if self.logger:
                self.logger.log_api_request(request_data, error_response)
            
            return error_response
    
    def score_solution(self, problem: str, solution: str, cas_result: str = None) -> float:
        """Score a solution branch using LLM reasoning"""
        
        prompt = f"""Evaluate this solution on a scale of 0.0 to 1.0.

Problem: {problem[:2000]}...

Proposed Solution: {solution}
"""
        if cas_result:
            prompt += f"\nCAS Verification Result: {cas_result}\n"
        
        prompt += """
Consider:
- Logical consistency
- Mathematical correctness
- Completeness
- CAS verification (if available)

Respond ONLY with a number between 0.0 and 1.0, nothing else."""

        response = self.generate_response(prompt, temperature=0.1, max_tokens=10)
        
        if response["success"]:
            try:
                # Clean up response (some local models might be chatty)
                content = response["content"].strip()
                # Find first number
                import re
                match = re.search(r"0\.[0-9]+|1\.0|0|1", content)
                if match:
                    score = float(match.group())
                    return max(0.0, min(1.0, score))
            except:
                return 0.5  # Default score if parsing fails
        
        return 0.5
    
    def generate_branches(self, problem: str, current_path: str, 
                         num_branches: int = 3) -> List[str]:
        """Generate multiple solution branches"""
        
        prompt = f"""Given this problem and current reasoning path, generate {num_branches} different next steps or approaches.

Problem: {problem[:2000]}...

Current Reasoning Path: {current_path}

Generate {num_branches} distinct next steps. Each should explore a different angle or approach.
Format: Number each step (1., 2., 3., etc.)"""

        response = self.generate_response(prompt, temperature=0.9, max_tokens=2000)
        
        if not response["success"]:
            return [f"Continue with standard approach: {current_path[:100]}..."]
        
        # Parse branches from response
        content = response["content"]
        branches = []
        
        for i in range(1, num_branches + 1):
            # Try to extract numbered items
            lines = content.split('\n')
            branch_content = []
            capturing = False
            
            for line in lines:
                if line.strip().startswith(f"{i}."):
                    capturing = True
                    branch_content.append(line)
                elif capturing and (line.strip().startswith(f"{i+1}.") or 
                                   (i == num_branches and not line.strip())):
                    break
                elif capturing:
                    branch_content.append(line)
            
            if branch_content:
                branches.append('\n'.join(branch_content).strip())
        
        # Fallback if parsing fails
        if len(branches) < num_branches:
            branches = content.split('\n\n')[:num_branches]
        
        return branches[:num_branches] if branches else ["Continue analysis"]

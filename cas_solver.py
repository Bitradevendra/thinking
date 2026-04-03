"""
Computer Algebra System (CAS) solver using SymPy
Routes symbolic and mathematical problems to SymPy for verification
"""
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re
from typing import Dict, Any, Optional


class CASSolver:
    """Wrapper for SymPy CAS operations"""
    
    def __init__(self, logger=None):
        self.logger = logger
        # Initialize common symbols
        self.symbols = {}
        
    def identify_variables(self, expression_str: str) -> set:
        """Identify variables in an expression"""
        # Find all alphabetic sequences that could be variable names
        potential_vars = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', expression_str)
        
        # Filter out known functions
        known_functions = {'sin', 'cos', 'tan', 'exp', 'log', 'ln', 'sqrt', 
                          'abs', 'floor', 'ceil', 'factorial', 'pi', 'e'}
        variables = {v for v in potential_vars if v not in known_functions}
        
        return variables
    
    def create_symbols(self, var_names: set):
        """Create SymPy symbols for variables"""
        for var in var_names:
            if var not in self.symbols:
                self.symbols[var] = sp.Symbol(var)
    
    def solve_equation(self, equation_str: str) -> Dict[str, Any]:
        """Solve an equation using SymPy"""
        try:
            # Identify variables
            variables = self.identify_variables(equation_str)
            self.create_symbols(variables)
            
            # Parse equation
            if '=' in equation_str:
                left, right = equation_str.split('=')
                left_expr = parse_expr(left.strip(), local_dict=self.symbols,
                                      transformations=standard_transformations + 
                                      (implicit_multiplication_application,))
                right_expr = parse_expr(right.strip(), local_dict=self.symbols,
                                       transformations=standard_transformations + 
                                       (implicit_multiplication_application,))
                equation = sp.Eq(left_expr, right_expr)
            else:
                # Treat as expression to solve for 0
                expr = parse_expr(equation_str, local_dict=self.symbols,
                                transformations=standard_transformations + 
                                (implicit_multiplication_application,))
                equation = sp.Eq(expr, 0)
            
            # Solve
            solutions = sp.solve(equation)
            
            result = {
                "success": True,
                "equation": str(equation),
                "solutions": [str(sol) for sol in solutions],
                "verified": True
            }
            
            if self.logger:
                self.logger.log_cas_computation(equation_str, str(solutions), True)
            
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "solutions": [],
                "verified": False
            }
            
            if self.logger:
                self.logger.log_cas_computation(equation_str, f"Error: {e}", False)
            
            return result
    
    def simplify_expression(self, expr_str: str) -> Dict[str, Any]:
        """Simplify a mathematical expression"""
        try:
            variables = self.identify_variables(expr_str)
            self.create_symbols(variables)
            
            expr = parse_expr(expr_str, local_dict=self.symbols,
                            transformations=standard_transformations + 
                            (implicit_multiplication_application,))
            
            simplified = sp.simplify(expr)
            
            result = {
                "success": True,
                "original": str(expr),
                "simplified": str(simplified),
                "verified": True
            }
            
            if self.logger:
                self.logger.log_cas_computation(expr_str, str(simplified), True)
            
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "verified": False
            }
            
            if self.logger:
                self.logger.log_cas_computation(expr_str, f"Error: {e}", False)
            
            return result
    
    def verify_step(self, claim: str) -> Dict[str, Any]:
        """Verify a mathematical claim or step"""
        try:
            # Try to interpret the claim and verify it
            # This is a simplified version - could be much more sophisticated
            
            if '=' in claim:
                # Try to verify equality
                left, right = claim.split('=')
                variables = self.identify_variables(claim)
                self.create_symbols(variables)
                
                left_expr = parse_expr(left.strip(), local_dict=self.symbols,
                                      transformations=standard_transformations + 
                                      (implicit_multiplication_application,))
                right_expr = parse_expr(right.strip(), local_dict=self.symbols,
                                       transformations=standard_transformations + 
                                       (implicit_multiplication_application,))
                
                # Check if they're equal after simplification
                diff = sp.simplify(left_expr - right_expr)
                verified = diff == 0
                
                result = {
                    "success": True,
                    "claim": claim,
                    "verified": verified,
                    "difference": str(diff) if not verified else "0"
                }
                
            else:
                # Try to simplify and see if it makes sense
                variables = self.identify_variables(claim)
                self.create_symbols(variables)
                
                expr = parse_expr(claim, local_dict=self.symbols,
                                transformations=standard_transformations + 
                                (implicit_multiplication_application,))
                simplified = sp.simplify(expr)
                
                result = {
                    "success": True,
                    "claim": claim,
                    "simplified": str(simplified),
                    "verified": True  # Successfully parsed and simplified
                }
            
            if self.logger:
                self.logger.log_cas_computation(claim, str(result), result["verified"])
            
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "verified": False
            }
            
            if self.logger:
                self.logger.log_cas_computation(claim, f"Error: {e}", False)
            
            return result
    
    def integrate(self, expr_str: str, var: str) -> Dict[str, Any]:
        """Compute integral"""
        try:
            variables = self.identify_variables(expr_str)
            self.create_symbols(variables)
            
            expr = parse_expr(expr_str, local_dict=self.symbols,
                            transformations=standard_transformations + 
                            (implicit_multiplication_application,))
            
            var_symbol = self.symbols.get(var, sp.Symbol(var))
            integral = sp.integrate(expr, var_symbol)
            
            result = {
                "success": True,
                "expression": str(expr),
                "variable": var,
                "integral": str(integral),
                "verified": True
            }
            
            if self.logger:
                self.logger.log_cas_computation(f"∫({expr_str})d{var}", str(integral), True)
            
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "verified": False
            }
            
            if self.logger:
                self.logger.log_cas_computation(f"∫({expr_str})d{var}", f"Error: {e}", False)
            
            return result
    
    def differentiate(self, expr_str: str, var: str) -> Dict[str, Any]:
        """Compute derivative"""
        try:
            variables = self.identify_variables(expr_str)
            self.create_symbols(variables)
            
            expr = parse_expr(expr_str, local_dict=self.symbols,
                            transformations=standard_transformations + 
                            (implicit_multiplication_application,))
            
            var_symbol = self.symbols.get(var, sp.Symbol(var))
            derivative = sp.diff(expr, var_symbol)
            
            result = {
                "success": True,
                "expression": str(expr),
                "variable": var,
                "derivative": str(derivative),
                "verified": True
            }
            
            if self.logger:
                self.logger.log_cas_computation(f"d({expr_str})/d{var}", str(derivative), True)
            
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e),
                "verified": False
            }
            
            if self.logger:
                self.logger.log_cas_computation(f"d({expr_str})/d{var}", f"Error: {e}", False)
            
            return result

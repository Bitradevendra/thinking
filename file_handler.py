"""
File input handler for attaching multiple files to the reasoning process
"""
import os
from typing import List, Dict, Any
from pathlib import Path
import PyPDF2


class FileInputHandler:
    """Handle multiple file inputs for the reasoning system"""
    
    def __init__(self, supported_types: List[str] = None, max_file_size: int = 10 * 1024 * 1024):
        self.supported_types = supported_types or ['.txt', '.md', '.py', '.pdf', '.json', '.csv']
        self.max_file_size = max_file_size
        
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a file before processing"""
        path = Path(file_path)
        
        if not path.exists():
            return {"valid": False, "error": "File does not exist"}
        
        if not path.is_file():
            return {"valid": False, "error": "Path is not a file"}
        
        if path.suffix.lower() not in self.supported_types:
            return {
                "valid": False, 
                "error": f"Unsupported file type. Supported: {', '.join(self.supported_types)}"
            }
        
        file_size = path.stat().st_size
        if file_size > self.max_file_size:
            return {
                "valid": False,
                "error": f"File too large ({file_size} bytes). Max: {self.max_file_size} bytes"
            }
        
        return {"valid": True, "size": file_size}
    
    def read_text_file(self, file_path: str) -> str:
        """Read a text-based file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    def read_pdf_file(self, file_path: str) -> str:
        """Read a PDF file"""
        try:
            text = []
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return "\n\n".join(text)
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read a file and return its content"""
        validation = self.validate_file(file_path)
        
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["error"],
                "content": ""
            }
        
        try:
            path = Path(file_path)
            
            if path.suffix.lower() == '.pdf':
                content = self.read_pdf_file(file_path)
            else:
                content = self.read_text_file(file_path)
            
            return {
                "success": True,
                "file_path": file_path,
                "file_name": path.name,
                "file_type": path.suffix,
                "content": content,
                "size": validation["size"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": ""
            }
    
    def read_multiple_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """Read multiple files and combine their content"""
        results = []
        all_content = []
        errors = []
        
        for file_path in file_paths:
            result = self.read_file(file_path)
            results.append(result)
            
            if result["success"]:
                header = f"\n\n{'='*80}\nFILE: {result['file_name']}\n{'='*80}\n\n"
                all_content.append(header + result["content"])
            else:
                errors.append(f"Error reading {file_path}: {result['error']}")
        
        combined_content = "\n\n".join(all_content)
        
        return {
            "success": len(errors) == 0,
            "files_processed": len([r for r in results if r["success"]]),
            "total_files": len(file_paths),
            "errors": errors,
            "combined_content": combined_content,
            "individual_results": results
        }
    
    def create_context_from_files(self, file_paths: List[str]) -> str:
        """Create a context string from multiple files to include in the problem"""
        result = self.read_multiple_files(file_paths)
        
        if not result["success"]:
            error_msg = "Some files could not be read:\n" + "\n".join(result["errors"])
            return error_msg
        
        header = f"""
The following content is from {result['files_processed']} attached file(s).
This context should be considered when reasoning about the problem.

{result['combined_content']}

END OF ATTACHED FILES
{'='*80}
"""
        return header

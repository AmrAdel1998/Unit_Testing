"""
AI Document Analyzer - Uses AI to understand requirements from documents
Supports OpenAI API and can be extended to other providers
"""

import os
import json
from typing import Dict, List, Optional


class AIDocumentAnalyzer:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize AI Document Analyzer
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY environment variable)
            model: Model to use (gpt-4o, gpt-4, etc.)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.use_ai = self.api_key is not None
        
        if not self.use_ai:
            print("Warning: No OpenAI API key found. Using fallback keyword extraction.")
            print("Set OPENAI_API_KEY environment variable or pass api_key to enable AI analysis.")

    def analyze_c_function(self, function_name: str, signature: str, source_code: str, related_docs: Optional[List[str]] = None) -> Dict:
        """
        Analyze a C function to infer behavior and produce unit test insights.
        Returns structured hints usable by the test generator:
        - purpose, inputs, outputs, side_effects
        - edge_cases, negative_cases
        - assertions: suggestions for validation
        """
        doc_context = "\n\n".join(related_docs or [])
        if not self.use_ai:
            # Fallback heuristics
            hints = {
                "purpose": f"Function {function_name} appears to implement logic based on its name.",
                "inputs": signature,
                "outputs": "Return value inferred from signature",
                "side_effects": "Unknown (fallback)",
                "edge_cases": [],
                "negative_cases": [],
                "assertions": []
            }
            # Simple patterns
            lname = function_name.lower()
            if lname.startswith('create_'):
                hints["purpose"] = "Creates and initializes a data structure"
                hints["assertions"].append("result is not None")
            if lname.startswith('destroy_'):
                hints["purpose"] = "Destroys/frees a data structure"
                hints["side_effects"] = "Memory deallocation"
                hints["assertions"].append("no crash on valid pointer")
                hints["assertions"].append("no crash on NULL pointer")
            if 'reverse' in lname or 'uppercase' in lname or 'lowercase' in lname:
                hints["purpose"] = "Mutates string buffer in-place"
                hints["assertions"].append("result is not None")
            if 'count' in lname:
                hints["purpose"] = "Counts occurrences"
                hints["assertions"].append("result is integer")
            return hints
        
        try:
            import openai
            openai.api_key = self.api_key
            prompt = f"""You are a senior C developer and white-box testing expert.
Analyze this C function's implementation and signature to identify all logic paths, boundary conditions, and potential vulnerabilities (e.g., NULL dereference, buffer overflow).

Function name: {function_name}
Signature: {signature}
Source code:
{source_code[:8000]}

Related requirements/context (if any):
{doc_context[:4000]}

Provide unit test insights to achieve 100% path coverage where possible:
- purpose: brief description of function goal
- inputs: specific values (normal, boundary, error) for each argument
- behavior: expected outcome for each input set
- edge_cases: specific scenarios like empty strings, max/min values, NULL pointers
- whitebox_paths: list of logical branches or conditions to test (e.g., 'if (ptr == NULL)', 'while loop iterations')
- assertion_hints: concrete Python assertion suggestions using 'result' or 'clib' state

Respond with valid JSON only:
{{
  "purpose": "...",
  "inputs": {{ "normal": [...], "boundary": [...], "error": [...] }},
  "behavior": "...",
  "edge_cases": [...],
  "whitebox_paths": [...],
  "assertion_hints": [...]
}}
"""
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a software testing architect specializing in C and white-box strategies. Respond with JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            result_text = response.choices[0].message.content
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            return json.loads(result_text)
        except Exception as e:
            # Check for invalid API key (401 error)
            error_str = str(e)
            if "invalid_api_key" in error_str or "Incorrect API key" in error_str or "401" in error_str:
                print(f"CRITICAL: Invalid OpenAI API key provided. Disabling AI features. Error: {e}")
                self.use_ai = False  # Switch to fallback mode permanently for this instance
            else:
                print(f"AI function analysis failed: {e}. Using fallback.")
            return self.analyze_c_function(function_name, signature, source_code, related_docs=related_docs or [])
    def analyze_document(self, document_text: str, document_name: str = "") -> Dict:
        """
        Analyze a document and extract requirements, test scenarios, and insights
        
        Args:
            document_text: Text content of the document
            document_name: Name of the document (optional)
            
        Returns:
            Dictionary with extracted information
        """
        if not self.use_ai:
            return self._fallback_analysis(document_text)
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""Analyze the following technical document and extract:
1. Functional requirements
2. Test scenarios and test cases
3. Edge cases and boundary conditions
4. Error handling requirements
5. Performance requirements (if any)

Document: {document_name}
Content:
{document_text[:8000]}  # Limit to avoid token limits

Provide a structured JSON response with:
- requirements: list of functional requirements
- test_scenarios: list of test scenarios
- edge_cases: list of edge cases
- error_handling: list of error handling requirements
- performance: list of performance requirements (if any)
"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a software testing expert. Extract requirements and test scenarios from technical documents. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content
            
            # Try to parse JSON from response
            try:
                # Extract JSON if wrapped in markdown code blocks
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0]
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0]
                
                result = json.loads(result_text)
                return result
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured text
                return {
                    "requirements": [result_text],
                    "test_scenarios": [],
                    "edge_cases": [],
                    "error_handling": [],
                    "analysis": result_text
                }
                
        except ImportError:
            print("OpenAI library not installed. Install with: pip install openai")
            return self._fallback_analysis(document_text)
        except Exception as e:
            # Check for invalid API key (401 error)
            error_str = str(e)
            if "invalid_api_key" in error_str or "Incorrect API key" in error_str or "401" in error_str:
                print(f"CRITICAL: Invalid OpenAI API key provided. Disabling AI features. Error: {e}")
                self.use_ai = False  # Switch to fallback mode permanently for this instance
            else:
                print(f"AI analysis failed: {e}. Using fallback analysis.")
            return self._fallback_analysis(document_text)
    
    def _fallback_analysis(self, document_text: str) -> Dict:
        """
        Fallback analysis using keyword extraction and simple heuristics
        """
        import re
        from utils import extract_requirements_from_text
        
        requirements = extract_requirements_from_text(document_text)
        
        # Extract test-related keywords
        test_keywords = re.findall(r'\b(test|testing|verify|validation|check|assert)\b', document_text, re.I)
        
        # Extract edge cases
        edge_case_patterns = [
            r'\b(edge case|boundary|limit|maximum|minimum|zero|null|empty)\b',
            r'\b(error|exception|failure|invalid)\b'
        ]
        edge_cases = []
        for pattern in edge_case_patterns:
            matches = re.findall(pattern, document_text, re.I)
            edge_cases.extend(matches)
        
        return {
            "requirements": requirements[:20],  # Limit to 20
            "test_scenarios": list(set(test_keywords))[:10],
            "edge_cases": list(set(edge_cases))[:10],
            "error_handling": [line for line in document_text.split('\n') if 'error' in line.lower() or 'exception' in line.lower()][:10],
            "analysis": "Fallback analysis using keyword extraction. Enable AI for better results."
        }
    
    def get_test_suggestions(self, function_signature: Dict, document_analysis: Dict) -> List[str]:
        """
        Generate test suggestions based on function signature and document analysis
        
        Args:
            function_signature: Dictionary with function info (name, args, return)
            document_analysis: Analysis result from analyze_document
            
        Returns:
            List of test suggestions
        """
        suggestions = []
        
        func_name = function_signature.get('name', '')
        func_args = function_signature.get('args', '')
        
        # Add suggestions based on requirements
        if document_analysis.get('requirements'):
            suggestions.append(f"Test {func_name} against requirements: {document_analysis['requirements'][0]}")
        
        # Add edge case suggestions
        if document_analysis.get('edge_cases'):
            suggestions.append(f"Test {func_name} with edge cases: {', '.join(document_analysis['edge_cases'][:3])}")
        
        # Add error handling suggestions
        if document_analysis.get('error_handling'):
            suggestions.append(f"Test {func_name} error handling scenarios")
        
        return suggestions


# Alternative: Use local LLM or other providers
class LocalAIAnalyzer:
    """Placeholder for local AI models (Ollama, etc.)"""
    def __init__(self):
        self.use_local = False
    
    def analyze_document(self, document_text: str) -> Dict:
        # Implement local AI analysis here
        return {"requirements": [], "test_scenarios": []}


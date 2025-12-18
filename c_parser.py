import os
from pycparser import c_parser, parse_file


class CProjectParser:
    def __init__(self, project_dir='.'):
        self.project_dir = project_dir

    def find_c_files(self):
        files = []
        for root, dirs, filenames in os.walk(self.project_dir):
            for fn in filenames:
                if fn.endswith('.c') or fn.endswith('.h'):
                    files.append(os.path.join(root, fn))
        return files

    def parse_project(self):
        # This is a simple approach: parse each .c file for function defs via pycparser
        parser = c_parser.CParser()
        functions = []
        
        # C keywords that should not be treated as functions
        c_keywords = {
            'for', 'if', 'while', 'do', 'switch', 'case', 'break', 'continue',
            'return', 'goto', 'else', 'elif', 'typedef', 'struct', 'union',
            'enum', 'const', 'static', 'extern', 'inline', 'volatile', 'register'
        }
        
        for filepath in self.find_c_files():
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    src = f.read()
                # pycparser expects preprocessed C. For many projects this will not work directly.
                # We'll use a naive regex fallback for simple extraction.
                import re
                # Improved pattern: match function definitions but exclude C keywords
                pattern = re.compile(r"([\w\*\s]+)\s+(\w+)\s*\(([^)]*)\)\s*\{", re.M)
                for m in pattern.finditer(src):
                    ret = m.group(1).strip()
                    name = m.group(2).strip()
                    args = m.group(3).strip()
                    
                    # Clean up return type (remove storage classes/qualifiers)
                    clean_ret = ret
                    for kw in ['static', 'const', 'inline', 'extern', 'volatile', 'register']:
                        clean_ret = re.sub(r'\b' + kw + r'\b', '', clean_ret)
                    clean_ret = clean_ret.strip()

                    # Skip if name is a C keyword
                    if name.lower() in c_keywords:
                        continue
                    
                    # Skip if return type contains keywords (likely not a function)
                    if any(keyword in ret.lower() for keyword in ['for', 'if', 'while', 'switch']):
                        continue
                    
                    # Skip if name starts with underscore and is likely a macro
                    if name.startswith('_') and name.isupper():
                        continue
                    
                    functions.append({'file': filepath, 'name': name, 'return': clean_ret, 'raw_return': ret, 'args': args})
            except Exception as e:
                print('Failed parse', filepath, e)
        return functions

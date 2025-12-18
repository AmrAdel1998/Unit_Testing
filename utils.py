# helper utilities go here (e.g., requirement extraction, simple NLP heuristics)

import re

def extract_requirements_from_text(text):
    # naive: lines that include words like "shall", "must", "should", "require"
    lines = text.splitlines()
    reqs = []
    for l in lines:
        if re.search(r'\b(shall|must|should|require)\b', l, re.I):
            reqs.append(l.strip())
    return reqs

"""Diagnostics and defensive coding verification for Pillar 1."""

import ast
import re
from typing import Dict, List
from pydantic import BaseModel, Field


class DiagnosticReport(BaseModel):
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    score: float = 100.0


class CodeDiagnostics:
    """Verifies that code written in client environments adheres to enterprise standards:

    - Syntactically valid Python
    - No hardcoded API keys or credentials
    - Defensive timeout and exception handling checks
    """

    @classmethod
    def analyze_python_code(cls, source_code: str) -> DiagnosticReport:
        errors = []
        warnings = []
        score = 100.0

        # 1. Syntax check via AST
        try:
            ast.parse(source_code)
        except SyntaxError as e:
            errors.append(f"Syntax Error: {e.msg} at line {e.lineno}")
            score -= 50.0

        # 2. Hardcoded secret heuristic
        secret_patterns = [
            r"""(?i)(api_key|secret|password|bearer|auth_token)\s*=\s*['"][a-zA-Z0-9_\-\.]{12,}['"]""",
            r"""sk-[a-zA-Z0-9]{20,}""",
        ]
        for pattern in secret_patterns:
            if re.search(pattern, source_code):
                errors.append("Security Alert: Detected possible hardcoded secret or API key.")
                score -= 30.0

        # 3. Timeout inspection in network calls
        if re.search(r"""(requests\.(get|post)|httpx\.(get|post))\(.*\)""", source_code):
            if "timeout=" not in source_code:
                warnings.append("Enterprise Reliability Warning: HTTP request without explicit timeout parameter.")
                score -= 10.0

        # 4. Bare except inspection
        if re.search(r"""except\s*:""", source_code):
            warnings.append("Reliability Warning: Bare 'except:' clause caught. Use specific exception types.")
            score -= 10.0

        score = max(0.0, score)
        return DiagnosticReport(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            score=score,
        )

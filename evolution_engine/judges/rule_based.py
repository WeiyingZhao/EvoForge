"""
Tier 1: Rule-Based Judge (Deterministic)

Ideal for coding, math, and data format tasks.
Uses Python assertions and regex patterns for validation.
"""
import re
import json
from typing import Dict, Any, List
from .base import BaseJudge


class RuleBasedJudge(BaseJudge):
    """
    Deterministic judge using explicit rules.

    Config format:
    {
        "rules": [
            {"type": "assert", "expression": "output['total'] > 0"},
            {"type": "regex", "pattern": r"^\d{4}-\d{2}-\d{2}$", "field": "date"},
            {"type": "json_schema", "schema": {...}},
            {"type": "python_test", "test_code": "assert len(output) > 0"}
        ]
    }
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.rules = config.get("rules", [])

    def evaluate(self, task: Dict[str, Any], output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate output against defined rules.

        Returns:
            {
                "score": float (0.0 to 1.0),
                "passed": bool,
                "failed_rules": list,
                "feedback": str
            }
        """
        results = []
        failed_rules = []

        for i, rule in enumerate(self.rules):
            rule_type = rule.get("type")
            passed = False

            try:
                if rule_type == "assert":
                    passed = self._check_assertion(rule["expression"], output)
                elif rule_type == "regex":
                    passed = self._check_regex(rule["pattern"], output, rule.get("field"))
                elif rule_type == "json_schema":
                    passed = self._check_json_schema(rule["schema"], output)
                elif rule_type == "python_test":
                    passed = self._run_python_test(rule["test_code"], output)
                else:
                    passed = False

                results.append(passed)

                if not passed:
                    failed_rules.append({"index": i, "rule": rule})

            except Exception as e:
                results.append(False)
                failed_rules.append({"index": i, "rule": rule, "error": str(e)})

        # Calculate score
        score = sum(results) / len(results) if results else 0.0

        return {
            "score": score,
            "passed": score == 1.0,
            "failed_rules": failed_rules,
            "total_rules": len(self.rules),
            "feedback": self.get_feedback(
                {"score": score, "failed_rules": failed_rules}
            ),
        }

    def _check_assertion(self, expression: str, output: Dict) -> bool:
        """Check Python assertion."""
        try:
            # Create safe evaluation context
            context = {"output": output}
            return eval(expression, {"__builtins__": {}}, context)
        except Exception:
            return False

    def _check_regex(self, pattern: str, output: Dict, field: str = None) -> bool:
        """Check regex pattern."""
        try:
            if field:
                value = str(output.get(field, ""))
            else:
                value = str(output)

            return bool(re.match(pattern, value))
        except Exception:
            return False

    def _check_json_schema(self, schema: Dict, output: Dict) -> bool:
        """Validate against JSON schema."""
        try:
            # TODO: Use jsonschema library for proper validation
            # For now, just check if it's valid JSON
            return isinstance(output, dict)
        except Exception:
            return False

    def _run_python_test(self, test_code: str, output: Dict) -> bool:
        """Run Python test code."""
        try:
            context = {"output": output}
            exec(test_code, {"__builtins__": {}}, context)
            return True
        except AssertionError:
            return False
        except Exception:
            return False

    def get_feedback(self, evaluation: Dict[str, Any]) -> str:
        """Generate feedback message."""
        score = evaluation.get("score", 0)
        failed_rules = evaluation.get("failed_rules", [])

        if score == 1.0:
            return "All validation rules passed successfully."

        feedback = f"Score: {score:.2%}. Failed rules:\n"
        for item in failed_rules:
            rule = item["rule"]
            feedback += f"- {rule.get('type')}: {rule.get('expression', rule.get('pattern', 'N/A'))}\n"

        return feedback

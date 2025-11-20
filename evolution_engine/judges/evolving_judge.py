"""
Tier 3: Evolving Judge (Advanced)

A dynamic judge that updates its own criteria over time.
Prevents agents from gaming static reward systems.
"""
from typing import Dict, Any, List
from .base import BaseJudge
import json


class EvolvingJudge(BaseJudge):
    """
    Self-improving judge that adapts its criteria.

    Config format:
    {
        "initial_rubric": "Initial evaluation criteria",
        "model": "gpt-4",
        "adaptation_threshold": 10,  # Number of evaluations before adapting
        "meta_prompt": "Analyze the evaluation history and suggest improvements"
    }
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.current_rubric = config.get("initial_rubric", "Evaluate output quality.")
        self.model = config.get("model", "gpt-4")
        self.adaptation_threshold = config.get("adaptation_threshold", 10)
        self.meta_prompt = config.get(
            "meta_prompt",
            "Analyze evaluation history and identify reward hacking patterns.",
        )

        # Track evaluation history
        self.evaluation_history: List[Dict] = []
        self.adaptations_made = 0

    def evaluate(self, task: Dict[str, Any], output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate using current rubric, and adapt if threshold reached.

        Returns:
            {
                "score": float,
                "feedback": str,
                "rubric_version": int,
                "adaptation_triggered": bool
            }
        """
        # Evaluate with current rubric
        eval_prompt = self._build_evaluation_prompt(task, output)

        # TODO: Call LLM API
        # response = llm_client.generate(eval_prompt, model=self.model)

        # Placeholder
        score = 0.75
        feedback = "Good output with room for improvement."

        evaluation = {
            "task": task,
            "output": output,
            "score": score,
            "feedback": feedback,
            "rubric_version": self.adaptations_made,
            "adaptation_triggered": False,
        }

        # Store in history
        self.evaluation_history.append(evaluation)

        # Check if adaptation is needed
        if len(self.evaluation_history) >= self.adaptation_threshold:
            self._adapt_rubric()
            evaluation["adaptation_triggered"] = True
            self.evaluation_history = []  # Reset history

        return evaluation

    def _adapt_rubric(self):
        """
        Analyze evaluation history and update rubric to close loopholes.

        This is the key feature that prevents reward hacking.
        """
        # Analyze recent evaluations
        analysis_prompt = f"""
You are a meta-evaluator analyzing a judge's performance.

**Current Rubric:**
{self.current_rubric}

**Recent Evaluations:**
{self._format_evaluation_history()}

**Task:**
1. Identify patterns where agents might be gaming the evaluation criteria
2. Suggest updates to the rubric to prevent reward hacking
3. Make the criteria more precise and robust

Provide the updated rubric as a JSON object:
{{
    "updated_rubric": "<new evaluation criteria>",
    "changes_made": ["list of changes"],
    "rationale": "why these changes prevent gaming"
}}
"""

        # TODO: Call LLM to generate updated rubric
        # response = llm_client.generate(analysis_prompt, model=self.model)

        # Placeholder - in real implementation, this would parse LLM response
        new_rubric = f"{self.current_rubric} Updated to prevent verbosity gaming."

        self.current_rubric = new_rubric
        self.adaptations_made += 1

        print(f"Judge adapted! Version {self.adaptations_made}: {new_rubric}")

    def _format_evaluation_history(self) -> str:
        """Format evaluation history for meta-analysis."""
        formatted = []
        for i, eval_item in enumerate(self.evaluation_history[-10:]):  # Last 10
            formatted.append(
                f"{i+1}. Score: {eval_item['score']:.2f}, "
                f"Task: {eval_item['task'].get('description', 'N/A')[:50]}..."
            )
        return "\n".join(formatted)

    def _build_evaluation_prompt(self, task: Dict[str, Any], output: Dict[str, Any]) -> str:
        """Build evaluation prompt using current rubric."""
        return f"""
Evaluate this agent output using the following rubric:

**Rubric (Version {self.adaptations_made}):**
{self.current_rubric}

**Task:**
{task.get('description', 'N/A')}

**Output:**
{json.dumps(output, indent=2)}

Provide score (0.0-1.0) and feedback.
"""

    def get_feedback(self, evaluation: Dict[str, Any]) -> str:
        """Get human-readable feedback."""
        feedback = evaluation.get("feedback", "")
        version = evaluation.get("rubric_version", 0)
        adapted = evaluation.get("adaptation_triggered", False)

        message = f"[Rubric v{version}] {feedback}"
        if adapted:
            message += "\n⚠️ Judge criteria updated to prevent gaming!"

        return message

    def get_rubric_history(self) -> List[str]:
        """Get history of all rubric versions."""
        # In a real implementation, we'd store all previous versions
        return [f"Version {self.adaptations_made}: {self.current_rubric}"]

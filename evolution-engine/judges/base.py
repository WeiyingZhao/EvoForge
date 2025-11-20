"""
Base Judge interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseJudge(ABC):
    """Abstract base class for all judges."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def evaluate(self, task: Dict[str, Any], output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate agent output for a given task.

        Args:
            task: The task that was attempted
            output: The agent's output

        Returns:
            Evaluation result with score, feedback, and metadata
        """
        pass

    @abstractmethod
    def get_feedback(self, evaluation: Dict[str, Any]) -> str:
        """
        Get human-readable feedback from evaluation.

        Args:
            evaluation: Evaluation result

        Returns:
            Feedback string
        """
        pass

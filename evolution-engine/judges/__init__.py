"""
Judge Factory - Evaluation mechanisms for agent outputs.
Implements three tiers: Rule-Based, LLM-as-a-Judge, and Evolving Judge.
"""
from .base import BaseJudge
from .rule_based import RuleBasedJudge
from .llm_judge import LLMJudge
from .evolving_judge import EvolvingJudge

__all__ = ["BaseJudge", "RuleBasedJudge", "LLMJudge", "EvolvingJudge"]


def create_judge(judge_type: str, config: dict) -> BaseJudge:
    """
    Factory function to create appropriate judge instance.

    Args:
        judge_type: One of "rule-based", "llm-judge", "evolving-judge"
        config: Judge configuration

    Returns:
        Judge instance
    """
    judges = {
        "rule-based": RuleBasedJudge,
        "llm-judge": LLMJudge,
        "evolving-judge": EvolvingJudge,
    }

    if judge_type not in judges:
        raise ValueError(f"Unknown judge type: {judge_type}")

    return judges[judge_type](config)

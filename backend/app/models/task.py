"""
Task and evaluation models.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship

from ..core.database import Base


class Task(Base):
    """
    A task for agent evaluation.
    Can be user-provided or synthetically generated.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))

    # Task content
    description = Column(Text)
    input_data = Column(JSON)
    expected_output = Column(JSON, nullable=True)  # Ground truth if available

    # Task metadata
    difficulty = Column(Float, default=1.0)  # 0.0 to 10.0
    category = Column(String, nullable=True)

    # Source
    source = Column(String)  # "user", "synthetic", "self-questioning"
    generated_by = Column(String, nullable=True)  # Model that generated it

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    results = relationship("TaskResult", back_populates="task")


class TaskResult(Base):
    """Result of an agent attempting a task."""

    __tablename__ = "task_results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    agent_variant_id = Column(Integer, ForeignKey("agent_variants.id"), nullable=True)

    # Execution
    agent_output = Column(JSON)
    execution_time_ms = Column(Float)

    # Evaluation
    is_success = Column(Boolean)
    score = Column(Float)  # 0.0 to 1.0
    judge_feedback = Column(Text, nullable=True)

    # Error handling
    error_occurred = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    task = relationship("Task", back_populates="results")

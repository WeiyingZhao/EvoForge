"""
Experience Memory Bank models - implements AgentEvolver's Self-Navigating mechanism.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from ..core.database import Base


class Experience(Base):
    """
    A lesson learned by the agent.
    Implements the Experience Pool from AgentEvolver.
    """

    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))

    # The task context
    task_description = Column(Text)
    task_category = Column(String, nullable=True)

    # What the agent did
    action_taken = Column(Text)  # The prompt/code the agent used

    # What happened
    outcome = Column(String)  # "success" or "failure"
    result_details = Column(JSON)

    # The lesson (natural language summary)
    lesson = Column(Text)  # e.g., "When joining tables, always check if the join key exists"

    # Vector embedding for similarity search
    embedding = Column(Vector(1536))  # OpenAI embedding dimension

    # Metadata for retrieval
    importance_score = Column(Float, default=1.0)  # Higher = more important
    times_retrieved = Column(Integer, default=0)
    last_retrieved_at = Column(DateTime, nullable=True)

    # Experience decay
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # User curation
    is_pinned = Column(Boolean, default=False)  # User marked as critical
    is_verified = Column(Boolean, default=False)  # User verified this is correct

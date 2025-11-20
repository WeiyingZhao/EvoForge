"""
Agent database models.
"""
from datetime import datetime
from typing import Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from ..core.database import Base


class Agent(Base):
    """Agent blueprint - the starting point of evolution."""

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Configuration
    role_prompt = Column(Text)  # Initial system prompt
    model_name = Column(String)  # e.g., "gpt-4", "claude-3-sonnet"
    tools_config = Column(JSON)  # Available tools/functions
    environment_config = Column(JSON)  # Sandbox settings

    # Evolution settings
    evolution_strategy = Column(String)  # "alpha-coder", "curiosity", "adversarial"
    evolution_layers = Column(JSON)  # Which layers to evolve: prompt, code, model

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    versions = relationship("AgentVersion", back_populates="agent")
    evolution_runs = relationship("EvolutionRun", back_populates="agent")


class AgentVersion(Base):
    """Versioned snapshot of an agent after evolution."""

    __tablename__ = "agent_versions"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    version = Column(String)  # e.g., "1.0", "1.1", "2.0"

    # Evolved components
    evolved_prompt = Column(Text)
    evolved_code = Column(Text, nullable=True)  # Python code if code evolution enabled
    evolved_weights_path = Column(String, nullable=True)  # Path to LoRA adapter

    # Performance metrics
    fitness_score = Column(Float)
    accuracy = Column(Float, nullable=True)

    # Metadata
    generation_number = Column(Integer)  # Which generation produced this
    parent_version_id = Column(Integer, ForeignKey("agent_versions.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship("Agent", back_populates="versions")
    parent = relationship("AgentVersion", remote_side=[id], backref="children")

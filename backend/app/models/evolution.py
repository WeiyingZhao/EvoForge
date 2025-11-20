"""
Evolution run database models.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Float, Text, Boolean
from sqlalchemy.orm import relationship

from ..core.database import Base


class EvolutionRun(Base):
    """A complete evolution session."""

    __tablename__ = "evolution_runs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))

    # Configuration
    strategy = Column(String)  # "alpha-coder", "curiosity", "adversarial"
    max_generations = Column(Integer)
    population_size = Column(Integer)
    mutation_rate = Column(Float)

    # Judge configuration
    judge_type = Column(String)  # "rule-based", "llm-judge", "evolving-judge"
    judge_config = Column(JSON)

    # Status
    status = Column(String)  # "running", "completed", "failed", "paused"
    current_generation = Column(Integer, default=0)

    # Results
    best_fitness = Column(Float, nullable=True)
    best_version_id = Column(Integer, ForeignKey("agent_versions.id"), nullable=True)

    # Metadata
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    # Relationships
    agent = relationship("Agent", back_populates="evolution_runs")
    generations = relationship("Generation", back_populates="evolution_run")


class Generation(Base):
    """A single generation in an evolution run."""

    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    evolution_run_id = Column(Integer, ForeignKey("evolution_runs.id"))
    generation_number = Column(Integer)

    # Metrics
    avg_fitness = Column(Float)
    best_fitness = Column(Float)
    worst_fitness = Column(Float)

    # Statistics
    num_variants = Column(Integer)
    num_successful = Column(Integer)
    num_failed = Column(Integer)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Float, nullable=True)

    # Relationships
    evolution_run = relationship("EvolutionRun", back_populates="generations")
    variants = relationship("AgentVariant", back_populates="generation")


class AgentVariant(Base):
    """A single agent variant in a generation (part of population)."""

    __tablename__ = "agent_variants"

    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(Integer, ForeignKey("generations.id"))

    # Content
    prompt = Column(Text)
    code = Column(Text, nullable=True)

    # Mutation info
    mutation_type = Column(String)  # "prompt_tweak", "code_rewrite", etc.
    parent_variant_id = Column(Integer, ForeignKey("agent_variants.id"), nullable=True)

    # Evaluation
    fitness_score = Column(Float, nullable=True)
    evaluation_result = Column(JSON, nullable=True)  # Detailed results
    is_successful = Column(Boolean, default=False)

    # Selection
    selected_for_next_gen = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    generation = relationship("Generation", back_populates="variants")
    parent = relationship("AgentVariant", remote_side=[id], backref="children")

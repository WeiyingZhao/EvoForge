"""
Agent management API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..core.database import get_db
from ..models.agent import Agent, AgentVersion

router = APIRouter()


# Pydantic schemas
class AgentCreate(BaseModel):
    name: str
    description: str | None = None
    role_prompt: str
    model_name: str
    tools_config: dict = {}
    environment_config: dict = {}
    evolution_strategy: str = "alpha-coder"
    evolution_layers: dict = {"prompt": True, "code": False, "model": False}


class AgentResponse(BaseModel):
    id: int
    name: str
    description: str | None
    role_prompt: str
    model_name: str
    evolution_strategy: str

    class Config:
        from_attributes = True


class AgentVersionResponse(BaseModel):
    id: int
    version: str
    fitness_score: float
    generation_number: int

    class Config:
        from_attributes = True


@router.post("/", response_model=AgentResponse)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent blueprint."""
    db_agent = Agent(**agent.model_dump())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.get("/", response_model=List[AgentResponse])
def list_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all agents."""
    agents = db.query(Agent).offset(skip).limit(limit).all()
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get agent by ID."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.get("/{agent_id}/versions", response_model=List[AgentVersionResponse])
def list_agent_versions(agent_id: int, db: Session = Depends(get_db)):
    """List all versions of an agent."""
    versions = (
        db.query(AgentVersion)
        .filter(AgentVersion.agent_id == agent_id)
        .order_by(AgentVersion.generation_number.desc())
        .all()
    )
    return versions


@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete an agent."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return {"message": "Agent deleted successfully"}

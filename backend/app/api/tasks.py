"""
Task management API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..core.database import get_db
from ..models.task import Task, TaskResult

router = APIRouter()


# Pydantic schemas
class TaskCreate(BaseModel):
    agent_id: int
    description: str
    input_data: dict
    expected_output: dict | None = None
    difficulty: float = 1.0
    category: str | None = None
    source: str = "user"


class TaskResponse(BaseModel):
    id: int
    agent_id: int
    description: str
    difficulty: float
    source: str

    class Config:
        from_attributes = True


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/agent/{agent_id}", response_model=List[TaskResponse])
def list_agent_tasks(agent_id: int, db: Session = Depends(get_db)):
    """List tasks for a specific agent."""
    tasks = db.query(Task).filter(Task.agent_id == agent_id).all()
    return tasks


@router.post("/generate-synthetic")
async def generate_synthetic_tasks(
    agent_id: int, num_tasks: int = 100, db: Session = Depends(get_db)
):
    """
    Generate synthetic tasks using Self-Questioning mechanism.
    Implements AgentEvolver's synthetic task generation.
    """
    # TODO: Implement synthetic task generation
    return {
        "message": f"Generating {num_tasks} synthetic tasks for agent {agent_id}",
        "status": "queued",
    }

"""
Experience Memory Bank API endpoints.
Implements AgentEvolver's Self-Navigating mechanism.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..core.database import get_db
from ..models.experience import Experience

router = APIRouter()


# Pydantic schemas
class ExperienceCreate(BaseModel):
    agent_id: int
    task_description: str
    action_taken: str
    outcome: str
    result_details: dict
    lesson: str
    task_category: str | None = None


class ExperienceResponse(BaseModel):
    id: int
    agent_id: int
    task_description: str
    lesson: str
    outcome: str
    importance_score: float
    is_pinned: bool

    class Config:
        from_attributes = True


@router.post("/", response_model=ExperienceResponse)
def create_experience(exp: ExperienceCreate, db: Session = Depends(get_db)):
    """Add a new experience to the memory bank."""
    # TODO: Generate embedding for similarity search
    db_exp = Experience(**exp.model_dump(), embedding=[0.0] * 1536)  # Placeholder
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp


@router.get("/agent/{agent_id}", response_model=List[ExperienceResponse])
def list_agent_experiences(
    agent_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)
):
    """List experiences for an agent."""
    experiences = (
        db.query(Experience)
        .filter(Experience.agent_id == agent_id, Experience.is_active == True)
        .order_by(Experience.importance_score.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return experiences


@router.post("/{experience_id}/pin")
def pin_experience(experience_id: int, db: Session = Depends(get_db)):
    """Pin an important experience (human-in-the-loop curation)."""
    exp = db.query(Experience).filter(Experience.id == experience_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")

    exp.is_pinned = True
    exp.importance_score = 10.0  # Max importance
    db.commit()
    return {"message": "Experience pinned"}


@router.delete("/{experience_id}")
def delete_experience(experience_id: int, db: Session = Depends(get_db)):
    """Delete a bad experience (human-in-the-loop curation)."""
    exp = db.query(Experience).filter(Experience.id == experience_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")

    exp.is_active = False
    db.commit()
    return {"message": "Experience deleted"}


@router.post("/search")
async def search_similar_experiences(
    agent_id: int, query: str, top_k: int = 5, db: Session = Depends(get_db)
):
    """
    Search for similar experiences using vector similarity.
    This implements the retrieval mechanism for Self-Navigating.
    """
    # TODO: Implement vector similarity search
    return {
        "message": f"Searching for top {top_k} similar experiences",
        "query": query,
        "results": [],
    }

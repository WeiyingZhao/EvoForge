"""
Evolution run API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from pydantic import BaseModel
import json
import asyncio

from ..core.database import get_db
from ..models.evolution import EvolutionRun, Generation
from ..models.agent import Agent

router = APIRouter()


# Pydantic schemas
class EvolutionRunCreate(BaseModel):
    agent_id: int
    strategy: str = "alpha-coder"
    max_generations: int = 100
    population_size: int = 50
    mutation_rate: float = 0.3
    judge_type: str = "rule-based"
    judge_config: dict = {}


class EvolutionRunResponse(BaseModel):
    id: int
    agent_id: int
    strategy: str
    status: str
    current_generation: int
    max_generations: int
    best_fitness: float | None

    class Config:
        from_attributes = True


class GenerationResponse(BaseModel):
    id: int
    generation_number: int
    avg_fitness: float
    best_fitness: float
    num_variants: int

    class Config:
        from_attributes = True


@router.post("/", response_model=EvolutionRunResponse)
async def create_evolution_run(run: EvolutionRunCreate, db: Session = Depends(get_db)):
    """Start a new evolution run."""
    # Verify agent exists
    agent = db.query(Agent).filter(Agent.id == run.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Create evolution run
    db_run = EvolutionRun(
        agent_id=run.agent_id,
        strategy=run.strategy,
        max_generations=run.max_generations,
        population_size=run.population_size,
        mutation_rate=run.mutation_rate,
        judge_type=run.judge_type,
        judge_config=run.judge_config,
        status="initialized",
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)

    # TODO: Trigger Ray evolution engine asynchronously
    # This will be implemented in the evolution engine module

    return db_run


@router.post("/{run_id}/start")
async def start_evolution_run(run_id: int, db: Session = Depends(get_db)):
    """Start an initialized evolution run."""
    run = db.query(EvolutionRun).filter(EvolutionRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Evolution run not found")

    if run.status != "initialized":
        raise HTTPException(
            status_code=400, detail=f"Cannot start run with status: {run.status}"
        )

    run.status = "running"
    db.commit()

    # TODO: Trigger Ray evolution engine
    return {"message": "Evolution run started", "run_id": run_id}


@router.get("/{run_id}", response_model=EvolutionRunResponse)
def get_evolution_run(run_id: int, db: Session = Depends(get_db)):
    """Get evolution run details."""
    run = db.query(EvolutionRun).filter(EvolutionRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Evolution run not found")
    return run


@router.get("/{run_id}/generations", response_model=List[GenerationResponse])
def list_generations(run_id: int, db: Session = Depends(get_db)):
    """List all generations in an evolution run."""
    generations = (
        db.query(Generation)
        .filter(Generation.evolution_run_id == run_id)
        .order_by(Generation.generation_number)
        .all()
    )
    return generations


@router.post("/{run_id}/pause")
def pause_evolution_run(run_id: int, db: Session = Depends(get_db)):
    """Pause a running evolution."""
    run = db.query(EvolutionRun).filter(EvolutionRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Evolution run not found")

    run.status = "paused"
    db.commit()
    return {"message": "Evolution run paused"}


@router.websocket("/{run_id}/stream")
async def evolution_stream(websocket: WebSocket, run_id: int):
    """WebSocket endpoint for real-time evolution updates."""
    await websocket.accept()

    try:
        # TODO: Connect to Ray evolution engine and stream updates
        while True:
            # Placeholder - will be replaced with real-time updates
            data = {
                "type": "generation_update",
                "generation": 1,
                "best_fitness": 0.75,
                "avg_fitness": 0.65,
            }
            await websocket.send_json(data)
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass

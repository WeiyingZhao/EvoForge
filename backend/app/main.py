"""
EvoForge FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.database import init_db
from .api import agents, evolution, tasks, experiences

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Self-Evolving AI Agent Platform",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include API routers
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(evolution.router, prefix="/api/evolution", tags=["evolution"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(experiences.router, prefix="/api/experiences", tags=["experiences"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
    )

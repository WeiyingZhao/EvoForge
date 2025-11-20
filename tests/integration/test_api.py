"""
Integration tests for API endpoints.
Tests agent creation, evolution runs, task generation, and export/import.
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from backend.app.main import app
from backend.app.core.database import Base, engine

# Create test client
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Setup test database before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestAgentAPI:
    """Test agent management API."""

    def test_create_agent(self, setup_database):
        """Test creating a new agent."""
        agent_data = {
            "name": "TestAgent",
            "description": "A test agent",
            "role_prompt": "You are a helpful assistant",
            "model_name": "gpt-4",
            "tools_config": {},
            "environment_config": {},
            "evolution_strategy": "alpha-coder",
            "evolution_layers": {"prompt": True, "code": False, "model": False}
        }

        response = client.post("/api/agents/", json=agent_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TestAgent"
        assert data["evolution_strategy"] == "alpha-coder"
        assert "id" in data

    def test_list_agents(self, setup_database):
        """Test listing all agents."""
        # Create a few agents
        for i in range(3):
            agent_data = {
                "name": f"Agent{i}",
                "role_prompt": f"Prompt {i}",
                "model_name": "gpt-4",
                "evolution_strategy": "alpha-coder",
            }
            client.post("/api/agents/", json=agent_data)

        response = client.get("/api/agents/")

        assert response.status_code == 200
        agents = response.json()
        assert len(agents) == 3

    def test_get_agent(self, setup_database):
        """Test getting a specific agent."""
        # Create an agent
        agent_data = {
            "name": "GetTestAgent",
            "role_prompt": "Test prompt",
            "model_name": "gpt-4",
            "evolution_strategy": "curiosity",
        }
        create_response = client.post("/api/agents/", json=agent_data)
        agent_id = create_response.json()["id"]

        # Get the agent
        response = client.get(f"/api/agents/{agent_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "GetTestAgent"
        assert data["evolution_strategy"] == "curiosity"

    def test_get_nonexistent_agent(self, setup_database):
        """Test getting an agent that doesn't exist."""
        response = client.get("/api/agents/99999")

        assert response.status_code == 404

    def test_delete_agent(self, setup_database):
        """Test deleting an agent."""
        # Create an agent
        agent_data = {
            "name": "DeleteTestAgent",
            "role_prompt": "Test",
            "model_name": "gpt-4",
        }
        create_response = client.post("/api/agents/", json=agent_data)
        agent_id = create_response.json()["id"]

        # Delete the agent
        response = client.delete(f"/api/agents/{agent_id}")

        assert response.status_code == 200

        # Verify it's deleted
        get_response = client.get(f"/api/agents/{agent_id}")
        assert get_response.status_code == 404

    def test_agent_versions(self, setup_database):
        """Test getting agent versions."""
        # Create an agent
        agent_data = {
            "name": "VersionTestAgent",
            "role_prompt": "Test",
            "model_name": "gpt-4",
        }
        create_response = client.post("/api/agents/", json=agent_data)
        agent_id = create_response.json()["id"]

        # Get versions (should be empty initially)
        response = client.get(f"/api/agents/{agent_id}/versions")

        assert response.status_code == 200
        versions = response.json()
        assert len(versions) == 0


class TestEvolutionAPI:
    """Test evolution run API."""

    def test_create_evolution_run(self, setup_database):
        """Test creating a new evolution run."""
        # First create an agent
        agent_data = {
            "name": "EvoAgent",
            "role_prompt": "Test",
            "model_name": "gpt-4",
        }
        agent_response = client.post("/api/agents/", json=agent_data)
        agent_id = agent_response.json()["id"]

        # Create evolution run
        run_data = {
            "agent_id": agent_id,
            "strategy": "alpha-coder",
            "max_generations": 50,
            "population_size": 30,
            "mutation_rate": 0.3,
            "judge_type": "rule-based",
        }

        response = client.post("/api/evolution/", json=run_data)

        assert response.status_code == 200
        data = response.json()
        assert data["agent_id"] == agent_id
        assert data["strategy"] == "alpha-coder"
        assert data["status"] == "initialized"

    def test_start_evolution_run(self, setup_database):
        """Test starting an evolution run."""
        # Create agent and run
        agent_data = {"name": "StartAgent", "role_prompt": "Test", "model_name": "gpt-4"}
        agent_response = client.post("/api/agents/", json=agent_data)
        agent_id = agent_response.json()["id"]

        run_data = {"agent_id": agent_id, "strategy": "curiosity"}
        run_response = client.post("/api/evolution/", json=run_data)
        run_id = run_response.json()["id"]

        # Start the run
        response = client.post(f"/api/evolution/{run_id}/start")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_get_evolution_run(self, setup_database):
        """Test getting evolution run details."""
        # Create agent and run
        agent_data = {"name": "GetRunAgent", "role_prompt": "Test", "model_name": "gpt-4"}
        agent_response = client.post("/api/agents/", json=agent_data)
        agent_id = agent_response.json()["id"]

        run_data = {"agent_id": agent_id}
        run_response = client.post("/api/evolution/", json=run_data)
        run_id = run_response.json()["id"]

        # Get the run
        response = client.get(f"/api/evolution/{run_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == run_id

    def test_pause_evolution_run(self, setup_database):
        """Test pausing an evolution run."""
        # Create agent and run
        agent_data = {"name": "PauseAgent", "role_prompt": "Test", "model_name": "gpt-4"}
        agent_response = client.post("/api/agents/", json=agent_data)
        agent_id = agent_response.json()["id"]

        run_data = {"agent_id": agent_id}
        run_response = client.post("/api/evolution/", json=run_data)
        run_id = run_response.json()["id"]

        # Pause the run
        response = client.post(f"/api/evolution/{run_id}/pause")

        assert response.status_code == 200

        # Verify status changed
        get_response = client.get(f"/api/evolution/{run_id}")
        assert get_response.json()["status"] == "paused"

    def test_list_generations(self, setup_database):
        """Test listing generations in an evolution run."""
        # Create agent and run
        agent_data = {"name": "GenAgent", "role_prompt": "Test", "model_name": "gpt-4"}
        agent_response = client.post("/api/agents/", json=agent_data)
        agent_id = agent_response.json()["id"]

        run_data = {"agent_id": agent_id}
        run_response = client.post("/api/evolution/", json=run_data)
        run_id = run_response.json()["id"]

        # Get generations (should be empty initially)
        response = client.get(f"/api/evolution/{run_id}/generations")

        assert response.status_code == 200
        generations = response.json()
        assert len(generations) == 0


class TestTaskAPI:
    """Test task management and synthetic generation API."""

    def test_create_task(self, setup_database):
        """Test creating a task."""
        # Create agent first
        agent_data = {"name": "TaskAgent", "role_prompt": "Test", "model_name": "gpt-4"}
        agent_response = client.post("/api/agents/", json=agent_data)
        agent_id = agent_response.json()["id"]

        # Create task
        task_data = {
            "agent_id": agent_id,
            "description": "Solve 2+2",
            "input_data": {"problem": "2+2"},
            "expected_output": {"answer": "4"},
            "difficulty": 0.3,
            "source": "user"
        }

        response = client.post("/api/tasks/", json=task_data)

        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Solve 2+2"
        assert data["source"] == "user"

    def test_list_agent_tasks(self, setup_database):
        """Test listing tasks for an agent."""
        # Create agent
        agent_data = {"name": "ListTaskAgent", "role_prompt": "Test", "model_name": "gpt-4"}
        agent_response = client.post("/api/agents/", json=agent_data)
        agent_id = agent_response.json()["id"]

        # Create a few tasks
        for i in range(3):
            task_data = {
                "agent_id": agent_id,
                "description": f"Task {i}",
                "input_data": {},
                "difficulty": 0.5
            }
            client.post("/api/tasks/", json=task_data)

        # List tasks
        response = client.get(f"/api/tasks/agent/{agent_id}")

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 3

    def test_generate_synthetic_tasks(self, setup_database):
        """Test synthetic task generation endpoint."""
        # Create agent
        agent_data = {"name": "SyntheticAgent", "role_prompt": "Test", "model_name": "gpt-4"}
        agent_response = client.post("/api/agents/", json=agent_data)
        agent_id = agent_response.json()["id"]

        # Request synthetic task generation
        response = client.post(
            f"/api/tasks/generate-synthetic?agent_id={agent_id}&num_tasks=50"
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data


class TestHealthEndpoints:
    """Test health and status endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["status"] == "running"

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

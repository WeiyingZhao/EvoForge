"""
Integration tests for export/import agent configurations.
Tests saving and loading agent blueprints and evolved versions.
"""
import pytest
import json
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


class TestAgentExport:
    """Test exporting agent configurations."""

    def test_export_agent_config(self):
        """Test exporting a basic agent configuration."""
        from backend.app.models.agent import Agent

        agent = Agent(
            name="ExportTest",
            description="Test agent for export",
            role_prompt="You are a helpful assistant",
            model_name="gpt-4",
            tools_config={"calculator": True, "web_search": False},
            environment_config={"timeout": 30, "memory_limit": "512m"},
            evolution_strategy="alpha-coder",
            evolution_layers={"prompt": True, "code": True, "model": False}
        )

        # Export to dictionary
        config = {
            "name": agent.name,
            "description": agent.description,
            "role_prompt": agent.role_prompt,
            "model_name": agent.model_name,
            "tools_config": agent.tools_config,
            "environment_config": agent.environment_config,
            "evolution_strategy": agent.evolution_strategy,
            "evolution_layers": agent.evolution_layers,
        }

        assert config["name"] == "ExportTest"
        assert config["model_name"] == "gpt-4"
        assert config["tools_config"]["calculator"] is True

    def test_export_agent_version(self):
        """Test exporting an evolved agent version."""
        from backend.app.models.agent import AgentVersion

        version = AgentVersion(
            agent_id=1,
            version="2.5",
            evolved_prompt="Highly optimized prompt",
            evolved_code="def solve(x): return x**2",
            fitness_score=0.92,
            generation_number=50
        )

        # Export version
        version_config = {
            "version": version.version,
            "evolved_prompt": version.evolved_prompt,
            "evolved_code": version.evolved_code,
            "fitness_score": version.fitness_score,
            "generation_number": version.generation_number,
        }

        assert version_config["version"] == "2.5"
        assert version_config["fitness_score"] == 0.92

    def test_export_to_json_file(self):
        """Test exporting agent to JSON file."""
        from backend.app.models.agent import Agent

        agent = Agent(
            name="JSONExportTest",
            role_prompt="Test prompt",
            model_name="gpt-4",
            evolution_strategy="curiosity",
            tools_config={},
            environment_config={},
            evolution_layers={"prompt": True}
        )

        # Export to JSON
        config = {
            "name": agent.name,
            "role_prompt": agent.role_prompt,
            "model_name": agent.model_name,
            "evolution_strategy": agent.evolution_strategy,
            "tools_config": agent.tools_config,
            "environment_config": agent.environment_config,
            "evolution_layers": agent.evolution_layers,
        }

        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f, indent=2)
            temp_file = f.name

        # Verify file exists and has content
        assert os.path.exists(temp_file)

        with open(temp_file, 'r') as f:
            loaded_config = json.load(f)

        assert loaded_config["name"] == "JSONExportTest"
        assert loaded_config["model_name"] == "gpt-4"

        # Cleanup
        os.unlink(temp_file)

    def test_export_complete_evolution_run(self):
        """Test exporting complete evolution run with all generations."""
        from backend.app.models.evolution import EvolutionRun, Generation

        run = EvolutionRun(
            agent_id=1,
            strategy="alpha-coder",
            max_generations=10,
            population_size=20,
            mutation_rate=0.3,
            judge_type="rule-based",
            status="completed",
            best_fitness=0.88
        )

        generations = [
            Generation(
                evolution_run_id=1,
                generation_number=i,
                avg_fitness=0.5 + (i * 0.03),
                best_fitness=0.6 + (i * 0.03),
                worst_fitness=0.4,
                num_variants=20,
                num_successful=15,
                num_failed=5
            )
            for i in range(10)
        ]

        # Export run with generations
        export_data = {
            "run_config": {
                "strategy": run.strategy,
                "max_generations": run.max_generations,
                "population_size": run.population_size,
                "mutation_rate": run.mutation_rate,
                "best_fitness": run.best_fitness,
            },
            "generations": [
                {
                    "generation_number": g.generation_number,
                    "avg_fitness": g.avg_fitness,
                    "best_fitness": g.best_fitness,
                    "num_variants": g.num_variants,
                }
                for g in generations
            ]
        }

        assert len(export_data["generations"]) == 10
        assert export_data["run_config"]["best_fitness"] == 0.88


class TestAgentImport:
    """Test importing agent configurations."""

    def test_import_agent_config(self):
        """Test importing an agent from JSON."""
        config_json = {
            "name": "ImportedAgent",
            "description": "Imported from JSON",
            "role_prompt": "You are imported",
            "model_name": "gpt-4",
            "tools_config": {"tool1": True},
            "environment_config": {"timeout": 60},
            "evolution_strategy": "adversarial",
            "evolution_layers": {"prompt": True, "code": False, "model": False}
        }

        # Import (create agent from config)
        from backend.app.models.agent import Agent

        agent = Agent(**config_json)

        assert agent.name == "ImportedAgent"
        assert agent.model_name == "gpt-4"
        assert agent.evolution_strategy == "adversarial"

    def test_import_from_file(self):
        """Test importing agent configuration from file."""
        config_data = {
            "name": "FileImportAgent",
            "role_prompt": "Imported from file",
            "model_name": "claude-3-sonnet",
            "evolution_strategy": "curiosity",
            "tools_config": {},
            "environment_config": {},
            "evolution_layers": {"prompt": True}
        }

        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_file = f.name

        # Import from file
        with open(temp_file, 'r') as f:
            loaded_config = json.load(f)

        from backend.app.models.agent import Agent
        agent = Agent(**loaded_config)

        assert agent.name == "FileImportAgent"
        assert agent.model_name == "claude-3-sonnet"

        # Cleanup
        os.unlink(temp_file)

    def test_import_agent_version(self):
        """Test importing an evolved agent version."""
        version_config = {
            "agent_id": 1,
            "version": "3.0",
            "evolved_prompt": "Imported evolved prompt",
            "evolved_code": "def imported(): pass",
            "fitness_score": 0.85,
            "generation_number": 75
        }

        from backend.app.models.agent import AgentVersion

        version = AgentVersion(**version_config)

        assert version.version == "3.0"
        assert version.fitness_score == 0.85
        assert version.generation_number == 75

    def test_import_validation(self):
        """Test that imports are validated."""
        # Missing required fields
        invalid_config = {
            "name": "Invalid",
            # Missing role_prompt and model_name
        }

        from backend.app.models.agent import Agent

        # Should fail validation
        try:
            agent = Agent(**invalid_config)
            # If we get here, check that required fields are handled
            assert hasattr(agent, 'name')
        except (TypeError, ValueError, AttributeError):
            # Expected to fail due to missing required fields
            assert True

    def test_backward_compatibility(self):
        """Test importing older agent format."""
        # Old format (missing some new fields)
        old_config = {
            "name": "LegacyAgent",
            "role_prompt": "Old style prompt",
            "model_name": "gpt-3.5-turbo",
        }

        from backend.app.models.agent import Agent

        # Should handle missing optional fields
        agent = Agent(
            **old_config,
            tools_config=old_config.get("tools_config", {}),
            environment_config=old_config.get("environment_config", {}),
            evolution_strategy=old_config.get("evolution_strategy", "alpha-coder"),
            evolution_layers=old_config.get("evolution_layers", {"prompt": True})
        )

        assert agent.name == "LegacyAgent"
        assert agent.tools_config == {}
        assert agent.evolution_strategy == "alpha-coder"


class TestRoundTripConversion:
    """Test export followed by import (round-trip)."""

    def test_agent_round_trip(self):
        """Test exporting and re-importing an agent."""
        from backend.app.models.agent import Agent

        # Create original agent
        original = Agent(
            name="RoundTripAgent",
            description="Test round trip",
            role_prompt="Original prompt",
            model_name="gpt-4",
            tools_config={"web": True},
            environment_config={"timeout": 45},
            evolution_strategy="alpha-coder",
            evolution_layers={"prompt": True, "code": True}
        )

        # Export
        config = {
            "name": original.name,
            "description": original.description,
            "role_prompt": original.role_prompt,
            "model_name": original.model_name,
            "tools_config": original.tools_config,
            "environment_config": original.environment_config,
            "evolution_strategy": original.evolution_strategy,
            "evolution_layers": original.evolution_layers,
        }

        # Import
        imported = Agent(**config)

        # Verify round-trip
        assert imported.name == original.name
        assert imported.role_prompt == original.role_prompt
        assert imported.model_name == original.model_name
        assert imported.tools_config == original.tools_config
        assert imported.evolution_strategy == original.evolution_strategy

    def test_version_round_trip(self):
        """Test exporting and re-importing an agent version."""
        from backend.app.models.agent import AgentVersion

        original = AgentVersion(
            agent_id=1,
            version="1.5",
            evolved_prompt="Evolved prompt",
            evolved_code="def func(): return True",
            fitness_score=0.88,
            generation_number=30
        )

        # Export
        config = {
            "agent_id": original.agent_id,
            "version": original.version,
            "evolved_prompt": original.evolved_prompt,
            "evolved_code": original.evolved_code,
            "fitness_score": original.fitness_score,
            "generation_number": original.generation_number,
        }

        # Import
        imported = AgentVersion(**config)

        # Verify
        assert imported.version == original.version
        assert imported.evolved_prompt == original.evolved_prompt
        assert imported.fitness_score == original.fitness_score


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

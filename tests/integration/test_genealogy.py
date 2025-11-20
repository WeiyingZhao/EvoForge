"""
Integration tests for genealogy tracking and fitness graphs.
Tests tracking agent lineage and evolution metrics.
"""
import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


class TestGenealogyTracking:
    """Test genealogy tracking system."""

    def test_variant_parent_tracking(self):
        """Test that agent variants track their parents."""
        from backend.app.models.evolution import AgentVariant

        # Create parent variant
        parent = AgentVariant(
            generation_id=1,
            prompt="Parent prompt",
            mutation_type="initial",
            fitness_score=0.7,
            is_successful=True
        )

        # Create child variant
        child = AgentVariant(
            generation_id=2,
            prompt="Child prompt",
            mutation_type="prompt_tweak",
            parent_variant_id=parent.id if hasattr(parent, 'id') else None,
            fitness_score=0.8,
            is_successful=True
        )

        # Verify lineage
        assert child.mutation_type == "prompt_tweak"
        assert child.fitness_score > parent.fitness_score

    def test_agent_version_lineage(self):
        """Test that agent versions track lineage."""
        from backend.app.models.agent import AgentVersion

        # Create parent version
        v1 = AgentVersion(
            agent_id=1,
            version="1.0",
            evolved_prompt="First version",
            fitness_score=0.6,
            generation_number=1
        )

        # Create child version
        v2 = AgentVersion(
            agent_id=1,
            version="1.1",
            evolved_prompt="Improved version",
            fitness_score=0.8,
            generation_number=2,
            parent_version_id=v1.id if hasattr(v1, 'id') else None
        )

        # Verify evolution
        assert v2.generation_number > v1.generation_number
        assert v2.fitness_score > v1.fitness_score

    def test_generation_metrics_tracking(self):
        """Test that generation metrics are tracked."""
        from backend.app.models.evolution import Generation

        gen = Generation(
            evolution_run_id=1,
            generation_number=5,
            avg_fitness=0.65,
            best_fitness=0.9,
            worst_fitness=0.3,
            num_variants=50,
            num_successful=35,
            num_failed=15,
            duration_seconds=120.5
        )

        assert gen.avg_fitness == 0.65
        assert gen.best_fitness == 0.9
        assert gen.num_variants == 50
        assert gen.num_successful == 35

    def test_fitness_progression(self):
        """Test tracking fitness improvement over generations."""
        from backend.app.models.evolution import Generation

        generations = []

        # Simulate improving fitness over generations
        for i in range(10):
            gen = Generation(
                evolution_run_id=1,
                generation_number=i,
                avg_fitness=0.5 + (i * 0.03),  # Gradual improvement
                best_fitness=0.6 + (i * 0.03),
                worst_fitness=0.4 + (i * 0.02),
                num_variants=50,
                num_successful=30 + i,
                num_failed=20 - i
            )
            generations.append(gen)

        # Verify progression
        for i in range(1, len(generations)):
            assert generations[i].avg_fitness >= generations[i-1].avg_fitness
            assert generations[i].best_fitness >= generations[i-1].best_fitness

    def test_mutation_type_tracking(self):
        """Test that mutation types are properly tracked."""
        from backend.app.models.evolution import AgentVariant

        mutation_types = [
            "prompt_tweak",
            "code_rewrite",
            "crossover",
            "experience_injection",
            "meta_optimizer"
        ]

        variants = []
        for i, mut_type in enumerate(mutation_types):
            variant = AgentVariant(
                generation_id=1,
                prompt=f"Variant {i}",
                mutation_type=mut_type,
                fitness_score=0.5 + (i * 0.1)
            )
            variants.append(variant)

        # Verify all mutation types tracked
        tracked_types = [v.mutation_type for v in variants]
        assert set(tracked_types) == set(mutation_types)


class TestFitnessGraphs:
    """Test fitness graph data generation."""

    def test_fitness_over_time(self):
        """Test generating fitness over time data."""
        from backend.app.models.evolution import Generation

        generations = []
        for i in range(20):
            gen = Generation(
                evolution_run_id=1,
                generation_number=i,
                avg_fitness=0.5 + (i * 0.02),
                best_fitness=0.6 + (i * 0.015),
                worst_fitness=0.3 + (i * 0.01),
                num_variants=50,
                num_successful=25 + i,
                num_failed=25 - i,
                created_at=datetime.utcnow()
            )
            generations.append(gen)

        # Extract data for graphing
        gen_numbers = [g.generation_number for g in generations]
        avg_fitness_values = [g.avg_fitness for g in generations]
        best_fitness_values = [g.best_fitness for g in generations]

        assert len(gen_numbers) == 20
        assert all(avg_fitness_values[i] <= avg_fitness_values[i+1]
                   for i in range(len(avg_fitness_values)-1))
        assert all(best_fitness_values[i] <= best_fitness_values[i+1]
                   for i in range(len(best_fitness_values)-1))

    def test_population_diversity_metrics(self):
        """Test calculating population diversity."""
        from backend.app.models.evolution import Generation

        gen = Generation(
            evolution_run_id=1,
            generation_number=10,
            avg_fitness=0.7,
            best_fitness=0.95,
            worst_fitness=0.3,
            num_variants=100,
            num_successful=70,
            num_failed=30
        )

        # Calculate diversity metrics
        fitness_range = gen.best_fitness - gen.worst_fitness
        success_rate = gen.num_successful / gen.num_variants

        assert abs(fitness_range - 0.65) < 0.01  # Allow floating point tolerance
        assert success_rate == 0.7

    def test_convergence_detection(self):
        """Test detecting when evolution has converged."""
        from backend.app.models.evolution import Generation

        # Simulate converged evolution (fitness plateaus)
        generations = []
        for i in range(10):
            if i < 5:
                # Improving phase
                fitness = 0.5 + (i * 0.1)
            else:
                # Converged phase
                fitness = 0.9

            gen = Generation(
                evolution_run_id=1,
                generation_number=i,
                avg_fitness=fitness,
                best_fitness=fitness + 0.05,
                worst_fitness=fitness - 0.05,
                num_variants=50,
                num_successful=40,
                num_failed=10
            )
            generations.append(gen)

        # Check for convergence (fitness not improving)
        recent_gens = generations[-3:]
        fitness_changes = [
            abs(recent_gens[i+1].avg_fitness - recent_gens[i].avg_fitness)
            for i in range(len(recent_gens)-1)
        ]

        # Should have very small changes (converged)
        assert all(change < 0.01 for change in fitness_changes)


class TestEvolutionRunMetrics:
    """Test evolution run-level metrics."""

    def test_evolution_run_completion(self):
        """Test tracking evolution run completion."""
        from backend.app.models.evolution import EvolutionRun

        run = EvolutionRun(
            agent_id=1,
            strategy="alpha-coder",
            max_generations=100,
            population_size=50,
            mutation_rate=0.3,
            judge_type="llm-judge",
            status="completed",
            current_generation=100,
            best_fitness=0.95,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )

        assert run.status == "completed"
        assert run.current_generation == run.max_generations
        assert run.best_fitness == 0.95

    def test_evolution_run_failure_tracking(self):
        """Test tracking failed evolution runs."""
        from backend.app.models.evolution import EvolutionRun

        run = EvolutionRun(
            agent_id=1,
            strategy="curiosity",
            max_generations=100,
            population_size=50,
            status="failed",
            current_generation=25,
            error_message="Out of memory",
            started_at=datetime.utcnow()
        )

        assert run.status == "failed"
        assert run.error_message == "Out of memory"
        assert run.current_generation < run.max_generations

    def test_best_variant_tracking(self):
        """Test tracking the best variant in an evolution run."""
        from backend.app.models.evolution import EvolutionRun

        run = EvolutionRun(
            agent_id=1,
            strategy="adversarial",
            max_generations=50,
            population_size=30,
            status="completed",
            best_fitness=0.92,
            best_version_id=42
        )

        assert run.best_fitness == 0.92
        assert run.best_version_id == 42


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

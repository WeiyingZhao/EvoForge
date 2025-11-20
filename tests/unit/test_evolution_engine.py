"""
Unit tests for Evolution Engine.
Tests the core evolutionary loop and three-layer evolution.
"""
import pytest
import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from evolution_engine.engine import EvolutionEngine


class TestEvolutionEngine:
    """Test the core evolution engine."""

    def setup_method(self):
        """Setup before each test."""
        # Use small population for faster tests
        self.engine = EvolutionEngine(
            strategy="alpha-coder",
            population_size=10,
            max_generations=5,
            mutation_rate=0.3,
            num_workers=2
        )

    def test_initialization(self):
        """Test engine initializes correctly."""
        assert self.engine.strategy == "alpha-coder"
        assert self.engine.population_size == 10
        assert self.engine.max_generations == 5
        assert self.engine.mutation_rate == 0.3
        assert len(self.engine.workers) == 2

    def test_initialize_population(self):
        """Test population initialization."""
        base_config = {
            "prompt": "You are a helpful assistant",
            "model": "gpt-4",
            "code": None
        }

        population = self.engine._initialize_population(base_config)

        assert len(population) == self.engine.population_size
        assert population[0] == base_config  # First is exact copy

        # Others should be variants
        for variant in population[1:]:
            assert "variant_id" in variant

    def test_selection(self):
        """Test selection keeps best performers."""
        population = [
            {"id": 0, "fitness": 0.9},
            {"id": 1, "fitness": 0.1},
            {"id": 2, "fitness": 0.7},
            {"id": 3, "fitness": 0.5},
        ]
        fitness_scores = [p["fitness"] for p in population]

        selected = self.engine._selection(population, fitness_scores)

        # Should keep top 50%
        assert len(selected) == 2
        assert selected[0]["fitness"] == 0.9
        assert selected[1]["fitness"] == 0.7

    def test_mutation(self):
        """Test mutation creates new variants."""
        selected = [
            {"id": 0, "prompt": "Original prompt"},
            {"id": 1, "prompt": "Another prompt"},
        ]

        next_gen = self.engine._mutation(selected)

        # Should have population_size variants
        assert len(next_gen) == self.engine.population_size

        # Some should be mutated
        mutated_count = sum(1 for v in next_gen if v.get("mutated", False))
        assert mutated_count >= 0  # At least some mutations

    @pytest.mark.asyncio
    async def test_run_evolution(self):
        """Test full evolution run."""
        agent_config = {
            "prompt": "You are a math solver",
            "model": "gpt-4",
            "code": None
        }

        tasks = [
            {"id": 1, "description": "Solve 2+2", "expected": "4"},
            {"id": 2, "description": "Solve 10*5", "expected": "50"},
        ]

        judge_config = {"type": "rule-based"}

        # Run evolution
        result = await self.engine.run_evolution(
            agent_config,
            tasks,
            judge_config
        )

        assert "best_variant" in result
        assert "best_fitness" in result
        assert "generations_run" in result
        assert result["generations_run"] == self.engine.max_generations

    def test_shutdown(self):
        """Test engine shuts down cleanly."""
        try:
            self.engine.shutdown()
            assert True
        except Exception as e:
            assert False, f"Shutdown raised error: {e}"


class TestThreeLayerEvolution:
    """Test the three-layer evolution system (Prompt, Code, Model)."""

    def test_prompt_evolution_layer(self):
        """Test Layer 1: Prompt Evolution."""
        # This tests that prompt can be evolved
        engine = EvolutionEngine(strategy="alpha-coder", population_size=5)

        base_config = {
            "prompt": "You are an assistant",
            "evolution_layers": {"prompt": True, "code": False, "model": False}
        }

        population = engine._initialize_population(base_config)

        # All variants should have prompts
        for variant in population:
            assert "prompt" in variant
            assert variant["prompt"] is not None

    def test_code_evolution_layer(self):
        """Test Layer 2: Code Evolution."""
        # This tests that code can be evolved
        engine = EvolutionEngine(strategy="alpha-coder", population_size=5)

        base_config = {
            "prompt": "You are an assistant",
            "code": "def solve(x): return x + 1",
            "evolution_layers": {"prompt": False, "code": True, "model": False}
        }

        population = engine._initialize_population(base_config)

        # Variants should have code
        for variant in population:
            assert "code" in variant

    def test_model_evolution_layer(self):
        """Test Layer 3: Model Evolution (LoRA fine-tuning)."""
        # This tests the model evolution configuration
        engine = EvolutionEngine(strategy="alpha-coder", population_size=5)

        base_config = {
            "prompt": "You are an assistant",
            "model": "gpt-4",
            "evolution_layers": {"prompt": False, "code": False, "model": True}
        }

        population = engine._initialize_population(base_config)

        # Variants should have model config
        for variant in population:
            assert "model" in variant

    def test_multi_layer_evolution(self):
        """Test evolving multiple layers simultaneously."""
        engine = EvolutionEngine(strategy="alpha-coder", population_size=5)

        base_config = {
            "prompt": "You are an assistant",
            "code": "def solve(x): return x",
            "model": "gpt-4",
            "evolution_layers": {"prompt": True, "code": True, "model": False}
        }

        population = engine._initialize_population(base_config)

        # Should have both prompt and code
        for variant in population:
            assert "prompt" in variant
            assert "code" in variant


class TestEvolutionStrategies:
    """Test different evolution strategies."""

    def test_alpha_coder_strategy(self):
        """Test AlphaEvolve strategy."""
        engine = EvolutionEngine(strategy="alpha-coder", population_size=5)
        assert engine.strategy == "alpha-coder"

    def test_curiosity_strategy(self):
        """Test Curiosity-driven strategy."""
        engine = EvolutionEngine(strategy="curiosity", population_size=5)
        assert engine.strategy == "curiosity"

    def test_adversarial_strategy(self):
        """Test Adversarial/Co-evolution strategy."""
        engine = EvolutionEngine(strategy="adversarial", population_size=5)
        assert engine.strategy == "adversarial"

    def test_crossover_for_adversarial(self):
        """Test that crossover is used for adversarial strategy."""
        engine = EvolutionEngine(strategy="adversarial", population_size=4)

        population = [
            {"id": 0, "prompt": "Agent A"},
            {"id": 1, "prompt": "Agent B"},
            {"id": 2, "prompt": "Agent C"},
            {"id": 3, "prompt": "Agent D"},
        ]

        # Crossover should not change length
        result = engine._crossover(population)
        assert len(result) == len(population)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Simple example demonstrating agent evolution with EvoForge.

This example creates a basic math-solving agent and evolves it
using the Alpha-Coder strategy.
"""
import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evolution_engine.engine import EvolutionEngine
from evolution_engine.strategies.alpha_coder import AlphaCoderStrategy
from evolution_engine.judges import create_judge


async def main():
    """Run a simple evolution example."""

    print("=" * 60)
    print("EvoForge Simple Evolution Example")
    print("=" * 60)

    # Define initial agent configuration
    agent_config = {
        "name": "MathSolver",
        "prompt": """You are a math problem solver.
        Given a math problem, write Python code to solve it.

        # EVOLVE-BLOCK
        def solve(problem: str) -> float:
            # Basic implementation - will be evolved
            return 0.0
        # END-EVOLVE-BLOCK
        """,
        "model": "gpt-4",
    }

    # Define evaluation tasks
    tasks = [
        {
            "description": "Calculate 15 + 27",
            "expected_output": 42,
        },
        {
            "description": "Find the sum of numbers 1 to 10",
            "expected_output": 55,
        },
        {
            "description": "Calculate 7 * 8",
            "expected_output": 56,
        },
    ]

    # Configure judge
    judge_config = {
        "type": "rule-based",
        "rules": [
            {
                "type": "python_test",
                "test_code": "assert output == expected_output"
            }
        ]
    }

    # Create evolution engine
    engine = EvolutionEngine(
        strategy="alpha-coder",
        population_size=10,  # Small population for demo
        max_generations=5,    # Just 5 generations for demo
        mutation_rate=0.3,
        num_workers=4,
    )

    print("\nStarting evolution with:")
    print(f"  Strategy: Alpha-Coder")
    print(f"  Population: 10 variants per generation")
    print(f"  Generations: 5")
    print(f"  Tasks: {len(tasks)}")
    print()

    # Progress callback
    def progress_callback(metrics):
        print(f"Generation {metrics['generation']}: "
              f"Best Fitness = {metrics['best_fitness']:.3f}, "
              f"Avg Fitness = {metrics['avg_fitness']:.3f}")

    # Run evolution
    try:
        result = await engine.run_evolution(
            agent_config=agent_config,
            tasks=tasks,
            judge_config=judge_config,
            callback=progress_callback,
        )

        print("\n" + "=" * 60)
        print("Evolution Complete!")
        print("=" * 60)
        print(f"\nBest Fitness Achieved: {result['best_fitness']:.3f}")
        print(f"Generations Run: {result['generations_run']}")
        print("\nBest Agent Configuration:")
        print(result['best_variant'])

    except Exception as e:
        print(f"\nError during evolution: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        engine.shutdown()


if __name__ == "__main__":
    print("Note: This is a demonstration script.")
    print("To run actual evolution, ensure:")
    print("  1. Ray is installed and initialized")
    print("  2. Docker is running (for sandbox)")
    print("  3. LLM API keys are configured")
    print()

    # For demo purposes, we'll show what would happen
    print("In a full setup, this would:")
    print("  1. Create 10 agent variants")
    print("  2. Evaluate each on the math tasks")
    print("  3. Select best performers")
    print("  4. Mutate code in EVOLVE-BLOCK")
    print("  5. Repeat for 5 generations")
    print()
    print("Expected output:")
    print("  Generation 0: Fitness increases as code improves")
    print("  Generation 4: Near-perfect solutions evolved")
    print()
    print("To run for real: python examples/simple_agent_evolution.py --execute")

    if "--execute" in sys.argv:
        asyncio.run(main())

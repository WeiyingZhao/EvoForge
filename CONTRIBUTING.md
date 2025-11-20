# Contributing to EvoForge

Thank you for your interest in contributing to EvoForge! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the feature and its use case
3. Explain how it aligns with EvoForge's goals

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest black isort  # Dev dependencies

# Run tests
pytest

# Format code
black .
isort .
```

### Frontend

```bash
cd frontend
npm install

# Run dev server
npm run dev

# Run linter
npm run lint

# Build
npm run build
```

### Full Stack

```bash
# Use Docker Compose
docker-compose up --build
```

## Project Structure

```
EvoForge/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── core/        # Configuration
│   └── tests/           # Backend tests
├── evolution-engine/     # Ray-based evolution
│   ├── strategies/      # Evolution strategies
│   ├── judges/          # Judge implementations
│   ├── sandbox/         # Sandboxed execution
│   └── memory/          # Experience bank
├── frontend/            # Next.js frontend
│   └── app/            # Pages and components
└── docs/               # Documentation
```

## Coding Standards

### Python

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use `black` for formatting
- Use `isort` for import ordering

```python
# Good
def evaluate_agent(
    agent_config: Dict[str, Any],
    task: Task,
    timeout: int = 30
) -> EvaluationResult:
    """
    Evaluate an agent on a task.

    Args:
        agent_config: Agent configuration
        task: Task to evaluate on
        timeout: Maximum execution time

    Returns:
        Evaluation results
    """
    pass
```

### TypeScript/JavaScript

- Use TypeScript for new code
- Follow ESLint configuration
- Use functional components with hooks
- Prefer `const` over `let`

```typescript
// Good
interface AgentConfig {
  name: string;
  strategy: EvolutionStrategy;
}

const AgentCard: React.FC<{ agent: AgentConfig }> = ({ agent }) => {
  return <div>{agent.name}</div>;
};
```

## Testing

### Backend Tests

```bash
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# Start services
docker-compose up -d

# Run integration tests
pytest tests/integration/
```

## Documentation

- Add docstrings to all functions and classes
- Update README.md if adding new features
- Add inline comments for complex logic
- Update ARCHITECTURE.md for architectural changes

## Commit Messages

Use clear, descriptive commit messages:

```
feat: add evolving judge implementation
fix: correct fitness calculation in alpha-coder strategy
docs: update API documentation for evolution endpoints
test: add tests for experience memory bank
refactor: simplify mutation logic in curiosity strategy
```

## Areas for Contribution

### High Priority

- [ ] vLLM integration for faster inference
- [ ] More comprehensive test coverage
- [ ] Performance optimizations for large populations
- [ ] Additional evolution strategies

### Medium Priority

- [ ] Support for more LLM providers (Llama, Mistral)
- [ ] Pre-built agent templates
- [ ] Enhanced visualization in dashboard
- [ ] Export/import agent configurations

### Documentation

- [ ] Tutorial videos
- [ ] More detailed examples
- [ ] API reference improvements
- [ ] Architecture diagrams

## Questions?

- Open a Discussion on GitHub
- Check existing Issues
- Review documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

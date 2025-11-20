# EvoForge Architecture

## System Overview

EvoForge is a distributed system for evolving AI agents. It consists of four main layers:

1. **Frontend Layer** - User interface for agent design and monitoring
2. **API Layer** - REST and WebSocket endpoints
3. **Evolution Engine** - Ray-based distributed evolution
4. **Data Layer** - PostgreSQL with pgvector for persistence

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Agent Builder │  │  Dashboard   │  │  Analytics   │      │
│  │ (ReactFlow)  │  │ (Real-time)  │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/WebSocket
┌───────────────────────────▼─────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Agents  │  │Evolution │  │  Tasks   │  │Experience│   │
│  │   API    │  │   API    │  │   API    │  │   API    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│              Evolution Engine (Ray Cluster)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Evolution Orchestrator                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Strategy │  │  Judge   │  │ Sandbox  │  │  Memory  │  │
│  │  Engine  │  │ Factory  │  │ Executor │  │   Bank   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │           Ray Worker Pool (Parallel Agents)           │ │
│  │  [Worker 1] [Worker 2] ... [Worker N]                │ │
│  └───────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│              Data Layer (PostgreSQL + pgvector)             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Agents  │  │Evolution │  │  Tasks   │  │Experience│  │
│  │          │  │   Runs   │  │          │  │  (Vector)│  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Evolution Flow

### 1. Initialization
```
User Creates Agent
    ↓
Frontend sends config to Backend
    ↓
Backend stores in PostgreSQL
    ↓
Returns Agent ID
```

### 2. Evolution Start
```
User clicks "Start Evolution"
    ↓
Backend creates EvolutionRun record
    ↓
Dispatches job to Ray Cluster
    ↓
Ray spawns Evolution Engine
```

### 3. Evolution Loop (per Generation)
```
┌─────────────────────────────────────────┐
│  1. Initialize Population (N variants)  │
│     - Base agent + mutations            │
└────────────────┬────────────────────────┘
                 ↓
┌────────────────────────────────────────┐
│  2. Parallel Evaluation                │
│     - Distribute to Ray Workers        │
│     - Each worker runs agent variant   │
│     - Execute in Docker Sandbox        │
└────────────────┬───────────────────────┘
                 ↓
┌────────────────────────────────────────┐
│  3. Judge Evaluation                   │
│     - Rule-based / LLM / Evolving      │
│     - Assign fitness scores            │
└────────────────┬───────────────────────┘
                 ↓
┌────────────────────────────────────────┐
│  4. Selection                          │
│     - Keep top performers              │
│     - Tournament selection             │
└────────────────┬───────────────────────┘
                 ↓
┌────────────────────────────────────────┐
│  5. Mutation                           │
│     - Strategy-specific mutations      │
│     - Create next generation           │
└────────────────┬───────────────────────┘
                 ↓
┌────────────────────────────────────────┐
│  6. Experience Recording               │
│     - Store lessons in Memory Bank     │
│     - Update vector embeddings         │
└────────────────┬───────────────────────┘
                 ↓
          Repeat or Converge
```

### 4. Real-time Updates
```
Evolution Engine
    ↓
Publishes metrics via WebSocket
    ↓
Backend forwards to Frontend
    ↓
Dashboard updates:
    - Fitness Graph
    - Genealogy Tree
    - Current Best
```

## Data Models

### Core Entities

```python
Agent
├── id: int
├── name: str
├── role_prompt: str
├── evolution_strategy: str
└── versions: List[AgentVersion]

AgentVersion
├── id: int
├── agent_id: int
├── version: str
├── evolved_prompt: str
├── fitness_score: float
└── parent_version_id: int (genealogy)

EvolutionRun
├── id: int
├── agent_id: int
├── strategy: str
├── status: str
├── current_generation: int
└── generations: List[Generation]

Generation
├── id: int
├── evolution_run_id: int
├── generation_number: int
├── best_fitness: float
└── variants: List[AgentVariant]

Experience
├── id: int
├── agent_id: int
├── task_description: str
├── lesson: str
├── embedding: Vector(1536)
└── importance_score: float
```

## Evolution Strategies Detail

### Alpha-Coder Strategy

```
Input: Code with # EVOLVE-BLOCK markers
    ↓
1. Parse code blocks
    ↓
2. Generate mutations (LLM proposes)
    ↓
3. Validate in sandbox
    ↓
4. Measure: runtime, memory, correctness
    ↓
5. Select best performers
    ↓
Output: Optimized code
```

**Fitness Function:**
```
fitness = 0.5 * correctness + 0.3 * (1/runtime) + 0.2 * (1/memory)
```

### Curiosity Strategy

```
Seed Examples (5-10)
    ↓
Self-Questioning
    ↓
Generate 1000+ synthetic tasks
    ↓
Agent attempts tasks
    ↓
Success/Failure → Experience Pool
    ↓
Next task: retrieve similar experiences
    ↓
Agent uses past lessons
    ↓
Improved performance
```

**Experience Retrieval:**
```python
query_embedding = embed(current_task)
similar = cosine_similarity(query_embedding, experience_embeddings)
top_k_lessons = get_top_k(similar, k=5)
inject_into_prompt(top_k_lessons)
```

### Adversarial Strategy

```
┌─────────────┐
│  Proposer   │ → Creates problem at difficulty D
└──────┬──────┘
       ↓
┌─────────────┐
│   Solver    │ → Attempts solution
└──────┬──────┘
       ↓
┌─────────────┐
│    Judge    │ → Scores solution
└──────┬──────┘
       ↓
    Rewards
       ↓
┌────────────────────────────────┐
│  Update all three via RL       │
│  Task-Relative REINFORCE++     │
└────────────────────────────────┘
```

**Reward Distribution:**
- Proposer: 1.0 if problem is challenging but solvable (0.4 < score < 0.8)
- Solver: score from judge
- Judge: consistency metric

## Sandboxing Architecture

```
User code → FastAPI endpoint
    ↓
Create temp file with code
    ↓
Docker run:
    - Image: python:3.11-slim
    - Volume: code file (read-only)
    - Limits:
        * Memory: 512MB
        * CPU: 1 core
        * Timeout: 30s
        * Network: disabled
    ↓
Execute and capture:
    - stdout/stderr
    - exit code
    - memory usage
    - execution time
    ↓
Kill container
    ↓
Parse results
    ↓
Return to evolution engine
```

## Scalability Considerations

### Horizontal Scaling

1. **Backend**: Run multiple FastAPI instances behind load balancer
2. **Ray Cluster**: Add worker nodes for more parallel agents
3. **Database**: Read replicas for queries, write to primary

### Vertical Scaling

1. **Ray Workers**: Increase CPUs/GPUs per worker
2. **Postgres**: Increase connections, memory
3. **Backend**: Increase uvicorn workers

### Performance Optimizations

1. **Caching**: Redis for session data, evolution states
2. **Async Operations**: All I/O is async (database, LLM calls)
3. **Batch Processing**: Evaluate multiple variants in single LLM call
4. **Vector Search**: pgvector with HNSW index for fast retrieval

## Monitoring & Observability

### Metrics Collected

1. **Evolution Metrics**
   - Generations completed
   - Average fitness per generation
   - Convergence rate

2. **System Metrics**
   - Ray worker utilization
   - Sandbox execution times
   - Database query performance

3. **Business Metrics**
   - Agents created
   - Evolution runs started
   - Success rate

### Logging

- **Backend**: Structured JSON logs (loguru)
- **Ray**: Ray dashboard (port 8265)
- **Database**: Query logs

## Security

1. **Sandbox Isolation**: Docker containers with no network
2. **Input Validation**: Pydantic models for all API inputs
3. **Rate Limiting**: Prevent abuse of expensive operations
4. **Secret Management**: Environment variables, never committed
5. **Code Review**: Human approval for production deployments

## Deployment

### Development
```bash
docker-compose up
```

### Production
```bash
# Use production docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Or Kubernetes (future)
kubectl apply -f k8s/
```

## Future Enhancements

1. **vLLM Integration**: Faster inference with PagedAttention
2. **Multi-GPU**: Distribute model calls across GPUs
3. **Checkpointing**: Save/resume evolution runs
4. **A/B Testing**: Compare strategies on same task set
5. **Model Zoo**: Pre-evolved agents as starting points

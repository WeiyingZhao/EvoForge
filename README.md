# EvoForge: Self-Evolving AI Agent Platform

**"From Static Prompts to Living Intelligence"**

EvoForge is a revolutionary platform that transforms AI agents from frozen artifacts into self-evolving systems. Instead of manually tweaking prompts and code, EvoForge enables agents to improve themselves autonomously through evolutionary algorithms inspired by cutting-edge research.

## 🌟 Key Features

### Three Evolution Strategies

1. **Alpha-Coder Loop** (Based on AlphaEvolve)
   - Optimizes code through mutation and natural selection
   - Agents rewrite their own logic to find better solutions
   - Best for: Algorithmic optimization, data science, math problems

2. **Curiosity Loop** (Based on AgentEvolver)
   - Self-Questioning: Generates synthetic training data
   - Self-Navigating: Learns from experience memory
   - Best for: Open-ended exploration, novel environments

3. **Adversarial Arena** (Based on Multi-Agent Evolve)
   - Three co-evolving agents: Proposer, Solver, Judge
   - Task-Relative REINFORCE++ for optimization
   - Best for: Complex reasoning, debate, competitive tasks

### Three Layers of Evolution

| Layer | What Evolves | Speed | Cost | Best For |
|-------|--------------|-------|------|----------|
| **Prompt** | System instructions, few-shot examples | Fast | Low | General tasks, behavior tuning |
| **Code** | Python functions, tool definitions | Medium | Medium | Algorithms, data processing |
| **Model** | LLM weights (LoRA/Fine-tuning) | Slow | High | Domain specialization, performance |

### Core Components

- **Judge Factory**: 3-tier evaluation system (Rule-Based, LLM-Judge, Evolving Judge)
- **Synthetic Task Generator**: Auto-generates training data from seed examples
- **Sandboxed Execution**: Secure Docker-based code execution with resource limits
- **Experience Memory Bank**: Vector-based memory for learning from past attempts
- **Ray Orchestration**: Distributed evolution with parallel agent populations

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- 16GB+ RAM recommended
- (Optional) NVIDIA GPU for model evolution
- API keys: OpenAI or Anthropic

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/EvoForge.git
cd EvoForge
```

2. **Set up environment variables**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add your API keys
```

3. **Start the platform**
```bash
docker-compose up -d
```

4. **Access the interfaces**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Ray Dashboard: http://localhost:8265
- API Documentation: http://localhost:8000/docs

## 📖 Usage Guide

### Creating Your First Agent

1. **Open the Agent Builder** (http://localhost:3000/builder)

2. **Drag and drop components**:
   - **Role Node**: Define the agent's identity and initial prompt
   - **Model Node**: Select the base LLM (GPT-4, Claude, etc.)
   - **Memory Node**: Configure experience pool settings
   - **Environment Node**: Set up tools and sandbox constraints

3. **Select Evolution Strategy**:
   - Choose from Alpha-Coder, Curiosity, or Adversarial
   - Configure parameters (population size, mutation rate, etc.)

4. **Configure the Judge**:
   - Rule-Based: Define Python assertions or regex patterns
   - LLM-Judge: Write natural language evaluation rubrics
   - Evolving Judge: Let the judge adapt its criteria over time

5. **Start Evolution**:
   - Click "Start Evolution"
   - Monitor real-time progress in the dashboard
   - Watch the Fitness Graph and Genealogy Tree

### Example: Evolving a Data Analyst Agent

```python
# Example agent configuration
{
  "name": "DataAnalystAgent",
  "role_prompt": "You analyze CSV datasets and answer questions about them.",
  "model": "gpt-4",
  "evolution_strategy": "alpha-coder",
  "evolution_layers": {
    "prompt": true,
    "code": true,
    "model": false
  },
  "judge": {
    "type": "rule-based",
    "rules": [
      {"type": "assert", "expression": "output['result'] is not None"},
      {"type": "python_test", "test_code": "assert isinstance(output['data'], list)"}
    ]
  }
}
```

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/          # REST endpoints
│   ├── models/       # Database models (SQLAlchemy + pgvector)
│   ├── services/     # Business logic
│   └── core/         # Configuration, database
```

### Evolution Engine (Ray)
```
evolution-engine/
├── engine.py         # Core evolution loop
├── strategies/       # Alpha-Coder, Curiosity, Adversarial
├── judges/           # Rule-Based, LLM, Evolving judges
├── sandbox/          # Docker-based code execution
└── memory/           # Experience Memory Bank
```

### Frontend (Next.js + ReactFlow)
```
frontend/
├── app/
│   ├── page.tsx          # Homepage
│   ├── builder/          # Visual agent builder
│   └── dashboard/        # Real-time evolution monitoring
```

## 🔬 Research Foundations

EvoForge implements methodologies from:

1. **AlphaEvolve** (Google DeepMind)
   - Code superoptimization through evolutionary search
   - Sandboxed validation and fitness evaluation

2. **AgentEvolver** (ModelScope)
   - Self-Questioning: Synthetic task generation
   - Self-Navigating: Experience-based learning
   - Self-Attributing: Process-level credit assignment

3. **Multi-Agent Evolve** (UIUC)
   - Co-evolution of Proposer, Solver, and Judge agents
   - Task-Relative REINFORCE++ algorithm
   - Self-Reward mechanism

## 📊 API Documentation

### Create an Agent
```bash
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MyAgent",
    "role_prompt": "You are a helpful assistant",
    "model_name": "gpt-4",
    "evolution_strategy": "alpha-coder"
  }'
```

### Start Evolution Run
```bash
curl -X POST http://localhost:8000/api/evolution \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": 1,
    "strategy": "alpha-coder",
    "max_generations": 100,
    "population_size": 50
  }'
```

### WebSocket: Real-time Updates
```javascript
const ws = new WebSocket('ws://localhost:8000/api/evolution/1/stream');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Generation:', data.generation);
  console.log('Best Fitness:', data.best_fitness);
};
```

## 🛡️ Security & Safety

- **Sandboxed Execution**: All code runs in isolated Docker containers
- **Resource Limits**: CPU, memory, and timeout constraints enforced
- **Network Isolation**: Agents cannot access external networks by default
- **Automatic Rollback**: Failed mutations don't affect stable agents
- **Human-in-the-Loop**: Pin/delete experiences, approve critical mutations

## 🔧 Configuration

### Evolution Settings
```env
# backend/.env
MAX_GENERATIONS=100
POPULATION_SIZE=50
MUTATION_RATE=0.3

# Sandbox
SANDBOX_TIMEOUT=30
SANDBOX_MEMORY_LIMIT=512m
SANDBOX_NETWORK_ENABLED=false
```

### Ray Cluster
```env
RAY_NUM_CPUS=8
RAY_NUM_GPUS=0
```

## 📈 Performance Tips

1. **Start with Prompt Evolution**: Fastest and cheapest iteration
2. **Use Synthetic Task Generation**: 5 examples → 1000s of training cases
3. **Enable Code Evolution for Algorithms**: Significant improvements in computational tasks
4. **Reserve Model Evolution for Production**: Expensive but maximizes performance
5. **Pin Important Experiences**: Guide learning with human expertise

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **AlphaEvolve** by Google DeepMind
- **AgentEvolver** by ModelScope
- **Multi-Agent Evolve** by UIUC
- Research survey: [Awesome Self-Evolving Agents](https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents)

## 📧 Support

- Documentation: http://localhost:3000/docs
- Issues: GitHub Issues
- Community: Discord (coming soon)

## 🗺️ Roadmap

- [ ] Support for more LLM providers (Llama, Mistral, etc.)
- [ ] vLLM integration for faster inference
- [ ] Multi-modal evolution (images, audio)
- [ ] Distributed Ray cluster support
- [ ] Pre-built agent templates
- [ ] Evolution marketplace

---

**Built with ❤️ for the future of AI development**

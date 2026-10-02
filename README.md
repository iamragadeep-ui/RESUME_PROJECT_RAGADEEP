# Delivery Support Resolution Agent

## Project overview

This project is a production-style multi-agent AI application for a retail logistics support workflow. It demonstrates a supervisor-driven orchestration pattern with specialized agents, tool calling, retrieval-augmented generation, vector search, human approval, validation, and grounded response generation.

## Business problem

Customers often contact support when a delivery is delayed, missing, or in a nonstandard state. Support teams need to investigate order records, carrier updates, policy rules, and prior cases before deciding whether to notify the customer, create a ticket, request a refund, or escalate to a human.

## Main goal

The system should determine the issue, retrieve the correct operational and policy context, recommend a safe action, and require approval for consequential decisions such as refunds or escalations.

## Features

- Multi-agent orchestration with a supervisor and task specialists
- Structured intent triage with Pydantic validations
- Mock operational tools for order, tracking, customer, and ticket data
- RAG pipeline with ChromaDB-backed knowledge search
- Evidence-based investigation and policy grounding
- Human approval workflow for refund or escalated actions
- Validation and guardrail checks before final response generation
- FastAPI backend with chat and workflow endpoints
- Next.js + Tailwind frontend dashboard
- Sample evaluation dataset and test scaffolding

## Architecture

```mermaid
flowchart TD
    U[User] --> FE[Next.js Frontend]
    FE --> API[FastAPI Backend]
    API --> SUP[Supervisor Agent]
    SUP --> TRI[Triage Agent]
    SUP --> RET[Data Retrieval Agent]
    SUP --> RAG[RAG / Knowledge Agent]
    SUP --> INV[Investigation Agent]
    RET --> TOOLS[Order / Tracking / Ticket Tools]
    RAG --> CHROMA[ChromaDB Vector Store]
    INV --> DEC[Decision Node]
    DEC --> AP[Human Approval]
    DEC --> ACT[Action Agent]
    ACT --> VAL[Validation Agent]
    VAL --> RESP[Response Agent]
    RESP --> U
```

## Agent architecture

```mermaid
flowchart LR
    Supervisor[Supervisor Agent]
    Supervisor --> Triage[Triage Agent]
    Supervisor --> Data[Data Retrieval Agent]
    Supervisor --> RAG[RAG Agent]
    Supervisor --> Investigation[Investigation Agent]
    Supervisor --> Action[Action Agent]
    Supervisor --> Validation[Validation Agent]
    Supervisor --> Response[Response Agent]
```

## RAG architecture

```mermaid
flowchart LR
    Docs[Knowledge Documents]
    Docs --> Loader[Document Loader]
    Loader --> Chunk[Chunking]
    Chunk --> Embed[Embeddings]
    Embed --> Chroma[ChromaDB]
    Chroma --> Retriever[Retriever]
    Retriever --> Rerank[Reranker]
    Rerank --> Context[Context Builder]
    Context --> LLM[LLM]
    LLM --> Cite[Citation-based Response]
```

## Multi-agent responsibilities

- Supervisor Agent: routes work and controls state transitions.
- Triage Agent: identifies intent, urgency, entities, and missing data.
- Data Retrieval Agent: fetches order, customer, tracking, and ticket history.
- RAG Agent: searches policy and support knowledge using ChromaDB.
- Investigation Agent: merges evidence and recommends the next action.
- Action Agent: executes safe, explicit actions like creating tickets or refund requests.
- Validation Agent: checks groundedness, policy compliance, and action safety.
- Response Agent: produces a final user-facing answer with citations and action status.

## Technology stack

- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: FastAPI, Pydantic, Python
- Agent architecture: LangChain + LangGraph-ready workflow using typed state
- LLM: OpenAI API via environment variables
- Vector database: ChromaDB
- Caching/session state: Redis-ready service layer
- Database: PostgreSQL with SQLite fallback option
- Observability: structured logs and workflow metadata
- Testing: Pytest

## Folder structure

```text
RESUME_PROJECT_RAGADEEP/
├── .env.example
├── README.md
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── database.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── investigation.py
│       │   ├── retrieval.py
│       │   ├── response.py
│       │   ├── supervisor.py
│       │   ├── triage.py
│       │   └── validator.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── main.py
│       ├── evaluation/
│       │   └── sample_cases.json
│       ├── graph/
│       │   ├── state.py
│       │   └── workflow.py
│       ├── models/
│       │   └── schemas.py
│       ├── prompts/
│       │   ├── investigation_prompt.py
│       │   ├── response_prompt.py
│       │   ├── retrieval_prompt.py
│       │   ├── supervisor_prompt.py
│       │   ├── triage_prompt.py
│       │   └── validation_prompt.py
│       ├── rag/
│       │   ├── knowledge.py
│       │   └── vector_store.py
│       ├── services/
│       │   ├── llm_service.py
│       │   └── memory_service.py
│       ├── tests/
│       │   └── test_workflow.py
│       └── tools/
│           └── mock_tools.py
├── data/
│   └── knowledge_base/
│       └── delivery_policy.txt
├── frontend/
│   ├── app/
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── next.config.mjs
├── scripts/
│   └── ingest_knowledge.py
└── .gitignore
```

## Installation

1. Clone the repository.
2. Copy `.env.example` to `.env` and set the required values.
3. Create a Python virtual environment.
4. Install the backend dependencies.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

5. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Environment variables

Set the following values in `.env`:

```bash
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4o-mini
APP_ENV=development
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/order_support
CHROMA_PERSIST_DIRECTORY=./data/chroma
VECTOR_COLLECTION=project_knowledge
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running locally

Start the backend:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Start the frontend:

```bash
cd frontend
npm run dev
```

Start the supporting services with Docker:

```bash
docker compose up -d postgres redis chroma
```

## API documentation

FastAPI automatically exposes OpenAPI documentation at:

- http://localhost:8000/docs
- http://localhost:8000/redoc

Endpoints include:

- POST /api/chat
- POST /api/agent/run
- POST /api/documents/upload
- POST /api/documents/ingest
- GET /api/sessions/{session_id}
- GET /api/workflows/{workflow_id}
- POST /api/approval/{workflow_id}
- GET /api/health
- GET /api/metrics

## Sample requests

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-001",
    "user_id": "user-100",
    "message": "My order ORD-4419 is delayed. Please review it.",
    "conversation_history": []
  }'
```

## Testing

Run the backend tests:

```bash
cd backend
pytest app/tests/test_workflow.py
```

## Evaluation

The project includes a sample dataset for evaluation. It covers normal, ambiguous, missing-information, tool-failure, and adversarial scenarios. Evaluation criteria include intent accuracy, retrieval relevance, groundedness, citation correctness, tool selection, policy compliance, and human escalation quality.

## Docker

Use the root Docker Compose file to launch the backend and supporting services:

```bash
docker compose up --build
```

## Deployment

The frontend is prepared for Vercel and the backend is structured for deployment behind Docker or on an app platform such as Azure App Service, Render, or Railway.

## Limitations

- The current demo uses mock operational APIs for local development.
- Real LLM calls require a valid OpenAI API key.
- ChromaDB is configured for local persistence and can be extended to a managed service.
- Human approval and workflow state are simplified for a demo but are ready for extension.

## Future enhancements

- Connect to real order and carrier APIs
- Add PostgreSQL-backed workflow persistence
- Expand the RAG collection with support SOPs and FAQs
- Add Redis session state and rate limiting
- Integrate full LangGraph state transitions and retries
- Add OpenTelemetry tracing and LangSmith evaluation dashboards
- Create a richer admin/metrics panel and evaluation report pipeline

## Summary

This app demonstrates a grounded, multi-agent AI support workflow for delivery problems and is structured to be extended to additional business domains such as banking, insurance, or healthcare.

# Adaptive AI Learning System

A stateful adaptive tutoring agent built with **LangGraph** and **LangChain**. The system maintains a persistent learner belief model, chooses teaching actions dynamically, and personalizes explanations based on each learner's profile and knowledge state.

> **Not** "an LLM with a better prompt." This is an agentic learning product that observes, decides, acts, evaluates, and updates state in a bounded loop.

**Architecture reference:** `adaptive_ai_learning_system_v1_2_architecture.pdf`

---

## What It Does

| Capability | Behavior |
|---|---|
| **Observe** | Reads learner profile, mastery, confidence, and recent evidence |
| **Decide** | Chooses teach, diagnose, practice, or continue |
| **Act** | Generates personalized lessons, diagnostics, or exercises |
| **Evaluate** | Scores learner responses (planned) |
| **Update** | Changes mastery, confidence, and preferences (planned) |
| **Loop** | Routes to the next action based on updated state |

---

## Current Status

| Phase | Description | Status |
|---|---|---|
| **Phase 0** | Architecture skeleton, domain models, service interfaces | Done |
| **Phase 1** | Understand → Load State → Tutor (hardcoded learner profile) | Done |
| **Phase 1B** | Tool-enabled Tutor with safe read-only tools (max 2 rounds) | Done |
| **Phase 2** | PostgreSQL persistence | In progress |
| **Phase 3** | Concept resolver + `find_concept()` | Planned |
| **Phase 4** | Diagnostic + uncertainty routing | Planned |
| **Phase 5** | Evaluator + mastery engine | Planned |
| **Phase 6** | Full adaptive routing loop | Partial (early prototype) |
| **Phase 7–10** | Learning-style inference, streaming, Android, LangSmith | Planned |

### Phase 2 detail

Learner data now comes from PostgreSQL at runtime. Concepts and evidence are
still hardcoded because their tables do not exist yet.

| Piece | Status |
|---|---|
| PostgreSQL 16 in Docker with a persistent volume | Done |
| SQLAlchemy engine, session factory, declarative `Base` | Done |
| `learner_profiles` and `user_concept_states` tables | Done |
| Alembic migration applied (`51ecff03db5c`) | Done |
| Learner seed script | Done |
| `LearnerRepository` returning domain objects | Done |
| `PostgresLearnerService` behind the existing interface | Done |
| Service container; node and tools share one backend | Done |
| `PostgresConceptService` / `PostgresEvidenceService` | Not started |
| `concepts`, `concept_edges`, `learning_evidence`, `sessions` tables | Not started |
| LangGraph PostgreSQL checkpointer | Not started |

---

## Architecture

```
User Message
     |
[Understand Request]        <- LLM Call #1 (structured output)
     |
[Load Learner State]        <- PostgresLearnerService (Phase 2)
     |
[Detect Next Action]        <- Deterministic routing
     |
     |-- teach    -> [Tutor Node]      <- LLM Call #2 + safe tools
     |-- practice -> [Practice Node]
     |-- diagnose -> [Diagnose Node]
     |
    END
```

### Tutor Tool Loop (Phase 1B)

```
Tutor LLM
  |- may call get_learner_state()
  |- may call get_mastery(concept)
  |- may call get_dependencies(concept)
  |- may call get_recent_evidence(concept)
       |
  Tool Runner (max 2 rounds)
       |
  Final personalized response
```

### Layer Separation

```
LangGraph State        -> temporary workflow/session data
Checkpointer           -> persists graph state between calls (Phase 2)
Learner Services + DB  -> permanent mastery, evidence, profile, concepts
```

---

## Project Structure

```
app/
├── ai/
│   ├── graph/
│   │   ├── state.py           # WorkflowState schema
│   │   └── build_graph.py     # LangGraph workflow definition
│   ├── nodes/
│   │   ├── understand_request.py
│   │   ├── load_learner_state.py
│   │   ├── detect_next_action.py
│   │   ├── tutor.py           # Tool-enabled tutor
│   │   ├── practice.py
│   │   └── diagnose.py
│   ├── tools/
│   │   ├── safe_reads.py      # Controlled read-only service wrapper
│   │   ├── tool_runner.py     # Bounded tool execution loop
│   │   ├── learner_tools.py   # get_learner_state, get_mastery
│   │   ├── concept_tools.py   # get_dependencies
│   │   └── evidence_tools.py  # get_recent_evidence
│   └── llm_schemas/
│       └── understand_request.py
├── domain/
│   ├── learner/               # LearnerState, LearningProfile
│   ├── mastery/               # MasterySnapshot, MasteryUpdate
│   ├── concepts/              # Concept, ConceptNeighborhood
│   ├── evidence/              # LearningEvidence
│   └── routing/               # TeachingAction, RoutingDecision
├── services/
│   ├── container.py           # Composition root; selects the backend
│   ├── learner_service/       # Interface + Hardcoded + Postgres
│   ├── concept_service/       # Interface + HardcodedConceptService
│   └── evidence_service/      # Interface + HardcodedEvidenceService
└── infrastructure/
    ├── llm/
    │   └── client.py          # Groq LLM client
    └── db/
        ├── base.py            # SQLAlchemy declarative Base
        ├── engine.py          # Engine + SessionLocal
        ├── models/            # LearnerProfile, UserConceptState
        └── repositories/      # LearnerRepository

alembic/                       # Migration environment + versions
scripts/
├── seed_db.py                 # Seed user-a and user-b profiles
└── check_learner_repository.py  # Verify repository reads
```

---

## Tech Stack

| Layer | Choice |
|---|---|
| Agent orchestration | LangGraph |
| LLM integration | LangChain + Groq |
| Primary LLM | `openai/gpt-oss-120b` (Groq) |
| Database | PostgreSQL 16 + SQLAlchemy + Alembic (Docker) |
| Observability (planned) | LangSmith |
| API (planned) | FastAPI |
| Mobile (planned) | Android (Kotlin + Jetpack Compose) |

---

## Setup

### Prerequisites

- Python 3.11+
- Groq API key ([console.groq.com](https://console.groq.com))
- Docker Desktop (for PostgreSQL)

### Install

```bash
git clone <your-repo-url>
cd "Adaptive Learning Agent"

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### Environment

Create `app/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql+psycopg://postgres:devpassword@localhost:5432/adaptive_learning
```

### Database

Start PostgreSQL, apply migrations, and seed the example learners:

```bash
docker start adaptive-learning-postgres

python -m alembic upgrade head
python -m scripts.seed_db
```

Verify the repository reads the seeded rows:

```bash
python -m scripts.check_learner_repository
```

---

## Running

From the project root:

```bash
python smoke_test_llm.py
```

This runs all three routes for both test users, so personalization
differences are visible in one pass.

Expected output per user:

```
Message: Teach me Python recursion
Intent: learn
Action: teach
Response: <personalized teaching explanation>

Message: Help me review Python recursion
Intent: review
Action: practice
Response: <practice question>

Message: Debug why my recursive function never stops
Intent: debug
Action: diagnose
Response: <diagnostic question>
```

### Test Users

| User ID | Profile |
|---|---|
| `user-a` | Example-first, shallow depth, slow pacing |
| `user-b` | Top-down, deep depth, code-heavy, fast pacing |

Both are stored in `learner_profiles` and read from PostgreSQL at runtime.
Set `LEARNER_BACKEND=hardcoded` in `app/.env` to fall back to the in-code
Phase 1 data.

---

## Design Principles

1. **Agentic where decisions matter** — the LLM chooses tools, teaching strategy, and concept resolution.
2. **Deterministic where correctness matters** — mastery updates, routing guards, persistence, and concept IDs are owned by code, not the LLM.
3. **Extend, don't rewrite** — each phase adds nodes or swaps service implementations behind stable interfaces.
4. **Bounded loops** — max 2 tool rounds per turn; no infinite graph traversal.
5. **Unknown is not zero** — no mastery record means unknown, not beginner.

---

## Safe Tool Allow-List (Phase 1B)

The Tutor LLM may only call these read-only tools:

| Tool | Purpose |
|---|---|
| `get_learner_state(user_id)` | Fetch learner profile + knowledge slice |
| `get_mastery(user_id, concept_id)` | Fetch mastery/confidence for one concept |
| `get_dependencies(concept_id)` | Fetch prerequisite neighborhood |
| `get_recent_evidence(user_id, concept_id)` | Fetch recent quiz/diagnostic signals |

No write tools, web access, SQL, or filesystem tools are exposed to the LLM.

---

## Roadmap

- [x] Phase 0 — Architecture skeleton
- [x] Phase 1 — Minimal stateful tutoring loop
- [x] Phase 1B — Controlled tool-calling extension
- [ ] Phase 2 — PostgreSQL learner state (schema, seed, and repository done)
- [ ] Phase 3 — Concept resolver + sparse dependencies
- [ ] Phase 4 — Diagnostic and uncertainty
- [ ] Phase 5 — Evaluator + mastery engine
- [ ] Phase 6 — Full adaptive routing loop
- [ ] Phase 7 — Learning-style inference
- [ ] Phase 8 — Latency + streaming
- [ ] Phase 9 — Android product integration
- [ ] Phase 10 — LangSmith evaluation + portfolio polish

---

## License

Private project — all rights reserved.

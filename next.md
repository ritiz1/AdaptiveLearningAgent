# Next Session — Move Concepts Into PostgreSQL (2 Hours)

## Current checkpoint

### Completed

- [x] PostgreSQL 16 container with a persistent Docker volume
- [x] `learner_profiles` and `user_concept_states` tables, migration `51ecff03db5c`
- [x] `scripts/seed_db.py` seeds `user-a` and `user-b` idempotently
- [x] `LearnerRepository` returns domain objects, not ORM rows
- [x] `PostgresLearnerService` behind the existing `LearnerService` interface
- [x] `app/services/container.py` composition root selects the backend
- [x] `LEARNER_BACKEND=postgres|hardcoded` switches implementations
- [x] Node and LLM tools resolve the same service instance per turn
- [x] Lazy engine and session factory; no database access at import time
- [x] Smoke test covers `user-a` and `user-b` and passes on both
- [x] A direct SQL profile edit visibly changes tutor behavior

### Important current state

Learner data is live from PostgreSQL. **Concepts and evidence are still
hardcoded** because their tables do not exist:

```text
app/services/concept_service/hardcoded.py    3 concepts, 1 prerequisite list
app/services/evidence_service/hardcoded.py   stub evidence
```

This session moves concepts into the database.

---

## Goal for the next 2 hours

Add `concepts` and `concept_edges` tables, a concept repository, and a
PostgreSQL-backed `ConceptService` behind the existing interface.

Do not modify the LangGraph workflow, node boundaries, routing logic, or
prompts.

---

## Decide before writing code

Two items here are developer-owned policy, not boilerplate. Settle them
first.

### A. Lazy concept creation is now a database write

`HardcodedConceptService.resolve_concept()` invents a concept and stores it
in memory when the name is unknown. Backed by PostgreSQL, that becomes an
`INSERT`.

Decide:

- [ ] `resolve_concept` may insert new concept rows
- [ ] `resolve_concept` is read-only and returns an unsaved `Concept`
- [ ] Writes are allowed but only from deterministic code, never a tool

Note that `resolve_concept` is **not** in `SAFE_READ_TOOL_NAMES`, so the LLM
cannot call it today. Keep it that way unless you decide otherwise.

### B. Concept IDs are currently unnormalized

The tutor LLM invents concept IDs. In the last smoke run it called
`get_mastery` with `python_functions` (underscore), while the hardcoded
registry uses `python-functions` (hyphen). Nothing reconciles the two, so
mastery lookups silently miss.

Decide:

- [ ] Normalize IDs in one place (slugify: lowercase, spaces/underscores to hyphens)
- [ ] Or defer entirely to the Phase 3 concept resolver

Do not scatter normalization across tools.

---

## First hour — Schema and repository

### 1. Create the models (25 minutes)

Create:

```text
app/infrastructure/db/models/concept.py
```

`Concept` table:

- [ ] `concept_id` primary key, `String(128)`
- [ ] `name` non-null, `String(256)`
- [ ] `description` nullable `Text`
- [ ] `created_at` timezone-aware `DateTime` with server default

`ConceptEdge` table:

- [ ] `from_concept_id` and `to_concept_id`, both foreign keys to `concepts`
- [ ] `relation` non-null, default `"prerequisite"`
- [ ] Composite primary key on `(from_concept_id, to_concept_id, relation)`
- [ ] Check constraint preventing self-edges
- [ ] Index on `to_concept_id` for prerequisite lookups

Register both in `app/infrastructure/db/models/__init__.py`.

### 2. Generate and inspect the migration (15 minutes)

```powershell
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "add concepts and concept edges"
```

Read the generated file before applying it. Confirm foreign keys, the
composite primary key, and that no existing table is altered.

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
```

### 3. Create the concept repository (20 minutes)

Create:

```text
app/infrastructure/db/repositories/concept_repository.py
```

Implement:

```text
get_concept(concept_id) -> Concept | None
get_prerequisites(concept_id) -> list[tuple[Concept, ConceptEdge]]
```

Rules unchanged from the learner repository:

- Repository owns every SQLAlchemy query
- Methods return domain objects, never ORM rows
- Constructor takes a `Session`, not a session factory

---

## Second hour — Service, seed, and wiring

### 4. Seed the concept graph (15 minutes)

Extend `scripts/seed_db.py` with an idempotent concept seed matching the
hardcoded registry:

```text
python-functions   Python Functions
call-stack         Call Stack
python-recursion   Python Recursion

python-functions -> python-recursion   prerequisite
call-stack       -> python-recursion   prerequisite
```

Keep the existing learner seed working. Insert-if-missing, as before.

### 5. Create the service (25 minutes)

Create:

```text
app/services/concept_service/postgres.py
```

`PostgresConceptService(ConceptService)`, taking a session factory and
opening a short session per method, matching `PostgresLearnerService`.

- [ ] `get_concept` delegates to the repository
- [ ] `get_dependencies` builds a `ConceptNeighborhood` and respects `max_depth`
- [ ] `resolve_concept` follows whichever policy you chose in decision A
- [ ] Unknown target still returns a neighborhood, not an exception

### 6. Wire it into the container (10 minutes)

In `app/services/container.py`, give `get_concept_service()` the same
treatment as the learner service:

```text
CONCEPT_BACKEND=postgres|hardcoded
```

Do not delete `concept_service/hardcoded.py`. It is the rollback path.

### 7. Verify (10 minutes)

Extend `scripts/check_learner_repository.py`, or add a sibling script:

- [ ] `get_concept("python-recursion")` returns the seeded concept
- [ ] `get_dependencies("python-recursion")` returns both prerequisites
- [ ] `max_depth=0` returns no prerequisites
- [ ] An unknown concept returns an empty neighborhood, not a crash
- [ ] `CONCEPT_BACKEND=hardcoded` still resolves the old service

Then run the full smoke test and confirm the tutor's `get_dependencies`
tool still returns useful data:

```powershell
.\.venv\Scripts\python.exe smoke_test_llm.py
```

---

## End-of-session success criteria

- [ ] `concepts` and `concept_edges` tables exist and are seeded
- [ ] `PostgresConceptService` implements the existing interface
- [ ] `get_dependencies` reads prerequisites from PostgreSQL
- [ ] Backend is switchable by environment variable
- [ ] Hardcoded concept service still exists but is unused by default
- [ ] Smoke test passes for both users on all three routes

---

## Save for a later session

- `learning_evidence` and `sessions` tables, then `PostgresEvidenceService`
- LangGraph PostgreSQL checkpointer for cross-turn session state
- Concept resolution and `find_concept()` (Phase 3)
- Diagnostic and uncertainty routing (Phase 4)
- Evaluator and mastery-update engine (Phase 5)
- Any change to graph nodes, routing, or prompts

---

## Known issues

- The tutor invents concept IDs that do not match the registry. See
  decision B above.
- `MasterySnapshot` returns `mastery_estimate=0.0` alongside
  `is_unknown=True`. Callers must check the flag, not the number.
- Scripts must run as modules with the project venv:
  `.\.venv\Scripts\python.exe -m scripts.seed_db`

---

## References

- Architecture: `adaptive_ai_learning_system_v1_2_architecture.pdf`
- Concept interface: `app/services/concept_service/interface.py`
- Pattern to copy: `app/services/learner_service/postgres.py`
- Repository pattern: `app/infrastructure/db/repositories/learner_repository.py`
- Composition root: `app/services/container.py`

# Fullstack Developer Prescreening

**Candidate:** Adjie Hari Fajar  
**Position:** Programmer (NextJS & Python)  
**Company:** PT Injani Systems  

---

## Overview

This repository contains the technical prescreening submission for the **Programmer (NextJS & Python)** position at PT Injani Systems.

It includes:
- Comprehensive technical answers, architectural analysis, and engineering rationale in [`docs/Adjie_Hari_Fajar_Fullstack_Developer_Prescreening_PT_Injani_Systems.docx`](./docs/Adjie_Hari_Fajar_Fullstack_Developer_Prescreening_PT_Injani_Systems.docx) accompanied by architectural diagrams in [`docs/`](./docs/).
- A complete, runnable **Next.js 14 (App Router)** frontend with Edge Middleware, cryptographic JWT verification (`jose`), and SLA analytics dashboard.
- A complete, runnable **FastAPI (Python)** backend with Pydantic v2 schemas, cryptographic JWT verification, Cloud Tasks worker endpoint, rate limiting, and WhatsApp order extraction service.
- Production **PostgreSQL 16** schemas with generated columns, range partitioning, and keyset-aligned indexing.
- Automated test suites (26 backend unit tests with pytest; frontend typechecking, linting, 8 strict cryptographic authentication tests via tsx, and Next.js production build).
- Separated GitHub Actions workflows: zero-credential automated Quality CI ([`.github/workflows/ci.yml`](./.github/workflows/ci.yml)) and guarded manual cloud deployment ([`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml)).
- Executive Word technical report: [`docs/Adjie_Hari_Fajar_Fullstack_Developer_Prescreening_PT_Injani_Systems.docx`](./docs/Adjie_Hari_Fajar_Fullstack_Developer_Prescreening_PT_Injani_Systems.docx).

---

## Questions Covered

- **Part A (Candidate Profile):**
  - **P1:** Work style, handling tasks with minimal direction, and autonomous discovery.
  - **P2:** Ownership, communication, and pragmatic engineering in a startup/small-team environment.
  - **P3:** 2–3 year engineering aspirations (technical lead, platform architecture, system reliability).
  - **P4:** Motivation for seeking this role at PT Injani Systems.
  - **P5:** Salary expectations format.
- **Part B (Technical Questions):**
  - **Q1:** Self-hosted open-weight LLM (Gemma 3 4B / 12B via Ollama / vLLM) for WhatsApp order extraction, prompt structuring, evaluation metrics, and business data safety boundaries.
  - **Q2:** SLA analytics dashboard architecture, PostgreSQL generated columns schema, and multi-step approval bottleneck tracking.
  - **Q3:** Google Cloud Tasks scheduled workflows: local emulation, production Cloud Logging / Cloud Trace monitoring, and dead-letter handling.
  - **Q4:** PostgreSQL query diagnosis with `EXPLAIN (ANALYZE, BUFFERS)`, composite index order `(user_id, status, created_at DESC, id DESC)` for keyset pagination, and table partitioning.
  - **Q5:** Next.js 14 API architecture: cryptographic JWT verification in Edge Middleware with `jose`, rate limiting, RFC 7807 error envelopes, and production considerations for role-based authorization and object-level IDOR protection.
  - **Q6:** Python async workers, comparison of FastAPI `BackgroundTasks` vs Celery vs Cloud Tasks, task progress reporting, and HTTP idempotency locks.
  - **Q7:** End-to-end fullstack system design, Docker containers, Workload Identity Federation (WIF) CI/CD, and GCP Cloud Run deployment.

---

## Tech Stack

- **Frontend:** Next.js 14 (App Router, Server Components, Edge Middleware), TypeScript, Tailwind CSS, `jose` (JWT verification).
- **Backend:** Python 3.12 / 3.13, FastAPI, Pydantic v2, Uvicorn, asyncio, HTTPX, pytest.
- **Database:** PostgreSQL 16 (Relational schemas, generated columns, range partitioning, composite B-tree indexing).
- **Cloud & Orchestration:** Google Cloud Tasks, Cloud Scheduler, Cloud Run, Cloud Logging, Cloud Secret Manager, Docker.
- **CI/CD:** GitHub Actions (split into zero-credential Quality CI and guarded Cloud Deployment).

---

## Repository Structure

```text
.
├── PRESCREENING_ANSWERS.md                 # Complete written answers (P1–P5, Q1–Q7)
├── README.md                               # Project documentation and execution instructions
│
├── database/                               # PostgreSQL Schemas and Analytics Queries
│   ├── schema_q2_sla.sql                   # Q2: Approval workflows, step definitions, generated SLA columns
│   ├── queries_q2_analytics.sql            # Q2: Analytical SQL queries for bottleneck detection
│   ├── schema_q4_transactions.sql          # Q4: 10M-row transactions schema, composite index, partitioning
│   └── explain_analysis_q4.sql             # Q4: EXPLAIN ANALYZE walkthrough & keyset pagination
│
├── backend/                                # Python FastAPI Service
│   ├── requirements.txt                    # Backend dependencies
│   ├── pytest.ini                          # Test configuration
│   ├── Dockerfile                          # Cloud Run container build
│   ├── .env.example                        # Backend environment variable template
│   ├── app/
│   │   ├── main.py                         # FastAPI entry point & exception handlers
│   │   ├── api/
│   │   │   ├── deps.py                     # Rate limiter, idempotency, auth dependencies
│   │   │   └── routes.py                   # REST routes (order extraction, task worker, submit)
│   │   ├── core/
│   │   │   ├── config.py                   # Environment configuration settings
│   │   │   ├── errors.py                   # Standardized error envelope (RFC 7807)
│   │   │   └── security.py                 # Cryptographic JWT & HMAC signature verification
│   │   ├── schemas/
│   │   │   ├── order.py                    # WhatsApp order extraction Pydantic models
│   │   │   └── task.py                     # Task progress & worker schemas
│   │   └── services/
│   │       ├── order_extractor.py          # Prompt builder & structured extraction logic
│   │       ├── evaluator.py                # Evaluation benchmark harness
│   │       └── task_manager.py             # In-memory async task lifecycle manager
│   └── tests/
│       ├── test_jwt_security.py            # JWT signature, expiration, and tampering tests
│       ├── test_cloud_tasks_worker.py      # Cloud Tasks worker and dead-letter retry tests
│       ├── test_order_extractor.py         # Intent and entity extraction tests
│       ├── test_idempotency_and_tasks.py   # Idempotency and task progress tests
│       └── test_error_and_security.py      # Webhook HMAC and rate limiter tests
│
├── frontend/                               # Next.js 14 App Router Project
│   ├── package.json                        # Node dependencies and scripts
│   ├── tsconfig.json                       # Strict TypeScript configuration
│   ├── next.config.mjs                     # Next.js configuration
│   ├── tailwind.config.ts                  # Tailwind styling config
│   ├── middleware.ts                       # Edge runtime JWT gatekeeper
│   ├── .env.example                        # Frontend environment variable template
│   ├── app/
│   │   ├── layout.tsx                      # Root layout with top navigation shell
│   │   ├── page.tsx                        # Engineering portal overview with system specs
│   │   ├── globals.css                     # Base typography and accessibility styling
│   │   ├── api/
│   │   │   ├── orders/route.ts             # Protected API route with rate limiting
│   │   │   └── webhooks/route.ts           # HMAC-protected webhook endpoint
│   │   └── dashboard/
│   │       ├── page.tsx                    # Q2: SLA Analytics Dashboard (React Server Component)
│   │       ├── loading.tsx                 # Restrained skeleton loading fallback
│   │       ├── error.tsx                   # Client error boundary
│   │       └── components/
│   │           └── sla-charts.tsx          # Metric cards, P50/P90 bottleneck chart, department table
│   ├── components/
│   │   └── Navbar.tsx                      # Unified application navigation header
│   ├── lib/
│   │   ├── auth.ts                         # Cryptographic JWT verification (jose)
│   │   ├── errors.ts                       # Standardized API response format
│   │   ├── rate-limit.ts                   # In-memory sliding window rate limiter
│   │   └── sla-data.ts                     # Deterministic assessment dataset & pure aggregations
│
├── .github/
│   └── workflows/
│       ├── ci.yml                          # Zero-secret Quality CI (Lint, Typecheck, Test, Build)
│       └── deploy.yml                      # Guarded Cloud Run and Vercel deployment pipeline
│
└── docs/
    ├── Adjie_Hari_Fajar_Fullstack_Developer_Prescreening_PT_Injani_Systems.docx
    └── *.png                               # Architectural diagrams & protocol flows
```

---

## Prerequisites

- **Python:** 3.12+ (or 3.13)
- **Node.js:** v20+ / npm v10+
- **Database (Optional for local review):** PostgreSQL 16
- **Package Managers:** `uv` or `pip` for Python; `npm` for Node.js.

---

## Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend

# Install exact dependencies
npm ci
```

### 3. PostgreSQL (Optional for Local Query Inspection)

The SQL schemas can be inspected or executed against any standard PostgreSQL 16 instance:

```bash
psql -U postgres -d your_database -f database/schema_q2_sla.sql
psql -U postgres -d your_database -f database/schema_q4_transactions.sql
```

---

## Environment Variables

Copy the provided example files to create local configuration:

### Backend (`backend/.env`)

```ini
ENVIRONMENT=development
PORT=8000
DATABASE_URL=postgresql://user:password@localhost:5432/injani_db
JWT_SECRET=change-this-to-a-secure-secret-with-at-least-32-chars
WEBHOOK_SECRET=change-this-to-a-secure-webhook-secret
OLLAMA_URL=http://localhost:11434
```

### Frontend (`frontend/.env.local`)

```ini
NEXT_PUBLIC_APP_ENV=development
BACKEND_API_URL=http://localhost:8000
JWT_SECRET=change-this-to-a-secure-secret-with-at-least-32-chars
WEBHOOK_SECRET=change-this-to-a-secure-webhook-secret
```

---

## Running the Application

### 1. Start the Backend Service

```bash
cd backend
.venv\Scripts\uvicorn app.main:app --reload --port 8000
```
- Interactive Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/healthz`

### 2. Start the Frontend Development Server

```bash
cd frontend
npm run dev
```
- Web Application: `http://localhost:3000`
- SLA Analytics Dashboard: `http://localhost:3000/dashboard`

---

## Frontend

The Next.js frontend includes a responsive SLA analytics dashboard. The dashboard uses a deterministic assessment dataset with URL-driven filters for demonstrating server-rendered analytical views.

---

## Testing & Verification

All quality gates have been executed locally:

### 1. Backend Test Suite (pytest)

```bash
cd backend
pytest -v
```

**Results:**
```text
tests/test_cloud_tasks_worker.py::test_cloud_task_worker_execution_success PASSED
tests/test_cloud_tasks_worker.py::test_cloud_task_worker_dead_letter_on_max_retries PASSED
tests/test_error_and_security.py::test_standardized_validation_error_format PASSED
tests/test_error_and_security.py::test_standardized_not_found_error_format PASSED
tests/test_error_and_security.py::test_hmac_webhook_verification_success_and_tampering PASSED
tests/test_error_and_security.py::test_missing_webhook_secret_fails_closed PASSED
tests/test_error_and_security.py::test_rate_limiter_exceeded PASSED
tests/test_idempotency_and_tasks.py::test_idempotent_order_submission_prevents_duplicate_runs PASSED
tests/test_idempotency_and_tasks.py::test_concurrent_idempotency_request_conflict PASSED
tests/test_idempotency_and_tasks.py::test_async_task_progress_lifecycle[asyncio] PASSED
tests/test_jwt_security.py::test_valid_jwt_token_verification PASSED
tests/test_jwt_security.py::test_forged_jwt_signature_rejected PASSED
tests/test_jwt_security.py::test_tampered_payload_rejected PASSED
tests/test_jwt_security.py::test_expired_jwt_token_rejected PASSED
tests/test_jwt_security.py::test_malformed_jwt_token_rejected PASSED
tests/test_jwt_security.py::test_empty_jwt_token_rejected PASSED
tests/test_jwt_security.py::test_unsupported_algorithm_rejected PASSED
tests/test_jwt_security.py::test_missing_exp_claim_rejected PASSED
tests/test_jwt_security.py::test_missing_jwt_secret_fails_closed PASSED
tests/test_jwt_security.py::test_configured_jwt_secret_signing_and_verification PASSED
tests/test_order_extractor.py::test_order_intent_and_entity_extraction PASSED
tests/test_order_extractor.py::test_indonesian_unit_normalization PASSED
tests/test_order_extractor.py::test_inquiry_intent_detection PASSED
tests/test_order_extractor.py::test_complaint_intent_detection PASSED
tests/test_order_extractor.py::test_prompt_builder_structure PASSED
tests/test_order_extractor.py::test_evaluator_metrics_calculation PASSED

======================= 26 passed in 0.97s =======================
```

### 2. Frontend Test Suite & Build

```bash
cd frontend

# 1. Typecheck
npm run typecheck
# Result: Exit code 0 (Zero type errors)

# 2. ESLint
npm run lint
# Result: Exit code 0 (No ESLint warnings or errors)

# 3. Strict Cryptographic Auth & Security Test Suite
npm run test:auth
# Result: 8/8 strict test cases passed via tsx (valid token, forged signature rejection,
# tampered payload rejection, expired token rejection, malformed token rejection,
# empty token rejection, valid webhook HMAC, tampered webhook HMAC rejection)

# 4. Production Next.js Build
npm run build
# Result: Production build compiled successfully (Exit code 0)
```

---

## API Overview

| Method | Endpoint | Description | Security |
|---|---|---|---|
| `POST` | `/api/v1/extract-order` | Extracts intent and structured line items from WhatsApp messages (Q1) | Rate limited (10 req/min) |
| `GET` | `/api/v1/evaluations/run` | Runs the precision, recall, and exact-match extraction benchmark (Q1c) | Internal / Public |
| `POST` | `/api/v1/tasks/worker` | Cloud Tasks worker execution endpoint with retry and DLQ handling (Q3) | Cloud Tasks header validation; Google OIDC verification recommended for production |
| `POST` | `/api/v1/orders/submit` | Idempotent order creation with background async processing (Q6) | `Idempotency-Key` header |
| `GET` | `/api/v1/tasks/{task_id}/progress` | Polling endpoint for background task completion status (Q6b) | Session / Public |
| `POST` | `/api/v1/webhooks/whatsapp` | Inbound WhatsApp webhook receiver (Q5) | `X-Hub-Signature-256` (HMAC) |
| `GET` | `/healthz` | Container health probe for Cloud Run / Kubernetes | Public |

---

## Key Engineering Decisions

1. **Cryptographic JWT Signature Verification (Security-First):**  
   Replaced insecure base64 decoding with full HMAC-SHA256 signature verification (`jose.jwtVerify` in Next.js Edge Middleware and `hashlib.sha256` in Python). Forged tokens, modified claims, and expired tokens are rejected at the edge before any database lookup.
2. **Business Data Safety Boundary for LLM Integration (Q1):**  
   The LLM is strictly confined to unstructured intent classification and slot extraction. Authoritative product pricing, stock levels, volume discounts, and taxes are retrieved exclusively from PostgreSQL and ERP services, eliminating hallucinations in commercial transactions.
3. **PostgreSQL Keyset-Aligned Indexing (Q4):**  
   Designed the composite index `(user_id, status, created_at DESC, id DESC) INCLUDE (amount, currency)`. Equality columns precede sort/cursor columns, guaranteeing deterministic keyset pagination without sort nodes and enabling Index-Only Scans when pages are marked all-visible.
4. **React Server Components & URL State for SLA Analytics (Q2):**  
   Delegated analytical percentiles and aggregations to PostgreSQL generated columns and Server Components. Filters are stored in URL query parameters, ensuring link shareability and zero client-side state boilerplate.
5. **Separation of Quality CI from Cloud Deployment (DevOps):**  
   Created a standalone automated Quality CI workflow ([`.github/workflows/ci.yml`](./.github/workflows/ci.yml)) that validates code quality (backend pytest, frontend typecheck, lint, auth tests, build) without requiring production cloud secrets. Cloud deployment is decoupled into a manual `workflow_dispatch` pipeline ([`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml)) using Workload Identity Federation.

---

## Assumptions

- **LLM Runtime:** Gemma 3 (4B for local prototyping / smaller instances, or 12B for high-throughput GPU serving) is intended for deployment via vLLM or Ollama. The local test suite uses a deterministic rule-based extractor to guarantee fully reproducible testing without requiring an active GPU daemon.
- **Single-Instance Caching:** The rate limiting and idempotency stores are implemented using thread-safe in-memory stores suitable for single-instance review. For multi-container production deployments, these components swap to Upstash Redis or Redis Cluster without changing public interface signatures.

---

## Known Limitations

- **Cloud Tasks Local Emulation:** While integration tests mock the Google headers directly, running full end-to-end task callbacks locally requires either the open-source Cloud Tasks emulator Docker container or ngrok.
- **PostgreSQL EXPLAIN ANALYZE:** Detailed query plan analysis is documented based on PostgreSQL query planner rules and table layout. Exact execution times in production will depend on server hardware and buffer cache warmth.

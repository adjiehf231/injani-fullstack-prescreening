# Fullstack Developer Prescreening — PT Injani Systems

Professional technical prescreening submission for the **Programmer (NextJS & Python)** position at **PT Injani Systems**.

---

## Overview

This repository contains the complete answers, production schemas, reference code implementations, automated test suites, and deployment blueprints for the Fullstack Developer Prescreening assessment.

The work adheres to production-grade engineering standards:
- **Part A (Candidate Profile):** Clear, structured professional answers for P1–P5 with candidate-specific inputs clearly highlighted.
- **Part B (Technical Questions Q1–Q7):** In-depth technical designs, production PostgreSQL schemas, Next.js 14 App Router patterns, Python FastAPI async worker patterns, LLM structured extraction, query optimization walkthroughs, and CI/CD pipelines.

The complete written answers can be reviewed in:
👉 **[`PRESCREENING_ANSWERS.md`](file:///d:/DOKUMEN%20AHF/Programmer%20%28NextJS%20&%20Python%29/PRESCREENING_ANSWERS.md)**

---

## Tech Stack

- **Frontend:** Next.js 14 (App Router, React Server Components, Edge Middleware), TypeScript, Tailwind CSS, Shadcn UI / Tremor, Recharts.
- **Backend:** Python 3.12 / 3.13, FastAPI, Pydantic v2, Uvicorn, asyncio, HTTPX.
- **AI / LLM:** Self-hosted open-weight LLMs (Gemma 3, Ollama, vLLM) with constrained JSON decoding.
- **Database:** PostgreSQL 16 (Relational modeling, Generated Columns, Partitioning, Composite & Partial Indexing).
- **Background Tasks & Cloud:** Google Cloud Tasks, Google Cloud Scheduler, Google Cloud Run, Cloud Logging, Cloud Monitoring, Cloud Secret Manager.
- **Testing & Tooling:** Pytest, uv, Docker, GitHub Actions (Workload Identity Federation).

---

## Project Structure

```
Programmer (NextJS & Python)/
├── PRESCREENING_ANSWERS.md                 # Complete answers for all questions (P1–P5, Q1–Q7)
├── README.md                               # System documentation & execution manual
├── fullstack_developer_prescreening SEPT 2026.pdf # Source assessment document
│
├── database/                               # PostgreSQL Production Schemas & Queries
│   ├── schema_q2_sla.sql                   # Q2: SLA Workflows, steps, assignees, generated columns
│   ├── queries_q2_analytics.sql            # Q2: Analytical SQL queries for bottleneck identification
│   ├── schema_q4_transactions.sql          # Q4: 10M-row transactions schema, indexing, partitioning
│   └── explain_analysis_q4.sql             # Q4: EXPLAIN ANALYZE walkthrough & cursor pagination
│
├── backend/                                # Python FastAPI Reference Implementation
│   ├── requirements.txt                    # Python dependencies
│   ├── pytest.ini                          # Pytest configuration
│   ├── Dockerfile                          # Production Cloud Run container definition
│   ├── .dockerignore                       # Docker build exclusion rules
│   ├── app/
│   │   ├── main.py                         # FastAPI app with centralized error handling & CORS
│   │   ├── api/
│   │   │   ├── deps.py                     # Rate limiter, idempotency store, auth dependencies
│   │   │   └── routes.py                   # REST endpoints (WhatsApp extraction, order submit, tasks)
│   │   ├── core/
│   │   │   ├── errors.py                   # Typed error schemas (RFC 7807) & domain exceptions
│   │   │   └── security.py                 # HMAC-SHA256 signature verification & JWT validation
│   │   ├── schemas/
│   │   │   ├── order.py                    # WhatsApp order entity & extraction Pydantic schemas
│   │   │   └── task.py                     # Task progress & status schemas
│   │   └── services/
│   │       ├── order_extractor.py          # Gemma 3 prompt builder & structured extraction engine
│   │       ├── evaluator.py                # Information extraction evaluation harness (P/R/F1/EM)
│   │       └── task_manager.py             # Async background task manager with progress reporting
│   └── tests/
│       ├── test_order_extractor.py         # Unit tests for order extraction & evaluation logic
│       ├── test_idempotency_and_tasks.py   # Unit tests for idempotency & task progress lifecycle
│       └── test_error_and_security.py      # Unit tests for standardized errors, HMAC, rate limiting
│
├── frontend/                               # Next.js 14 App Router Reference Implementation
│   ├── middleware.ts                       # Next.js Edge middleware for path gating & auth check
│   ├── lib/
│   │   ├── auth.ts                         # JWT & Webhook HMAC verification helpers
│   │   ├── errors.ts                       # Typed Next.js API response & error envelope
│   │   └── rate-limit.ts                   # In-memory sliding window rate limiter without Redis
│   └── app/
│       ├── api/
│       │   ├── orders/route.ts             # Typed API route (validation, rate limit, backend proxy)
│       │   └── webhooks/route.ts           # External webhook route (HMAC-SHA256 protected)
│       └── dashboard/
│           ├── page.tsx                    # Q2: SLA Analytics Dashboard (React Server Component)
│           └── components/
│               └── sla-charts.tsx          # SLA KPI cards, bottleneck chart, department backlog table
│
└── .github/
    └── workflows/
        └── deploy.yml                      # Q7: GitHub Actions CI/CD pipeline (Vercel & Cloud Run)
```

---

## Setup & Prerequisites

- **Python:** 3.12+ (or 3.13)
- **Package Manager:** `uv` (recommended) or standard `pip`
- **Node.js:** v20+ / npm v10+

### 1. Backend Setup

```bash
cd backend

# Create virtual environment with uv (or python -m venv .venv)
uv venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Environment Variables

Create `.env` in `backend/`:
```ini
ENVIRONMENT=development
PORT=8000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/injani_db
WEBHOOK_SECRET=injani-webhook-secret-token
JWT_SECRET=injani-production-secret-key-32-chars
OLLAMA_URL=http://localhost:11434
```

Create `.env.local` in `frontend/`:
```ini
NEXT_PUBLIC_APP_ENV=development
BACKEND_API_URL=http://localhost:8000
WEBHOOK_SECRET=injani-webhook-secret-token
JWT_SECRET=injani-production-secret-key-32-chars
```

---

## Running Backend & Verification

### Run the FastAPI Backend
```bash
cd backend
.venv\Scripts\uvicorn app.main:app --reload --port 8000
```
Interactive Swagger documentation will be available at `http://localhost:8000/docs`.

### Run Automated Tests (Pytest)
```bash
cd backend
.venv\Scripts\pytest -v
```

**Actual Test Execution Results:**
```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\DOKUMEN AHF\Programmer (NextJS & Python)\backend
configfile: pytest.ini
testpaths: tests
collected 13 items

tests/test_error_and_security.py::test_standardized_validation_error_format PASSED      [ 7%]
tests/test_error_and_security.py::test_standardized_not_found_error_format PASSED       [15%]
tests/test_error_and_security.py::test_hmac_webhook_verification_success_and_tampering PASSED [23%]
tests/test_error_and_security.py::test_rate_limiter_exceeded PASSED                    [30%]
tests/test_idempotency_and_tasks.py::test_idempotent_order_submission_prevents_duplicate_runs PASSED [38%]
tests/test_idempotency_and_tasks.py::test_concurrent_idempotency_request_conflict PASSED [46%]
tests/test_idempotency_and_tasks.py::test_async_task_progress_lifecycle[asyncio] PASSED [53%]
tests/test_order_extractor.py::test_order_intent_and_entity_extraction PASSED          [61%]
tests/test_order_extractor.py::test_indonesian_unit_normalization PASSED               [69%]
tests/test_order_extractor.py::test_inquiry_intent_detection PASSED                    [76%]
tests/test_order_extractor.py::test_complaint_intent_detection PASSED                  [84%]
tests/test_order_extractor.py::test_prompt_builder_structure PASSED                    [92%]
tests/test_order_extractor.py::test_evaluator_metrics_calculation PASSED               [100%]

======================= 13 passed in 1.53s =======================
```

---

## API Endpoints Summary

| Method | Path | Description | Authentication / Security |
|---|---|---|---|
| `POST` | `/api/v1/extract-order` | Extracts intent and items from WhatsApp chat message (Q1) | Rate limited (10 req/min) |
| `GET` | `/api/v1/evaluations/run` | Executes the precision, recall, F1, and exact-match benchmark (Q1c) | Public / Internal |
| `POST` | `/api/v1/orders/submit` | Idempotent order submission with async background PDF compilation (Q6) | `Idempotency-Key` header |
| `GET` | `/api/v1/tasks/{task_id}/progress` | Real-time progress polling for background tasks (Q6b) | Public / User session |
| `POST` | `/api/v1/webhooks/whatsapp` | Inbound WhatsApp webhook receiver (Q5) | `X-Hub-Signature-256` (HMAC-SHA256) |
| `GET` | `/healthz` | Kubernetes / Cloud Run liveness & readiness probe | Public |

---

## Key Engineering Decisions

1. **Self-Hosted LLM Architecture (Q1):**  
   Selected quantized **Gemma 3 via vLLM / Ollama** with constrained JSON decoding rather than token-billed APIs. This reduces marginal cost per message to zero and allows local compliance with Indonesian data privacy standards.
2. **Server-Side Rendering & URL State for SLA Analytics (Q2):**  
   Leveraged **React Server Components (RSC)** and **`searchParams`** URL state. By delegating data aggregation directly to PostgreSQL and keeping state in the URL query string, we eliminated hundreds of lines of client-side state boilerplate (Redux/Zustand) while guaranteeing shareable, bookmarkable filter views.
3. **Database Indexing & Schema (Q2 & Q4):**  
   Implemented generated columns (`elapsed_minutes`, `is_sla_breached`) in PostgreSQL for zero-cost duration lookups, and composite B-tree index `(user_id, status, created_at DESC)` with `INCLUDE` clause for 100% Index-Only Scans on a 10M-row table.
4. **Edge Middleware vs. Route Handlers (Q5):**  
   Divided authentication into coarse-grained Edge Middleware (fast gating, expiration check, header injection) and Route Handlers (cryptographic verification, RBAC, DB lookups). Webhooks bypass JWT checks and are validated via HMAC-SHA256 in route handlers.
5. **Idempotent Background Jobs (Q6):**  
   Enforced strict HTTP idempotency via unique `Idempotency-Key` headers, using atomic check-and-set locking to prevent duplicate order inserts or duplicate background jobs on network retries.
6. **Workload Identity Federation in CI/CD (Q7):**  
   Configured GitHub Actions using Google Cloud Workload Identity Federation (WIF) instead of static JSON service account keys, eliminating key leakage risks.

---

## Candidate Input Required

The following candidate-specific facts are required in [`PRESCREENING_ANSWERS.md`](file:///d:/DOKUMEN%20AHF/Programmer%20%28NextJS%20&%20Python%29/PRESCREENING_ANSWERS.md) prior to submission:
- **Part A, Header:** Candidate full name.
- **P1:** Specific example of handling an ambiguous task in a past role.
- **P2:** Specific team size and experience in a startup/small team (or motivation if joining for the first time).
- **P3:** Personal 2–3 year career aspirations.
- **P4:** Specific motivation for seeking this role at PT Injani Systems.
- **P5:** Expected gross monthly salary in IDR.

---

## Known Limitations

- **In-Memory Rate Limiting & Idempotency Store:** The included reference implementation uses an in-memory sliding-window store for single-instance Node.js and Python processes. In a distributed multi-instance deployment (e.g. Vercel Edge + multi-container Cloud Run), this should be backed by Upstash Redis or AWS ElastiCache.
- **Local Ollama Dependency:** To run full end-to-end local inference with `gemma3:8b`, an Ollama daemon with the model pulled (`ollama run gemma3:8b`) must be running at `http://localhost:11434`. In the absence of an active GPU, the built-in rule-based fallback handles test execution deterministically.

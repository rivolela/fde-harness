# FDE Harness: CI/CD Pipeline & Enterprise Test Plan

This document details the **Continuous Integration & Continuous Deployment (CI/CD)** pipeline and the **Multi-Layer Test Planning** tailored for Forward Deployed Engineering engagements (e.g. Deloitte client environments).

---

## 1. Multi-Layer Testing Strategy (The FDE Test Pyramid)

Unlike traditional web applications, an enterprise AI system deployed forward into client infrastructure requires five distinct layers of validation:

```
                      ▲
                     / \
                    /   \     Layer 5: Friday 5 PM Disaster & Incident Recovery Drills
                   /=====\
                  /       \    Layer 4: Shadow-Mode / Dual-Run Validation (Silent Canary)
                 /=========\
                /           \   Layer 3: AI Grounding, Faithfulness & Guardrail Evals
               /=============\
              /               \  Layer 2: Enterprise Data & Connector Integration Tests
             /=================\
            /                   \ Layer 1: Deterministic Unit & AST Defensive Tests
           +---------------------+
```

### Layer 1: Deterministic Unit & Defensive AST Testing
- **Scope**: Syntax validity, module logic, AST checks for unhandled network timeouts, bare `except` blocks, and credential/secret leakage.
- **Execution Target**: Pre-commit hook & Every CI pull request.
- **Pass Gate**: 100% pass, zero hardcoded secrets detected.
- **Implementation**: [`tests/test_harness.py`](file:///Users/calicojack/Development/valuefirst/FDE-Deloitte/tests/test_harness.py), `fde_harness.engineering.diagnostics.CodeDiagnostics`.

### Layer 2: Enterprise Data & Connector Integration Tests
- **Scope**: Legacy DB schema drift, dirty input sanitization, handling null sentinels (`N/A`, `NULL`, `-`), and read-only query enforcement.
- **Execution Target**: Automated staging builds.
- **Pass Gate**: Zero write operations permitted during inspection; all null sentinels normalized.
- **Implementation**: `fde_harness.engineering.connectors.EnterpriseConnector`.

### Layer 3: AI Grounding, Faithfulness & Guardrail Evals
- **Scope**: Evaluates model hallucination against retrieved enterprise policy chunks, verifies latency thresholds (<2500ms), and enforces compliance regex guardrails (SSN, credit cards, trade secrets).
- **Execution Target**: Nightly evaluation runs & release candidate branches.
- **Pass Gate**:
  - Grounding / Faithfulness score $\ge 85\%$.
  - PII / Compliance leakage = $0\%$.
  - End-to-end P95 Latency $< 2500\text{ ms}$.
- **Implementation**: `fde_harness.ai_systems.evals.EnterpriseEvaluator`.

### Layer 4: Shadow-Mode Dual-Run Testing (Client Staging)
- **Scope**: Incoming production client requests are replicated asynchronously into the FDE agent alongside existing human operators. Outputs are logged and compared for concordance without impacting client SLA.
- **Execution Target**: Pre-production pilot (Weeks 3-5 in milestone roadmap).
- **Pass Gate**: $\ge 90\%$ agreement with senior human operators over 500 consecutive real cases.

### Layer 5: Incident Recovery & Friday 5 PM Drills
- **Scope**: Validates automated fallback modes (e.g. dead-letter queues, rate-limiting backoff, degraded responses) and automated client incident reporting.
- **Execution Target**: Weekly scheduled chaos drill.
- **Pass Gate**: Mean time to mitigation $< 5\text{ minutes}$; calm client statement generated automatically.
- **Implementation**: `fde_harness.consulting.incident_room.IncidentCommander`.

---

## 2. CI/CD Pipeline Architecture

The CI/CD workflow is defined in [`.github/workflows/ci.yml`](file:///Users/calicojack/Development/valuefirst/FDE-Deloitte/.github/workflows/ci.yml) and runs on GitHub Actions:

```
[ Push / PR ]
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 1: Static Analysis & Security Scan                    │
│ • Ruff / Flake8 Linting                                     │
│ • CodeDiagnostics Secret & Timeout AST Scanner              │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 2: Unit & Integration Test Suite                      │
│ • python3 -m unittest discover tests                        │
│ • Code Coverage Report (Target > 90%)                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 3: AI Grounding & Guardrail Regression Gate           │
│ • Run benchmark eval against synthetic golden dataset       │
│ • Enforce Grounding >= 85% & Zero PII Leakage               │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 4: Self-Evolution Telemetry & Proposal Check          │
│ • Run HarnessEvolver to verify proposal schema integrity    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 5: Forward Deployment (Canary / In-VPC Staging)       │
│ • 10% Canary traffic allocation                             │
│ • Automated rollback on error spike > 1%                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Test Matrix & Thresholds

| Test Suite | Frequency | Timeout | Pass Criteria | Blocking? |
| :--- | :--- | :--- | :--- | :--- |
| **AST & Secret Scan** | Every Commit | 30s | 0 secrets, 0 syntax errors | **Yes** (Blocks Merge) |
| **Unit Test Suite** | Every PR | 2m | 100% pass | **Yes** (Blocks Merge) |
| **Enterprise RAG Evals** | Nightly / Release | 10m | Grounding $\ge 85\%$, Cost $\le \$0.05$/case | **Yes** (Blocks Release) |
| **PII & Compliance Gate** | Every PR | 1m | 0 PII violations | **Yes** (Hard Security Gate) |
| **Shadow Concordance** | Continuous | N/A | $\ge 90\%$ operator agreement | **No** (Advisory for Canary) |
| **Incident Drills** | Weekly | 5m | MTTR $< 5$ mins | **No** (Readiness Metric) |

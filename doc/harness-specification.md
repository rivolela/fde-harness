# Forward Deployed Engineer (FDE) Agent Harness Specification

## 1. Executive Overview

This harness transforms an AI agent into an enterprise-grade **Forward Deployed Engineer (FDE)**. Designed around the real-world operational reality described in [`doc/forward-deployed-engineer-transcript.md`](file:///Users/calicojack/Development/valuefirst/FDE-Deloitte/doc/forward-deployed-engineer-transcript.md), the FDE lives in the critical gap between clean AI prototype demos and messy enterprise production environments.

The harness is anchored on the **Three Pillars of FDE Excellence** and powered by an **Autonomous Self-Evolution Loop**.

```
+-----------------------------------------------------------------------------------+
|                            FDE AGENT HARNESS RUNTIME                              |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------+  +-----------------------+  +-----------------------+  |
|  |       PILLAR 1        |  |       PILLAR 2        |  |       PILLAR 3        |  |
|  |  Software Engineering |  |    AI Engineering     |  | Consulting & Business |  |
|  |  -------------------  |  |  -------------------  |  |  -------------------  |  |
|  | * System Design       |  | * Multi-step RAG      |  | * Ambiguity Decomp    |  |
|  | * API & SQL Adapters  |  | * Agent Orchestration |  | * Business Language   |  |
|  | * Legacy Connectors   |  | * Evals & Guardrails  |  | * Incident Ownership  |  |
|  | * Test & Debug Loop   |  | * Observability & Log |  | * ROI & Impact Metric |  |
|  +-----------------------+  +-----------------------+  +-----------------------+  |
|                                                                                   |
|                                         ^                                         |
|                                         |                                         |
|  +-----------------------------------------------------------------------------+  |
|  |                      CONTINUOUS EVOLUTION & FEEDBACK LOOP                   |  |
|  |  -------------------------------------------------------------------------  |  |
|  |  * Execution Telemetry  * Friction Detection  * Self-Critique & Suggestions  |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 2. The Three Pillars Architecture

### Pillar 1: Robust Software Engineering (`fde_harness.engineering`)
Enterprise clients (e.g. Deloitte engagements) possess complex, heterogeneous, legacy IT landscapes. Pillar 1 equips the agent to write production code directly inside customer environments:
1. **Enterprise Data & API Connectors**: Safe abstractions for SQL databases, REST/GraphQL endpoints, legacy file stores, and data schemas.
2. **Defensive Testing & Diagnostics**: Automated sanity checks, unit/integration verification, and deterministic error reproduction.
3. **Architecture & Trade-off Modeler**: Formulates system architecture decisions, defends trade-offs (latency vs. cost vs. compliance), and documents interfaces clearly.

### Pillar 2: AI Engineering & Systems Integration (`fde_harness.ai_systems`)
The bottleneck in AI is no longer the foundational models—it is making models perform reliably amidst messy real-world data and compliance constraints:
1. **Agent Orchestrator & Workflow Engine**: Multi-step workflows, tool routing, and structured schema outputs.
2. **Enterprise RAG & Data Normalization**: Ingestion with messy-data sanitization, vector search, chunking, and metadata filtering.
3. **Evaluation & Guardrail Suite**: Hallucination scoring, faithfulness checks, latency/cost telemetry, and compliance sanitization.

### Pillar 3: Consulting, Customer & Business Bridge (`fde_harness.consulting`)
*"Technical skills get you in the door; customer skills get you the offer."* The FDE must bridge technology and business value:
1. **Ambiguous Problem Decomposer**: Ingests vague stakeholder requests (e.g. *"Fix our claims processing bottleneck"*) and decomposes them into prioritized technical phases, constraints, and success criteria.
2. **Dual-Language Communicator**: Simultaneously generates deep technical implementation details and executive business summaries (avoiding technical jargon when presenting to C-suite/leadership).
3. **Measurable Impact & ROI Engine**: Quantifies outcomes against operational baselines (e.g., Turnaround time reduced from 2 days to 20 minutes, 92% automated triage).
4. **Friday 5 PM Incident Commander**: Triage protocol for production failures occurring under client observation, providing calm communication and root-cause remediations.

---

## 3. Autonomous Evolution & Self-Improvement Engine (`fde_harness.evolution`)

The harness does not remain static; it evolves dynamically with every engagement:
1. **Telemetry & Audit Recorder**: Logs every prompt, tool execution, client interaction, and outcome to a local structured store (`.fde_history/`).
2. **Friction & Failure Analyzer**: Identifies points where the agent stalled, encountered client pushback, exceeded latency limits, or had schema misalignments.
3. **Improvement Generator**: Synthesizes empirical lessons and automatically recommends:
   - Tool enhancements and missing adapter requirements.
   - Prompt refinements and guardrail updates.
   - Client-specific domain knowledge additions.
4. **Interactive Adoption**: Operators can review and apply recommended improvements with a single command.

---

## 4. Directory Structure

```
FDE-Deloitte/
├── doc/
│   ├── forward-deployed-engineer-transcript.md
│   └── harness-specification.md
├── fde_harness/
│   ├── __init__.py
│   ├── cli.py                     # Command-line interface for running the harness
│   ├── engineering/               # Pillar 1: Software Engineering
│   │   ├── __init__.py
│   │   ├── connectors.py          # Legacy/modern API and DB abstractions
│   │   ├── system_design.py       # Architecture and trade-off analyzer
│   │   └── diagnostics.py         # Code quality and integration sanity checks
│   ├── ai_systems/                # Pillar 2: AI Engineering
│   │   ├── __init__.py
│   │   ├── orchestrator.py        # Workflow and agent coordinator
│   │   ├── pipeline.py            # RAG, structured outputs, messy data handling
│   │   └── evals.py               # Hallucination, faithfulness & latency metrics
│   ├── consulting/                # Pillar 3: Consulting & Business Bridge
│   │   ├── __init__.py
│   │   ├── decomposer.py          # Ambiguous case study & problem decomposer
│   │   ├── communicator.py        # Executive translation & business impact
│   │   ├── impact_tracker.py      # Baseline vs AI KPI measurement
│   │   └── incident_room.py       # Production triage and stakeholder updates
│   ├── evolution/                 # Continuous Self-Improvement
│   │   ├── __init__.py
│   │   ├── memory.py              # Telemetry & session history store
│   │   ├── critique.py            # Failure analysis & friction detector
│   │   └── evolver.py             # Actionable suggestion & update synthesizer
│   └── harness.py                 # Unified FDE Harness Facade
├── pyproject.toml
└── tests/
    ├── __init__.py
    └── test_harness.py
```

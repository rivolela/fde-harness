# FDE-Harness: Forward Deployed Engineer Agent Harness

Enterprise runtime harness forged around the role of a **Forward Deployed Engineer (FDE)**. Designed from real-world enterprise deployment realities (inspired by Palantir, OpenAI, Anthropic, and top-tier enterprise consulting engagements), this harness bridges the critical gap between clean prototype demos and messy production environments.

---

## 🗺 Documentation Map: Who Reads What?

This repository separates concerns across distinct documentation layers:

| Document | Audience | Purpose |
| :--- | :--- | :--- |
| **[`README.md`](README.md)** (Current) | **Humans & Developers** | Project overview, architecture, quickstart, and operating guide. |
| **[`AGENTS.md`](AGENTS.md)** | **AI Coding Agents** | Operational rules, policy invariants, AST diagnostics, and pitfalls loaded automatically by autonomous agents. |
| **[`HARNESS.md`](HARNESS.md)** | **Engineers & Architects** | Deep-dive specification of the 7-phase software development lifecycle and BMAD integration. |
| **[`doc/`](doc/)** | **Enterprise Context** | Original FDE interview transcripts and architectural design notes. |

---

## 🏛 The Three Pillars of FDE

```
+-----------------------------------------------------------------------------------+
|                            FDE AGENT HARNESS RUNTIME                              |
+-----------------------------------------------------------------------------------+
|  +-----------------------+  +-----------------------+  +-----------------------+  |
|  |       PILLAR 1        |  |       PILLAR 2        |  |       PILLAR 3        |  |
|  |  Software Engineering |  |    AI Engineering     |  | Consulting & Business |  |
|  |  -------------------  |  |  -------------------  |  |  -------------------  |  |
|  | * System Design       |  | * Multi-step RAG      |  | * Ambiguity Decomp    |  |
|  | * API & SQL Connectors|  | * Agent Orchestration |  | * Business Language   |  |
|  | * Legacy Cleaners     |  | * Evals & Guardrails  |  | * Incident Ownership  |  |
|  | * Defensive Testing   |  | * Cost/Latency Evals  |  | * ROI & Impact Metric |  |
|  +-----------------------+  +-----------------------+  +-----------------------+  |
|                                         ^                                         |
|  +-----------------------------------------------------------------------------+  |
|  |                      CONTINUOUS EVOLUTION & FEEDBACK LOOP                   |  |
|  |  * Telemetry Logging  * Friction Detection  * Self-Critique & Suggestions   |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### Pillar 1: Robust Software Engineering (`fde_harness.engineering`)
- **Connectors & Schema Validation**: Safe, read-only enterprise database abstractions and API contract testers.
- **Legacy Data Sanitization**: Robust cleaners dealing with dirty data, missing keys, and enterprise null sentinels (`N/A`, `NULL`, `-`).
- **Defensive Diagnostics**: AST syntax checks, hardcoded credentials/secret scanner, and network timeout validators.
- **Architecture Trade-offs**: Formal trade-off analyzer (cost vs. latency vs. compliance).

### Pillar 2: AI Engineering & Production Systems (`fde_harness.ai_systems`)
- **Enterprise RAG Pipeline**: Ingestion, header/footer cleaning, chunking, and deterministic relevance ranking.
- **Enterprise Evaluator & Guardrails**: Groundedness scoring, PII/compliance checks, and **Human-in-the-Loop (HITL) enforcement** (AI acts strictly as a co-author, rejecting unsupervised autopilot actions and auditing human sign-offs).
- **Workflow Orchestration**: Multi-step pipeline coordinator with audit telemetry in `.fde_evolution/traces.jsonl`.

### Pillar 3: Consulting, Customer & Business Bridge (`fde_harness.consulting`)
- **Ambiguous Problem Decomposer**: Resolves vague stakeholder problem statements into structured, 3-phase delivery plans.
- **Dual-Track Communicator**: Translates deep technical architecture into C-suite executive briefings without jargon.
- **Verified Impact Tracker**: Quantifies baseline vs. actual impact (e.g. cycle time reduction from 48 hours to 30 minutes) and computes ROI.
- **Friday 5 PM Incident Commander**: Simulates high-stakes production incident triage under client observation.

### 🔄 Continuous Evolution Loop (`fde_harness.evolution`)
- **Telemetry Memory**: Logs executions, latencies, feedback, and friction to `.fde_evolution/traces.jsonl`.
- **Friction Critique**: Detects recurring failure patterns, latency bottlenecks, and client pushback.
- **Self-Evolution Generator**: Formulates concrete, prioritized improvement proposals (`PROMPT_REFINEMENT`, `TOOL_EXPANSION`, `WORKFLOW_GUARD`).

---

## ⚡ Quickstart

> [!NOTE]
> **Cross-Project Portability**: BMAD framework skills (`.agent/skills/`) and core configurations (`_bmad/`) are tracked in Git. When you clone or template this repository into a new client project, your AI coding assistant (Antigravity, Cursor, Claude Code) immediately inherits all 20+ specialized BMAD skills alongside the FDE governance rules in `AGENTS.md`.

### 1. Requirements & Setup
Python 3.10+ is required.

```bash
# Clone the repository
git clone https://github.com/valuefirst/fde-harness.git
cd fde-harness

# Install dependencies in editable mode
pip install -e .

# Initialize the repository telemetry & workspace
fde-harness init --client "Enterprise-Client"
```

### 1b. Installing into an Existing Client Repository (Automated)

When working inside an existing client codebase, you can bootstrap the harness with a single command:

**Option A — Via `pip` and CLI:**
```bash
pip install git+https://github.com/valuefirst/fde-harness.git
fde-harness init --client "Acme-Insurance"
```

**Option B — Via 1-Line Curl Installer:**
```bash
curl -fsSL https://raw.githubusercontent.com/valuefirst/fde-harness/main/install.sh | bash -s -- --client "Acme-Insurance"
```

*This automatically copies all 29 BMAD agent skills (`.agent/skills`), syncs `_bmad/`, configures `AGENTS.md` & `HARNESS.md`, updates `.gitignore`, and sets up telemetry.*


### 2. Launching with an AI Agent (Fastest Path)
Open this repository in your AI coding assistant (Antigravity, Cursor, Claude Code, or BMAD). Because [`AGENTS.md`](AGENTS.md) is pre-configured, the agent automatically adopts the FDE role and repository guardrails.

Choose either intake mode:

#### 🟢 Path A: Start from a Raw Client Problem
Provide any ambiguous client request directly into your agent chat:
> *"Start the FDE Workflow for this problem: 'Our loan underwriting analysts take 48 hours to process qualification PDFs. Leadership wants AI automation to cut cycle time to under 1 hour without risking compliance fines.' Execute the 7-phase software development cycle: decompose root causes, evaluate architecture trade-offs, generate delivery milestones, build the pipeline, verify guardrails, calculate ROI impact, and trigger self-evolution."*

#### 📄 Path B: Start from a Document or Spec (`doc/`)
Point your agent to an existing transcript, policy, or client specification:
> *"Start the FDE Workflow using the client context in `doc/forward-deployed-engineer-transcript.md`. Ingest the document, extract requirements and constraints, decompose the root problems, and run the 7-phase FDE software development cycle."*

---

### 3. Verify Environment & Simulations (Terminal)
To run automated verification or headless simulation in your terminal:

```bash
# Run unit test suite
python3 -m unittest discover tests

# Run full end-to-end 7-phase simulation script
python3 fde_execution_cycle.py
```

---

## 🔄 The 7-Phase FDE Software Cycle

The harness integrates the **BMAD Method (BMM)** with the **Three Pillars of FDE**:

```
[Phase 1] Ambiguous Intake & Spec   ──► BMAD: bmad-spec         | FDE: AmbiguousProblemDecomposer
[Phase 2] Architecture Spine        ──► BMAD: bmad-architecture | FDE: SystemTradeOffAnalyzer
[Phase 3] Planning & Roadmap        ──► BMAD: bmad-sprint-plan  | FDE: PhasedMilestone Tracker
[Phase 4] Implementation & Build    ──► BMAD: bmad-build        | FDE: WorkflowOrchestrator & RAG
[Phase 5] Verification & Guardrails ──► BMAD: bmad-code-review  | FDE: CodeDiagnostics & Evaluator
[Phase 6] Client Walkthrough & ROI  ──► BMAD: bmad-walkthrough  | FDE: DualTrackCommunicator & Impact
[Phase 7] Evolution & Retrospective ──► BMAD: bmad-retro        | FDE: UsageCritiqueAnalyzer & Evolver
```

*See [`HARNESS.md`](HARNESS.md) for detailed phase breakdowns and implementation code.*

---

## 🤖 Operating Mode 1: AI Agent Driven (Recommended)

You can drive the entire FDE workflow conversationally through any AI agent (Antigravity, Cursor, BMAD agent, Claude Code) using natural language. The agent automatically ingests [`AGENTS.md`](AGENTS.md) to follow repository guardrails.

### One-Prompt Full Cycle Run
> **"Start the FDE Workflow for our loan underwriting team: analysts currently take 48 hours to review qualification PDFs and leadership needs an automated pipeline without compliance risks. Execute all 7 phases end-to-end."**

### Phase-by-Phase Interactive Prompts
| Phase | What It Does | Prompt to Give Your Agent |
|---|---|---|
| **Phase 1: Spec & Intake** | Unpacks vague client requirements | *"Decompose this ambiguous client problem: [paste request]. Clarify root cause, constraints, and target metrics."* |
| **Phase 2: Architecture** | Evaluates system trade-offs | *"Evaluate architecture trade-offs for [solution] across latency, cost, and In-VPC compliance."* |
| **Phase 3: Milestones** | Generates a 3-phase delivery roadmap | *"Create the phased delivery milestones and success criteria for this initiative."* |
| **Phase 4: Build & Ingest** | Sanitizes legacy data & configures RAG | *"Build the ingestion pipeline: register sanitized legacy tables and configure RAG retrieval for [data]."* |
| **Phase 5: Guardrails** | Scans code safety & runs evals | *"Run defensive diagnostics on the implementation and evaluate grounding score and PII guardrails."* |
| **Phase 6: Executive Brief** | Translates technical impact to ROI | *"Generate the executive briefing and calculate annual cost savings and turnaround time reduction."* |
| **Phase 7: Self-Evolution** | Analyzes traces for improvements | *"Run the self-evolution engine and generate harness improvement proposals from recent telemetry."* |

### Specialized Drills
- **Friday 5 PM Incident Drill**:
  > *"Run a Friday 5 PM production incident drill. Simulate a high-stakes failure under client observation, propose immediate mitigation, and provide a calm executive communication update."*
- **Continuous Harness Evolution**:
  > *"Analyze system friction in `.fde_evolution/traces.jsonl` and produce prioritized evolution proposals."*

---

## 💻 Operating Mode 2: Headless CLI & Python API

For terminal execution, automated scripts, or CI/CD pipelines:

### CLI Commands:
```bash
# End-to-end simulation
python3 -m fde_harness.cli run-scenario

# Ambiguity decomposition
python3 -m fde_harness.cli decompose "Loan application review queue is delayed by 3 days."

# High-stakes incident drill
python3 -m fde_harness.cli incident-drill

# Self-evolution engine
python3 -m fde_harness.cli evolve
```

### Python Programmatic Usage:
```python
from fde_harness import FDEHarness

harness = FDEHarness(client_name="Acme-Financial-Client")

# Phase 1: Ambiguity Intake
plan = harness.handle_ambiguous_case("Vague client request...")

# Run Full Scenario
results = harness.run_end_to_end_scenario(
    problem_statement="Underwriting takes 48 hours...",
    raw_data=[{"Applicant": "Jane Doe", "Income": "N/A"}]
)

# Trigger Evolution
proposals = harness.trigger_self_evolution()
```

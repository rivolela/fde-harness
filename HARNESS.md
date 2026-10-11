# FDE Agent Harness: Standard Software Development Cycle

This document defines the **standard end-to-end software development cycle** for the Forward Deployed Engineer (FDE) Agent Harness, integrating the **BMAD Method (BMM)** with the **Three Pillars of FDE** and the **Autonomous Self-Evolution Loop**.

---

## 1. Cycle Architecture Overview

The FDE software cycle maps each phase of enterprise client delivery from initial vague stakeholder requests to verified production code and continuous self-improvement:

```
+─────────────────────────────────────────────────────────────────────────────────────────────+
|                                  FDE SOFTWARE LIFECYCLE                                      |
+─────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                             |
|  [PHASE 1] Ambiguous Intake & Spec          ──►  BMAD: bmad-spec / bmad-prd                 |
|            • Clarify assumptions & scope          • FDE: AmbiguousProblemDecomposer         |
|                                                                                             |
|  [PHASE 2] Architecture Spine               ──►  BMAD: bmad-architecture                    |
|            • Invariants, trade-offs, schemas      • FDE: SystemTradeOffAnalyzer & Connectors|
|                                                                                             |
|  [PHASE 3] Planning & Roadmap               ──►  BMAD: bmad-sprint-planning                 |
|            • Phased milestones, gate readiness    • FDE: PhasedMilestone Tracker            |
|                                                                                             |
|  [PHASE 4] Implementation & Build           ──►  BMAD: bmad-build                           |
|            • Legacy data cleaning & RAG agent     • FDE: WorkflowOrchestrator & RAG         |
|                                                                                             |
|  [PHASE 5] Verification & Guardrails        ──►  BMAD: bmad-code-review & qa                |
|            • Faithfulness, PII, latency, tests    • FDE: CodeDiagnostics & Evaluator        |
|                                                                                             |
|  [PHASE 6] Client Walkthrough & ROI         ──►  BMAD: bmad-walkthrough                     |
|            • Executive briefing & ROI metrics     • FDE: DualTrackCommunicator & Impact     |
|                                                                                             |
|  [PHASE 7] Evolution & Lessons Learned      ──►  BMAD: bmad-retrospective                   |
|            • Telemetry critique & proposals       • FDE: UsageCritiqueAnalyzer & Evolver    |
|                                                                                             |
+─────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 2. Complete Python Execution Pipeline

Below is the standard, reusable Python script implementing the entire 7-phase cycle:

```python
"""fde_execution_cycle.py

Standard end-to-end software cycle execution inside the FDE Harness.
"""

from fde_harness import FDEHarness
from fde_harness.engineering import SystemTradeOffAnalyzer, TradeOffOption
from fde_harness.ai_systems import WorkflowPlan, WorkflowStep

def run_fde_software_cycle():
    # Initialize the Harness with client context
    harness = FDEHarness(client_name="Enterprise-Client")
    print("=" * 70)
    print("🚀 STARTING FDE SOFTWARE DEVELOPMENT CYCLE")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # PHASE 1: AMBIGUOUS PROBLEM INTAKE & DECOMPOSITION (bmad-spec / Pillar 3)
    # -------------------------------------------------------------------------
    client_problem = (
        "Our underwriting analysts take 48 hours to process loan qualification PDFs. "
        "Leadership wants AI automation to cut cycle time without risking compliance fines."
    )
    print("\n[PHASE 1] Decomposing Ambiguous Problem...")
    plan = harness.handle_ambiguous_case(client_problem)
    print(f"  ✓ Root Cause: {plan.clarified_problem}")
    print(f"  ✓ Target Metrics: {plan.target_business_metrics[0]}")

    # -------------------------------------------------------------------------
    # PHASE 2: ARCHITECTURE SPINE & TRADE-OFFS (bmad-architecture / Pillar 1)
    # -------------------------------------------------------------------------
    print("\n[PHASE 2] Fixing Invariants & Evaluating Architecture Trade-offs...")
    options = [
        TradeOffOption(
            name="Public Cloud Multi-tenant LLM",
            pros=["Lowest operational overhead", "Fastest prototyping"],
            cons=["Strict client data privacy barrier", "Third-party dependency"],
            cost_level="Low",
            latency_level="Medium",
            compliance_fit="Strict-Requires-VPC"
        ),
        TradeOffOption(
            name="In-VPC Containerized Model + Local Vector Store",
            pros=["Zero external data transit", "Deterministic audit logs", "Predictable latency"],
            cons=["Requires private infrastructure provisioning"],
            cost_level="Medium",
            latency_level="Low",
            compliance_fit="Excellent"
        )
    ]
    tradeoff = SystemTradeOffAnalyzer.evaluate(
        decision_topic="LLM Inference Topology & Vector Store",
        options=options,
        recommended_option="In-VPC Containerized Model + Local Vector Store",
        rationale="Client compliance strictly mandates data residency inside private VPC boundaries."
    )
    print(f"  ✓ Architecture Decision: {tradeoff['recommended_option']}")
    print(f"  ✓ Trade-off Rationale: {tradeoff['rationale']}")

    # -------------------------------------------------------------------------
    # PHASE 3: PLANNING & PHASED ROADMAP (bmad-sprint-planning / Pillar 3)
    # -------------------------------------------------------------------------
    print("\n[PHASE 3] Generating Phased Delivery Milestones...")
    for m in plan.milestones:
        print(f"  • [Phase {m.phase}] {m.name} ({m.timeline}) -> {m.success_criteria}")

    # -------------------------------------------------------------------------
    # PHASE 4: IMPLEMENTATION & ORCHESTRATION (bmad-build / Pillar 1 & 2)
    # -------------------------------------------------------------------------
    print("\n[PHASE 4] Executing Workflow & Data Pipeline...")
    # 4a. Legacy dirty data ingestion
    legacy_records = [
        {"Applicant": "John Doe", "Tax_ID": "N/A", "Credit_Score": 720, "Income": "$120,000"},
        {"Applicant": "Jane Smith", "Tax_ID": "987-65-4321", "Credit_Score": 680, "Income": " - "}
    ]
    harness.connector.register_table("applicant_records", legacy_records)
    print(f"  ✓ Registered sanitized legacy table: {list(harness.connector.inspect_schema().keys())}")

    # 4b. RAG Pipeline Ingestion
    policy_doc = (
        "ENTERPRISE FINANCIAL SERVICES UNDERWRITING GUIDELINES:\n"
        "Applicants with credit scores above 700 and income verification are eligible for fast-track 30-minute approval.\n"
        "Tax identification numbers must be masked in staging logs."
    )
    harness.rag.ingest_document("underwriting_policy_v1", policy_doc)
    retrieved = harness.rag.retrieve("credit score above 700 fast-track approval", top_k=1)
    context_text = retrieved[0].content if retrieved else ""
    generated_response = "Applicant John Doe (Score 720) qualifies for fast-track approval under Guidelines."
    print(f"  ✓ RAG Ingestion & Retrieval complete ({len(retrieved)} chunk matched).")

    # -------------------------------------------------------------------------
    # PHASE 5: DEFENSIVE VERIFICATION & GUARDRAILS (bmad-qa / Pillar 1 & 2)
    # -------------------------------------------------------------------------
    print("\n[PHASE 5] Defensive Diagnostics & Compliance Guardrails...")
    # 5a. Code diagnostics
    pipeline_code = """
import httpx
def query_model(payload: dict) -> dict:
    resp = httpx.post("https://internal.vpc/v1/predict", json=payload, timeout=5.0)
    return resp.json()
"""
    diag = harness.diagnostics.analyze_python_code(pipeline_code)
    print(f"  ✓ Code Safety Score: {diag.score}/100 (Valid: {diag.is_valid})")

    # 5b. Enterprise Evaluator
    eval_result = harness.evaluator.run_eval(
        context=context_text,
        response=generated_response,
        latency_ms=145.0,
        input_token_count=350,
        output_token_count=65
    )
    print(f"  ✓ Grounding Score: {eval_result.grounding_score * 100:.0f}%")
    print(f"  ✓ Guardrail Compliance: {'PASS' if eval_result.passed_guardrails else 'FAIL'}")

    # 5c. Human-in-the-Loop Review & Telemetry Audit (AI as Co-Author, Not Autopilot)
    signoff = harness.evaluator.record_human_signoff(
        decision_id="DEC-UNDERWRITING-QUAL-720",
        reviewer_id="FDE-Lead-Engineer",
        status="APPROVED",
        notes="Verified In-VPC RAG citations against Underwriting Guidelines v1. Co-authored recommendation accepted."
    )
    print(f"  ✓ Human-in-the-Loop Sign-off: {signoff['status']} by {signoff['reviewer_id']}")
    print(f"  ✓ Decision Audited in: .fde_evolution/traces.jsonl")

    # -------------------------------------------------------------------------
    # PHASE 6: CLIENT WALKTHROUGH & BUSINESS IMPACT (bmad-walkthrough / Pillar 3)
    # -------------------------------------------------------------------------
    print("\n[PHASE 6] Calculating Business Impact & Executive Briefing...")
    impact = harness.impact_tracker.calculate_impact(
        initiative_name="Automated Underwriting Triage",
        baseline_turnaround_hours=48.0,
        current_turnaround_hours=0.5,  # 30 minutes
        cases_processed_monthly=2000
    )
    briefing = harness.communicator.generate_briefing(
        feature_name="Fast-Track Underwriting Engine",
        technical_details="In-VPC deterministic RAG with schema sanitization",
        turnaround_before="48 hours",
        turnaround_after="30 minutes",
        cost_savings=f"${impact.annual_cost_savings_usd:,.0f}/year"
    )
    print(f"  ✓ Turnaround Reduction: {impact.turnaround_reduction_pct}% (48h -> 30m)")
    print(f"  ✓ Annual Projected Savings: ${impact.annual_cost_savings_usd:,.2f}")
    print(f"  ✓ Resume Impact Bullet:\n    \"{impact.impact_resume_statement}\"")

    # -------------------------------------------------------------------------
    # PHASE 7: RETROSPECTIVE & SELF-EVOLUTION (bmad-retrospective / Evolution)
    # -------------------------------------------------------------------------
    print("\n[PHASE 7] Running Self-Evolution Engine...")
    proposals = harness.trigger_self_evolution()
    print(f"  ✓ Generated {len(proposals)} evolution proposal(s):")
    for p in proposals[:2]:
        print(f"    • [{p.category}] {p.title} ({p.target_pillar})")

    print("\n" + "=" * 70)
    print("✅ FDE SOFTWARE CYCLE COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_fde_software_cycle()
```

---

## 3. How to Run

### Via AI Agent (Recommended — No Python Commands Needed):
Prompt your AI agent (Antigravity, Cursor, BMAD agent, or Claude Code) in natural language:
```text
"Start the FDE Workflow for [client problem]. Execute the 7-phase FDE software development cycle end-to-end: decompose the problem, evaluate architecture trade-offs, plan delivery milestones, build the RAG and data sanitation pipeline, run defensive guardrails, calculate ROI impact, and trigger self-evolution proposals."
```
Or interactively by phase (e.g. *"Decompose this ambiguous client problem..."*, *"Evaluate architecture trade-offs for..."*, *"Run Friday 5 PM incident drill"*).

### Via CLI:
```bash
# Execute end-to-end simulation
python3 -m fde_harness.cli run-scenario

# Run ambiguity decomposition
python3 -m fde_harness.cli decompose "Loan application review queue is delayed by 3 days."

# Simulate Friday 5 PM production incident
python3 -m fde_harness.cli incident-drill

# Generate self-evolution improvements
python3 -m fde_harness.cli evolve
```

### Programmatically in Python:
```python
from fde_harness import FDEHarness

harness = FDEHarness(client_name="Enterprise-Client")
plan = harness.handle_ambiguous_case("Vague client request...")
results = harness.run_end_to_end_scenario(...)
proposals = harness.trigger_self_evolution()
```

---

## 4. CI/CD Pipeline & Multi-Layer Test Planning

Full detailed specifications:
- **Test Plan & Strategy**: [`doc/cicd-and-testing-plan.md`](doc/cicd-and-testing-plan.md)
- **GitHub Actions Configuration**: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

### The 5-Layer FDE Test Pyramid
1. **Layer 1: Deterministic Unit & AST Defensive Tests** (`tests/test_harness.py`): Syntax checks, credential/secret scanner, and network timeout validation.
2. **Layer 2: Enterprise Data & Connector Integration Tests** (`connectors.py`): Legacy DB schema drift, null sentinel normalization (`N/A`, `NULL`, `-`), and read-only enforcement.
3. **Layer 3: AI Grounding, Faithfulness & Guardrail Evals** (`evals.py`): Grounding $\ge 85\%$, 0 PII leaks, and latency $< 2500$ ms.
4. **Layer 4: Shadow-Mode Dual-Run Testing**: Real client requests replicated asynchronously in shadow mode alongside human operators ($\ge 90\%$ concordance).
5. **Layer 5: Friday 5 PM Incident Recovery Drills** (`incident_room.py`): Outage simulation under client observation; validates automated mitigations and calm client communication.

### Automated CI/CD Gates
- **Pre-Merge PR Gate**: Executes Layer 1 (AST security & secret scan) + Layer 2 (Unit tests) + Layer 3 (AI eval guardrails).
- **Staging / Canary Gate**: 10% canary traffic allocation with automated rollback if latency or error thresholds spike.
- **Continuous Evolution Check**: Verifies `HarnessEvolver` proposals before sprint releases.

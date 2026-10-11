"""Unified FDE Harness Facade integrating all 3 pillars and continuous evolution."""

import time
import uuid
from typing import Any, Dict, List, Optional

from .engineering import (
    CodeDiagnostics,
    EnterpriseConnector,
    SystemTradeOffAnalyzer,
)
from .ai_systems import (
    DocumentChunk,
    EnterpriseEvaluator,
    EnterpriseRAGPipeline,
    EvaluationResult,
    WorkflowOrchestrator,
    WorkflowPlan,
    WorkflowStep,
)
from .consulting import (
    AmbiguousProblemDecomposer,
    BusinessImpactMetrics,
    DecomposedPlan,
    DualTrackCommunicator,
    ExecutiveBriefing,
    ImpactTracker,
    IncidentCommander,
    IncidentReport,
)
from .evolution import (
    EvolutionMemory,
    HarnessEvolver,
    ImprovementProposal,
    InteractionEvent,
)


class FDEHarness:
    """The central Forward Deployed Engineer Agent Harness.

    Coordinates Software Engineering, AI Systems, Consulting Bridge, and Continuous Evolution.
    """

    def __init__(self, client_name: str = "Enterprise-Client", storage_dir: str = ".fde_evolution"):
        self.client_name = client_name
        self.storage_dir = storage_dir

        # Pillar 1 components
        self.connector = EnterpriseConnector(client_name=client_name)
        self.diagnostics = CodeDiagnostics()
        self.tradeoffs = SystemTradeOffAnalyzer()

        # Pillar 2 components
        self.rag = EnterpriseRAGPipeline()
        self.evaluator = EnterpriseEvaluator()
        self.orchestrator = WorkflowOrchestrator()

        # Pillar 3 components
        self.decomposer = AmbiguousProblemDecomposer()
        self.communicator = DualTrackCommunicator()
        self.impact_tracker = ImpactTracker()
        self.incident_commander = IncidentCommander()

        # Evolution components
        self.memory = EvolutionMemory(storage_dir=storage_dir)
        self.evolver = HarnessEvolver(storage_dir=storage_dir)

    def handle_ambiguous_case(self, vague_problem: str) -> DecomposedPlan:
        """Decomposes an ambiguous client problem (Pillar 3) and records telemetry."""
        start = time.perf_counter()
        plan = self.decomposer.decompose(vague_problem, client_context=self.client_name)
        latency = (time.perf_counter() - start) * 1000

        self.memory.log_event(
            InteractionEvent(
                event_id=f"evt_{uuid.uuid4().hex[:8]}",
                event_type="ambiguous_case_decomposition",
                input_prompt=vague_problem,
                output_summary=f"Decomposed into {len(plan.milestones)} phases with {len(plan.target_business_metrics)} metrics",
                success=True,
                latency_ms=round(latency, 2),
            )
        )
        return plan

    def run_end_to_end_scenario(
        self,
        problem_statement: str,
        sample_enterprise_doc: str,
        query: str,
        baseline_hours: float = 48.0,
        target_hours: float = 0.5,
        monthly_volume: int = 1200,
    ) -> Dict[str, Any]:
        """Runs an end-to-end simulation executing all three pillars and logging telemetry."""
        # 1. Pillar 3: Decompose
        plan = self.handle_ambiguous_case(problem_statement)

        # 2. Pillar 2: RAG Ingestion & Query
        chunks = self.rag.ingest_document("client_doc_01", sample_enterprise_doc)
        retrieved = self.rag.retrieve(query, top_k=2)
        context_text = " ".join([c.content for c in retrieved])
        response_text = f"Automated recommendation for {query}: matched client rules in {len(retrieved)} retrieved sections."

        # Evaluation
        eval_result = self.evaluator.run_eval(
            context=context_text,
            response=response_text,
            latency_ms=180.0,
            input_token_count=450,
            output_token_count=90,
        )

        # 3. Pillar 3: Impact & Executive Briefing
        impact = self.impact_tracker.calculate_impact(
            initiative_name="Automated Intake & Triage",
            baseline_turnaround_hours=baseline_hours,
            current_turnaround_hours=target_hours,
            cases_processed_monthly=monthly_volume,
        )

        briefing = self.communicator.generate_briefing(
            feature_name="Forward-Deployed Triage Engine",
            technical_details="Hybrid vector retrieval with deterministic schema validation",
            turnaround_before=f"{baseline_hours:.0f} hours",
            turnaround_after=f"{int(target_hours*60)} minutes",
            cost_savings=f"${impact.annual_cost_savings_usd:,.0f}/year",
        )

        return {
            "client": self.client_name,
            "decomposed_plan": plan.model_dump(),
            "retrieved_chunks": [c.model_dump() for c in retrieved],
            "evaluation": eval_result.model_dump(),
            "business_impact": impact.model_dump(),
            "executive_briefing": briefing.model_dump(),
        }

    def simulate_friday_incident(self, symptom: str, root_cause: str, fix: str) -> IncidentReport:
        """Simulates and handles a high-stakes Friday 5 PM incident (Pillar 3)."""
        report = self.incident_commander.handle_incident(
            incident_id=f"INC-{uuid.uuid4().hex[:6].upper()}",
            severity="SEV-1",
            symptom=symptom,
            technical_cause=root_cause,
            fix_applied=fix,
        )

        self.memory.log_event(
            InteractionEvent(
                event_id=f"evt_{uuid.uuid4().hex[:8]}",
                event_type="incident_drill",
                input_prompt=symptom,
                output_summary=f"Resolved SEV-1: {fix}",
                success=True,
                latency_ms=120.0,
                friction_detected=True,
                friction_notes=f"Root cause: {root_cause}",
            )
        )
        return report

    def trigger_self_evolution(self) -> List[ImprovementProposal]:
        """Analyzes historical usage telemetry and returns concrete improvement proposals."""
        return self.evolver.generate_proposals()

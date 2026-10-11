"""Ambiguous problem decomposition for Pillar 3 (Signature FDE Case Study capability)."""

from typing import List
from pydantic import BaseModel, Field


class PhasedMilestone(BaseModel):
    phase: int
    name: str
    timeline: str
    deliverables: List[str]
    success_criteria: str


class DecomposedPlan(BaseModel):
    client_statement: str
    clarified_problem: str
    core_bottlenecks: List[str]
    assumptions_to_validate: List[str]
    milestones: List[PhasedMilestone] = Field(default_factory=list)
    compliance_and_risks: List[str] = Field(default_factory=list)
    target_business_metrics: List[str] = Field(default_factory=list)


class AmbiguousProblemDecomposer:
    """Decomposes vague, high-level client business requests into structured,

    defensible technical delivery plans.
    """

    @classmethod
    def decompose(cls, vague_problem: str, client_context: str = "Enterprise / Regulated") -> DecomposedPlan:
        # Structured decomposition rules tailored for FDE enterprise engagements
        clarified = f"Root cause analysis of: '{vague_problem}' within context: {client_context}"

        bottlenecks = [
            "Manual review queues creating linear scaling dependencies.",
            "Fragmented legacy data silos with unstructured document formats.",
            "Strict compliance boundaries preventing public cloud data transit without VPC peering.",
        ]

        assumptions = [
            "Historical labeled data or audit logs exist and are accessible for evaluation.",
            "Client stakeholders can dedicate 2 hours/week for feedback and acceptance criteria alignment.",
            "Deployment target allows hybrid or private containerized workloads.",
        ]

        milestones = [
            PhasedMilestone(
                phase=1,
                name="Phase 1: Discovery & Prototype Smoke Test",
                timeline="Weeks 1-2",
                deliverables=[
                    "Data ingestion sample & schema mapping",
                    "Offline benchmark evaluation suite against 100 historical records",
                    "Stakeholder alignment on baseline KPIs",
                ],
                success_criteria="Demonstrate >85% accuracy on sample dataset with zero data leakage.",
            ),
            PhasedMilestone(
                phase=2,
                name="Phase 2: Forward Deployed Integration",
                timeline="Weeks 3-5",
                deliverables=[
                    "Integration with customer legacy staging database/API",
                    "Dual-run validation alongside human operators",
                    "Automated guardrails and audit logging",
                ],
                success_criteria="Process 500 real cases daily in shadow mode with 0 downtime.",
            ),
            PhasedMilestone(
                phase=3,
                name="Phase 3: Production Rollout & Operator Handover",
                timeline="Weeks 6-8",
                deliverables=[
                    "Gradual canary deployment (10% -> 50% -> 100%)",
                    "Operator runbook and executive telemetry dashboard",
                    "Measurement of turn-around time reduction and ROI",
                ],
                success_criteria="Cut operational turnaround time by >80% while passing compliance audit.",
            ),
        ]

        risks = [
            "Data drift when real-world distribution differs from initial sample.",
            "User adoption friction: operators hesitating to trust automated triage recommendations.",
            "Enterprise security review delays for model endpoints.",
        ]

        target_metrics = [
            "Turnaround time reduced from 48 hours to under 30 minutes.",
            "Automated triage rate of >70% with high confidence threshold.",
            "100% auditable traceability for every automated decision.",
        ]

        return DecomposedPlan(
            client_statement=vague_problem,
            clarified_problem=clarified,
            core_bottlenecks=bottlenecks,
            assumptions_to_validate=assumptions,
            milestones=milestones,
            compliance_and_risks=risks,
            target_business_metrics=target_metrics,
        )

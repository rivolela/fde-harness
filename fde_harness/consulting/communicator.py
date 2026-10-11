"""Dual-track communication for Pillar 3: translating engineering into business impact."""

from typing import List
from pydantic import BaseModel, Field


class TechnicalSpec(BaseModel):
    architecture_overview: str
    components_involved: List[str]
    api_contracts: List[str]
    latency_and_throughput: str
    failure_recovery_mode: str


class ExecutiveBriefing(BaseModel):
    executive_summary: str
    business_problem_solved: str
    key_metrics_and_roi: str
    risk_mitigation: str
    next_action_for_leadership: str


class DualTrackCommunicator:
    """Bridges the communication gap between technical engineers and executive stakeholders."""

    @classmethod
    def generate_briefing(
        cls,
        feature_name: str,
        technical_details: str,
        turnaround_before: str,
        turnaround_after: str,
        cost_savings: str,
    ) -> ExecutiveBriefing:
        exec_summary = (
            f"We have deployed {feature_name} directly within your infrastructure. "
            f"This solution directly resolves manual processing backlogs by introducing automated, "
            f"verifiable decision-support."
        )

        business_problem = (
            f"Operators previously spent significant manual effort reconciling fragmented data. "
            f"The system now automates initial intake and triage while preserving human oversight."
        )

        metrics = (
            f"• Processing turnaround time reduced from {turnaround_before} to {turnaround_after}.\n"
            f"• Projected annual labor and efficiency savings: {cost_savings}.\n"
            f"• 100% compliance audit trail maintained."
        )

        risk_mitigation = (
            "No data leaves your secure enterprise boundary. All outputs adhere to deterministic guardrails "
            "with human-in-the-loop fallback for low-confidence edge cases."
        )

        next_action = "Approve transition from pilot staging to full production rollout for Phase 1."

        return ExecutiveBriefing(
            executive_summary=exec_summary,
            business_problem_solved=business_problem,
            key_metrics_and_roi=metrics,
            risk_mitigation=risk_mitigation,
            next_action_for_leadership=next_action,
        )

    @classmethod
    def generate_tech_spec(
        cls,
        feature_name: str,
        components: List[str],
        contracts: List[str],
        latency: str,
        recovery: str,
    ) -> TechnicalSpec:
        return TechnicalSpec(
            architecture_overview=f"Production integration topology for {feature_name}",
            components_involved=components,
            api_contracts=contracts,
            latency_and_throughput=latency,
            failure_recovery_mode=recovery,
        )

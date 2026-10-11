"""Measurable business impact tracking for Pillar 3."""

from typing import Dict, Optional
from pydantic import BaseModel


class BusinessImpactMetrics(BaseModel):
    initiative_name: str
    baseline_turnaround_hours: float
    current_turnaround_hours: float
    turnaround_reduction_pct: float
    cases_processed_monthly: int
    hourly_labor_rate_usd: float = 85.0
    monthly_hours_saved: float
    annual_cost_savings_usd: float
    impact_resume_statement: str


class ImpactTracker:
    """Tracks and calculates verified business impact and ROI metrics for FDE initiatives."""

    @classmethod
    def calculate_impact(
        cls,
        initiative_name: str,
        baseline_turnaround_hours: float,
        current_turnaround_hours: float,
        cases_processed_monthly: int,
        hours_saved_per_case: Optional[float] = None,
        hourly_labor_rate_usd: float = 85.0,
    ) -> BusinessImpactMetrics:
        reduction_pct = (
            (baseline_turnaround_hours - current_turnaround_hours) / baseline_turnaround_hours
        ) * 100.0

        if hours_saved_per_case is None:
            # Estimate labor savings as 60% of cycle reduction time
            hours_saved_per_case = max(0.1, (baseline_turnaround_hours - current_turnaround_hours) * 0.6)

        monthly_hours_saved = round(hours_saved_per_case * cases_processed_monthly, 1)
        annual_savings = round(monthly_hours_saved * 12 * hourly_labor_rate_usd, 2)

        # Generate the signature impact bullet as highlighted in the FDE video
        if baseline_turnaround_hours >= 24:
            b_str = f"{baseline_turnaround_hours / 24:.1f} days"
        else:
            b_str = f"{baseline_turnaround_hours:.1f} hours"

        if current_turnaround_hours < 1.0:
            c_str = f"{int(current_turnaround_hours * 60)} minutes"
        else:
            c_str = f"{current_turnaround_hours:.1f} hours"

        impact_bullet = (
            f"Built and forward-deployed an end-to-end AI system for {initiative_name} that slashed turnaround "
            f"from {b_str} to {c_str} ({reduction_pct:.0f}% reduction), saving {monthly_hours_saved:,.0f} operator hours "
            f"monthly and driving ${annual_savings:,.0f} in annual efficiency gains."
        )

        return BusinessImpactMetrics(
            initiative_name=initiative_name,
            baseline_turnaround_hours=baseline_turnaround_hours,
            current_turnaround_hours=current_turnaround_hours,
            turnaround_reduction_pct=round(reduction_pct, 1),
            cases_processed_monthly=cases_processed_monthly,
            hourly_labor_rate_usd=hourly_labor_rate_usd,
            monthly_hours_saved=monthly_hours_saved,
            annual_cost_savings_usd=annual_savings,
            impact_resume_statement=impact_bullet,
        )

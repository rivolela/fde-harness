"""Usage critique and friction pattern detector for Continuous Evolution."""

from collections import Counter
from typing import List
from pydantic import BaseModel, Field
from .memory import InteractionEvent


class FrictionPattern(BaseModel):
    category: str  # 'high_latency', 'client_jargon_pushback', 'schema_mismatch', 'unhandled_edge_case'
    occurrences: int
    severity: str  # 'LOW', 'MEDIUM', 'HIGH'
    example_notes: List[str] = Field(default_factory=list)
    suggested_focus: str


class UsageCritiqueAnalyzer:
    """Analyzes interaction telemetry to identify where the agent is encountering friction or limitations."""

    @classmethod
    def analyze_events(cls, events: List[InteractionEvent]) -> List[FrictionPattern]:
        patterns: List[FrictionPattern] = []
        if not events:
            return patterns

        # 1. Friction notes analysis
        friction_events = [e for e in events if e.friction_detected]
        
        # 2. Latency friction
        high_latency = [e for e in events if e.latency_ms > 3000]
        if high_latency:
            patterns.append(
                FrictionPattern(
                    category="high_latency",
                    occurrences=len(high_latency),
                    severity="MEDIUM" if len(high_latency) < 5 else "HIGH",
                    example_notes=[f"Latency spiked to {e.latency_ms:.0f}ms on {e.event_type}" for e in high_latency[:3]],
                    suggested_focus="Implement streaming responses or async background processing for enterprise calls.",
                )
            )

        # 3. Client pushback or negative feedback
        feedback_events = [e for e in events if e.client_feedback]
        jargon_notes = [e.client_feedback for e in feedback_events if e.client_feedback and "jargon" in e.client_feedback.lower()]
        if jargon_notes:
            patterns.append(
                FrictionPattern(
                    category="client_jargon_pushback",
                    occurrences=len(jargon_notes),
                    severity="HIGH",
                    example_notes=jargon_notes[:3],
                    suggested_focus="Enforce executive dual-track translation to eliminate deep ML jargon from client updates.",
                )
            )

        # 4. Failed interactions
        failures = [e for e in events if not e.success]
        if failures:
            patterns.append(
                FrictionPattern(
                    category="unhandled_edge_case",
                    occurrences=len(failures),
                    severity="HIGH",
                    example_notes=[e.output_summary for e in failures[:3]],
                    suggested_focus="Harden input sanitization and add fallback recovery hooks in workflow orchestrator.",
                )
            )

        return patterns

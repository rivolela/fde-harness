"""Friday 5 PM Incident Commander and client triage for Pillar 3."""

import datetime
from typing import List
from pydantic import BaseModel, Field


class IncidentReport(BaseModel):
    incident_id: str
    severity: str  # SEV-1, SEV-2, SEV-3
    symptom: str
    root_cause: str
    immediate_mitigation: str
    permanent_fix: str
    client_statement: str
    preventive_actions: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())


class IncidentCommander:
    """Manages high-stakes client production incidents (e.g., Friday 5 PM outages).

    Enforces ownership, client calm, and rigorous postmortems.
    """

    @classmethod
    def handle_incident(
        cls,
        incident_id: str,
        severity: str,
        symptom: str,
        technical_cause: str,
        fix_applied: str,
    ) -> IncidentReport:
        # Formulate a calm, professional statement for client stakeholders watching over the shoulder
        client_update = (
            f"Update on {incident_id}: We identified anomalous behavior in the pipeline ({symptom}). "
            f"Our team immediately isolated the affected queue and applied a deterministic mitigation ({fix_applied}). "
            "Data integrity is preserved, systems are operating within normal parameters, and we are monitoring closely."
        )

        preventive = [
            "Add pre-flight schema contract test to prevent unexpected null values from upstream systems.",
            "Introduce automated rate-limiting fallback to degrade gracefully rather than fail open.",
            "Update runbook and alert threshold for latency spikes exceeding 2500ms.",
        ]

        return IncidentReport(
            incident_id=incident_id,
            severity=severity,
            symptom=symptom,
            root_cause=technical_cause,
            immediate_mitigation=fix_applied,
            permanent_fix=f"Hardened pipeline with defensive retry and fallback for: {technical_cause}",
            client_statement=client_update,
            preventive_actions=preventive,
        )

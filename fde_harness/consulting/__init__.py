"""Pillar 3: Consulting, Customer & Business Bridge Core.

Translates technical excellence into client-facing value, decomposes ambiguous problems,
maintains dual-track communication, tracks measurable ROI, and owns production incidents.
"""

from .decomposer import AmbiguousProblemDecomposer, DecomposedPlan
from .communicator import DualTrackCommunicator, ExecutiveBriefing, TechnicalSpec
from .impact_tracker import ImpactTracker, BusinessImpactMetrics
from .incident_room import IncidentCommander, IncidentReport

__all__ = [
    "AmbiguousProblemDecomposer",
    "DecomposedPlan",
    "DualTrackCommunicator",
    "ExecutiveBriefing",
    "TechnicalSpec",
    "ImpactTracker",
    "BusinessImpactMetrics",
    "IncidentCommander",
    "IncidentReport",
]

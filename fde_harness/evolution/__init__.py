"""Continuous Evolution & Self-Improvement Engine.

Empowers the FDE Agent to log usage telemetry, analyze friction patterns, critique its performance,
and generate self-improving upgrades according to real-world usage.
"""

from .memory import EvolutionMemory, SessionTrace, InteractionEvent
from .critique import UsageCritiqueAnalyzer, FrictionPattern
from .evolver import HarnessEvolver, ImprovementProposal

__all__ = [
    "EvolutionMemory",
    "SessionTrace",
    "InteractionEvent",
    "UsageCritiqueAnalyzer",
    "FrictionPattern",
    "HarnessEvolver",
    "ImprovementProposal",
]

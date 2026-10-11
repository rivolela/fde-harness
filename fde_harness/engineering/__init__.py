"""Pillar 1: Robust Software Engineering Core.

Provides foundational tools for enterprise integrations, legacy system connectors,
architecture design trade-offs, and defensive testing.
"""

from .connectors import EnterpriseConnector, LegacyDataCleaner, SchemaDefinition
from .system_design import ArchitectureComponent, ArchitectureDesign, SystemTradeOffAnalyzer, TradeOffOption
from .diagnostics import CodeDiagnostics, DiagnosticReport

__all__ = [
    "EnterpriseConnector",
    "LegacyDataCleaner",
    "SchemaDefinition",
    "ArchitectureComponent",
    "ArchitectureDesign",
    "SystemTradeOffAnalyzer",
    "TradeOffOption",
    "CodeDiagnostics",
    "DiagnosticReport",
]

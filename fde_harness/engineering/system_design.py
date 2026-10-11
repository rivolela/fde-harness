"""System design modeling and trade-off defense for Pillar 1."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ArchitectureComponent(BaseModel):
    name: str
    role: str
    tech_stack: str
    dependencies: List[str] = Field(default_factory=list)
    scalability_notes: Optional[str] = None


class ArchitectureDesign(BaseModel):
    system_name: str
    overview: str
    components: List[ArchitectureComponent] = Field(default_factory=list)
    data_flows: List[str] = Field(default_factory=list)
    security_boundaries: List[str] = Field(default_factory=list)
    client_constraints: List[str] = Field(default_factory=list)


class TradeOffOption(BaseModel):
    name: str
    pros: List[str]
    cons: List[str]
    cost_level: str  # Low, Medium, High
    latency_level: str  # Low, Medium, High
    compliance_fit: str  # Excellent, Moderate, Strict-Requires-VPC


class SystemTradeOffAnalyzer:
    """Evaluates architectural trade-offs and generates defensible recommendations

    tailored for client technical reviews.
    """

    @staticmethod
    def evaluate(
        decision_topic: str,
        options: List[TradeOffOption],
        recommended_option: str,
        rationale: str,
    ) -> Dict[str, Any]:
        return {
            "decision_topic": decision_topic,
            "options": [opt.model_dump() for opt in options],
            "recommended_option": recommended_option,
            "rationale": rationale,
            "defensibility_summary": (
                f"For topic '{decision_topic}', '{recommended_option}' was selected because: {rationale} "
                "This aligns with client latency and security requirements while balancing cost."
            ),
        }

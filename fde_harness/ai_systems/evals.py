"""Evaluation suite and guardrails for Pillar 2 AI systems."""

import json
import os
import re
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    is_grounded: bool
    grounding_score: float  # 0.0 to 1.0
    latency_ms: float
    estimated_cost_usd: float
    violations: List[str] = Field(default_factory=list)
    passed_guardrails: bool = True
    requires_human_review: bool = True  # Enforces Human-in-the-Loop (AI as co-author, not autopilot)
    human_in_the_loop_verified: bool = False
    audit_trail_target: str = ".fde_evolution/traces.jsonl"
    summary: str = ""


class EnterpriseEvaluator:
    """Evaluates AI responses against real-world enterprise criteria:

    - Groundedness (does the response hallucinate facts not in retrieved context?)
    - Guardrails (PII, confidential credentials, prohibited terms, autopilot bypass)
    - Human-in-the-Loop verification (AI as co-author, human executor review)
    - Latency and cost estimation
    """

    COST_PER_1K_INPUT_TOKENS = 0.0015
    COST_PER_1K_OUTPUT_TOKENS = 0.0020

    @classmethod
    def evaluate_groundedness(cls, context: str, response: str) -> float:
        """Calculates factual overlap between response tokens and context."""
        context_words = set(context.lower().split())
        response_words = [w for w in response.lower().split() if len(w) > 3]

        if not response_words:
            return 1.0

        supported = [w for w in response_words if w in context_words]
        score = len(supported) / len(response_words)
        return round(min(1.0, max(0.0, score)), 2)

    @classmethod
    def check_guardrails(cls, text: str) -> List[str]:
        """Checks for enterprise compliance violations (PII, credentials, unapproved autopilot mode)."""
        violations = []
        # Basic PII regex heuristics
        if re.search(r"\b\d{3}-\d{2}-\d{4}\b", text):
            violations.append("PII Exposure: Detected potential Social Security Number (SSN).")
        if re.search(r"\b(?:\d{4}-){3}\d{4}\b", text):
            violations.append("PII Exposure: Detected potential Credit Card Number.")
        if re.search(r"(?i)\bconfidential\s+trade\s+secret\b", text):
            violations.append("Compliance Violation: Detected unredacted internal trade secret label.")
        # Human-in-the-Loop / Autopilot bypass checks
        if re.search(r"(?i)\b(bypass(?:ing)?\s+human\s+review|unsupervised\s+auto-?pilot|disable\s+(?:audit|oversight))\b", text):
            violations.append("Governance Violation: Attempted to bypass human review or execute in unmonitored autopilot mode.")
        return violations

    @classmethod
    def run_eval(
        cls,
        context: str,
        response: str,
        latency_ms: float,
        input_token_count: int = 500,
        output_token_count: int = 150,
    ) -> EvaluationResult:
        grounding_score = cls.evaluate_groundedness(context, response)
        is_grounded = grounding_score >= 0.60
        violations = cls.check_guardrails(response)
        passed_guardrails = len(violations) == 0

        cost = (
            (input_token_count / 1000.0) * cls.COST_PER_1K_INPUT_TOKENS
            + (output_token_count / 1000.0) * cls.COST_PER_1K_OUTPUT_TOKENS
        )

        summary = (
            f"Grounding: {grounding_score*100:.0f}% ({'PASS' if is_grounded else 'FAIL'}) | "
            f"Latency: {latency_ms:.1f}ms | Cost: ${cost:.4f} | Guardrails: {'PASS' if passed_guardrails else 'FAIL'} | "
            f"HITL: Required (Co-Author Mode)"
        )

        return EvaluationResult(
            is_grounded=is_grounded,
            grounding_score=grounding_score,
            latency_ms=latency_ms,
            estimated_cost_usd=round(cost, 5),
            violations=violations,
            passed_guardrails=passed_guardrails,
            requires_human_review=True,
            human_in_the_loop_verified=False,
            audit_trail_target=".fde_evolution/traces.jsonl",
            summary=summary,
        )

    @classmethod
    def record_human_signoff(
        cls,
        decision_id: str,
        reviewer_id: str,
        status: str = "APPROVED",
        notes: str = "",
        storage_dir: str = ".fde_evolution",
    ) -> Dict[str, Any]:
        """Audits human-in-the-loop sign-off into .fde_evolution/traces.jsonl.

        Enforces AI as co-author, ensuring every critical production decision is
        reviewed by an FDE executor and persisted in immutable telemetry.
        """
        os.makedirs(storage_dir, exist_ok=True)
        audit_file = os.path.join(storage_dir, "traces.jsonl")
        audit_record = {
            "event_id": f"hitl_{decision_id}",
            "event_type": "human_in_the_loop_review",
            "decision_id": decision_id,
            "reviewer_id": reviewer_id,
            "status": status,
            "notes": notes,
            "timestamp": time.time(),
            "co_author_mode": True,
        }
        with open(audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(audit_record) + "\n")
        return audit_record

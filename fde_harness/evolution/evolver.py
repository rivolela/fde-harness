"""Evolution proposal synthesizer and improvement generator."""

import json
import os
import time
from typing import Dict, List
from pydantic import BaseModel, Field
from .critique import FrictionPattern
from .memory import EvolutionMemory, InteractionEvent


class ImprovementProposal(BaseModel):
    proposal_id: str
    target_pillar: str  # 'Pillar 1: Software Engineering', 'Pillar 2: AI Systems', 'Pillar 3: Consulting'
    category: str  # 'PROMPT_REFINEMENT', 'TOOL_EXPANSION', 'WORKFLOW_GUARD', 'DOMAIN_KNOWLEDGE'
    title: str
    rationale: str
    action_items: List[str]
    status: str = "PROPOSED"  # 'PROPOSED', 'APPLIED', 'REJECTED'
    created_at: float = Field(default_factory=time.time)


class HarnessEvolver:
    """Synthesizes usage telemetry and critique into concrete, actionable harness improvements."""

    def __init__(self, storage_dir: str = ".fde_evolution"):
        self.storage_dir = storage_dir
        self.memory = EvolutionMemory(storage_dir)
        self.proposals_file = os.path.join(storage_dir, "proposals.json")

    def generate_proposals(self) -> List[ImprovementProposal]:
        events = self.memory.load_recent_events(limit=100)
        from .critique import UsageCritiqueAnalyzer
        patterns = UsageCritiqueAnalyzer.analyze_events(events)

        proposals: List[ImprovementProposal] = []
        prop_idx = int(time.time())

        # If no events yet, provide initial baseline self-improvement suggestions based on enterprise deployment best practices
        if not events:
            proposals.append(
                ImprovementProposal(
                    proposal_id=f"PROP-{prop_idx}-01",
                    target_pillar="Pillar 3: Consulting",
                    category="PROMPT_REFINEMENT",
                    title="Enforce executive-first executive summary framing",
                    rationale="Initial baseline: ensure all client communication leads with quantified business impact before technical details.",
                    action_items=[
                        "Update default communication prompts to lead with time-saved metrics.",
                        "Add automated check for banned ML jargon terms in client briefings.",
                    ],
                )
            )
            proposals.append(
                ImprovementProposal(
                    proposal_id=f"PROP-{prop_idx}-02",
                    target_pillar="Pillar 1: Software Engineering",
                    category="TOOL_EXPANSION",
                    title="Add automated schema drift detection for client DB queries",
                    rationale="Enterprise databases frequently change schema between client sprints without notice.",
                    action_items=[
                        "Implement table hash caching in EnterpriseConnector.",
                        "Trigger non-blocking warning when new unmapped columns appear.",
                    ],
                )
            )
            return proposals

        for pattern in patterns:
            prop_idx += 1
            if pattern.category == "client_jargon_pushback":
                proposals.append(
                    ImprovementProposal(
                        proposal_id=f"PROP-{prop_idx}",
                        target_pillar="Pillar 3: Consulting",
                        category="PROMPT_REFINEMENT",
                        title="Aggressively strip internal AI terminology from client updates",
                        rationale=f"Detected {pattern.occurrences} instances of client pushback regarding technical jargon.",
                        action_items=[
                            "Add a pre-send filter replacing terms like 'embeddings', 'logits', 'temperature' with business equivalents.",
                            "Reinforce DualTrackCommunicator guidelines.",
                        ],
                    )
                )
            elif pattern.category == "high_latency":
                proposals.append(
                    ImprovementProposal(
                        proposal_id=f"PROP-{prop_idx}",
                        target_pillar="Pillar 2: AI Systems",
                        category="WORKFLOW_GUARD",
                        title="Add chunk caching and parallel retrieval to lower latency",
                        rationale=f"Observed {pattern.occurrences} requests exceeding 3000ms latency threshold.",
                        action_items=[
                            "Implement in-memory cache for frequently asked enterprise domain queries.",
                            "Batch retrieval calls in EnterpriseRAGPipeline.",
                        ],
                    )
                )
            elif pattern.category == "unhandled_edge_case":
                proposals.append(
                    ImprovementProposal(
                        proposal_id=f"PROP-{prop_idx}",
                        target_pillar="Pillar 1: Software Engineering",
                        category="TOOL_EXPANSION",
                        title="Expand defensive input sanitizers for dirty enterprise formats",
                        rationale=f"Recorded {pattern.occurrences} unexpected failures during pipeline execution.",
                        action_items=[
                            "Broaden null sentinel heuristics in LegacyDataCleaner.",
                            "Add automatic fallback mock generation when table query fails.",
                        ],
                    )
                )

        if not patterns and events:
            proposals.append(
                ImprovementProposal(
                    proposal_id=f"PROP-{prop_idx}-PROACTIVE",
                    target_pillar="Pillar 2: AI Systems",
                    category="WORKFLOW_GUARD",
                    title="Scale benchmarking to 500+ enterprise regression test cases",
                    rationale=f"Recent {len(events)} interactions executed cleanly. Next maturity step is rigorous regression suite scaling.",
                    action_items=[
                        "Synthesize 20 edge-case synthetic enterprise policy documents.",
                        "Add automated ground-truth faithfulness benchmarks before each sprint release.",
                    ],
                )
            )

        self._save_proposals(proposals)
        return proposals

    def _save_proposals(self, proposals: List[ImprovementProposal]) -> None:
        existing = self.load_proposals()
        existing_ids = {p.proposal_id for p in existing}
        for p in proposals:
            if p.proposal_id not in existing_ids:
                existing.append(p)

        with open(self.proposals_file, "w", encoding="utf-8") as f:
            json.dump([p.model_dump() for p in existing], f, indent=2)

    def load_proposals(self) -> List[ImprovementProposal]:
        if not os.path.exists(self.proposals_file):
            return []
        try:
            with open(self.proposals_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [ImprovementProposal(**d) for d in data]
        except Exception:
            return []

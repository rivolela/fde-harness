"""Telemetry and session trace persistence for Continuous Evolution."""

import json
import os
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class InteractionEvent(BaseModel):
    event_id: str
    event_type: str  # e.g., 'case_study', 'pipeline_run', 'client_presentation', 'incident'
    input_prompt: str
    output_summary: str
    success: bool
    latency_ms: float
    client_feedback: Optional[str] = None
    friction_detected: bool = False
    friction_notes: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)


class SessionTrace(BaseModel):
    session_id: str
    events: List[InteractionEvent] = Field(default_factory=list)


class EvolutionMemory:
    """Stores and retrieves usage telemetry and interaction traces."""

    def __init__(self, storage_dir: str = ".fde_evolution"):
        self.storage_dir = storage_dir
        self.traces_file = os.path.join(storage_dir, "traces.jsonl")
        os.makedirs(self.storage_dir, exist_ok=True)

    def log_event(self, event: InteractionEvent) -> None:
        """Appends an interaction event to traces.jsonl."""
        with open(self.traces_file, "a", encoding="utf-8") as f:
            f.write(event.model_dump_json() + "\n")

    def load_recent_events(self, limit: int = 50) -> List[InteractionEvent]:
        """Loads the most recent events."""
        if not os.path.exists(self.traces_file):
            return []

        events: List[InteractionEvent] = []
        with open(self.traces_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        events.append(InteractionEvent(**data))
                    except Exception:
                        continue
        return events[-limit:]

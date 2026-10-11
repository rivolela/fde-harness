"""Workflow orchestration and multi-step execution for Pillar 2."""

import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class WorkflowStep(BaseModel):
    step_id: str
    name: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, failed
    execution_time_ms: float = 0.0
    output_summary: Optional[str] = None
    error: Optional[str] = None


class WorkflowPlan(BaseModel):
    plan_id: str
    objective: str
    steps: List[WorkflowStep] = Field(default_factory=list)
    total_duration_ms: float = 0.0
    status: str = "pending"


class WorkflowOrchestrator:
    """Orchestrates multi-step AI integration workflows with end-to-end telemetry."""

    def __init__(self):
        self._step_handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}

    def register_step_handler(self, step_name: str, handler: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        self._step_handlers[step_name] = handler

    def execute_plan(self, plan: WorkflowPlan, initial_state: Optional[Dict[str, Any]] = None) -> WorkflowPlan:
        state = initial_state or {}
        total_start = time.perf_counter()
        plan.status = "in_progress"

        for step in plan.steps:
            step.status = "in_progress"
            step_start = time.perf_counter()
            handler = self._step_handlers.get(step.name)

            if not handler:
                step.status = "failed"
                step.error = f"No handler registered for step '{step.name}'"
                plan.status = "failed"
                break

            try:
                result = handler(state)
                state.update(result)
                step.status = "completed"
                step.output_summary = f"Generated {len(result.keys())} state keys"
            except Exception as exc:
                step.status = "failed"
                step.error = str(exc)
                plan.status = "failed"
                break
            finally:
                step.execution_time_ms = round((time.perf_counter() - step_start) * 1000, 2)

        if plan.status != "failed":
            plan.status = "completed"

        plan.total_duration_ms = round((time.perf_counter() - total_start) * 1000, 2)
        return plan

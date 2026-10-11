<!-- bmad:context -->
<!-- Verified 2026-10-10 against ccf49bd. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## FDE-Harness

Forward Deployed Engineer (FDE) Agent Harness bridging enterprise client reality and production AI systems. Python 3.10+, Pydantic, Click, Rich, httpx. Full software lifecycle and execution architecture are documented in `HARNESS.md`.

## Policy

- Human-in-the-Loop (HITL) mandatory: AI operates strictly as a co-author, never an autonomous autopilot. Every architecture decision, code rollout, and high-impact action must be reviewed and signed off by the human FDE executor.
- Maintain strict client compliance: default to In-VPC topology and zero external data transit.
- Audit logging: all decisions, evaluations (`EnterpriseEvaluator`), and human sign-offs must be logged to `.fde_evolution/traces.jsonl`.
- Never commit credentials or API keys; AST scanner (`CodeDiagnostics`) strictly flags hardcoded secrets.
- Every client delivery must track verified business metrics (baseline vs. achieved cycle time and ROI).

## Where things are

- Standard 7-phase execution cycle & pipeline: `HARNESS.md` and `fde_execution_cycle.py`
- Pillar 1 (Engineering - Connectors, Sanitizers, Diagnostics, Trade-offs): `fde_harness/engineering/`
- Pillar 2 (AI Systems - RAG, Enterprise Evaluator, Workflow Engine): `fde_harness/ai_systems/`
- Pillar 3 (Consulting - Ambiguity Decomposer, Executive Briefing, Impact Tracker, Incident Commander): `fde_harness/consulting/`
- Continuous Evolution Engine & Telemetry: `fde_harness/evolution/` (traces stored in `.fde_evolution/traces.jsonl`)
- Historical specs and interview transcripts: `doc/`

## Running and verifying

- Verify unit tests with `python3 -m unittest discover tests` (do not invoke bare `pytest`, which fails without optional pygments).
- Run full end-to-end 7-phase simulation: `python3 fde_execution_cycle.py`.
- Harness CLI commands: `python3 -m fde_harness.cli <init|decompose|incident-drill|evolve|run-scenario>`.

## Conventions that differ from defaults

- BMAD framework (`_bmad/`, `.agent/skills/`) is committed and tracked in git so that any cloned client repository immediately equips AI coding agents with all specialized skills. Ephemeral output (`_bmad-output/`) and machine overrides (`*.user.toml`) are gitignored.
- Legacy enterprise data contains string sentinels (`"N/A"`, `"NULL"`, `"-"`); always sanitize through `clean_legacy_record()` before downstream usage.
- All external HTTP/network calls must have explicit `timeout` arguments, enforced defensively during AST scans.
- Dual-track communication is mandatory: technical architectural decisions must pair with non-technical executive impact briefings.

## Known pitfalls

- Never delete `.fde_evolution/` — friction detection and telemetry critique depend on historical execution logs.
- Never bypass the `AmbiguousProblemDecomposer` for raw client requests; always structure vague problems into measurable, 3-phase delivery plans.

<!-- /bmad:context -->

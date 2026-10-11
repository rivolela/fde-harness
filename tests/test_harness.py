"""Comprehensive test suite for the Forward Deployed Engineer (FDE) Agent Harness."""

import os
import shutil
import unittest

from fde_harness.engineering import (
    CodeDiagnostics,
    EnterpriseConnector,
    LegacyDataCleaner,
    SystemTradeOffAnalyzer,
)
from fde_harness.ai_systems import (
    EnterpriseEvaluator,
    EnterpriseRAGPipeline,
    WorkflowOrchestrator,
    WorkflowPlan,
    WorkflowStep,
)
from fde_harness.consulting import (
    AmbiguousProblemDecomposer,
    DualTrackCommunicator,
    ImpactTracker,
    IncidentCommander,
)
from fde_harness.evolution import (
    EvolutionMemory,
    HarnessEvolver,
    InteractionEvent,
    UsageCritiqueAnalyzer,
)
from fde_harness import FDEHarness


class TestFDEHarness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = ".test_fde_evolution"

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    # ------------------ PILLAR 1 TESTS ------------------
    def test_legacy_data_cleaner(self):
        dirty_record = {
            "First Name": " Alice ",
            "Tax-ID": "N/A",
            "Age": 30,
            "Notes": " - ",
        }
        cleaned = LegacyDataCleaner.sanitize_record(dirty_record)
        self.assertEqual(cleaned["first_name"], "Alice")
        self.assertIsNone(cleaned["tax_id"])
        self.assertEqual(cleaned["age"], 30)
        self.assertIsNone(cleaned["notes"])

    def test_enterprise_connector_safety(self):
        connector = EnterpriseConnector(client_name="TestBank", read_only=True)
        connector.register_table("accounts", [{"id": 1, "balance": 5000}])

        # Read query
        read_res = connector.execute_query("SELECT * FROM accounts")
        self.assertTrue(read_res["success"])
        self.assertEqual(read_res["row_count"], 1)

        # Write query should be blocked
        write_res = connector.execute_query("DELETE FROM accounts WHERE id = 1")
        self.assertFalse(write_res["success"])
        self.assertIn("Safety Violation", write_res["error"])

    def test_code_diagnostics_ast_and_secrets(self):
        # Code with hardcoded secret and no timeout
        bad_code = """
import requests
api_key = "sk-1234567890123456789012345"
def call():
    requests.get("https://api.internal.corp")
"""
        diag = CodeDiagnostics.analyze_python_code(bad_code)
        self.assertFalse(diag.is_valid)
        self.assertTrue(any("Security Alert" in e for e in diag.errors))
        self.assertTrue(any("timeout" in w for w in diag.warnings))

    # ------------------ PILLAR 2 TESTS ------------------
    def test_rag_pipeline_retrieval(self):
        pipeline = EnterpriseRAGPipeline(chunk_size=100, chunk_overlap=10)
        pipeline.ingest_document(
            doc_id="policy_01",
            raw_text="Enterprise risk compliance mandates that all financial audits be preserved for 7 years.",
        )
        results = pipeline.retrieve("financial audits compliance", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertGreater(results[0].relevance_score, 0)
        self.assertIn("audits", results[0].content)

    def test_enterprise_evaluator_guardrails(self):
        clean_text = "The system successfully processed the application."
        pii_text = "Customer SSN is 000-12-3456."

        self.assertEqual(len(EnterpriseEvaluator.check_guardrails(clean_text)), 0)
        violations = EnterpriseEvaluator.check_guardrails(pii_text)
        self.assertGreaterEqual(len(violations), 1)
        self.assertIn("SSN", violations[0])

        # Test autopilot bypass rejection (Human-in-the-Loop policy)
        autopilot_text = "Deploying immediately and bypassing human review in autopilot mode."
        autopilot_violations = EnterpriseEvaluator.check_guardrails(autopilot_text)
        self.assertGreaterEqual(len(autopilot_violations), 1)
        self.assertIn("bypass human review", autopilot_violations[0].lower())

        # Test human-in-the-loop sign-off audit logging to test directory
        test_audit_dir = ".test_fde_evolution"
        signoff = EnterpriseEvaluator.record_human_signoff(
            decision_id="TEST-DEC-001",
            reviewer_id="Test-FDE",
            status="APPROVED",
            notes="Reviewed co-authored model recommendation.",
            storage_dir=test_audit_dir,
        )
        self.assertEqual(signoff["status"], "APPROVED")
        self.assertTrue(signoff["co_author_mode"])
        import os
        self.assertTrue(os.path.exists(os.path.join(test_audit_dir, "traces.jsonl")))

    def test_workflow_orchestrator(self):
        orch = WorkflowOrchestrator()
        orch.register_step_handler("step_a", lambda s: {"val": s.get("input", 0) + 10})

        plan = WorkflowPlan(
            plan_id="p1",
            objective="test",
            steps=[WorkflowStep(step_id="s1", name="step_a", description="add 10")],
        )
        completed = orch.execute_plan(plan, initial_state={"input": 5})
        self.assertEqual(completed.status, "completed")
        self.assertEqual(completed.steps[0].status, "completed")

    # ------------------ PILLAR 3 TESTS ------------------
    def test_ambiguous_problem_decomposer(self):
        decomposed = AmbiguousProblemDecomposer.decompose(
            "Fix our loan origination backlog with AI.", client_context="Global Investment Bank"
        )
        self.assertGreaterEqual(len(decomposed.milestones), 3)
        self.assertGreaterEqual(len(decomposed.target_business_metrics), 2)
        self.assertEqual(decomposed.milestones[0].phase, 1)

    def test_impact_tracker_roi_calculation(self):
        impact = ImpactTracker.calculate_impact(
            initiative_name="Credit Underwriting Bot",
            baseline_turnaround_hours=48.0,
            current_turnaround_hours=0.33,  # 20 mins
            cases_processed_monthly=1000,
        )
        self.assertGreater(impact.turnaround_reduction_pct, 99.0)
        self.assertGreater(impact.annual_cost_savings_usd, 100000.0)
        self.assertIn("2.0 days", impact.impact_resume_statement)
        self.assertIn("minutes", impact.impact_resume_statement)

    def test_incident_commander(self):
        report = IncidentCommander.handle_incident(
            incident_id="INC-001",
            severity="SEV-1",
            symptom="Pipeline stall",
            technical_cause="DB lock",
            fix_applied="Killed deadlocks and added transaction timeout",
        )
        self.assertEqual(report.severity, "SEV-1")
        self.assertIn("We identified anomalous behavior", report.client_statement)
        self.assertGreaterEqual(len(report.preventive_actions), 2)

    # ------------------ EVOLUTION TESTS ------------------
    def test_evolution_telemetry_and_proposals(self):
        memory = EvolutionMemory(storage_dir=self.test_dir)
        # Log simulated friction events
        memory.log_event(
            InteractionEvent(
                event_id="e1",
                event_type="test",
                input_prompt="test",
                output_summary="test",
                success=False,
                latency_ms=4500.0,
                friction_detected=True,
                client_feedback="Too much technical jargon for the steering committee.",
            )
        )

        evolver = HarnessEvolver(storage_dir=self.test_dir)
        proposals = evolver.generate_proposals()
        self.assertGreaterEqual(len(proposals), 1)

        # Verify proposals can be re-loaded
        loaded = evolver.load_proposals()
        self.assertEqual(len(loaded), len(proposals))

    # ------------------ END-TO-END HARNESS TEST ------------------
    def test_fde_harness_facade(self):
        harness = FDEHarness(client_name="Enterprise-Test", storage_dir=self.test_dir)
        results = harness.run_end_to_end_scenario(
            problem_statement="Automate claims triage",
            sample_enterprise_doc="Underwriting policy 101: all approvals require two signatures.",
            query="approvals two signatures",
            baseline_hours=24.0,
            target_hours=0.5,
            monthly_volume=500,
        )
        self.assertEqual(results["client"], "Enterprise-Test")
        self.assertIn("decomposed_plan", results)
        self.assertIn("business_impact", results)
        self.assertIn("executive_briefing", results)

    def test_cli_init_command(self):
        from click.testing import CliRunner
        from fde_harness.cli import main

        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(main, ["init", "--client", "AutomatedTestCorp"])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.exists(".agent/skills"))
            self.assertTrue(os.path.exists("_bmad"))
            self.assertTrue(os.path.exists("AGENTS.md"))
            self.assertTrue(os.path.exists("HARNESS.md"))
            self.assertTrue(os.path.exists(".fde_evolution/traces.jsonl"))
            self.assertTrue(os.path.exists(".gitignore"))

    def test_cli_init_co_ai_mode(self):
        from click.testing import CliRunner
        from pathlib import Path
        from fde_harness.cli import main

        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create simulated .git directory
            Path(".git").mkdir()
            result = runner.invoke(main, ["init", "--client", "ClientCo", "--co-ai"])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.exists(".agent/skills"))
            self.assertTrue(os.path.exists("_bmad"))
            self.assertTrue(os.path.exists("AGENTS.md"))
            self.assertTrue(os.path.exists("HARNESS.md"))
            
            # .gitignore should NOT be created or modified
            self.assertFalse(os.path.exists(".gitignore"))

            # .git/info/exclude should contain the exclusion rules
            exclude_path = Path(".git/info/exclude")
            self.assertTrue(exclude_path.exists())
            content = exclude_path.read_text()
            self.assertIn("_bmad/", content)
            self.assertIn(".agent/", content)
            self.assertIn("AGENTS.md", content)


if __name__ == "__main__":
    unittest.main()


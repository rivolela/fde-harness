"""Interactive CLI for the FDE Agent Harness using Click and Rich."""

import json
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from fde_harness import FDEHarness

console = Console()


from pathlib import Path


@click.group()
def main():
    """Forward Deployed Engineer (FDE) Agent Harness - Enterprise Problem-Solving Framework."""
    pass


@main.command("init")
@click.option("--client", "-c", default="Enterprise-Client", help="Client or organization name for this deployment")
def init_cmd(client: str):
    """Initialize FDE Harness telemetry and governance in the current repository."""
    evo_dir = Path(".fde_evolution")
    evo_dir.mkdir(exist_ok=True)
    traces_file = evo_dir / "traces.jsonl"
    if not traces_file.exists():
        traces_file.touch()

    agents_file = Path("AGENTS.md")
    if not agents_file.exists():
        agents_file.write_text(f"""# FDE Rules for {client}

- Human-in-the-Loop (HITL) mandatory: AI operates strictly as a co-author, never an autonomous autopilot.
- Maintain strict client compliance: default to In-VPC topology and zero external data transit.
- Audit logging: all decisions, evaluations, and human sign-offs must be logged to `.fde_evolution/traces.jsonl`.
- Never commit credentials or API keys; AST scanner strictly flags hardcoded secrets.
- Every client delivery must track verified business metrics (baseline vs. achieved cycle time and ROI).
- Dual-track communication: technical architectural decisions must pair with non-technical executive impact briefings.
""")
        console.print("[bold green]✓ Created AGENTS.md with FDE governance policy[/bold green]")

    console.print(
        Panel(
            f"[bold green]✓ Initialized FDE Harness repository![/bold green]\n\n"
            f"[bold]Client / Project:[/bold] {client}\n"
            f"[bold]Telemetry Directory:[/bold] .fde_evolution/ (traces.jsonl ready)\n"
            f"[bold]Agent Governance:[/bold] AGENTS.md verified\n\n"
            f"Run [cyan]fde-harness decompose[/cyan] to begin decomposing client requirements.",
            title="FDE Workspace Initialized",
        )
    )


@main.command("decompose")
@click.argument("problem_statement", required=False)
def decompose_cmd(problem_statement: str):
    """Decompose an ambiguous enterprise client problem (Signature FDE Case Study)."""
    if not problem_statement:
        problem_statement = (
            "Our claims triage department is overwhelmed with unstructured customer PDF filings. "
            "Cycle time is 48 hours and leadership demands AI integration without risking regulatory fines."
        )

    harness = FDEHarness()
    console.print(Panel(f"[bold cyan]Client Problem:[/bold cyan] {problem_statement}", title="Ambiguous Problem Statement"))

    plan = harness.handle_ambiguous_case(problem_statement)

    # Display milestones
    table = Table(title="Phased Implementation Roadmap", show_header=True, header_style="bold magenta")
    table.add_column("Phase", style="dim", width=8)
    table.add_column("Milestone Name", style="bold")
    table.add_column("Timeline")
    table.add_column("Success Criteria")

    for m in plan.milestones:
        table.add_row(str(m.phase), m.name, m.timeline, m.success_criteria)

    console.print(table)

    # Display Target Business Metrics
    console.print("\n[bold green]Target Business Impact & Metrics:[/bold green]")
    for metric in plan.target_business_metrics:
        console.print(f"  • {metric}")


@main.command("run-scenario")
def scenario_cmd():
    """Run an end-to-end enterprise scenario covering all 3 pillars."""
    harness = FDEHarness()
    console.print("[bold yellow]Running End-to-End Enterprise FDE Simulation...[/bold yellow]\n")

    doc_sample = """
    POLICY 402 - ENTERPRISE OPERATIONS MANUAL
    All insurance claims under $10,000 without prior fraud flags are eligible for fast-track review.
    Unstructured submissions containing tax identifiers must be redacted prior to external API routing.
    Turnaround requirement for priority tier is under 45 minutes.
    """

    results = harness.run_end_to_end_scenario(
        problem_statement="Claims processing bottleneck taking 48 hours per submission.",
        sample_enterprise_doc=doc_sample,
        query="fast-track review eligibility under 10000",
        baseline_hours=48.0,
        target_hours=0.33,  # 20 minutes
        monthly_volume=1500,
    )

    # 1. Engineering & AI Pillar outputs
    eval_info = results["evaluation"]
    console.print(
        Panel(
            f"[bold]Grounding Score:[/bold] {eval_info['grounding_score']*100:.0f}%\n"
            f"[bold]Latency:[/bold] {eval_info['latency_ms']:.1f}ms\n"
            f"[bold]Estimated Cost:[/bold] ${eval_info['estimated_cost_usd']:.4f}\n"
            f"[bold]Guardrails Passed:[/bold] {'[green]YES[/green]' if eval_info['passed_guardrails'] else '[red]NO[/red]'}",
            title="Pillar 1 & 2: Systems & AI Engineering Health",
        )
    )

    # 2. Consulting & Business Impact
    impact = results["business_impact"]
    briefing = results["executive_briefing"]

    impact_table = Table(title="Pillar 3: Verified Business Impact", header_style="bold green")
    impact_table.add_column("Metric", style="bold")
    impact_table.add_column("Value")

    impact_table.add_row("Turnaround Reduction", f"{impact['turnaround_reduction_pct']:.1f}% (48h -> 20m)")
    impact_table.add_row("Monthly Hours Saved", f"{impact['monthly_hours_saved']:,.0f} hours")
    impact_table.add_row("Annual Efficiency Savings", f"${impact['annual_cost_savings_usd']:,.2f}")
    console.print(impact_table)

    console.print(
        Panel(
            f"[bold cyan]Executive Summary:[/bold cyan]\n{briefing['executive_summary']}\n\n"
            f"[bold cyan]Key ROI:[/bold cyan]\n{briefing['key_metrics_and_roi']}\n\n"
            f"[bold cyan]FDE Resume Bullet:[/bold cyan]\n[italic yellow]{impact['impact_resume_statement']}[/italic yellow]",
            title="Dual-Track Communication: Executive Briefing",
        )
    )


@main.command("incident-drill")
def incident_cmd():
    """Simulate a Friday 5 PM production incident drill under client observation."""
    harness = FDEHarness()
    console.print("[bold red]🚨 Friday 5:00 PM Incident Alert: Ingestion Pipeline Spiking Errors[/bold red]")

    report = harness.simulate_friday_incident(
        symptom="NullPointerException on legacy SAP export batch at 5:02 PM",
        root_cause="Client upstream ERP deployed unannounced schema change with empty tax_id fields",
        fix="Activated LegacyDataCleaner fallback null sentinel filter and rerouted failed batch to shadow queue",
    )

    console.print(
        Panel(
            f"[bold yellow]Incident ID:[/bold yellow] {report.incident_id} ({report.severity})\n"
            f"[bold yellow]Immediate Fix:[/bold yellow] {report.immediate_mitigation}\n\n"
            f"[bold green]Client-Facing Communication (Calm & Professional):[/bold green]\n"
            f"{report.client_statement}",
            title="Incident Commander Resolution",
        )
    )


@main.command("evolve")
def evolve_cmd():
    """Trigger the continuous evolution engine to critique usage and generate self-improvement proposals."""
    harness = FDEHarness()
    console.print("[bold cyan]Analyzing historical usage telemetry and generating self-evolution proposals...[/bold cyan]\n")

    proposals = harness.trigger_self_evolution()

    table = Table(title="Harness Self-Evolution Proposals", header_style="bold cyan")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Target Pillar", style="bold")
    table.add_column("Category", style="yellow")
    table.add_column("Title")
    table.add_column("Action Items")

    for p in proposals:
        actions = " • " + "\n • ".join(p.action_items)
        table.add_row(p.proposal_id, p.target_pillar, p.category, p.title, actions)

    console.print(table)
    console.print("\n[green]✓ Self-evolution proposals recorded in .fde_evolution/proposals.json[/green]")


if __name__ == "__main__":
    main()

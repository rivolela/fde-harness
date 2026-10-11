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
@click.option("--bmad/--no-bmad", default=True, help="Automatically install BMAD framework & agent skills")
@click.option("--force", "-f", is_flag=True, default=False, help="Overwrite existing configuration files")
@click.option("--co-ai", "--local-only", is_flag=True, default=False, help="Run as personal Co-AI: automatically exclude all FDE/BMAD files in .git/info/exclude without touching client's .gitignore")
def init_cmd(client: str, bmad: bool, force: bool, co_ai: bool):
    """Automatically bootstrap FDE Harness, BMAD skills, and governance in any repository."""
    import shutil
    templates_dir = Path(__file__).parent / "templates"
    
    # 1. Telemetry Directory
    evo_dir = Path(".fde_evolution")
    evo_dir.mkdir(exist_ok=True)
    traces_file = evo_dir / "traces.jsonl"
    if not traces_file.exists():
        traces_file.touch()

    # 2. Agent Governance & Policy
    agents_file = Path("AGENTS.md")
    if not agents_file.exists() or force:
        if (templates_dir / "AGENTS.md").exists():
            template_content = (templates_dir / "AGENTS.md").read_text()
            agents_file.write_text(template_content)
        else:
            agents_file.write_text(f"""# FDE Rules for {client}

- Human-in-the-Loop (HITL) mandatory: AI operates strictly as a co-author, never an autonomous autopilot.
- Maintain strict client compliance: default to In-VPC topology and zero external data transit.
- Audit logging: all decisions, evaluations, and human sign-offs must be logged to `.fde_evolution/traces.jsonl`.
- Never commit credentials or API keys; AST scanner strictly flags hardcoded secrets.
- Every client delivery must track verified business metrics (baseline vs. achieved cycle time and ROI).
- Dual-track communication: technical architectural decisions must pair with non-technical executive impact briefings.
""")
        console.print("[bold green]✓ Configured AGENTS.md governance rules[/bold green]")

    # 3. HARNESS.md lifecycle guide
    harness_file = Path("HARNESS.md")
    if (not harness_file.exists() or force) and (templates_dir / "HARNESS.md").exists():
        shutil.copy2(templates_dir / "HARNESS.md", harness_file)
        console.print("[bold green]✓ Installed HARNESS.md execution lifecycle guide[/bold green]")

    # 4. BMAD Framework & Skills installation
    skills_installed = 0
    if bmad and templates_dir.exists():
        # Install .agent/skills
        src_agent = templates_dir / "agent"
        if src_agent.exists():
            target_agent = Path(".agent")
            shutil.copytree(src_agent, target_agent, dirs_exist_ok=True)
            # Also provide .agents directory for backwards compatibility
            target_agents_alt = Path(".agents")
            shutil.copytree(src_agent, target_agents_alt, dirs_exist_ok=True)
            skills_dir = target_agent / "skills"
            if skills_dir.exists():
                skills_installed = len([d for d in skills_dir.iterdir() if d.is_dir()])
            console.print(f"[bold green]✓ Installed {skills_installed} BMAD agent skills in .agent/skills/[/bold green]")

        # Install _bmad/ configuration
        src_bmad = templates_dir / "bmad"
        if src_bmad.exists():
            target_bmad = Path("_bmad")
            shutil.copytree(src_bmad, target_bmad, dirs_exist_ok=True)
            console.print("[bold green]✓ Installed _bmad/ framework configuration[/bold green]")

    # 5. Git Tracking or Local Exclusion
    if co_ai:
        git_dir = Path(".git")
        if git_dir.exists() and git_dir.is_dir():
            exclude_file = git_dir / "info" / "exclude"
            exclude_file.parent.mkdir(parents=True, exist_ok=True)
            exclude_rules = """
# Personal FDE Co-AI Harness & BMAD (strictly local)
_bmad/
_bmad-output/
*.user.toml
.agent/
.agents/
.fde_evolution/
AGENTS.md
HARNESS.md
"""
            current_exclude = exclude_file.read_text(encoding="utf-8") if exclude_file.exists() else ""
            if "_bmad/" not in current_exclude:
                with exclude_file.open("a", encoding="utf-8") as f:
                    f.write(exclude_rules)
            console.print("[bold green]✓ Configured .git/info/exclude: FDE & BMAD hidden from client Git repo (zero client diff)[/bold green]")
        else:
            console.print("[bold yellow]! Warning: .git directory not found. Ensure .git/info/exclude is configured once git is initialized.[/bold yellow]")
    else:
        gitignore_file = Path(".gitignore")
        recommended_rules = """
# BMAD Framework (Core and skills are tracked for cross-repo portability; outputs are ignored)
_bmad-output/
*.user.toml

# FDE Harness Telemetry Cache
.test_fde_evolution/
"""
        if gitignore_file.exists():
            content = gitignore_file.read_text()
            # Clean up any lines ignoring _bmad or .agent
            lines = content.splitlines()
            filtered_lines = [
                line for line in lines
                if line.strip() not in ("_bmad/", ".agent/", ".agents/", "_bmad", ".agent", ".agents")
            ]
            new_content = "\n".join(filtered_lines)
            if "_bmad-output/" not in new_content:
                new_content += recommended_rules
            gitignore_file.write_text(new_content)
            console.print("[bold green]✓ Updated .gitignore to ensure BMAD skills remain tracked in Git[/bold green]")
        else:
            gitignore_file.write_text(f"""# Python & Environment
__pycache__/
*.pyc
.venv/
.env
{recommended_rules}
""")
            console.print("[bold green]✓ Created .gitignore with portable BMAD rules[/bold green]")

    # Final summary banner
    summary_table = Table(title="FDE Workspace Provisioning Complete", header_style="bold cyan")
    summary_table.add_column("Component", style="bold")
    summary_table.add_column("Status", style="green")
    summary_table.add_column("Details")

    summary_table.add_row("Client / Target", client, "Configured in runtime and governance")
    summary_table.add_row("Telemetry Store", "Active", ".fde_evolution/traces.jsonl initialized")
    summary_table.add_row("Agent Governance", "Installed", "AGENTS.md & HARNESS.md configured")
    if bmad:
        summary_table.add_row("BMAD Skills", f"{skills_installed} Ready", "Equipped in .agent/skills/ for AI coding assistants")
        summary_table.add_row("BMAD Config", "Installed", "_bmad/ framework core synced")
    
    if co_ai:
        summary_table.add_row("Git Tracking", "Local Only (Co-AI)", "Excluded in .git/info/exclude (clean client PRs)")
        next_panel_msg = (
            f"[bold green]Ready to solve problems for {client} with your local Co-AI![/bold green]\n\n"
            f"Next Steps:\n"
            f"1. Zero Client Footprint: All FDE & BMAD files are excluded locally in [cyan].git/info/exclude[/cyan].\n"
            f"2. Your client Git repo remains 100% clean with no foreign files in your pull requests.\n"
            f"3. Use with your AI agent: Ask [cyan]Antigravity[/cyan] or [cyan]Cursor[/cyan] to fix bugs or build features with [cyan]bmad-build[/cyan]."
        )
    else:
        summary_table.add_row("Git Tracking", "Configured", ".gitignore updated (BMAD un-ignored, outputs cached)")
        next_panel_msg = (
            f"[bold green]Ready to solve problems for {client}![/bold green]\n\n"
            f"Next Steps:\n"
            f"1. Commit the harness into your repo: [cyan]git add .agent _bmad AGENTS.md .gitignore && git commit -m 'feat: install FDE Harness + BMAD'[/cyan]\n"
            f"2. Decompose a client problem: [cyan]fde-harness decompose '<problem statement>'[/cyan]\n"
            f"3. Run with your AI agent: Ask [cyan]Antigravity[/cyan] or [cyan]Cursor[/cyan] to start the 7-phase cycle."
        )

    console.print("\n")
    console.print(summary_table)
    console.print(
        Panel(
            next_panel_msg,
            title="Installation Successful",
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

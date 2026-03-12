#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AGENCY CLI - Terminal Command Center                       ║
║                   Control your AI Agent Swarm from the Terminal               ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python agency-cli.py [COMMAND] [OPTIONS]

Commands:
    status          Show system status
    agents          List all available agents
    activate        Activate an agent
    deactivate      Deactivate an agent
    execute         Execute a task with an agent
    workflow        Run a workflow
    swarm           Execute a swarm of tasks
    autonomous      Control autonomous mode
    logs            View system logs
    dashboard       Launch interactive dashboard

Examples:
    python agency-cli.py status
    python agency-cli.py agents --division Engineering
    python agency-cli.py activate frontend-developer
    python agency-cli.py execute --agent content-creator --task "Write a blog post"
    python agency-cli.py workflow --file marketing-campaign.yaml
    python agency-cli.py autonomous start
"""

import asyncio
import json
import sys
from typing import Optional
from pathlib import Path

import typer
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich import box

# Add API to path
sys.path.insert(0, str(Path(__file__).parent / "api"))

from agents.agent_definitions import AGENT_DEFINITIONS, AGENT_BY_ID

app = typer.Typer(
    name="agency",
    help="🏢 Agency Management System CLI",
    rich_markup_mode="rich"
)
console = Console()

# Configuration
API_BASE_URL = "http://localhost:8000"


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def api_get(endpoint: str):
    """Make GET request to API."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}{endpoint}")
            return response.json()
        except Exception as e:
            console.print(f"[red]❌ API Error: {e}[/red]")
            return None


async def api_post(endpoint: str, data: dict = None):
    """Make POST request to API."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{API_BASE_URL}{endpoint}", json=data)
            return response.json()
        except Exception as e:
            console.print(f"[red]❌ API Error: {e}[/red]")
            return None


def get_division_color(division: str) -> str:
    """Get color for division."""
    colors = {
        "Engineering": "blue",
        "Marketing": "green",
        "Product": "magenta",
        "Testing": "yellow",
        "Support": "cyan",
        "Specialized": "red"
    }
    return colors.get(division, "white")


# ═══════════════════════════════════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════

@app.command()
def status(
    watch: bool = typer.Option(False, "--watch", "-w", help="Live status updates")
):
    """Show system status."""
    async def _show_status():
        data = await api_get("/api/v1/system/status")
        if not data:
            console.print("[red]❌ Could not connect to Agency API[/red]")
            console.print(f"[dim]Is the server running? Start with: python api/main.py[/dim]")
            return

        # Create status panel
        status_color = "green" if data["status"] == "healthy" else "red"
        
        console.print(Panel.fit(
            f"[bold {status_color}]{data['status'].upper()}[/bold {status_color}]\n"
            f"[dim]Uptime: {data['uptime']:.0f}s[/dim]",
            title="🏢 Agency System Status",
            border_style=status_color
        ))

        # Agents table
        agents_table = Table(title="Agents", box=box.ROUNDED)
        agents_table.add_column("Active", style="green", justify="right")
        agents_table.add_column("Total", style="cyan", justify="right")
        agents_table.add_row(
            str(data["active_agents"]),
            str(data["total_agents"])
        )
        console.print(agents_table)

        # Workflows table
        workflows_table = Table(title="Workflows", box=box.ROUNDED)
        workflows_table.add_column("Active", style="yellow", justify="right")
        workflows_table.add_column("Queue Depth", style="magenta", justify="right")
        workflows_table.add_row(
            str(data["active_workflows"]),
            str(data["queue_depth"])
        )
        console.print(workflows_table)

        # Metrics
        metrics = data.get("metrics", {})
        console.print(f"\n[bold]System Metrics:[/bold]")
        console.print(f"  CPU: {metrics.get('cpu_usage', 0):.1f}%")
        console.print(f"  Memory: {metrics.get('memory_usage', 0):.1f}%")
        console.print(f"  Timestamp: {data['timestamp']}")

    asyncio.run(_show_status())


@app.command()
def agents(
    division: Optional[str] = typer.Option(None, "--division", "-d", help="Filter by division"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
):
    """List all available agents."""
    filtered_agents = AGENT_DEFINITIONS
    
    if division:
        filtered_agents = [
            a for a in filtered_agents 
            if a["division"].lower() == division.lower()
        ]

    if json_output:
        console.print(json.dumps(filtered_agents, indent=2))
        return

    # Create table
    table = Table(
        title="🤖 Available Agents",
        box=box.DOUBLE_EDGE,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("ID", style="dim", width=25)
    table.add_column("Name", style="cyan", width=30)
    table.add_column("Division", style="green", width=15)
    table.add_column("Role", style="white", width=30)
    table.add_column("Status", style="yellow", width=10)

    for agent in filtered_agents:
        div_color = get_division_color(agent["division"])
        status = "🟢 Active" if agent.get("active", True) else "🔴 Inactive"
        
        table.add_row(
            agent["id"],
            agent["name"],
            f"[{div_color}]{agent['division']}[/{div_color}]",
            agent["personality"]["role"],
            status
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(filtered_agents)} agents[/dim]")


@app.command()
def agent(
    agent_id: str = typer.Argument(..., help="Agent ID to inspect"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON")
):
    """Show detailed information about an agent."""
    agent_data = AGENT_BY_ID.get(agent_id)
    
    if not agent_data:
        console.print(f"[red]❌ Agent '{agent_id}' not found[/red]")
        return

    if json_output:
        console.print(json.dumps(agent_data, indent=2))
        return

    # Display agent info
    p = agent_data["personality"]
    c = agent_data["capabilities"]
    
    console.print(Panel.fit(
        f"[bold cyan]{agent_data['name']}[/bold cyan]\n"
        f"[dim]{p['role']}[/dim]\n\n"
        f"[bold]Catchphrase:[/bold] \"{p['catchphrase']}\"\n\n"
        f"[bold]Description:[/bold] {c['description']}\n\n"
        f"[bold]Expertise:[/bold] {', '.join(p['expertise_areas'][:5])}\n\n"
        f"[bold]Skills:[/bold] {', '.join(c['skills'][:5])}\n\n"
        f"[bold]Tools:[/bold] {', '.join(c['tools'][:5])}\n\n"
        f"[dim]Model: {agent_data['model']} | Temp: {agent_data['temperature']}[/dim]",
        title=f"🤖 Agent: {agent_id}",
        border_style="blue"
    ))


@app.command()
def activate(
    agent_id: str = typer.Argument(..., help="Agent ID to activate")
):
    """Activate an agent."""
    async def _activate():
        result = await api_post(f"/api/v1/agents/{agent_id}/activate")
        if result:
            console.print(f"[green]✅ Activated agent: {agent_id}[/green]")
        else:
            console.print(f"[red]❌ Failed to activate agent: {agent_id}[/red]")
    
    asyncio.run(_activate())


@app.command()
def deactivate(
    agent_id: str = typer.Argument(..., help="Agent ID to deactivate")
):
    """Deactivate an agent."""
    async def _deactivate():
        result = await api_post(f"/api/v1/agents/{agent_id}/deactivate")
        if result:
            console.print(f"[yellow]🔴 Deactivated agent: {agent_id}[/yellow]")
        else:
            console.print(f"[red]❌ Failed to deactivate agent: {agent_id}[/red]")
    
    asyncio.run(_deactivate())


@app.command()
def execute(
    agent: str = typer.Option(..., "--agent", "-a", help="Agent ID to execute"),
    task: str = typer.Option(..., "--task", "-t", help="Task instruction"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="Additional context (JSON)")
):
    """Execute a task with an agent."""
    async def _execute():
        console.print(f"[blue]🤖 Executing task with {agent}...[/blue]")
        
        task_data = {
            "instruction": task,
            "input": {},
            "expected_output": "text"
        }
        
        ctx = json.loads(context) if context else {}
        
        payload = {
            "agent_id": agent,
            "task_data": task_data,
            "context": ctx,
            "priority": 5
        }
        
        result = await api_post("/api/v1/tasks/single", payload)
        
        if result:
            console.print(Panel(
                result.get("output", "No output"),
                title=f"✅ Task Complete ({result.get('execution_time', 0):.2f}s)",
                border_style="green"
            ))
        else:
            console.print("[red]❌ Task execution failed[/red]")
    
    asyncio.run(_execute())


@app.command()
def workflow(
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Workflow YAML file"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Workflow name"),
    list_workflows: bool = typer.Option(False, "--list", "-l", help="List available workflows")
):
    """Execute or manage workflows."""
    async def _workflow():
        if list_workflows:
            workflows = await api_get("/api/v1/workflows")
            if workflows:
                table = Table(title="📋 Workflows")
                table.add_column("Name")
                table.add_column("Description")
                for wf in workflows:
                    table.add_row(wf["name"], wf["description"][:50] + "...")
                console.print(table)
            return
        
        # Execute workflow
        console.print(f"[blue]🚀 Starting workflow...[/blue]")
        # Implementation would load workflow from file and execute
        console.print("[yellow]⚠️ Workflow execution from file not yet implemented[/yellow]")
    
    asyncio.run(_workflow())


@app.command()
def swarm(
    agents_str: str = typer.Option(..., "--agents", help="Comma-separated agent IDs"),
    task: str = typer.Option(..., "--task", "-t", help="Task for each agent"),
    parallel: bool = typer.Option(True, "--parallel/--sequential", help="Execute in parallel")
):
    """Execute a task with multiple agents (swarm)."""
    async def _swarm():
        agent_ids = [a.strip() for a in agents_str.split(",")]
        
        console.print(f"[blue]🐝 Initiating swarm with {len(agent_ids)} agents...[/blue]")
        
        tasks = []
        for agent_id in agent_ids:
            tasks.append({
                "agent_id": agent_id,
                "task_data": {"instruction": task},
                "context": {},
                "priority": 5
            })
        
        result = await api_post("/api/v1/tasks/swarm", tasks)
        
        if result:
            console.print(f"[green]✅ Swarm initiated: {result.get('swarm_id')}[/green]")
            console.print(f"[dim]Tasks queued: {result.get('task_count')}[/dim]")
        else:
            console.print("[red]❌ Swarm execution failed[/red]")
    
    asyncio.run(_swarm())


@app.command()
def autonomous(
    action: str = typer.Argument(..., help="Action: start, stop, status"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Config JSON")
):
    """Control autonomous execution mode."""
    async def _autonomous():
        if action == "start":
            cfg = json.loads(config) if config else {}
            result = await api_post("/api/v1/autonomous/start", cfg)
            if result:
                console.print("[green]🤖 AUTONOMOUS MODE ACTIVATED[/green]")
            else:
                console.print("[red]❌ Failed to start autonomous mode[/red]")
        
        elif action == "stop":
            result = await api_post("/api/v1/autonomous/stop")
            if result:
                console.print("[yellow]🛑 AUTONOMOUS MODE DEACTIVATED[/yellow]")
        
        elif action == "status":
            result = await api_get("/api/v1/autonomous/status")
            if result:
                status = "🟢 ACTIVE" if result.get("enabled") else "🔴 INACTIVE"
                console.print(f"Autonomous Mode: {status}")
                console.print(f"Running: {result.get('running')}")
                if result.get("decision_history_count"):
                    console.print(f"Decisions made: {result['decision_history_count']}")
        
        else:
            console.print(f"[red]❌ Unknown action: {action}[/red]")
    
    asyncio.run(_autonomous())


@app.command()
def dashboard():
    """Launch interactive terminal dashboard."""
    console.print("[yellow]⚠️ Interactive dashboard requires Textual[/yellow]")
    console.print("[dim]Install with: pip install textual[/dim]")
    console.print("\n[blue]Launching simple live dashboard...[/blue]")
    
    async def _dashboard():
        with Live(refresh_per_second=2) as live:
            while True:
                data = await api_get("/api/v1/system/status")
                if data:
                    layout = Layout()
                    # Simplified display
                    content = f"""
🏢 Agency System Status: {'[green]HEALTHY[/green]' if data['status'] == 'healthy' else '[red]ERROR[/red]'}

Agents: {data['active_agents']}/{data['total_agents']} active
Workflows: {data['active_workflows']} active | Queue: {data['queue_depth']}

Press Ctrl+C to exit
                    """
                    live.update(Panel(content, title="Agency Dashboard"))
                await asyncio.sleep(2)
    
    try:
        asyncio.run(_dashboard())
    except KeyboardInterrupt:
        console.print("\n[dim]Dashboard closed[/dim]")


@app.command()
def quickstart():
    """Quick start guide."""
    guide = """
[bold cyan]🏢 Agency Management System - Quick Start[/bold cyan]

[bold]1. Start the API Server:[/bold]
   cd api && python main.py

[bold]2. Check System Status:[/bold]
   python agency-cli.py status

[bold]3. List Available Agents:[/bold]
   python agency-cli.py agents

[bold]4. Execute a Task:[/bold]
   python agency-cli.py execute -a content-creator -t "Write a blog post about AI"

[bold]5. Run Agent Swarm:[/bold]
   python agency-cli.py swarm --agents content-creator,growth-hacker -t "Create marketing campaign"

[bold]6. Enable Autonomous Mode:[/bold]
   python agency-cli.py autonomous start

[bold]7. View Agent Details:[/bold]
   python agency-cli.py agent frontend-developer

[bold]Useful Flags:[/bold]
   --json, -j     Output as JSON
   --watch, -w    Live updates
   --help         Show detailed help

[dim]For more information: python agency-cli.py --help[/dim]
    """
    console.print(guide)


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show version")
):
    """🏢 Agency Management System CLI - Control your AI Agent Swarm"""
    if version:
        console.print("[bold]Agency CLI[/bold] version 1.0.0")
        raise typer.Exit()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app()

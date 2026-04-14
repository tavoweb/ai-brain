import os
import click
from datetime import datetime
from rich.prompt import Prompt

from ai_brain.utils.display import console, print_header, print_success, print_error, print_info, create_table, render_table, print_markdown
from ai_brain.core.brain_manager import initialize_project
from ai_brain.core.graph_engine import scan_directory
from ai_brain.core.snapshot_service import create_snapshot
from ai_brain.core.context_generator import generate_context_string
from ai_brain.storage.local_state import save_graph, add_history_entry, is_initialized
from ai_brain.storage.db import get_all_projects, update_last_synced

@click.group()
def cli():
    """🧠 AI-Brain: Persistent Long-Term Memory for projects."""
    pass

@cli.command()
@click.option('--name', prompt='Project name', help='Name of the project to initialize')
def init(name: str):
    """Initialize ai-brain in the current folder."""
    print_header()
    cwd = os.getcwd()
    initialize_project(cwd, name)

@cli.command()
def sync():
    """Scan current files, update the graph, and ask for a session summary."""
    print_header()
    cwd = os.getcwd()
    
    if not is_initialized(cwd):
        print_error("Project not initialized. Run 'aib init' first.")
        return
        
    print_info("Scanning directory graph...")
    graph = scan_directory(cwd)
    save_graph(cwd, graph)
    
    summary = Prompt.ask("[bold cyan]Please provide a brief session summary[/bold cyan]")
    now = datetime.now().isoformat()
    
    add_history_entry(cwd, now, summary)
    update_last_synced(cwd)
    
    print_success("Project state synchronized.")

@cli.command()
def backup():
    """Create a compressed snapshot of the current state."""
    print_header()
    cwd = os.getcwd()
    
    if not is_initialized(cwd):
        print_error("Project not initialized. Run 'aib init' first.")
        return
        
    print_info("Creating snapshot...")
    create_snapshot(cwd)

def _safe_print_context(context):
    """Try to print context, fallback to ASCII-only if encoding fails."""
    try:
        console.print(context, highlight=False, markup=False)
    except UnicodeEncodeError:
        # Fallback: strip all non-ASCII
        safe_context = "".join(c for c in context if ord(c) < 128)
        console.print(safe_context, highlight=False, markup=False)

@cli.command()
def inject():
    """Output a formatted Markdown block containing project context."""
    print_header()
    cwd = os.getcwd()
    
    if not is_initialized(cwd):
        print_error("Project not initialized. Run 'aib init' first.")
        return
        
    context = generate_context_string(cwd)
    
    print_info("=== START CONTEXT STRING ===\n")
    _safe_print_context(context)
    print("\n")
    print_info("=== END CONTEXT STRING ===")

@cli.command()
def analyze():
    """Deep scan to generate descriptions for files and directories."""
    print_header()
    cwd = os.getcwd()
    
    if not is_initialized(cwd):
        print_error("Project not initialized. Run 'aib init' first.")
        return
        
    print_info("Analyzing project structure and extracting descriptions...")
    graph = scan_directory(cwd, deep_scan=True)
    save_graph(cwd, graph)
    
    print_success("Project analysis complete. Descriptions saved.")

def _create_rule_files(project_root):
    """Create AI instruction files (.cursorrules, .clauderules, AI_INSTRUCTIONS.md)."""
    rules_content = """# AI-Brain Rules for AI Assistants

This project uses AI-Brain for persistent project context. 
Before analyzing the project or starting a large task:

1. Locate and read `.ai-brain/graph.json` to understand the current symbol map.
2. If context drift occurs, ask the user to run `aib inject` and paste the result.
3. This project categorizes logic into [MODELS], [CTRLS], [SERVICES], and [HELPERS]. Use the Symbol Map to find specific logic.
4. When you finish a task, remind the user to run `aib sync` to update the project history.
"""
    
    files = [".cursorrules", ".clauderules", "AI_INSTRUCTIONS.md"]
    created = []
    
    for filename in files:
        path = os.path.join(project_root, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(rules_content)
        created.append(filename)
    
    return created

@cli.command()
def rules():
    """Generate instruction files for AI assistants (Cursor, Claude, etc.)"""
    print_header()
    cwd = os.getcwd()
    
    if not is_initialized(cwd):
        print_error("Project not initialized. Run 'aib init' first.")
        return
        
    print_info("Generating AI instruction files...")
    created_files = _create_rule_files(cwd)
    
    for f in created_files:
        print_success(f"Created {f}")
    
    print("\n")
    print_info("These files will help AI assistants recognize AI-Brain structures automatically.")

@cli.command()
def list():
    """Show all projects managed by ai-brain."""
    print_header()
    projects = get_all_projects()
    
    if not projects:
        print_info("No projects found in global registry.")
        return
        
    table = create_table("Tracked Projects", "Name", "Path", "Last Synced")
    
    for p in projects:
        # Simplistic date parsing to make it readable
        try:
            last_synced = datetime.fromisoformat(p["last_synced_at"]).strftime("%Y-%m-%d %H:%M:%S")
        except:
            last_synced = p["last_synced_at"]
            
        table.add_row(p["name"], p["path"], last_synced)
        
    render_table(table)

if __name__ == '__main__':
    cli()

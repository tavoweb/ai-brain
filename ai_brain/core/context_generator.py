import json
from ai_brain.storage.local_state import load_config, load_history, load_graph

def _format_tree(node: dict, indent=""):
    """Format the graph tree into a string."""
    result = ""
    for key, val in node.items():
        if isinstance(val, dict):
            result += f"{indent}📂 {key}/\n"
            result += _format_tree(val, indent + "  ")
        else:
            result += f"{indent}📄 {key}\n"
    return result

def generate_context_string(project_root: str) -> str:
    """Generate Markdown representation of project state."""
    config = load_config(project_root)
    history = load_history(project_root)
    graph = load_graph(project_root)
    
    if not config:
        return "Error: Project not found or initialized."

    lines = [
        f"# AI-Brain Context: {config.get('project_name', 'Unknown')}",
        "This is an auto-generated context summary. Use this to catch up on the project state.\n",
        f"**Initialized At:** {config.get('initialized_at', 'Unknown')}",
        "",
        "## Recent History",
        "*(Chronological Session Summaries)*"
    ]
    
    if not history:
        lines.append("- No history recorded yet.")
    else:
        # Show only last 5 entries for brevity
        for entry in history[-5:]:
            lines.append(f"- **{entry['timestamp']}**: {entry['summary']}")
            
    lines.extend([
        "",
        "## Overall Project Architecture",
        "```",
        _format_tree(graph) if graph else "(Empty or un-synced project)",
        "```"
    ])
    
    return "\n".join(lines)

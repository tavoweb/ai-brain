import json
from ai_brain.storage.local_state import load_config, load_history, load_graph

def _format_tree(node: dict, indent=""):
    """Format the graph tree into a string with descriptions."""
    result = ""
    # In the new structure, children are under the "children" key
    children = node.get("children", {})
    
    # Sort children to show directories first, then files
    sorted_items = sorted(children.items(), key=lambda item: (item[1].get("_type") != "directory", item[0]))

    for name, metadata in sorted_items:
        _type = metadata.get("_type", "file")
        _desc = metadata.get("_desc", "")
        
        desc_str = f" - {(_desc[:100] + '...') if len(_desc) > 100 else _desc}" if _desc and _desc not in ["File", "Directory"] else ""

        if _type == "directory":
            result += f"{indent}[DIR] {name}/{desc_str}\n"
            result += _format_tree(metadata, indent + "  ")
        else:
            result += f"{indent}[FILE] {name}{desc_str}\n"
            
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

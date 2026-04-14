import json
from ai_brain.storage.local_state import load_config, load_history, load_graph

def _to_ascii(text: str) -> str:
    """Helper to ensure a string only contains ASCII characters."""
    if not text:
        return ""
    # Filter out any characters with ordinal value >= 128
    return "".join(c for c in text if ord(c) < 128)

def _extract_all_symbols(node: dict, path_acc="") -> list:
    """Recursively extracts all symbols and their categories from the graph."""
    symbols_flat = []
    children = node.get("children", {})
    
    for name, metadata in children.items():
        current_path = f"{path_acc}/{name}" if path_acc else name
        _type = metadata.get("_type", "file")
        
        if _type == "directory":
            symbols_flat.extend(_extract_all_symbols(metadata, current_path))
        else:
            file_symbols = metadata.get("_symbols", [])
            category = metadata.get("_category", "other")
            desc = metadata.get("_desc", "")
            
            symbols_flat.append({
                "path": current_path,
                "name": name,
                "desc": desc,
                "symbols": file_symbols,
                "category": category
            })
            
    return symbols_flat

def _render_compact_list(files: list) -> str:
    """Renders a list of files as a compact comma-separated string."""
    if not files:
        return ""
    names = [f"`{f['name']}`" for f in files]
    return ", ".join(names)

def generate_symbol_map(graph: dict) -> str:
    """Generates a structured Markdown symbol map with stats and compact categories."""
    all_files = _extract_all_symbols(graph)
    
    categories = {
        "models": {"name": "Domain Models & Core Logic", "icon": "[MODELS]", "files": [], "priority": 1},
        "controllers": {"name": "Controllers & API Endpoints", "icon": "[CTRLS]", "files": [], "priority": 2},
        "services": {"name": "Services & Integrations", "icon": "[SERVICES]", "files": [], "priority": 2},
        "helpers": {"name": "Helpers & Utils", "icon": "[HELPERS]", "files": [], "priority": 3},
        "security": {"name": "Security & Middleware", "icon": "[SECURITY]", "files": [], "priority": 3},
        "other": {"name": "Other Files", "icon": "[OTHER]", "files": [], "priority": 4}
    }
    
    total_symbols = 0
    for f in all_files:
        cat = f["category"]
        if cat in categories:
            categories[cat]["files"].append(f)
        else:
            categories["other"]["files"].append(f)
        total_symbols += len(f["symbols"])
            
    output = []
    
    # Summary Table
    output.append("## [SUMMARY] Project Overview")
    output.append(f"| Category | Files |")
    output.append(f"| :--- | :--- |")
    for cat_id, cat_info in categories.items():
        if cat_info["files"]:
            output.append(f"| {cat_info['name']} | {len(cat_info['files'])} |")
    output.append(f"| **Total Symbols** | **{total_symbols}** |")
    output.append("")

    # Process each category
    for cat_id, cat_info in categories.items():
        if not cat_info["files"]:
            continue
            
        output.append(f"## {cat_info['icon']} {cat_info['name']}")
        output.append("")
        
        with_symbols = [f for f in cat_info["files"] if f["symbols"]]
        no_symbols = [f for f in cat_info["files"] if not f["symbols"]]
        
        # Priority categories or files with symbols get detailed view
        for f in with_symbols:
            output.append(f"### `{f['name']}` ({f['path']})")
            if f["desc"] and f["desc"] not in ["File", "Unknown file"]:
                output.append(f"*{f['desc']}*")
            
            for sym in f["symbols"]:
                sym_type_char = "+" if sym["type"] == "class" else "-"
                output.append(f"  {sym_type_char} **`{sym['name']}`** ({sym['type']}): {sym['description']}")
            output.append("")
        
        # Low priority category or files without symbols get compact view
        if no_symbols:
            if cat_info["priority"] >= 3:
                output.append(f"**Other files:** {_render_compact_list(no_symbols)}")
            else:
                # Still show as bullets for models/controllers but without extra lines
                for f in no_symbols:
                    desc = f": {f['desc']}" if f["desc"] and f["desc"] not in ["File", "Unknown file"] else ""
                    output.append(f"* `{f['name']}` ({f['path']}){desc}")
        
        output.append("")
        output.append("---")
        
    return "\n".join(output)

def generate_context_string(project_root: str) -> str:
    """Generate Markdown representation of project state."""
    config = load_config(project_root)
    history = load_history(project_root)
    graph = load_graph(project_root)
    
    if not config:
        return "Error: Project not found or initialized."

    project_name = _to_ascii(config.get('project_name', 'Unknown'))
    
    lines = [
        f"# AI-Brain Passport: {project_name}",
        "This is a condensed project context summary for AI Assistants.\n",
        f"**Project Root:** `{project_root}`",
        f"**Initialized:** {config.get('initialized_at', 'Unknown')}",
        "",
        "## Recent History",
        "*(Review most recent changes)*"
    ]
    
    if not history:
        lines.append("- No recorded history yet.")
    else:
        for entry in history[-3:]: # Only last 3 for brevity
            safe_summary = _to_ascii(entry.get('summary', ''))
            lines.append(f"- **{entry['timestamp']}**: {safe_summary}")
            
    lines.extend([
        "",
        "# Symbol Map & Logic Index",
        "",
        generate_symbol_map(graph) if graph else "(Empty or un-synced project)"
    ])
    
    return "\n".join(lines)

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
            
            # Special case: migrations and tests are usually too noisy to highlight
            if "database/migrations" in current_path or "tests/" in current_path or "temp_backup" in current_path:
                category = "other"
                file_symbols = [] # Clear symbols to prevent highlighting
            
            symbols_flat.append({
                "path": current_path,
                "name": name,
                "desc": desc,
                "symbols": file_symbols,
                "category": category
            })
            
    return symbols_flat

def _render_compact_list(files: list, chunk_size: int = 10, max_files: int = 30) -> str:
    """Renders a list of files as compact comma-separated chunks with a hard limit."""
    if not files:
        return ""
    
    total_count = len(files)
    to_show = files[:max_files]
    names = [f"`{f['name']}`" for f in to_show]
    
    # Split names into chunks for better readability in terminal
    chunks = [names[i:i + chunk_size] for i in range(0, len(names), chunk_size)]
    output = "\n".join([", ".join(chunk) for chunk in chunks])
    
    if total_count > max_files:
        output += f"\n... and {total_count - max_files} more files."
    
    return output

def generate_symbol_map(graph: dict) -> str:
    """Generates a structured Markdown symbol map with strict limits and noise reduction."""
    all_files = _extract_all_symbols(graph)
    
    categories = {
        "models": {"name": "Domain Models & Core Logic", "icon": "[MODELS]", "files": [], "priority": 1, "can_detail": True},
        "controllers": {"name": "Controllers & API Endpoints", "icon": "[CTRLS]", "files": [], "priority": 2, "can_detail": True},
        "services": {"name": "Services & Integrations", "icon": "[SERVICES]", "files": [], "priority": 2, "can_detail": True},
        "helpers": {"name": "Helpers & Utils", "icon": "[HELPERS]", "files": [], "priority": 3, "can_detail": False},
        "security": {"name": "Security & Middleware", "icon": "[SECURITY]", "files": [], "priority": 3, "can_detail": False},
        "other": {"name": "Other Files", "icon": "[OTHER]", "files": [], "priority": 4, "can_detail": False}
    }
    
    total_symbols = 0
    for f in all_files:
        cat = f["category"]
        # Ensure category exists or fallback to other
        if cat not in categories:
            cat = "other"
            
        categories[cat]["files"].append(f)
        total_symbols += len(f["symbols"])
            
    output = []
    
    # Summary Table
    output.append("## [SUMMARY] Project Overview")
    output.append(f"| Category | Files | Highlighted |")
    output.append(f"| :--- | :--- | :--- |")
    for cat_id, cat_info in categories.items():
        if cat_info["files"]:
            # A file is "highlighted" if it has symbols AND is in a detail-enabled category
            highlighted_count = len([f for f in cat_info["files"] if f["symbols"] and cat_info["can_detail"]])
            output.append(f"| {cat_info['name']} | {len(cat_info['files'])} | {highlighted_count} |")
    output.append(f"| **Total Symbols** | **{total_symbols}** | - |")
    output.append("")

    # Global limit to total detailed files across the whole report
    MAX_GLOBAL_DETAILED = 30
    global_detailed_count = 0

    # Process each category
    for cat_id, cat_info in categories.items():
        if not cat_info["files"]:
            continue
            
        output.append(f"## {cat_info['icon']} {cat_info['name']}")
        output.append("")
        
        # Decide which files get "Detailed View"
        with_symbols = [f for f in cat_info["files"] if f["symbols"] and cat_info["can_detail"]]
        no_symbols = [f for f in cat_info["files"] if f not in with_symbols]
        
        # Limit how many detailed files we show in this category
        CAT_FILE_LIMIT = 10
        to_detail = []
        
        for f in with_symbols:
            if global_detailed_count < MAX_GLOBAL_DETAILED and len(to_detail) < CAT_FILE_LIMIT:
                to_detail.append(f)
                global_detailed_count += 1
            else:
                no_symbols.append(f) # Move to compact list

        for f in to_detail:
            output.append(f"### `{f['name']}` ({f['path']})")
            if f["desc"] and f["desc"] not in ["File", "Unknown file"]:
                output.append(f"*{f['desc']}*")
            
            # Limit symbols per file to 10
            SYM_LIMIT = 10
            for sym in f["symbols"][:SYM_LIMIT]:
                sym_type_char = "+" if sym["type"] == "class" else "-"
                output.append(f"  {sym_type_char} **`{sym['name']}`** ({sym['type']}): {sym['description']}")
            
            if len(f["symbols"]) > SYM_LIMIT:
                output.append(f"  ... and {len(f['symbols']) - SYM_LIMIT} more symbols.")
            
            output.append("")
        
        if no_symbols:
            if not to_detail or len(no_symbols) > 5:
                output.append(f"**Other files recorded:**")
                output.append(_render_compact_list(no_symbols))
            else:
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
        for entry in history[-3:]: 
            safe_summary = _to_ascii(entry.get('summary', ''))
            lines.append(f"- **{entry['timestamp']}**: {safe_summary}")
            
    lines.extend([
        "",
        "# Symbol Map & Logic Index",
        "",
        generate_symbol_map(graph) if graph else "(Empty or un-synced project)"
    ])
    
    return "\n".join(lines)

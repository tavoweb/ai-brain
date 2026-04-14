import os
from pathlib import Path
from ai_brain.core.analyzer import extract_file_description, get_directory_description

# Directories and files that should never be scanned
IGNORED_DIRS = {".git", "node_modules", "venv", "__pycache__", "backups", ".ai-brain", ".idea", ".vscode", ".venv"}
IGNORED_FILES = {".DS_Store", "global.db", "__init__.py"}

def scan_directory(project_root: str, deep_scan: bool = False) -> dict:
    """
    Recursively scan directory to build a graph.
    If deep_scan is True, it will read file contents to generate descriptions.
    """
    base_path = Path(project_root)
    # The root of the graph
    graph = {
        "_type": "directory",
        "_desc": get_directory_description(base_path.name) if deep_scan else "Project root",
        "children": {}
    }
    
    for dirpath, dirnames, filenames in os.walk(base_path):
        # Exclude directories in-place to avoid traversing them
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        
        rel_path = Path(dirpath).relative_to(base_path)
        
        # Traverse to the correct node in the graph
        current_node = graph
        if rel_path != Path('.'):
            for part in rel_path.parts:
                if part not in current_node["children"]:
                    current_node["children"][part] = {
                        "_type": "directory",
                        "_desc": get_directory_description(part) if deep_scan else "Directory",
                        "children": {}
                    }
                current_node = current_node["children"][part]
        
        # Add files to the current directory node
        for f in filenames:
            if f not in IGNORED_FILES:
                file_path = Path(dirpath) / f
                current_node["children"][f] = {
                    "_type": "file",
                    "_desc": extract_file_description(file_path) if deep_scan else "File"
                }
                
    return graph

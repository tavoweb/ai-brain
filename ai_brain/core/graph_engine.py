import os
from pathlib import Path

IGNORED_DIRS = {".git", "node_modules", "venv", "__pycache__", "backups", ".ai-brain", ".idea", ".vscode"}
IGNORED_FILES = {".DS_Store", "global.db"}

def scan_directory(project_root: str) -> dict:
    """Recursively scan directory to build a graph, ignoring standard excludes."""
    graph = {}
    base_path = Path(project_root)
    
    for dirpath, dirnames, filenames in os.walk(base_path):
        # Exclude directories in-place to avoid traversing them
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        
        current_node = graph
        rel_path = Path(dirpath).relative_to(base_path)
        
        if rel_path == Path('.'):
            # We are at the root
            pass
        else:
            # Traverse to the correct dictionary depth
            for part in rel_path.parts:
                if part not in current_node:
                    current_node[part] = {}
                current_node = current_node[part]
        
        # Add files as keys with None (or minimal metadata)
        for f in filenames:
            if f not in IGNORED_FILES:
                current_node[f] = "file"
                
    return graph

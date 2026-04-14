import os
from pathlib import Path
from ai_brain.core.analyzer import extract_file_metadata, get_directory_description

# Directories and files that should never be scanned
IGNORED_DIRS = {
    ".git", "node_modules", "vendor", "storage", "backups", "dist", "build", 
    ".ai-brain", ".idea", ".vscode", ".venv", "venv", "__pycache__", 
    ".next", "out", "public/build", "temp_backup", "temp", "tmp", "logs", "cache",
    "bower_components"
}
IGNORED_FILES = {".DS_Store", "global.db", "__init__.py"}

def scan_directory(project_root: str, deep_scan: bool = False) -> dict:
    """
    Recursively scan directory to build a graph.
    If deep_scan is True, it will read file contents to generate metadata.
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
                if deep_scan:
                    metadata = extract_file_metadata(file_path)
                    current_node["children"][f] = {
                        "_type": "file",
                        "_desc": metadata["description"],
                        "_symbols": metadata["symbols"],
                        "_category": metadata["category"]
                    }
                else:
                    current_node["children"][f] = {
                        "_type": "file",
                        "_desc": "File"
                    }
                
    return graph

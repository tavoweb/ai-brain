import os
from datetime import datetime
from ai_brain.storage.db import init_db, register_project
from ai_brain.storage.local_state import init_local_state, is_initialized
from ai_brain.utils.display import print_success, print_error, print_info

def initialize_project(project_path: str, project_name: str) -> bool:
    """Initialize AI-Brain in the current directory."""
    if is_initialized(project_path):
        print_error(f"Project already initialized at {project_path}")
        return False

    now = datetime.now().isoformat()
    
    # Init global DB if not exists
    init_db()
    
    # Register in global DB
    register_project(project_name, project_path)
    
    # Setup local state (.ai-brain dir)
    init_local_state(project_path, project_name, now)
    
    print_success(f"Initialized AI-Brain project '{project_name}'.")
    print_info("Use 'aib sync' to scan your project files.")
    return True

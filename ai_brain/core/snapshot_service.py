import os
import zipfile
from pathlib import Path
from datetime import datetime
from ai_brain.utils.display import print_success, print_error

IGNORED_DIRS = {".git", "node_modules", "venv", "__pycache__", "backups"}

def create_snapshot(project_root: str) -> str:
    """Creates a zip snapshot of the directory."""
    backups_dir = Path(project_root) / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = backups_dir / f"snapshot_{timestamp}.zip"
    
    base_path = Path(project_root)
    file_count = 0
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dirpath, dirnames, filenames in os.walk(base_path):
                # We do NOT include the backups directory in the backup
                dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
                
                for f in filenames:
                    file_path = Path(dirpath) / f
                    rel_path = file_path.relative_to(base_path)
                    zipf.write(file_path, arcname=rel_path)
                    file_count += 1
                    
        print_success(f"Snapshot created successfully: {zip_filename.name} ({file_count} files)")
        return str(zip_filename)
        
    except Exception as e:
        print_error(f"Failed to create snapshot: {e}")
        if zip_filename.exists():
            zip_filename.unlink()
        return ""

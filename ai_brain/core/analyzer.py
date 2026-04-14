import os
from pathlib import Path

def extract_file_description(file_path: Path) -> str:
    """Attempts to extract a brief description from a file's header or docstring."""
    ext = file_path.suffix.lower()
    
    try:
        # Read first few lines of the file
        content_lines = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(10):  # Check first 10 lines
                line = f.readline()
                if not line:
                    break
                # Remove non-ASCII characters that cause trouble in some terminals
                sanitized_line = "".join(c for c in line.strip() if ord(c) < 128)
                if sanitized_line:
                    content_lines.append(sanitized_line)
        
        if not content_lines:
            return f"{ext[1:].upper() if ext else 'Unknown'} file"

        # Python-specific extraction (docstrings)
        if ext == ".py":
            full_content = "\n".join(content_lines)
            if '"""' in full_content:
                parts = full_content.split('"""')
                if len(parts) > 1:
                    return parts[1].split('"""')[0].strip().replace("\n", " ")
            # Fallback to first comment
            for line in content_lines:
                if line.startswith("#"):
                    return line.lstrip("#").strip()
        
        # JS/TS/CSS/PHP specific extraction
        if ext in [".js", ".ts", ".css", ".php"]:
            for line in content_lines:
                if line.startswith("//"):
                    return line.lstrip("/").strip()
                if "/*" in line:
                    desc = line.split("/*")[1].split("*/")[0].strip()
                    if desc: return desc
        
        # Markdown extraction
        if ext == ".md":
            for line in content_lines:
                if line.startswith("#"):
                    return line.lstrip("#").strip()
                if line:
                    return line[:100]  # First non-empty line
        
        # Generic fallback
        for line in content_lines:
            if line and not line.startswith(("import", "from", "package", "using")):
                return line[:80] + ("..." if len(line) > 80 else "")

    except Exception:
        pass
        
    return f"{ext[1:].upper() if ext else 'Unknown'} file"

def get_directory_description(dir_name: str) -> str:
    """Provides a description for a directory based on common naming conventions."""
    common_dirs = {
        "src": "Source code for the main application",
        "core": "Core logic, services, and business rules",
        "utils": "Utility functions and helper classes",
        "storage": "Data persistence and state management",
        "tests": "Unit and integration tests",
        "docs": "Documentation and project guides",
        "assets": "Static assets like images or styles",
        "scripts": "Automation and maintenance scripts",
        "api": "API endpoints and route handlers",
        "components": "Reusable UI components",
        "models": "Data models and structures",
        "controllers": "Request handlers and logic flow"
    }
    return common_dirs.get(dir_name.lower(), "Project directory")

import os
import re
from pathlib import Path

def _to_ascii(text: str) -> str:
    """Helper to ensure a string only contains ASCII characters for terminal compatibility."""
    if not text:
        return ""
    # Filter out any characters with ordinal value >= 128
    return "".join(c for c in text if ord(c) < 128)

def extract_file_metadata(file_path: Path) -> dict:
    """
    Extracts description and symbols (classes, functions) from a file.
    Returns: { "description": str, "symbols": list, "category": str }
    """
    ext = file_path.suffix.lower()
    metadata = {
        "description": "",
        "symbols": [],
        "category": categorize_path(file_path)
    }
    
    # Noise words and license markers to skip for general description
    skip_keywords = {
        "<?php", "namespace", "use", "class", "interface", "trait", 
        "abstract class", "public", "private", "protected", "@package", "@author", 
        "The MIT License", "import ", "from ", "require ", "include "
    }
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            
        # 1. Extract general description (heuristic from the first 100 lines)
        desc_found = False
        for i in range(min(100, len(lines))):
            line = lines[i].strip()
            # Strict ASCII sanitization
            cleaned = _to_ascii(line).lstrip("/*# \t-")
            
            if not cleaned or any(k.lower() in cleaned.lower() for k in skip_keywords):
                continue
                
            if len(cleaned) > 5 and cleaned[0].isalpha():
                metadata["description"] = cleaned[:100] + ("..." if len(cleaned) > 100 else "")
                desc_found = True
                break
        
        if not desc_found:
            metadata["description"] = f"{ext[1:].upper() if ext else 'Unknown'} file"

        # 2. Extract Symbols (Classes and Functions)
        patterns = {
            ".php": [
                (r'class\s+([a-zA-Z0-9_]+)', "class"),
                (r'function\s+([a-zA-Z0-9_]+)', "function"),
                (r'trait\s+([a-zA-Z0-9_]+)', "trait"),
                (r'interface\s+([a-zA-Z0-9_]+)', "interface")
            ],
            ".py": [
                (r'class\s+([a-zA-Z0-9_]+)', "class"),
                (r'def\s+([a-zA-Z0-9_]+)', "function")
            ],
            ".js": [
                (r'class\s+([a-zA-Z0-9_]+)', "class"),
                (r'function\s+([a-zA-Z0-9_]+)', "function"),
                (r'const\s+([a-zA-Z0-9_]+)\s*=\s*\(.*?\)\s*=>', "function")
            ],
            ".ts": [
                (r'class\s+([a-zA-Z0-9_]+)', "class"),
                (r'function\s+([a-zA-Z0-9_]+)\s*\(', "function"),
                (r'interface\s+([a-zA-Z0-9_]+)', "interface")
            ]
        }

        if ext in patterns:
            for i, line in enumerate(lines):
                for pattern, sym_type in patterns[ext]:
                    match = re.search(pattern, line)
                    if match:
                        name = _to_ascii(match.group(1))
                        
                        # Try to find a docblock or meaningful comment before this line
                        sym_desc = ""
                        code_keywords = {
                            "return", "public", "private", "protected", "if ", "else", 
                            "while", "for ", "foreach", "switch", "case", "break", 
                            "continue", "echo", "print", "{", "}", "<?php", "namespace", "use "
                        }
                        
                        for j in range(i-1, max(-1, i-7), -1):
                            prev_line = _to_ascii(lines[j]).strip().lstrip("/*# \t-")
                            
                            # Skip empty lines or lines that look like code
                            if not prev_line:
                                continue
                            
                            if any(k in prev_line.lower() for k in code_keywords):
                                continue
                                
                            if prev_line[0].isalpha() or prev_line.startswith("@"):
                                sym_desc = prev_line[:80]
                                break
                        
                        metadata["symbols"].append({
                            "name": name,
                            "type": sym_type,
                            "description": sym_desc
                        })

    except Exception:
        pass
        
    return metadata

def categorize_path(file_path: Path) -> str:
    """Categorizes a file based on its path and naming conventions."""
    path_str = str(file_path).lower()
    
    if "helpers" in path_str or "utils" in path_str or "functions" in path_str:
        return "helpers"
    if "controllers" in path_str or "api/" in path_str:
        return "controllers"
    if "models" in path_str or "classes" in path_str or "entities" in path_str or "core" in path_str:
        return "models"
    if "services" in path_str or "scrapers" in path_str or "integrations" in path_str or "scripts" in path_str:
        return "services"
    if "middleware" in path_str or "auth" in path_str or "rate_limit" in path_str:
        return "security"
    
    return "other"

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
        "controllers": "Request handlers and logic flow",
        "events": "Internal application events and listeners",
        "filesystem": "Local and cloud file systems management",
        "http": "HTTP kernels, middlewares, and requests handling",
        "middleware": "Request intermediaries and filters",
        "routing": "URL registration and request dispatching",
        "database": "Migrations, seeds, and database managers",
        "translation": "Localization and translations",
        "validation": "Data validation rules and logic",
        "notifications": "Multi-channel notifications (mail, slack, database)",
        "auth": "Authentication and authorization logic",
        "command": "CLI commands and terminal interactions",
        "config": "Project configuration files",
        "contracts": "Interface definitions and abstractions",
        "foundation": "Core framework components and base classes",
        "queue": "Background jobs and queue processing",
        "redis": "Redis caching and data structures",
        "session": "Session management and middleware",
        "bus": "Command bus and job dispatching",
        "support": "Helper classes and miscellaneous utilities"
    }
    return common_dirs.get(dir_name.lower(), "Project directory")

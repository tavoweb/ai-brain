import json
import os
from pathlib import Path

LOCAL_DIR_NAME = ".ai-brain"

def get_local_dir(project_root: str) -> Path:
    return Path(project_root) / LOCAL_DIR_NAME

def is_initialized(project_root: str) -> bool:
    return (get_local_dir(project_root) / "config.json").exists()

def init_local_state(project_root: str, name: str, init_time: str):
    """Create local .ai-brain directory and base files."""
    local_dir = get_local_dir(project_root)
    local_dir.mkdir(parents=True, exist_ok=True)
    
    config_path = local_dir / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({
            "project_name": name,
            "initialized_at": init_time,
        }, f, indent=4)
        
    history_path = local_dir / "history.json"
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

    graph_path = local_dir / "graph.json"
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=4)

def load_config(project_root: str) -> dict:
    config_path = get_local_dir(project_root) / "config.json"
    if not config_path.exists():
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_history(project_root: str) -> list:
    history_path = get_local_dir(project_root) / "history.json"
    if not history_path.exists():
        return []
    with open(history_path, "r", encoding="utf-8") as f:
        return json.load(f)

def add_history_entry(project_root: str, timestamp: str, summary: str):
    history = load_history(project_root)
    history.append({
        "timestamp": timestamp,
        "summary": summary
    })
    history_path = get_local_dir(project_root) / "history.json"
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def save_graph(project_root: str, graph_data: dict):
    graph_path = get_local_dir(project_root) / "graph.json"
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=4)

def load_graph(project_root: str) -> dict:
    graph_path = get_local_dir(project_root) / "graph.json"
    if not graph_path.exists():
        return {}
    with open(graph_path, "r", encoding="utf-8") as f:
        return json.load(f)

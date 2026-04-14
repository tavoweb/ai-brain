# 🧠 AI-Brain

A "Persistent Long-Term Memory" and "Stateful Backup" system for developers working with AI.

AI-Brain solves the "Context Drift" problem. It maintains a "Project Passport" that tracks the visual and logical structure of a project, so any LLM (ChatGPT, Claude) can instantly resume work without re-explaining the codebase.

## Features

- **Project Registration:** Keep track of all your AI-assisted projects globally.
- **Graph Scanning:** Maps out your directory structure into a JSON graph.
- **Stateful Backups:** Automatically zip and backup your codebase without `.git` or `node_modules` clutter.
- **Context Generation:** Generates an easy-to-copy Markdown summary of your project and recent history for prompt injection.

## Installation

Ensure you have Python 3.10+ installed.

Clone this repository or navigate to its directory, then run:

```bash
pip install -e .
```

This will install the `aib` command globally on your system.

## Usage

Navigate to any coding project you want to track:

```bash
cd /path/to/your/project
```

### Initialize
```bash
aib init
```
Initializes AI-Brain for the current folder. Prompts you for a project name.

### Sync State
```bash
aib sync
```
Scans the current files, updates the local project graph map, and asks you for a brief "session summary" (e.g., "Added login module") to append to the project history.

### Backup
```bash
aib backup
```
Creates a compressed ZIP snapshot of the current state and saves it in a `backups/` directory inside your project, ignoring heavy folders like `node_modules` or `.venv`.

### Inject Context
```bash
aib inject
```
Outputs a formatted Markdown block containing the entire project architecture and recent changes. Copy this block and paste it into ChatGPT/Claude at the start of a new session so it instantly knows your project context!

### List Projects
```bash
aib list
```
Shows a comprehensive table of all projects managed by AI-Brain globally across your system, along with their last update status.

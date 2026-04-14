# 🧠 AI-Brain

A "Persistent Long-Term Memory" and "Stateful Backup" system for developers working with AI.

AI-Brain solves the "Context Drift" problem. It maintains a **Project Passport** with a logical **Symbol Map** that tracks the structure, classes, and logic of a project, so any LLM (ChatGPT, Claude, Cursor) can instantly resume work without re-explaining the codebase.

## 🚀 Features

- **Project Registration:** Keep track of all your AI-assisted projects globally in a local database.
- **Symbol Map Scanning:** Automatically detects classes, functions, and logic in PHP, Python, JS, and TS.
- **Intelligent Categorization:** Groups code into [MODELS], [CTRLS], [SERVICES], and [HELPERS] for better AI orientation.
- **Stateful Backups:** Automatically zip and backup your codebase, ignoring heavy folders like `node_modules` or `.venv`.
- **AI Rule Generation:** Automatically creates `.cursorrules` and `.clauderules` to make AI assistants "aware" of the project structure.
- **Condensed Context:** Generates an optimized, terminal-safe Markdown summary of your project for prompt injection.

## 📦 Installation

Ensure you have **Python 3.10+** installed.

Clone this repository or navigate to its directory, then run:

```bash
pip install -e .
```

This will install the `aib` command globally on your system.

## 🛠️ Usage

Navigate to any coding project you want to track:

```bash
cd /path/to/your/project
```

### 1. Initialize
```bash
aib init
```
Initializes AI-Brain for the current folder. Prompts you for a project name.

### 2. Deep Analysis (Symbol Map)
```bash
aib analyze
```
Deeply scans the project structure and extracts symbols (classes, methods). This is the key to providing high-quality context to AI models.

### 3. Sync State
```bash
aib sync
```
Updates the local project map and asks for a brief "session summary" (e.g., "Implemented login validation") to maintain the project's long-term memory.

### 4. AI Rules
```bash
aib rules
```
Generates `.cursorrules`, `.clauderules`, and `AI_INSTRUCTIONS.md` files. This tells AI assistants (like Cursor or Claude) to automatically look for AI-Brain metadata.

### 5. Inject Context
```bash
aib inject
```
Outputs a condensed Markdown block containing the project architecture and recent changes. Copy-paste this into your AI session to give it an instant "brain transplant" of your project!

### 6. Backup
```bash
aib backup
```
Creates a compressed ZIP snapshot of the current state, ignoring heavy system folders.

### 7. List Projects
```bash
aib list
```
Shows all tracked projects globally on your system.

---
*Built to eliminate context drift and accelerate AI-assisted development.*

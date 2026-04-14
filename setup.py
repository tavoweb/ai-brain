from setuptools import setup, find_packages

setup(
    name="ai-brain",
    version="0.1.0",
    description="A Persistent Long-Term Memory and Stateful Backup system for AI-assisted development.",
    author="Antigravity",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0"
    ],
    entry_points={
        "console_scripts": [
            "aib=ai_brain.main:cli",
        ],
    },
    python_requires=">=3.10",
)

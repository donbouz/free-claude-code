"""free-claude-code: A free alternative Claude Code implementation.

This package provides a CLI tool that interfaces with various free/open
AI providers to replicate Claude Code-like functionality.
"""

__version__ = "0.1.0"
__author__ = "free-claude-code contributors"
__license__ = "MIT"

from free_claude_code.agent import Agent
from free_claude_code.config import Config

__all__ = ["Agent", "Config", "__version__"]

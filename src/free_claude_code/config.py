"""Configuration management for free-claude-code.

Loads and validates environment variables and application settings.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from dotenv import load_dotenv

# Load .env file if present
load_dotenv()


@dataclass
class ModelConfig:
    """Configuration for the AI model provider."""

    # Provider selection: 'openai', 'anthropic', 'openrouter', etc.
    provider: str = field(default_factory=lambda: os.getenv("MODEL_PROVIDER", "openrouter"))

    # Model name/identifier
    model_name: str = field(
        default_factory=lambda: os.getenv("MODEL_NAME", "anthropic/claude-3-5-sonnet")
    )

    # API key for the chosen provider
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("API_KEY"))

    # Base URL override (useful for OpenRouter or self-hosted endpoints)
    base_url: Optional[str] = field(default_factory=lambda: os.getenv("BASE_URL"))

    # Maximum tokens to generate per response
    max_tokens: int = field(
        default_factory=lambda: int(os.getenv("MAX_TOKENS", "8192"))
    )

    # Temperature for generation (0.0 = deterministic, 1.0 = creative)
    # Lowered default from 0.7 to 0.3 — I prefer more deterministic output for coding tasks
    temperature: float = field(
        default_factory=lambda: float(os.getenv("TEMPERATURE", "0.3"))
    )


@dataclass
class AppConfig:
    """Top-level application configuration."""

    model: ModelConfig = field(default_factory=ModelConfig)

    # Directory where the agent is allowed to operate
    workspace_dir: str = field(
        default_factory=lambda: os.getenv("WORKSPACE_DIR", os.getcwd())
    )

    # Maximum number of agentic iterations before giving up
    max_iterations: int = field(
        default_factory=lambda: int(os.getenv("MAX_ITERATIONS", "50"))
    )

    # Enable verbose / debug logging
    debug: bool = field(
        default_factory=lambda: os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")
    )

    # Whether to auto-confirm tool calls without prompting the user
    auto_confirm: bool = field(
        default_factory=lambda: os.getenv("AUTO_CONFIRM", "false").lower()
        in ("1", "true", "yes")
    )

    def validate(self) -> None:
        """Raise ValueError if required configuration is missing or invalid."""
        if not self.model.api_key:
            raise ValueError(
                "API_KEY environment variable is not set. "
                "Please copy .env.example to .env and fill in your credentials."
            )

        if self.model.max_tokens < 1:
            raise ValueError("MAX_TOKENS must be a positive integer.")

        if not (0.0 <= self.model.temperature <= 2.0):
            raise ValueError("TEMPERATURE must be between 0.0 and 2.0.")

        if self.max_iterations < 1:
            raise ValueError("MAX_ITERATIONS must be a positive integer.")


# Module-level singleton — import this in other modules
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Return the glo
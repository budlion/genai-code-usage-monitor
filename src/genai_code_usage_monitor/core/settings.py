"""Configuration settings using Pydantic."""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with Pydantic validation."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CODEX_",
        case_sensitive=False,
    )

    # API settings
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_org_id: Optional[str] = Field(default=None, description="OpenAI organization ID")

    # Plan settings
    plan: str = Field(default="custom", description="Usage plan name")
    custom_limit_tokens: Optional[int] = Field(
        default=None, description="Custom token limit", ge=0
    )
    custom_limit_cost: Optional[float] = Field(
        default=None, description="Custom cost limit", ge=0.0
    )

    # Display settings
    view: str = Field(
        default="realtime", description="View mode: realtime, daily, or monthly"
    )
    theme: str = Field(default="auto", description="Display theme: light, dark, classic, auto")

    # Time settings
    timezone: str = Field(default="auto", description="Timezone for display")
    time_format: str = Field(default="auto", description="Time format: 12h, 24h, or auto")
    reset_hour: int = Field(default=0, description="Daily reset hour (0-23)", ge=0, le=23)

    # Refresh settings
    refresh_rate: int = Field(
        default=10, description="Data refresh rate in seconds", ge=1, le=60
    )
    refresh_per_second: float = Field(
        default=0.75, description="Display refresh rate in Hz", ge=0.1, le=20.0
    )

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default=None, description="Log file path")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Storage settings
    config_dir: Path = Field(
        default_factory=lambda: Path.home() / ".codex-monitor",
        description="Configuration directory",
    )
    cache_enabled: bool = Field(default=True, description="Enable caching")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds", ge=0)

    def model_post_init(self, __context) -> None:
        """Post-initialization processing."""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Set log level from debug flag
        if self.debug:
            self.log_level = "DEBUG"

    @property
    def config_file(self) -> Path:
        """Get path to configuration file."""
        return self.config_dir / "last_used.json"

    @property
    def cache_dir(self) -> Path:
        """Get path to cache directory."""
        return self.config_dir / "cache"

    @property
    def usage_db_path(self) -> Path:
        """Get path to usage database."""
        return self.config_dir / "usage.db"

    def get_api_key(self) -> Optional[str]:
        """
        Get OpenAI API key from settings or environment.

        Returns:
            API key or None
        """
        return self.openai_api_key or os.getenv("OPENAI_API_KEY")

    def validate_view(self) -> bool:
        """Validate view mode setting."""
        return self.view in ["realtime", "daily", "monthly"]

    def validate_theme(self) -> bool:
        """Validate theme setting."""
        return self.theme in ["auto", "light", "dark", "classic"]

    def validate_time_format(self) -> bool:
        """Validate time format setting."""
        return self.time_format in ["auto", "12h", "24h"]


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get global settings instance.

    Returns:
        Settings object
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """
    Reload settings from environment.

    Returns:
        New Settings object
    """
    global _settings
    _settings = Settings()
    return _settings

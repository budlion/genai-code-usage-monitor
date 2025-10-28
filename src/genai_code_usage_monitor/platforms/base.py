"""Abstract base class for AI platform adapters.

This module defines the Platform interface that all platform-specific
adapters must implement to provide consistent usage tracking across
different AI platforms.
"""

from abc import ABC, abstractmethod
from typing import Optional

from genai_code_usage_monitor.core.models import SessionData, UsageStats


class Platform(ABC):
    """Abstract base class for AI platform adapters.

    All platform-specific implementations must inherit from this class
    and implement all abstract methods to provide a consistent interface
    for usage tracking, cost calculation, and session management.

    Attributes:
        platform_name: Human-readable name of the platform
        data_directory: Path to platform-specific data storage
    """

    def __init__(self, data_directory: Optional[str] = None):
        """Initialize the platform adapter.

        Args:
            data_directory: Optional custom directory for storing platform data.
                          If not provided, uses platform's default location.
        """
        self.data_directory = data_directory

    @abstractmethod
    def get_usage_data(self) -> UsageStats:
        """Retrieve current usage statistics from the platform.

        This method should fetch and aggregate all relevant usage data
        including token counts, API calls, and costs for the current
        tracking period (typically daily or session-based).

        Returns:
            UsageStats: Aggregated usage statistics including:
                - total_tokens: Total tokens used
                - total_cost: Total cost in USD
                - total_calls: Number of API calls
                - prompt_tokens: Tokens used in prompts
                - completion_tokens: Tokens used in completions
                - models: Dictionary of model names to token counts
                - api_calls: List of individual API call records

        Raises:
            RuntimeError: If unable to access or parse usage data
            FileNotFoundError: If required data files are missing
        """
        pass

    @abstractmethod
    def get_session_info(self) -> Optional[SessionData]:
        """Retrieve information about the current or most recent session.

        A session represents a continuous period of API usage, typically
        bounded by application start/stop or explicit session markers.

        Returns:
            Optional[SessionData]: Session information including:
                - session_id: Unique identifier for the session
                - start_time: When the session began
                - end_time: When the session ended (None if active)
                - total_tokens: Tokens used in this session
                - total_cost: Cost incurred in this session
                - api_calls: List of API calls in this session
                - models_used: Dictionary of models to usage counts
            Returns None if no session data is available.

        Raises:
            RuntimeError: If unable to access session data
        """
        pass

    @abstractmethod
    def calculate_cost(
        self,
        tokens: int,
        model: str,
        is_prompt: bool = True,
        is_cached: bool = False
    ) -> float:
        """Calculate cost for token usage on this platform.

        Different platforms have different pricing models. This method
        encapsulates platform-specific pricing logic including:
        - Different rates for prompt vs completion tokens
        - Cache discounts (e.g., Claude's 90% cache discount)
        - Model-specific pricing tiers

        Args:
            tokens: Number of tokens to calculate cost for
            model: Model name/identifier (e.g., "gpt-4", "claude-sonnet-4")
            is_prompt: Whether these are prompt tokens (True) or completion tokens (False)
            is_cached: Whether cached tokens pricing applies (e.g., Claude cache)

        Returns:
            float: Cost in USD for the specified token usage

        Examples:
            >>> platform.calculate_cost(1000, "gpt-4", is_prompt=True)
            0.03  # $30 per 1M tokens

            >>> platform.calculate_cost(1000, "claude-sonnet-4", is_cached=True)
            0.0003  # 90% discount on cached tokens
        """
        pass

    @abstractmethod
    def get_platform_name(self) -> str:
        """Get the human-readable name of this platform.

        Returns:
            str: Platform name (e.g., "OpenAI Codex", "Claude Code")
        """
        pass

    def get_model_info(self, model: str) -> dict:
        """Get detailed information about a model's pricing and capabilities.

        This is an optional method that platforms can override to provide
        additional model-specific information.

        Args:
            model: Model name/identifier

        Returns:
            dict: Dictionary containing model information such as:
                - name: Model name
                - prompt_price: Price per 1M prompt tokens
                - completion_price: Price per 1M completion tokens
                - context_window: Maximum context size
                - supports_caching: Whether the model supports prompt caching
        """
        return {
            "name": model,
            "platform": self.get_platform_name(),
        }

    def __repr__(self) -> str:
        """Return string representation of the platform adapter."""
        return f"{self.__class__.__name__}(platform='{self.get_platform_name()}')"

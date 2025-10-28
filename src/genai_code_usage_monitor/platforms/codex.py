"""OpenAI Codex platform adapter.

This module provides the platform adapter for OpenAI's Codex and GPT models,
integrating with the existing UsageTracker and PricingCalculator components.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from genai_code_usage_monitor.core.models import SessionData, UsageStats
from genai_code_usage_monitor.core.pricing import PricingCalculator
from genai_code_usage_monitor.data.api_client import UsageTracker
from genai_code_usage_monitor.platforms.base import Platform


class CodexPlatform(Platform):
    """Platform adapter for OpenAI Codex and GPT models.

    This adapter integrates with the existing UsageTracker and PricingCalculator
    to provide a unified interface for OpenAI API usage tracking. It supports
    all GPT models including GPT-3.5, GPT-4, and legacy Codex models.

    Attributes:
        usage_tracker: UsageTracker instance for managing API call logs
        pricing_calculator: PricingCalculator instance for cost calculations
        storage_path: Path to local storage directory

    Example:
        >>> platform = CodexPlatform()
        >>> stats = platform.get_usage_data()
        >>> print(f"Total cost: ${stats.total_cost:.2f}")
        Total cost: $5.47
    """

    def __init__(self, data_directory: Optional[str] = None):
        """Initialize the Codex platform adapter.

        Args:
            data_directory: Optional custom directory for storing usage data.
                          Defaults to ~/.codex-monitor/ if not provided.
        """
        super().__init__(data_directory)

        # Set up storage directory
        if data_directory:
            self.storage_path = Path(data_directory)
        else:
            self.storage_path = Path.home() / ".codex-monitor"

        # Initialize components
        self.usage_tracker = UsageTracker(self.storage_path)
        self.pricing_calculator = PricingCalculator()

    def get_usage_data(self) -> UsageStats:
        """Retrieve current usage statistics from OpenAI API usage logs.

        Fetches usage data for the current day from local storage and
        aggregates it into a UsageStats object.

        Returns:
            UsageStats: Aggregated usage statistics for today including:
                - Total tokens used across all models
                - Total cost in USD
                - Number of API calls
                - Breakdown by prompt/completion tokens
                - Per-model token usage

        Raises:
            RuntimeError: If unable to read or parse usage data files
        """
        try:
            # Get today's statistics from the usage tracker
            stats = self.usage_tracker.get_daily_stats()
            return stats
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve Codex usage data: {str(e)}")

    def get_session_info(self) -> Optional[SessionData]:
        """Retrieve information about the current API usage session.

        For OpenAI/Codex, a session is defined as the current day's usage.
        This method aggregates all API calls from today into a session object.

        Returns:
            Optional[SessionData]: Session information for today, or None if
                                  no API calls have been made today.

        Raises:
            RuntimeError: If unable to access session data
        """
        try:
            # Get today's calls
            calls = self.usage_tracker.get_recent_calls(hours=24)

            if not calls:
                return None

            # Find session boundaries
            start_time = min(call.timestamp for call in calls)
            end_time = max(call.timestamp for call in calls)

            # Calculate totals
            total_tokens = sum(call.tokens.total_tokens for call in calls)
            total_cost = sum(call.cost for call in calls)

            # Count models used
            models_used = {}
            for call in calls:
                if call.model in models_used:
                    models_used[call.model] += call.tokens.total_tokens
                else:
                    models_used[call.model] = call.tokens.total_tokens

            # Create session data
            session = SessionData(
                session_id=f"codex-{start_time.strftime('%Y%m%d')}",
                start_time=start_time,
                end_time=end_time,
                total_tokens=total_tokens,
                total_cost=total_cost,
                api_calls=calls,
                models_used=models_used,
            )

            return session

        except ValidationError as e:
            raise RuntimeError(f"Failed to parse session data: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve session info: {str(e)}")

    def calculate_cost(
        self,
        tokens: int,
        model: str,
        is_prompt: bool = True,
        is_cached: bool = False
    ) -> float:
        """Calculate cost for token usage on OpenAI models.

        OpenAI uses different pricing for prompt and completion tokens.
        Cache discounts are not applicable to OpenAI models (ignored).

        Args:
            tokens: Number of tokens to calculate cost for
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
            is_prompt: Whether these are prompt tokens (True) or completion tokens (False)
            is_cached: Not used for OpenAI (no cache discount)

        Returns:
            float: Cost in USD for the specified token usage

        Example:
            >>> platform = CodexPlatform()
            >>> cost = platform.calculate_cost(1000, "gpt-4", is_prompt=True)
            >>> print(f"${cost:.4f}")
            $0.0300
        """
        try:
            # Get model pricing
            pricing = self.pricing_calculator.get_model_pricing(model)

            # Calculate cost based on token type
            price_per_million = pricing["prompt"] if is_prompt else pricing["completion"]
            cost = (tokens / 1_000_000) * price_per_million

            return cost

        except Exception as e:
            raise ValueError(f"Failed to calculate cost for model '{model}': {str(e)}")

    def get_platform_name(self) -> str:
        """Get the platform name.

        Returns:
            str: "OpenAI Codex"
        """
        return "OpenAI Codex"

    def get_model_info(self, model: str) -> dict:
        """Get detailed information about an OpenAI model.

        Args:
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo")

        Returns:
            dict: Dictionary containing:
                - name: Model name
                - platform: "OpenAI Codex"
                - prompt_price_per_1m: Prompt token price per 1M tokens
                - completion_price_per_1m: Completion token price per 1M tokens
                - avg_price_per_1m: Average price per 1M tokens
                - cost_per_1k_tokens: Cost per 1K tokens

        Example:
            >>> platform = CodexPlatform()
            >>> info = platform.get_model_info("gpt-4")
            >>> print(info['prompt_price_per_1m'])
            30.0
        """
        base_info = super().get_model_info(model)
        pricing_info = self.pricing_calculator.get_model_info(model)
        base_info.update(pricing_info)
        return base_info

    def log_api_call(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        request_id: Optional[str] = None
    ):
        """Log an API call to local storage.

        This is a convenience method that wraps the UsageTracker's log_api_call
        method for direct logging of API calls.

        Args:
            model: Model name used for the API call
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            request_id: Optional OpenAI request ID

        Returns:
            APICall: The logged API call object

        Example:
            >>> platform = CodexPlatform()
            >>> call = platform.log_api_call("gpt-4", 100, 50)
            >>> print(f"Cost: ${call.cost:.4f}")
            Cost: $0.0060
        """
        return self.usage_tracker.log_api_call(
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            request_id=request_id
        )

    def get_usage_summary(self) -> dict:
        """Get a comprehensive usage summary across different time periods.

        Returns:
            dict: Summary with 'today', 'week', and 'month' keys, each containing:
                - tokens: Total tokens used
                - cost: Total cost in USD
                - calls: Number of API calls

        Example:
            >>> platform = CodexPlatform()
            >>> summary = platform.get_usage_summary()
            >>> print(f"This week: ${summary['week']['cost']:.2f}")
            This week: $12.45
        """
        return self.usage_tracker.get_usage_summary()

    def __repr__(self) -> str:
        """Return string representation of the Codex platform adapter."""
        return f"CodexPlatform(storage='{self.storage_path}')"

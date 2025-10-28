"""Claude Code platform adapter.

This module provides the platform adapter for Anthropic's Claude Code,
supporting Claude Sonnet and Opus models with prompt caching discounts.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import ValidationError

from genai_code_usage_monitor.core.models import APICall, SessionData, TokenUsage, UsageStats
from genai_code_usage_monitor.platforms.base import Platform


# Claude model pricing (as of 2025, prices in USD per 1M tokens)
CLAUDE_PRICING: Dict[str, Dict[str, float]] = {
    "claude-sonnet-4": {
        "prompt": 3.00,  # $3 per 1M prompt tokens
        "completion": 15.00,  # $15 per 1M completion tokens
        "cached_prompt": 0.30,  # 90% discount on cached tokens
    },
    "claude-sonnet-3.5": {
        "prompt": 3.00,
        "completion": 15.00,
        "cached_prompt": 0.30,
    },
    "claude-opus": {
        "prompt": 15.00,  # $15 per 1M prompt tokens
        "completion": 75.00,  # $75 per 1M completion tokens
        "cached_prompt": 1.50,  # 90% discount on cached tokens
    },
    "claude-opus-3": {
        "prompt": 15.00,
        "completion": 75.00,
        "cached_prompt": 1.50,
    },
    # Default fallback for unknown Claude models
    "default": {
        "prompt": 3.00,
        "completion": 15.00,
        "cached_prompt": 0.30,
    },
}


class ClaudePlatform(Platform):
    """Platform adapter for Anthropic's Claude Code.

    This adapter provides usage tracking for Claude models including support
    for prompt caching (90% discount on cached tokens). It reads data from
    the ~/.claude-monitor/ directory (or custom location).

    Claude's unique features:
    - Prompt caching with 90% discount on repeated prompts
    - Different pricing tiers for Sonnet (cheaper) and Opus (more capable)
    - Extended context windows (up to 200K tokens)

    Attributes:
        storage_path: Path to local storage directory for Claude usage data
        pricing: Dictionary of Claude model pricing information

    Example:
        >>> platform = ClaudePlatform()
        >>> stats = platform.get_usage_data()
        >>> print(f"Total cost: ${stats.total_cost:.2f}")
        Total cost: $2.34

        >>> # Calculate cost with cache discount
        >>> cost = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)
        >>> print(f"Cached cost: ${cost:.4f}")
        Cached cost: $0.0030
    """

    def __init__(self, data_directory: Optional[str] = None):
        """Initialize the Claude platform adapter.

        Args:
            data_directory: Optional custom directory for storing usage data.
                          Defaults to ~/.claude-monitor/ if not provided.
        """
        super().__init__(data_directory)

        # Set up storage directory
        if data_directory:
            self.storage_path = Path(data_directory)
        else:
            self.storage_path = Path.home() / ".claude-monitor"

        # Create directory if it doesn't exist
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Usage log file
        self.usage_file = self.storage_path / "usage_log.jsonl"

        # Pricing configuration
        self.pricing = CLAUDE_PRICING.copy()

    def get_usage_data(self) -> UsageStats:
        """Retrieve current usage statistics from Claude usage logs.

        Reads the usage log file and aggregates all API calls from today
        into a UsageStats object.

        Returns:
            UsageStats: Aggregated usage statistics for today including:
                - Total tokens used across all Claude models
                - Total cost in USD (including cache discounts)
                - Number of API calls
                - Breakdown by prompt/completion tokens
                - Per-model token usage

        Raises:
            RuntimeError: If unable to read or parse usage data files
            FileNotFoundError: If usage log file doesn't exist and no calls made
        """
        try:
            # Get today's calls
            calls = self._get_recent_calls(hours=24)

            # Create stats object
            stats = UsageStats(date=datetime.now())

            # Aggregate all calls
            for call in calls:
                stats.update_from_call(call)

            return stats

        except Exception as e:
            # If file doesn't exist yet, return empty stats
            if not self.usage_file.exists():
                return UsageStats(date=datetime.now())
            raise RuntimeError(f"Failed to retrieve Claude usage data: {str(e)}")

    def get_session_info(self) -> Optional[SessionData]:
        """Retrieve information about the current Claude usage session.

        For Claude, a session is defined as continuous usage within the
        current day. This method aggregates all API calls from today.

        Returns:
            Optional[SessionData]: Session information for today including:
                - session_id: Format "claude-YYYYMMDD"
                - start_time: Timestamp of first call today
                - end_time: Timestamp of last call today
                - total_tokens: Sum of all tokens used
                - total_cost: Sum of all costs (with cache discounts)
                - api_calls: List of all API calls
                - models_used: Dictionary mapping models to token counts
            Returns None if no API calls have been made today.

        Raises:
            RuntimeError: If unable to access session data
        """
        try:
            # Get today's calls
            calls = self._get_recent_calls(hours=24)

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
                session_id=f"claude-{start_time.strftime('%Y%m%d')}",
                start_time=start_time,
                end_time=end_time,
                total_tokens=total_tokens,
                total_cost=total_cost,
                api_calls=calls,
                models_used=models_used,
            )

            return session

        except ValidationError as e:
            raise RuntimeError(f"Failed to parse Claude session data: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve Claude session info: {str(e)}")

    def calculate_cost(
        self,
        tokens: int,
        model: str,
        is_prompt: bool = True,
        is_cached: bool = False
    ) -> float:
        """Calculate cost for token usage on Claude models.

        Claude supports prompt caching which provides a 90% discount on
        cached prompt tokens. Completion tokens are never cached.

        Args:
            tokens: Number of tokens to calculate cost for
            model: Model name (e.g., "claude-sonnet-4", "claude-opus")
            is_prompt: Whether these are prompt tokens (True) or completion (False)
            is_cached: Whether cached pricing applies (90% discount for prompts)

        Returns:
            float: Cost in USD for the specified token usage

        Example:
            >>> platform = ClaudePlatform()
            >>> # Regular prompt tokens
            >>> cost1 = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=True)
            >>> print(f"Regular: ${cost1:.4f}")
            Regular: $0.0300

            >>> # Cached prompt tokens (90% discount)
            >>> cost2 = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)
            >>> print(f"Cached: ${cost2:.4f}")
            Cached: $0.0030

            >>> # Completion tokens (no caching)
            >>> cost3 = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=False)
            >>> print(f"Completion: ${cost3:.4f}")
            Completion: $0.1500
        """
        try:
            # Get model pricing
            pricing = self._get_model_pricing(model)

            # Determine price per million tokens
            if is_cached and is_prompt:
                # Cached prompt tokens get 90% discount
                price_per_million = pricing["cached_prompt"]
            elif is_prompt:
                # Regular prompt tokens
                price_per_million = pricing["prompt"]
            else:
                # Completion tokens (never cached)
                price_per_million = pricing["completion"]

            # Calculate cost
            cost = (tokens / 1_000_000) * price_per_million

            return cost

        except Exception as e:
            raise ValueError(f"Failed to calculate cost for model '{model}': {str(e)}")

    def get_platform_name(self) -> str:
        """Get the platform name.

        Returns:
            str: "Claude Code"
        """
        return "Claude Code"

    def get_model_info(self, model: str) -> dict:
        """Get detailed information about a Claude model.

        Args:
            model: Model name (e.g., "claude-sonnet-4", "claude-opus")

        Returns:
            dict: Dictionary containing:
                - name: Model name
                - platform: "Claude Code"
                - prompt_price_per_1m: Prompt token price per 1M tokens
                - completion_price_per_1m: Completion token price per 1M tokens
                - cached_prompt_price_per_1m: Cached prompt price per 1M tokens
                - cache_discount: Percentage discount for cached tokens
                - supports_caching: Always True for Claude models

        Example:
            >>> platform = ClaudePlatform()
            >>> info = platform.get_model_info("claude-sonnet-4")
            >>> print(f"Cache discount: {info['cache_discount']}%")
            Cache discount: 90%
        """
        base_info = super().get_model_info(model)
        pricing = self._get_model_pricing(model)

        base_info.update({
            "prompt_price_per_1m": pricing["prompt"],
            "completion_price_per_1m": pricing["completion"],
            "cached_prompt_price_per_1m": pricing["cached_prompt"],
            "cache_discount": "90%",
            "supports_caching": True,
        })

        return base_info

    def log_api_call(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cached_tokens: int = 0,
        request_id: Optional[str] = None
    ) -> APICall:
        """Log a Claude API call to local storage.

        Args:
            model: Model name used for the API call
            prompt_tokens: Number of prompt tokens (non-cached)
            completion_tokens: Number of completion tokens
            cached_tokens: Number of cached prompt tokens (90% discount)
            request_id: Optional Claude request ID

        Returns:
            APICall: The logged API call object

        Example:
            >>> platform = ClaudePlatform()
            >>> call = platform.log_api_call(
            ...     "claude-sonnet-4",
            ...     prompt_tokens=1000,
            ...     completion_tokens=500,
            ...     cached_tokens=5000
            ... )
            >>> print(f"Cost: ${call.cost:.4f}")
            Cost: $0.0180
        """
        # Calculate costs
        prompt_cost = self.calculate_cost(prompt_tokens, model, is_prompt=True)
        completion_cost = self.calculate_cost(completion_tokens, model, is_prompt=False)
        cached_cost = self.calculate_cost(cached_tokens, model, is_cached=True)
        total_cost = prompt_cost + completion_cost + cached_cost

        # Create token usage object (total includes cached)
        tokens = TokenUsage(
            prompt_tokens=prompt_tokens + cached_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + cached_tokens + completion_tokens,
        )

        # Create API call record
        call = APICall(
            timestamp=datetime.now(),
            model=model,
            tokens=tokens,
            cost=total_cost,
            request_id=request_id,
            status="completed",
        )

        # Save to file
        self._save_call(call)

        return call

    # Private helper methods

    def _get_model_pricing(self, model: str) -> Dict[str, float]:
        """Get pricing for a specific Claude model.

        Args:
            model: Model name

        Returns:
            Dictionary with prompt, completion, and cached_prompt pricing
        """
        # Try exact match first
        if model in self.pricing:
            return self.pricing[model]

        # Try prefix matching (e.g., "claude-sonnet-4-20250514" matches "claude-sonnet-4")
        for key in self.pricing:
            if key != "default" and model.startswith(key):
                return self.pricing[key]

        # Return default pricing
        return self.pricing["default"]

    def _save_call(self, call: APICall) -> None:
        """Save API call to storage file.

        Args:
            call: APICall object to save
        """
        with open(self.usage_file, "a") as f:
            f.write(call.model_dump_json() + "\n")

    def _get_recent_calls(self, hours: int = 24) -> List[APICall]:
        """Get recent API calls from storage.

        Args:
            hours: Number of hours to look back

        Returns:
            List of APICall objects
        """
        if not self.usage_file.exists():
            return []

        cutoff_time = datetime.now() - timedelta(hours=hours)
        calls = []

        with open(self.usage_file, "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    call = APICall(**data)
                    if call.timestamp >= cutoff_time:
                        calls.append(call)
                except Exception:
                    # Skip malformed lines
                    continue

        return calls

    def get_usage_summary(self) -> dict:
        """Get a comprehensive usage summary across different time periods.

        Returns:
            dict: Summary with 'today', 'week', and 'month' keys, each containing:
                - tokens: Total tokens used
                - cost: Total cost in USD (including cache discounts)
                - calls: Number of API calls

        Example:
            >>> platform = ClaudePlatform()
            >>> summary = platform.get_usage_summary()
            >>> print(f"This week: ${summary['week']['cost']:.2f}")
            This week: $8.23
        """
        today_calls = self._get_recent_calls(hours=24)
        week_calls = self._get_recent_calls(hours=168)  # 7 days
        month_calls = self._get_recent_calls(hours=720)  # 30 days

        return {
            "today": {
                "tokens": sum(c.tokens.total_tokens for c in today_calls),
                "cost": sum(c.cost for c in today_calls),
                "calls": len(today_calls),
            },
            "week": {
                "tokens": sum(c.tokens.total_tokens for c in week_calls),
                "cost": sum(c.cost for c in week_calls),
                "calls": len(week_calls),
            },
            "month": {
                "tokens": sum(c.tokens.total_tokens for c in month_calls),
                "cost": sum(c.cost for c in month_calls),
                "calls": len(month_calls),
            },
        }

    def __repr__(self) -> str:
        """Return string representation of the Claude platform adapter."""
        return f"ClaudePlatform(storage='{self.storage_path}')"

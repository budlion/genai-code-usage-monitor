"""Pricing calculator for OpenAI models."""

from typing import Dict
from typing import Optional


# OpenAI model pricing (as of 2025, prices in USD per 1M tokens)
# Note: These prices are examples and should be updated with actual OpenAI pricing
MODEL_PRICING: Dict[str, Dict[str, float]] = {
    # GPT-4 models
    "gpt-4": {
        "prompt": 30.00,  # $30 per 1M prompt tokens
        "completion": 60.00,  # $60 per 1M completion tokens
    },
    "gpt-4-32k": {
        "prompt": 60.00,
        "completion": 120.00,
    },
    "gpt-4-turbo": {
        "prompt": 10.00,
        "completion": 30.00,
    },
    "gpt-4-turbo-preview": {
        "prompt": 10.00,
        "completion": 30.00,
    },
    # GPT-3.5 models
    "gpt-3.5-turbo": {
        "prompt": 0.50,  # $0.50 per 1M tokens
        "completion": 1.50,
    },
    "gpt-3.5-turbo-16k": {
        "prompt": 3.00,
        "completion": 4.00,
    },
    # Code models (Codex-based or GPT for code)
    "code-davinci-002": {
        "prompt": 0.00,  # Deprecated but free
        "completion": 0.00,
    },
    "gpt-4-code": {
        "prompt": 10.00,
        "completion": 30.00,
    },
    # Claude models (Anthropic)
    "claude-3-opus": {
        "prompt": 15.00,  # $15 per 1M prompt tokens
        "completion": 75.00,  # $75 per 1M completion tokens
        "cached_prompt": 1.50,  # 90% discount for cached tokens
    },
    "claude-3-sonnet": {
        "prompt": 3.00,  # $3 per 1M prompt tokens
        "completion": 15.00,  # $15 per 1M completion tokens
        "cached_prompt": 0.30,  # 90% discount for cached tokens
    },
    "claude-3-haiku": {
        "prompt": 0.25,  # $0.25 per 1M prompt tokens
        "completion": 1.25,  # $1.25 per 1M completion tokens
        "cached_prompt": 0.025,  # 90% discount for cached tokens
    },
    "claude-3.5-sonnet": {
        "prompt": 3.00,
        "completion": 15.00,
        "cached_prompt": 0.30,
    },
    "claude-2.1": {
        "prompt": 8.00,
        "completion": 24.00,
        "cached_prompt": 0.80,
    },
    "claude-2.0": {
        "prompt": 8.00,
        "completion": 24.00,
        "cached_prompt": 0.80,
    },
    # Default fallback
    "default": {
        "prompt": 1.00,
        "completion": 2.00,
    },
}


class PricingCalculator:
    """Calculate costs for OpenAI API usage."""

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None):
        """
        Initialize pricing calculator.

        Args:
            custom_pricing: Optional custom pricing dictionary
        """
        self.pricing = MODEL_PRICING.copy()
        if custom_pricing:
            self.pricing.update(custom_pricing)

    def get_model_pricing(self, model: str) -> Dict[str, float]:
        """
        Get pricing for a specific model.

        Args:
            model: Model name

        Returns:
            Dictionary with prompt and completion pricing
        """
        # Try exact match first
        if model in self.pricing:
            return self.pricing[model]

        # Try prefix matching (e.g., "gpt-4-0613" matches "gpt-4")
        for key in self.pricing:
            if model.startswith(key):
                return self.pricing[key]

        # Return default pricing
        return self.pricing["default"]

    def calculate_cost(
        self, model: str, prompt_tokens: int, completion_tokens: int
    ) -> float:
        """
        Calculate cost for an API call.

        Args:
            model: Model name
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens

        Returns:
            Total cost in USD
        """
        pricing = self.get_model_pricing(model)

        # Calculate cost (pricing is per 1M tokens)
        prompt_cost = (prompt_tokens / 1_000_000) * pricing["prompt"]
        completion_cost = (completion_tokens / 1_000_000) * pricing["completion"]

        return prompt_cost + completion_cost

    def calculate_cached_cost(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cached_tokens: int = 0,
    ) -> tuple[float, float]:
        """
        Calculate cost for an API call with cached tokens.

        Args:
            model: Model name
            prompt_tokens: Number of prompt tokens (excluding cached)
            completion_tokens: Number of completion tokens
            cached_tokens: Number of cached prompt tokens (90% discount)

        Returns:
            Tuple of (total_cost, savings_from_cache)
        """
        pricing = self.get_model_pricing(model)

        # Calculate regular prompt cost (non-cached tokens)
        regular_prompt_cost = (prompt_tokens / 1_000_000) * pricing["prompt"]

        # Calculate cached token cost (90% discount if supported)
        if "cached_prompt" in pricing:
            cached_cost = (cached_tokens / 1_000_000) * pricing["cached_prompt"]
            # Calculate what it would have cost without cache
            savings = (cached_tokens / 1_000_000) * pricing["prompt"] - cached_cost
        else:
            # Model doesn't support caching, charge full price
            cached_cost = (cached_tokens / 1_000_000) * pricing["prompt"]
            savings = 0.0

        # Calculate completion cost
        completion_cost = (completion_tokens / 1_000_000) * pricing["completion"]

        total_cost = regular_prompt_cost + cached_cost + completion_cost

        return total_cost, savings

    def supports_caching(self, model: str) -> bool:
        """
        Check if a model supports cached tokens.

        Args:
            model: Model name

        Returns:
            True if model supports caching
        """
        pricing = self.get_model_pricing(model)
        return "cached_prompt" in pricing

    def calculate_total_cost(
        self, model: str, total_tokens: int, prompt_ratio: float = 0.5
    ) -> float:
        """
        Calculate cost based on total tokens with estimated ratio.

        Args:
            model: Model name
            total_tokens: Total number of tokens
            prompt_ratio: Ratio of prompt tokens to total (default 0.5)

        Returns:
            Estimated total cost in USD
        """
        prompt_tokens = int(total_tokens * prompt_ratio)
        completion_tokens = total_tokens - prompt_tokens

        return self.calculate_cost(model, prompt_tokens, completion_tokens)

    def estimate_tokens_for_budget(
        self, model: str, budget: float, prompt_ratio: float = 0.5
    ) -> int:
        """
        Estimate how many tokens can be used within a budget.

        Args:
            model: Model name
            budget: Available budget in USD
            prompt_ratio: Ratio of prompt tokens to total

        Returns:
            Estimated number of tokens
        """
        pricing = self.get_model_pricing(model)

        # Calculate weighted average price per 1M tokens
        avg_price = (
            pricing["prompt"] * prompt_ratio
            + pricing["completion"] * (1 - prompt_ratio)
        )

        # Calculate tokens
        tokens = int((budget / avg_price) * 1_000_000)

        return tokens

    def format_cost(self, cost: float) -> str:
        """
        Format cost as string with currency symbol.

        Args:
            cost: Cost in USD

        Returns:
            Formatted cost string
        """
        if cost < 0.01:
            return f"${cost:.4f}"
        elif cost < 1.0:
            return f"${cost:.3f}"
        else:
            return f"${cost:.2f}"

    def add_custom_model(
        self, model: str, prompt_price: float, completion_price: float
    ) -> None:
        """
        Add custom model pricing.

        Args:
            model: Model name
            prompt_price: Prompt token price per 1M tokens
            completion_price: Completion token price per 1M tokens
        """
        self.pricing[model] = {
            "prompt": prompt_price,
            "completion": completion_price,
        }

    def get_all_models(self) -> list:
        """
        Get list of all models with pricing.

        Returns:
            List of model names
        """
        return list(self.pricing.keys())

    def get_model_info(self, model: str) -> Dict[str, any]:
        """
        Get detailed information about a model's pricing.

        Args:
            model: Model name

        Returns:
            Dictionary with model information
        """
        pricing = self.get_model_pricing(model)

        return {
            "model": model,
            "prompt_price_per_1m": pricing["prompt"],
            "completion_price_per_1m": pricing["completion"],
            "avg_price_per_1m": (pricing["prompt"] + pricing["completion"]) / 2,
            "cost_per_1k_tokens": ((pricing["prompt"] + pricing["completion"]) / 2)
            / 1000,
        }


# Global pricing calculator instance
_default_calculator: Optional[PricingCalculator] = None


def get_pricing_calculator() -> PricingCalculator:
    """
    Get the default pricing calculator instance.

    Returns:
        PricingCalculator instance
    """
    global _default_calculator
    if _default_calculator is None:
        _default_calculator = PricingCalculator()
    return _default_calculator

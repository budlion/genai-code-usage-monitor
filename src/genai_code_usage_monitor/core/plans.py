"""Plan definitions and management for Codex Monitor."""

from typing import Dict
from typing import Optional

from genai_code_usage_monitor.core.models import PlanLimits


# Define available plans
PLANS: Dict[str, PlanLimits] = {
    "free": PlanLimits(
        name="Free Tier",
        token_limit=100_000,  # Example: 100k tokens per day
        cost_limit=0.0,
        rate_limit_rpm=20,  # 20 requests per minute
        rate_limit_tpm=40_000,  # 40k tokens per minute
        is_custom=False,
    ),
    "payg": PlanLimits(
        name="Pay-As-You-Go",
        token_limit=None,  # No hard token limit
        cost_limit=100.0,  # $100 daily budget as default
        rate_limit_rpm=3_500,  # Higher rate limits
        rate_limit_tpm=90_000,
        is_custom=False,
    ),
    "tier1": PlanLimits(
        name="Tier 1",
        token_limit=1_000_000,  # 1M tokens per day
        cost_limit=50.0,
        rate_limit_rpm=500,
        rate_limit_tpm=60_000,
        is_custom=False,
    ),
    "tier2": PlanLimits(
        name="Tier 2",
        token_limit=5_000_000,  # 5M tokens per day
        cost_limit=250.0,
        rate_limit_rpm=1_000,
        rate_limit_tpm=150_000,
        is_custom=False,
    ),
    "custom": PlanLimits(
        name="Custom (P90-based)",
        token_limit=None,  # Will be calculated by P90 analysis
        cost_limit=50.0,  # Default cost limit
        rate_limit_rpm=None,
        rate_limit_tpm=None,
        is_custom=True,
    ),
}


class PlanManager:
    """Manage plans and their limits."""

    def __init__(self, plan_name: str = "custom"):
        """
        Initialize plan manager.

        Args:
            plan_name: Name of the plan to use
        """
        self.plan_name = plan_name
        self._current_plan = self._get_plan(plan_name)

    def _get_plan(self, plan_name: str) -> PlanLimits:
        """
        Get plan by name.

        Args:
            plan_name: Name of the plan

        Returns:
            PlanLimits object

        Raises:
            ValueError: If plan not found
        """
        if plan_name not in PLANS:
            raise ValueError(
                f"Plan '{plan_name}' not found. Available plans: {list(PLANS.keys())}"
            )
        return PLANS[plan_name].model_copy(deep=True)

    @property
    def current_plan(self) -> PlanLimits:
        """Get current plan."""
        return self._current_plan

    @property
    def limits(self) -> PlanLimits:
        """Get current plan limits (alias for current_plan)."""
        return self._current_plan

    def set_custom_limits(
        self,
        token_limit: Optional[int] = None,
        cost_limit: Optional[float] = None,
        rate_limit_rpm: Optional[int] = None,
        rate_limit_tpm: Optional[int] = None,
    ) -> None:
        """
        Set custom limits for the current plan.

        Args:
            token_limit: Custom token limit
            cost_limit: Custom cost limit
            rate_limit_rpm: Custom requests per minute limit
            rate_limit_tpm: Custom tokens per minute limit
        """
        if token_limit is not None:
            self._current_plan.token_limit = token_limit
        if cost_limit is not None:
            self._current_plan.cost_limit = cost_limit
        if rate_limit_rpm is not None:
            self._current_plan.rate_limit_rpm = rate_limit_rpm
        if rate_limit_tpm is not None:
            self._current_plan.rate_limit_tpm = rate_limit_tpm

    def switch_plan(self, plan_name: str) -> PlanLimits:
        """
        Switch to a different plan.

        Args:
            plan_name: Name of the plan to switch to

        Returns:
            New PlanLimits object
        """
        self.plan_name = plan_name
        self._current_plan = self._get_plan(plan_name)
        return self._current_plan

    def update_from_p90(self, p90_tokens: int, confidence: float = 0.95) -> None:
        """
        Update plan limits based on P90 analysis.

        Args:
            p90_tokens: P90 token usage
            confidence: Confidence level of the analysis
        """
        if self._current_plan.is_custom or self.plan_name == "custom":
            # Set limit slightly above P90 to account for variance
            buffer_multiplier = 1.1 if confidence >= 0.95 else 1.2
            self._current_plan.token_limit = int(p90_tokens * buffer_multiplier)

    def get_warning_thresholds(self) -> Dict[str, float]:
        """
        Get warning threshold percentages.

        Returns:
            Dictionary of threshold names to percentages
        """
        return {
            "low": 0.5,  # 50% - info level
            "medium": 0.75,  # 75% - warning level
            "high": 0.90,  # 90% - alert level
            "critical": 0.95,  # 95% - critical level
        }

    def check_limit_status(
        self, current_tokens: int, current_cost: float
    ) -> Dict[str, any]:
        """
        Check current usage against limits.

        Args:
            current_tokens: Current token usage
            current_cost: Current cost

        Returns:
            Dictionary with status information
        """
        status = {
            "tokens": {"value": current_tokens, "limit": self._current_plan.token_limit},
            "cost": {"value": current_cost, "limit": self._current_plan.cost_limit},
            "warning_level": "normal",
        }

        thresholds = self.get_warning_thresholds()

        # Check token limit
        if self._current_plan.token_limit:
            token_percentage = current_tokens / self._current_plan.token_limit
            status["tokens"]["percentage"] = token_percentage * 100

            for level, threshold in reversed(list(thresholds.items())):
                if token_percentage >= threshold:
                    status["warning_level"] = level
                    break

        # Check cost limit
        if self._current_plan.cost_limit:
            cost_percentage = current_cost / self._current_plan.cost_limit
            status["cost"]["percentage"] = cost_percentage * 100

            # Update warning level if cost is more critical
            for level, threshold in reversed(list(thresholds.items())):
                if cost_percentage >= threshold:
                    # Take the more severe warning level
                    current_level = status["warning_level"]
                    if (
                        list(thresholds.keys()).index(level)
                        > list(thresholds.keys()).index(current_level)
                    ):
                        status["warning_level"] = level
                    break

        return status

    @staticmethod
    def list_available_plans() -> Dict[str, str]:
        """
        List all available plans with descriptions.

        Returns:
            Dictionary of plan names to descriptions
        """
        return {name: plan.name for name, plan in PLANS.items()}

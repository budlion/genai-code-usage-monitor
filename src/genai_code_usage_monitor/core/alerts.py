"""Alert system for monitoring usage thresholds and predicting costs."""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from .models import (
    Alert,
    AlertLevel,
    BurnRate,
    MonitorState,
    PlanLimits,
    UsageStats,
)


class AlertSystem:
    """
    Alert system for real-time monitoring and predictions.

    Features:
    - Multi-level alert thresholds (INFO, WARNING, CRITICAL, DANGER)
    - Real-time cost prediction based on burn rate
    - Remaining time estimation until limits are reached
    - Burn rate alerts for rapid consumption
    - Session reset recommendations
    """

    def __init__(
        self,
        plan_limits: PlanLimits,
        alert_thresholds: Optional[dict] = None,
    ):
        """
        Initialize alert system.

        Args:
            plan_limits: Plan limits to monitor against
            alert_thresholds: Custom alert thresholds (optional)
        """
        self.plan_limits = plan_limits
        self.alerts: List[Alert] = []

        # Default thresholds can be overridden
        self.thresholds = alert_thresholds or {
            "INFO": 50.0,  # 50%
            "WARNING": 75.0,  # 75%
            "CRITICAL": 90.0,  # 90%
            "DANGER": 95.0,  # 95%
        }

    def check_usage_alerts(
        self, current_stats: UsageStats, burn_rate: BurnRate
    ) -> List[Alert]:
        """
        Check for usage alerts based on current statistics.

        Args:
            current_stats: Current usage statistics
            burn_rate: Current burn rate analysis

        Returns:
            List of active alerts
        """
        alerts = []

        # Check token usage
        if self.plan_limits.token_limit:
            token_percentage = (
                current_stats.total_tokens / self.plan_limits.token_limit
            ) * 100
            token_alerts = self._create_threshold_alerts(
                metric_type="token_usage",
                current_value=current_stats.total_tokens,
                limit_value=self.plan_limits.token_limit,
                percentage=token_percentage,
                burn_rate=burn_rate,
            )
            alerts.extend(token_alerts)

        # Check cost usage
        if self.plan_limits.cost_limit:
            cost_percentage = (
                current_stats.total_cost / self.plan_limits.cost_limit
            ) * 100
            cost_alerts = self._create_threshold_alerts(
                metric_type="cost_usage",
                current_value=current_stats.total_cost,
                limit_value=self.plan_limits.cost_limit,
                percentage=cost_percentage,
                burn_rate=burn_rate,
            )
            alerts.extend(cost_alerts)

        # Check burn rate alerts
        burn_rate_alerts = self._check_burn_rate_alerts(burn_rate, current_stats)
        alerts.extend(burn_rate_alerts)

        self.alerts = alerts
        return alerts

    def _create_threshold_alerts(
        self,
        metric_type: str,
        current_value: float,
        limit_value: float,
        percentage: float,
        burn_rate: BurnRate,
    ) -> List[Alert]:
        """Create alerts based on usage percentage thresholds."""
        alerts = []

        # Determine alert level
        level = AlertLevel.from_usage_percentage(percentage)

        # Only create alert if threshold is exceeded
        if percentage >= level.threshold:
            remaining = limit_value - current_value
            time_to_limit = self._estimate_time_to_limit(
                remaining, burn_rate, metric_type
            )

            # Create alert message
            if metric_type == "token_usage":
                message = (
                    f"Token usage at {percentage:.1f}% "
                    f"({current_value:,} / {limit_value:,} tokens)"
                )
                unit = "tokens"
            else:
                message = (
                    f"Cost usage at {percentage:.1f}% "
                    f"(${current_value:.2f} / ${limit_value:.2f})"
                )
                unit = "dollars"

            # Add time prediction if available
            if time_to_limit:
                if time_to_limit < 60:
                    time_str = f"{time_to_limit:.1f} minutes"
                elif time_to_limit < 1440:
                    time_str = f"{time_to_limit/60:.1f} hours"
                else:
                    time_str = f"{time_to_limit/1440:.1f} days"
                message += f". Estimated time to limit: {time_str}"

            # Generate recommended action
            recommended_action = self._generate_recommendation(
                level, percentage, time_to_limit, metric_type
            )

            alert = Alert(
                level=level,
                message=message,
                severity=int(percentage),
                metric_type=metric_type,
                current_value=current_value,
                threshold_value=limit_value * (level.threshold / 100),
                recommended_action=recommended_action,
            )
            alerts.append(alert)

        return alerts

    def _check_burn_rate_alerts(
        self, burn_rate: BurnRate, current_stats: UsageStats
    ) -> List[Alert]:
        """Check for abnormal burn rate patterns."""
        alerts = []

        # Alert if burn rate is unusually high
        if burn_rate.tokens_per_minute > 10000:  # Configurable threshold
            time_to_limit = burn_rate.estimated_time_to_limit
            if time_to_limit and time_to_limit < 60:  # Less than 1 hour
                alert = Alert(
                    level=AlertLevel.DANGER,
                    message=(
                        f"High burn rate detected: {burn_rate.tokens_per_minute:,.0f} tokens/min. "
                        f"Limit may be reached in {time_to_limit:.1f} minutes!"
                    ),
                    severity=95,
                    metric_type="burn_rate",
                    current_value=burn_rate.tokens_per_minute,
                    threshold_value=10000,
                    recommended_action=(
                        "Consider reducing request frequency or implementing rate limiting. "
                        "Review recent API calls for inefficiencies."
                    ),
                )
                alerts.append(alert)

        # Alert if cost per minute is high
        if burn_rate.cost_per_minute > 1.0:  # $1/min = $60/hour
            alert = Alert(
                level=AlertLevel.WARNING,
                message=(
                    f"High cost burn rate: ${burn_rate.cost_per_minute:.2f}/min "
                    f"(${burn_rate.cost_per_minute * 60:.2f}/hour)"
                ),
                severity=80,
                metric_type="cost_burn_rate",
                current_value=burn_rate.cost_per_minute,
                threshold_value=1.0,
                recommended_action=(
                    "Monitor cost carefully. Consider optimizing prompts or "
                    "using more cost-effective models."
                ),
            )
            alerts.append(alert)

        return alerts

    def _estimate_time_to_limit(
        self, remaining: float, burn_rate: BurnRate, metric_type: str
    ) -> Optional[float]:
        """
        Estimate time in minutes until limit is reached.

        Args:
            remaining: Remaining capacity (tokens or cost)
            burn_rate: Current burn rate
            metric_type: Type of metric

        Returns:
            Estimated minutes to limit, or None if cannot estimate
        """
        if metric_type == "token_usage" and burn_rate.tokens_per_minute > 0:
            return remaining / burn_rate.tokens_per_minute
        elif metric_type == "cost_usage" and burn_rate.cost_per_minute > 0:
            return remaining / burn_rate.cost_per_minute
        return None

    def _generate_recommendation(
        self,
        level: AlertLevel,
        percentage: float,
        time_to_limit: Optional[float],
        metric_type: str,
    ) -> str:
        """Generate recommended action based on alert level."""
        if level == AlertLevel.DANGER:
            if time_to_limit and time_to_limit < 30:
                return (
                    "IMMEDIATE ACTION REQUIRED: Stop current session and reset. "
                    "Limit will be reached imminently."
                )
            return (
                "Consider stopping the current session immediately. "
                "Session reset strongly recommended."
            )
        elif level == AlertLevel.CRITICAL:
            return (
                "Plan to reset session soon. Review usage patterns and "
                "optimize prompts to reduce consumption."
            )
        elif level == AlertLevel.WARNING:
            return (
                "Monitor usage closely. Consider implementing rate limiting "
                "or optimizing API calls."
            )
        else:  # INFO
            return "Usage within normal range. Continue monitoring."

    def predict_cost(
        self, burn_rate: BurnRate, hours_ahead: float = 1.0
    ) -> Tuple[float, float]:
        """
        Predict future cost based on current burn rate.

        Args:
            burn_rate: Current burn rate
            hours_ahead: Hours to predict ahead

        Returns:
            Tuple of (predicted_cost, confidence)
        """
        minutes_ahead = hours_ahead * 60
        predicted_cost = burn_rate.cost_per_minute * minutes_ahead
        confidence = burn_rate.confidence

        return predicted_cost, confidence

    def predict_tokens(
        self, burn_rate: BurnRate, hours_ahead: float = 1.0
    ) -> Tuple[int, float]:
        """
        Predict future token usage based on current burn rate.

        Args:
            burn_rate: Current burn rate
            hours_ahead: Hours to predict ahead

        Returns:
            Tuple of (predicted_tokens, confidence)
        """
        minutes_ahead = hours_ahead * 60
        predicted_tokens = int(burn_rate.tokens_per_minute * minutes_ahead)
        confidence = burn_rate.confidence

        return predicted_tokens, confidence

    def should_reset_session(
        self, current_stats: UsageStats, monitor_state: MonitorState
    ) -> Tuple[bool, str]:
        """
        Determine if session should be reset based on usage patterns.

        Args:
            current_stats: Current usage statistics
            monitor_state: Current monitor state

        Returns:
            Tuple of (should_reset, reason)
        """
        # Check if any DANGER alerts exist
        danger_alerts = [a for a in self.alerts if a.level == AlertLevel.DANGER]
        if danger_alerts:
            return True, "DANGER level alert triggered"

        # Check if approaching limits with high burn rate
        if self.plan_limits.token_limit:
            token_percentage = (
                current_stats.total_tokens / self.plan_limits.token_limit
            ) * 100
            if (
                token_percentage > 90
                and monitor_state.burn_rate.tokens_per_minute > 5000
            ):
                return True, "Approaching token limit with high burn rate"

        if self.plan_limits.cost_limit:
            cost_percentage = (
                current_stats.total_cost / self.plan_limits.cost_limit
            ) * 100
            if (
                cost_percentage > 90
                and monitor_state.burn_rate.cost_per_minute > 0.5
            ):
                return True, "Approaching cost limit with high burn rate"

        # Check time to limit
        if monitor_state.burn_rate.estimated_time_to_limit:
            if monitor_state.burn_rate.estimated_time_to_limit < 30:
                return True, "Less than 30 minutes until limit reached"

        return False, ""

    def get_session_health_score(self, monitor_state: MonitorState) -> float:
        """
        Calculate a health score (0-100) for the current session.

        Args:
            monitor_state: Current monitor state

        Returns:
            Health score (100 = healthy, 0 = critical)
        """
        score = 100.0

        # Deduct based on token usage percentage
        if self.plan_limits.token_limit:
            token_percentage = (
                monitor_state.daily_stats.total_tokens / self.plan_limits.token_limit
            ) * 100
            score -= token_percentage * 0.4  # Max 40 point deduction

        # Deduct based on cost usage percentage
        if self.plan_limits.cost_limit:
            cost_percentage = (
                monitor_state.daily_stats.total_cost / self.plan_limits.cost_limit
            ) * 100
            score -= cost_percentage * 0.4  # Max 40 point deduction

        # Deduct based on burn rate
        if monitor_state.burn_rate.tokens_per_minute > 10000:
            score -= 10
        if monitor_state.burn_rate.cost_per_minute > 1.0:
            score -= 10

        return max(0.0, score)

    def format_alert_summary(self) -> str:
        """
        Format a summary of all current alerts.

        Returns:
            Formatted alert summary string
        """
        if not self.alerts:
            return "No active alerts"

        lines = ["Active Alerts:", "=" * 50]

        # Group by level
        by_level = {}
        for alert in self.alerts:
            level_name = alert.level.value
            if level_name not in by_level:
                by_level[level_name] = []
            by_level[level_name].append(alert)

        # Sort by severity (DANGER -> CRITICAL -> WARNING -> INFO)
        level_order = ["DANGER", "CRITICAL", "WARNING", "INFO"]
        for level_name in level_order:
            if level_name in by_level:
                lines.append(f"\n{level_name} ({len(by_level[level_name])}):")
                for alert in by_level[level_name]:
                    lines.append(f"  - {alert.message}")
                    if alert.recommended_action:
                        lines.append(f"    Action: {alert.recommended_action}")

        return "\n".join(lines)

    def get_critical_alerts(self) -> List[Alert]:
        """Get only critical and danger level alerts."""
        return [
            a
            for a in self.alerts
            if a.level in [AlertLevel.CRITICAL, AlertLevel.DANGER]
        ]

    def clear_alerts(self) -> None:
        """Clear all current alerts."""
        self.alerts = []

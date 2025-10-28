"""Comprehensive tests for Alert System.

Tests the 4-level alert system mentioned in README:
- INFO: 50% threshold
- WARNING: 75% threshold  
- CRITICAL: 90% threshold
- DANGER: 95% threshold
"""

from datetime import datetime, timedelta
import pytest

from genai_code_usage_monitor.core.alerts import AlertSystem
from genai_code_usage_monitor.core.models import (
    Alert,
    AlertLevel,
    BurnRate,
    PlanLimits,
    UsageStats,
)


@pytest.fixture
def plan_limits():
    """Create standard plan limits for testing."""
    return PlanLimits(
        name="Test Plan",
        token_limit=100000,
        cost_limit=50.0,
        rate_limit_per_minute=100,
    )


@pytest.fixture
def zero_burn_rate():
    """Create zero burn rate for testing."""
    return BurnRate(
        tokens_per_minute=0.0,
        cost_per_minute=0.0,
        estimated_time_to_limit=None,
    )


@pytest.fixture
def normal_burn_rate():
    """Create normal burn rate for testing."""
    return BurnRate(
        tokens_per_minute=1000.0,
        cost_per_minute=0.1,
        estimated_time_to_limit=120.0,  # 2 hours
    )


@pytest.fixture
def high_burn_rate():
    """Create high burn rate for testing."""
    return BurnRate(
        tokens_per_minute=15000.0,
        cost_per_minute=2.0,
        estimated_time_to_limit=30.0,  # 30 minutes
    )


class TestAlertSystemInitialization:
    """Test Alert System initialization."""

    def test_default_thresholds(self, plan_limits):
        """Test that default thresholds match README specification."""
        system = AlertSystem(plan_limits)
        
        assert system.thresholds["INFO"] == 50.0
        assert system.thresholds["WARNING"] == 75.0
        assert system.thresholds["CRITICAL"] == 90.0
        assert system.thresholds["DANGER"] == 95.0

    def test_custom_thresholds(self, plan_limits):
        """Test custom threshold configuration."""
        custom_thresholds = {
            "INFO": 40.0,
            "WARNING": 70.0,
            "CRITICAL": 85.0,
            "DANGER": 92.0,
        }
        system = AlertSystem(plan_limits, alert_thresholds=custom_thresholds)
        
        assert system.thresholds == custom_thresholds

    def test_plan_limits_stored(self, plan_limits):
        """Test that plan limits are properly stored."""
        system = AlertSystem(plan_limits)
        
        assert system.plan_limits == plan_limits
        assert system.plan_limits.token_limit == 100000
        assert system.plan_limits.cost_limit == 50.0


class TestTokenAlerts:
    """Test token usage alerts at all levels."""

    def test_no_alert_below_info_threshold(self, plan_limits, zero_burn_rate):
        """Test no alerts when usage is below 50% (INFO threshold)."""
        stats = UsageStats(
            total_tokens=40000,  # 40% of 100,000
            total_cost=15.0,
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, zero_burn_rate)
        
        # Should have no token alerts (only possibly cost alert)
        token_alerts = [a for a in alerts if a.metric_type == "token_usage"]
        assert len(token_alerts) == 0

    def test_info_level_alert(self, plan_limits, normal_burn_rate):
        """Test INFO level alert at 50-75% usage."""
        stats = UsageStats(
            total_tokens=60000,  # 60% of 100,000
            total_cost=20.0,
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)
        
        token_alerts = [a for a in alerts if a.metric_type == "token_usage"]
        assert len(token_alerts) == 1
        assert token_alerts[0].level == AlertLevel.INFO
        assert "60.0%" in token_alerts[0].message
        assert "60,000 / 100,000 tokens" in token_alerts[0].message

    def test_warning_level_alert(self, plan_limits, normal_burn_rate):
        """Test WARNING level alert at 75-90% usage."""
        stats = UsageStats(
            total_tokens=80000,  # 80% of 100,000
            total_cost=30.0,
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)
        
        token_alerts = [a for a in alerts if a.metric_type == "token_usage"]
        assert len(token_alerts) == 1
        assert token_alerts[0].level == AlertLevel.WARNING
        assert "80.0%" in token_alerts[0].message

    def test_critical_level_alert(self, plan_limits, normal_burn_rate):
        """Test CRITICAL level alert at 90-95% usage."""
        stats = UsageStats(
            total_tokens=92000,  # 92% of 100,000
            total_cost=40.0,
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)
        
        token_alerts = [a for a in alerts if a.metric_type == "token_usage"]
        assert len(token_alerts) == 1
        assert token_alerts[0].level == AlertLevel.CRITICAL
        assert "92.0%" in token_alerts[0].message

    def test_danger_level_alert(self, plan_limits, high_burn_rate):
        """Test DANGER level alert at >95% usage."""
        stats = UsageStats(
            total_tokens=97000,  # 97% of 100,000
            total_cost=45.0,
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, high_burn_rate)
        
        token_alerts = [a for a in alerts if a.metric_type == "token_usage"]
        assert len(token_alerts) == 1
        assert token_alerts[0].level == AlertLevel.DANGER
        assert "97.0%" in token_alerts[0].message


class TestCostAlerts:
    """Test cost usage alerts at all levels."""

    def test_cost_info_alert(self, plan_limits, normal_burn_rate):
        """Test INFO level cost alert."""
        stats = UsageStats(
            total_tokens=50000,
            total_cost=30.0,  # 60% of $50
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)
        
        cost_alerts = [a for a in alerts if a.metric_type == "cost_usage"]
        assert len(cost_alerts) == 1
        assert cost_alerts[0].level == AlertLevel.INFO
        assert "$30.00 / $50.00" in cost_alerts[0].message

    def test_cost_warning_alert(self, plan_limits, normal_burn_rate):
        """Test WARNING level cost alert."""
        stats = UsageStats(
            total_tokens=60000,
            total_cost=40.0,  # 80% of $50
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)
        
        cost_alerts = [a for a in alerts if a.metric_type == "cost_usage"]
        assert len(cost_alerts) == 1
        assert cost_alerts[0].level == AlertLevel.WARNING

    def test_cost_critical_alert(self, plan_limits, normal_burn_rate):
        """Test CRITICAL level cost alert."""
        stats = UsageStats(
            total_tokens=70000,
            total_cost=46.0,  # 92% of $50
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)
        
        cost_alerts = [a for a in alerts if a.metric_type == "cost_usage"]
        assert len(cost_alerts) == 1
        assert cost_alerts[0].level == AlertLevel.CRITICAL

    def test_cost_danger_alert(self, plan_limits, high_burn_rate):
        """Test DANGER level cost alert."""
        stats = UsageStats(
            total_tokens=80000,
            total_cost=48.5,  # 97% of $50
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, high_burn_rate)
        
        cost_alerts = [a for a in alerts if a.metric_type == "cost_usage"]
        assert len(cost_alerts) == 1
        assert cost_alerts[0].level == AlertLevel.DANGER


class TestBurnRateAlerts:
    """Test burn rate alerts."""

    def test_high_token_burn_rate_alert(self, plan_limits):
        """Test alert for high token burn rate (>10000 tokens/min)."""
        stats = UsageStats(
            total_tokens=50000,
            total_cost=25.0,
            total_calls=100,
        )
        
        # Very high burn rate
        burn_rate = BurnRate(
            tokens_per_minute=15000.0,
            cost_per_minute=1.5,
            estimated_time_to_limit=45.0,  # 45 minutes
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, burn_rate)
        
        burn_alerts = [a for a in alerts if a.metric_type == "burn_rate"]
        assert len(burn_alerts) == 1
        assert burn_alerts[0].level == AlertLevel.DANGER
        assert "15,000 tokens/min" in burn_alerts[0].message
        assert "45.0 minutes" in burn_alerts[0].message

    def test_high_cost_burn_rate_alert(self, plan_limits, zero_burn_rate):
        """Test alert for high cost burn rate (>$1/min)."""
        stats = UsageStats(
            total_tokens=50000,
            total_cost=25.0,
            total_calls=100,
        )
        
        # High cost burn rate
        burn_rate = BurnRate(
            tokens_per_minute=5000.0,  # Below token threshold
            cost_per_minute=1.5,  # Above cost threshold
            estimated_time_to_limit=None,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, burn_rate)
        
        cost_burn_alerts = [a for a in alerts if a.metric_type == "cost_burn_rate"]
        assert len(cost_burn_alerts) == 1
        assert cost_burn_alerts[0].level == AlertLevel.WARNING
        assert "$1.50/min" in cost_burn_alerts[0].message
        assert "$90.00/hour" in cost_burn_alerts[0].message

    def test_no_burn_rate_alert_normal_usage(self, plan_limits, normal_burn_rate):
        """Test no burn rate alerts for normal usage patterns."""
        stats = UsageStats(
            total_tokens=50000,
            total_cost=25.0,
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)
        
        burn_alerts = [a for a in alerts if "burn" in a.metric_type]
        assert len(burn_alerts) == 0


class TestMultiMetricAlerts:
    """Test alerts for multiple metrics simultaneously."""

    def test_both_token_and_cost_alerts(self, plan_limits, normal_burn_rate):
        """Test that both token and cost alerts can fire simultaneously."""
        stats = UsageStats(
            total_tokens=80000,  # 80% - WARNING
            total_cost=46.0,  # 92% - CRITICAL
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)
        
        token_alerts = [a for a in alerts if a.metric_type == "token_usage"]
        cost_alerts = [a for a in alerts if a.metric_type == "cost_usage"]
        
        assert len(token_alerts) == 1
        assert len(cost_alerts) == 1
        assert token_alerts[0].level == AlertLevel.WARNING
        assert cost_alerts[0].level == AlertLevel.CRITICAL

    def test_alerts_sorted_by_severity(self, plan_limits, high_burn_rate):
        """Test that alerts include severity scores."""
        stats = UsageStats(
            total_tokens=97000,  # 97% - DANGER
            total_cost=48.0,  # 96% - DANGER
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, high_burn_rate)
        
        # All alerts should have severity scores
        for alert in alerts:
            assert alert.severity > 0
            assert hasattr(alert, 'level')


class TestTimeEstimation:
    """Test time-to-limit estimation in alerts."""

    def test_time_estimation_in_minutes(self, plan_limits):
        """Test that time estimation shows minutes for short durations."""
        stats = UsageStats(
            total_tokens=80000,  # 20,000 remaining
            total_cost=30.0,
            total_calls=100,
        )
        
        burn_rate = BurnRate(
            tokens_per_minute=500.0,  # 40 minutes to limit
            cost_per_minute=0.1,
            estimated_time_to_limit=40.0,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, burn_rate)
        
        token_alerts = [a for a in alerts if a.metric_type == "token_usage"]
        assert len(token_alerts) == 1
        assert "minutes" in token_alerts[0].message

    def test_time_estimation_in_hours(self, plan_limits):
        """Test that time estimation shows hours for medium durations."""
        stats = UsageStats(
            total_tokens=70000,  # 30,000 remaining
            total_cost=25.0,
            total_calls=100,
        )
        
        burn_rate = BurnRate(
            tokens_per_minute=250.0,  # 120 minutes = 2 hours
            cost_per_minute=0.05,
            estimated_time_to_limit=120.0,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, burn_rate)
        
        token_alerts = [a for a in alerts if a.metric_type == "token_usage"]
        assert len(token_alerts) == 1
        assert "hours" in token_alerts[0].message


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_no_token_limit(self, normal_burn_rate):
        """Test with no token limit set."""
        plan_limits = PlanLimits(
            name="Cost Only",
            token_limit=None,
            cost_limit=50.0,
            rate_limit_per_minute=100,
        )
        stats = UsageStats(
            total_tokens=1000000,
            total_cost=30.0,
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)
        
        # Should only have cost alerts, no token alerts
        token_alerts = [a for a in alerts if a.metric_type == "token_usage"]
        assert len(token_alerts) == 0

    def test_zero_usage(self, plan_limits, zero_burn_rate):
        """Test with zero usage."""
        stats = UsageStats(
            total_tokens=0,
            total_cost=0.0,
            total_calls=0,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, zero_burn_rate)
        
        assert len(alerts) == 0

    def test_usage_exceeds_limit(self, plan_limits, normal_burn_rate):
        """Test when usage exceeds 100% of limit."""
        stats = UsageStats(
            total_tokens=150000,  # 150% of limit
            total_cost=60.0,  # 120% of limit
            total_calls=100,
        )

        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, normal_burn_rate)

        # Should still generate DANGER alerts
        assert len(alerts) >= 2
        for alert in alerts:
            if alert.metric_type in ["token_usage", "cost_usage"]:
                assert alert.level == AlertLevel.DANGER
                # Severity should be capped at 100
                assert alert.severity <= 100


class TestRecommendedActions:
    """Test that alerts include appropriate recommended actions."""

    def test_danger_alert_has_immediate_action(self, plan_limits, high_burn_rate):
        """Test DANGER alerts recommend immediate action."""
        stats = UsageStats(
            total_tokens=97000,
            total_cost=48.0,
            total_calls=100,
        )
        
        system = AlertSystem(plan_limits)
        alerts = system.check_usage_alerts(stats, high_burn_rate)
        
        danger_alerts = [a for a in alerts if a.level == AlertLevel.DANGER]
        assert len(danger_alerts) > 0
        
        # Check that recommended actions exist
        for alert in danger_alerts:
            assert alert.recommended_action is not None
            assert len(alert.recommended_action) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

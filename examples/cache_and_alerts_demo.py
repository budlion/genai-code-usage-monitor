"""
Demonstration of cache token calculation and multi-level alert system.

This example shows:
1. Creating cached token usage records
2. Using the enhanced pricing calculator for Claude models
3. Setting up and using the alert system
4. Predicting costs and remaining time
5. Getting session reset recommendations
"""

from datetime import datetime

from genai_code_usage_monitor.core.alerts import AlertSystem
from genai_code_usage_monitor.core.models import (
    Alert,
    AlertLevel,
    APICall,
    BurnRate,
    CachedTokenUsage,
    MonitorState,
    PlanLimits,
    TokenUsage,
    UsageStats,
)
from genai_code_usage_monitor.core.pricing import PricingCalculator


def demo_cached_tokens():
    """Demonstrate cached token cost calculation."""
    print("\n" + "=" * 60)
    print("CACHED TOKEN CALCULATION DEMO")
    print("=" * 60)

    # Initialize pricing calculator
    calc = PricingCalculator()

    # Example: Claude 3 Sonnet with cached tokens
    model = "claude-3-sonnet"
    prompt_tokens = 5000
    completion_tokens = 1000
    cached_tokens = 50000  # 50k tokens served from cache

    # Calculate cost with cache
    total_cost, savings = calc.calculate_cached_cost(
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cached_tokens=cached_tokens,
    )

    print(f"\nModel: {model}")
    print(f"Prompt tokens (new): {prompt_tokens:,}")
    print(f"Completion tokens: {completion_tokens:,}")
    print(f"Cached tokens: {cached_tokens:,}")
    print(f"\nTotal cost: ${total_cost:.4f}")
    print(f"Savings from cache: ${savings:.4f}")
    print(f"Cache hit rate: {cached_tokens / (cached_tokens + prompt_tokens) * 100:.1f}%")

    # Compare with non-cached cost
    regular_cost = calc.calculate_cost(
        model=model,
        prompt_tokens=prompt_tokens + cached_tokens,
        completion_tokens=completion_tokens,
    )
    print(f"\nWithout cache: ${regular_cost:.4f}")
    print(f"Total savings: ${regular_cost - total_cost:.4f} ({savings / regular_cost * 100:.1f}%)")

    # Create a CachedTokenUsage object
    cached_usage = CachedTokenUsage(
        cached_tokens=cached_tokens,
        cache_hit_rate=cached_tokens / (cached_tokens + prompt_tokens),
        savings=savings,
    )
    print(f"\nCachedTokenUsage object:")
    print(f"  - Cached tokens: {cached_usage.cached_tokens:,}")
    print(f"  - Hit rate: {cached_usage.cache_hit_percentage:.1f}%")
    print(f"  - Savings: ${cached_usage.savings:.4f}")


def demo_alert_levels():
    """Demonstrate alert level system."""
    print("\n" + "=" * 60)
    print("ALERT LEVEL SYSTEM DEMO")
    print("=" * 60)

    # Test different usage percentages
    test_percentages = [45, 60, 80, 92, 97]

    print("\nAlert levels for different usage percentages:")
    for percentage in test_percentages:
        level = AlertLevel.from_usage_percentage(percentage)
        print(f"  {percentage}% -> {level.formatted_message}")
        print(f"    Threshold: {level.threshold}%, Color: {level.color_code}XXX\033[0m")


def demo_alert_system():
    """Demonstrate the alert system."""
    print("\n" + "=" * 60)
    print("ALERT SYSTEM DEMO")
    print("=" * 60)

    # Set up plan limits
    plan_limits = PlanLimits(
        name="Professional Plan",
        token_limit=1_000_000,
        cost_limit=100.0,
        rate_limit_rpm=100,
    )

    # Initialize alert system
    alert_system = AlertSystem(plan_limits)

    # Simulate usage at different levels
    scenarios = [
        {
            "name": "Light usage (30%)",
            "tokens": 300_000,
            "cost": 30.0,
            "burn_rate": BurnRate(
                tokens_per_minute=100,
                cost_per_minute=0.01,
                calls_per_minute=5,
            ),
        },
        {
            "name": "Moderate usage (60%)",
            "tokens": 600_000,
            "cost": 60.0,
            "burn_rate": BurnRate(
                tokens_per_minute=500,
                cost_per_minute=0.05,
                calls_per_minute=10,
            ),
        },
        {
            "name": "Heavy usage (80%)",
            "tokens": 800_000,
            "cost": 80.0,
            "burn_rate": BurnRate(
                tokens_per_minute=2000,
                cost_per_minute=0.2,
                calls_per_minute=20,
            ),
        },
        {
            "name": "Critical usage (93%)",
            "tokens": 930_000,
            "cost": 93.0,
            "burn_rate": BurnRate(
                tokens_per_minute=5000,
                cost_per_minute=0.5,
                calls_per_minute=30,
                estimated_time_to_limit=14.0,
            ),
        },
    ]

    for scenario in scenarios:
        print(f"\n{scenario['name']}")
        print("-" * 40)

        stats = UsageStats(
            total_tokens=scenario["tokens"],
            total_cost=scenario["cost"],
            total_calls=100,
        )

        alerts = alert_system.check_usage_alerts(stats, scenario["burn_rate"])

        if alerts:
            for alert in alerts:
                print(f"  {alert.formatted_message}")
                if alert.recommended_action:
                    print(f"  Action: {alert.recommended_action}")
        else:
            print("  No alerts")


def demo_predictions():
    """Demonstrate cost and time predictions."""
    print("\n" + "=" * 60)
    print("PREDICTION DEMO")
    print("=" * 60)

    plan_limits = PlanLimits(
        name="Professional Plan",
        token_limit=1_000_000,
        cost_limit=100.0,
    )

    alert_system = AlertSystem(plan_limits)

    # Current burn rate
    burn_rate = BurnRate(
        tokens_per_minute=2500,
        cost_per_minute=0.25,
        calls_per_minute=10,
        confidence=0.85,
    )

    print("\nCurrent burn rate:")
    print(f"  Tokens: {burn_rate.tokens_per_minute:,.0f} tokens/min")
    print(f"  Cost: ${burn_rate.cost_per_minute:.2f}/min")
    print(f"  Confidence: {burn_rate.confidence * 100:.0f}%")

    # Predict costs for different time horizons
    time_horizons = [1, 4, 8, 24]
    print("\nCost predictions:")
    for hours in time_horizons:
        predicted_cost, confidence = alert_system.predict_cost(burn_rate, hours)
        print(f"  Next {hours:2d} hour(s): ${predicted_cost:6.2f} "
              f"(confidence: {confidence * 100:.0f}%)")

    # Predict tokens
    print("\nToken predictions:")
    for hours in time_horizons:
        predicted_tokens, confidence = alert_system.predict_tokens(burn_rate, hours)
        print(f"  Next {hours:2d} hour(s): {predicted_tokens:8,} tokens "
              f"(confidence: {confidence * 100:.0f}%)")


def demo_session_health():
    """Demonstrate session health scoring."""
    print("\n" + "=" * 60)
    print("SESSION HEALTH DEMO")
    print("=" * 60)

    plan_limits = PlanLimits(
        name="Professional Plan",
        token_limit=1_000_000,
        cost_limit=100.0,
    )

    alert_system = AlertSystem(plan_limits)

    # Different session states
    scenarios = [
        {
            "name": "Healthy session",
            "tokens": 200_000,
            "cost": 20.0,
            "tokens_per_min": 100,
            "cost_per_min": 0.01,
        },
        {
            "name": "Warning session",
            "tokens": 600_000,
            "cost": 60.0,
            "tokens_per_min": 1000,
            "cost_per_min": 0.1,
        },
        {
            "name": "Critical session",
            "tokens": 900_000,
            "cost": 90.0,
            "tokens_per_min": 5000,
            "cost_per_min": 0.5,
        },
    ]

    for scenario in scenarios:
        monitor_state = MonitorState(
            daily_stats=UsageStats(
                total_tokens=scenario["tokens"],
                total_cost=scenario["cost"],
            ),
            burn_rate=BurnRate(
                tokens_per_minute=scenario["tokens_per_min"],
                cost_per_minute=scenario["cost_per_min"],
            ),
            plan_limits=plan_limits,
        )

        health_score = alert_system.get_session_health_score(monitor_state)
        should_reset, reason = alert_system.should_reset_session(
            monitor_state.daily_stats, monitor_state
        )

        print(f"\n{scenario['name']}:")
        print(f"  Health score: {health_score:.1f}/100")
        print(f"  Should reset: {should_reset}")
        if should_reset:
            print(f"  Reason: {reason}")


def demo_complete_workflow():
    """Demonstrate complete workflow with all features."""
    print("\n" + "=" * 60)
    print("COMPLETE WORKFLOW DEMO")
    print("=" * 60)

    # Set up
    calc = PricingCalculator()
    plan_limits = PlanLimits(
        name="Professional Plan",
        token_limit=1_000_000,
        cost_limit=100.0,
    )
    alert_system = AlertSystem(plan_limits)

    # Simulate API call with cached tokens
    call = APICall(
        timestamp=datetime.now(),
        model="claude-3-sonnet",
        tokens=TokenUsage(prompt_tokens=3000, completion_tokens=1000),
        cost=0.0,  # Will calculate
        cached_tokens=CachedTokenUsage(
            cached_tokens=20000,
            cache_hit_rate=0.87,
            savings=0.54,
        ),
    )

    # Calculate actual cost
    total_cost, savings = calc.calculate_cached_cost(
        model=call.model,
        prompt_tokens=call.tokens.prompt_tokens,
        completion_tokens=call.tokens.completion_tokens,
        cached_tokens=call.cached_tokens.cached_tokens if call.cached_tokens else 0,
    )
    call.cost = total_cost

    # Update stats
    stats = UsageStats(total_tokens=850_000, total_cost=85.0)
    stats.update_from_call(call)

    # Calculate burn rate
    burn_rate = BurnRate(
        tokens_per_minute=3000,
        cost_per_minute=0.3,
        calls_per_minute=12,
        estimated_time_to_limit=50.0,
    )

    # Check alerts
    alerts = alert_system.check_usage_alerts(stats, burn_rate)

    # Display results
    print("\nAPI Call Summary:")
    print(f"  Model: {call.model}")
    print(f"  Regular tokens: {call.tokens.total_tokens:,}")
    if call.cached_tokens:
        print(f"  Cached tokens: {call.cached_tokens.cached_tokens:,}")
        print(f"  Cache savings: ${call.cached_tokens.savings:.4f}")
    print(f"  Cost: ${call.cost:.4f}")

    print(f"\nCurrent Usage:")
    print(f"  Total tokens: {stats.total_tokens:,} / {plan_limits.token_limit:,}")
    print(f"  Total cost: ${stats.total_cost:.2f} / ${plan_limits.cost_limit:.2f}")
    print(f"  Cache savings: ${stats.total_cache_savings:.4f}")

    print(f"\nBurn Rate:")
    print(f"  {burn_rate.tokens_per_minute:,.0f} tokens/min")
    print(f"  ${burn_rate.cost_per_minute:.2f}/min")
    if burn_rate.estimated_time_to_limit:
        print(f"  Time to limit: {burn_rate.estimated_time_to_limit:.1f} minutes")

    print(f"\nAlerts: {len(alerts)}")
    if alerts:
        print(alert_system.format_alert_summary())

    # Health check
    monitor_state = MonitorState(
        daily_stats=stats, burn_rate=burn_rate, plan_limits=plan_limits
    )
    health_score = alert_system.get_session_health_score(monitor_state)
    print(f"\nSession Health: {health_score:.1f}/100")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CODEX MONITOR: CACHE & ALERTS DEMO")
    print("=" * 60)

    demo_cached_tokens()
    demo_alert_levels()
    demo_alert_system()
    demo_predictions()
    demo_session_health()
    demo_complete_workflow()

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60 + "\n")

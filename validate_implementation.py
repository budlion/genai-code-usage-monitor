#!/usr/bin/env python3
"""
Validation script to verify the cache and alerts implementation.

This script validates that all new features are properly implemented
and working correctly.
"""

import sys
from datetime import datetime


def validate_models():
    """Validate models.py changes."""
    print("Validating models.py...")
    try:
        from src.codex_monitor.core.models import (
            CachedTokenUsage,
            AlertLevel,
            Alert,
            APICall,
            UsageStats,
            TokenUsage,
        )

        # Test CachedTokenUsage
        cached = CachedTokenUsage(
            cached_tokens=10000,
            cache_hit_rate=0.85,
            savings=0.27
        )
        assert cached.cached_tokens == 10000
        assert cached.cache_hit_percentage == 85.0
        print("  ✓ CachedTokenUsage works")

        # Test AlertLevel
        assert AlertLevel.INFO.threshold == 50.0
        assert AlertLevel.WARNING.threshold == 75.0
        assert AlertLevel.CRITICAL.threshold == 90.0
        assert AlertLevel.DANGER.threshold == 95.0

        level = AlertLevel.from_usage_percentage(85)
        assert level == AlertLevel.WARNING
        print("  ✓ AlertLevel works")

        # Test Alert
        alert = Alert(
            level=AlertLevel.WARNING,
            message="Test alert",
            severity=75,
            metric_type="usage",
            current_value=75000,
            threshold_value=100000,
        )
        assert alert.level == AlertLevel.WARNING
        assert not alert.is_critical
        print("  ✓ Alert works")

        # Test APICall with cached tokens
        call = APICall(
            timestamp=datetime.now(),
            model="claude-3-sonnet",
            tokens=TokenUsage(prompt_tokens=1000, completion_tokens=500),
            cost=0.01,
            cached_tokens=cached,
        )
        assert call.cached_tokens is not None
        assert call.cached_tokens.cached_tokens == 10000
        print("  ✓ APICall with cached tokens works")

        # Test UsageStats with cache fields
        stats = UsageStats(
            total_tokens=50000,
            total_cost=5.0,
            total_cached_tokens=10000,
            total_cache_savings=0.90,
        )
        assert stats.total_cached_tokens == 10000
        assert stats.total_cache_savings == 0.90
        print("  ✓ UsageStats with cache fields works")

        print("✓ All models validated successfully!\n")
        return True
    except Exception as e:
        print(f"✗ Models validation failed: {e}\n")
        return False


def validate_pricing():
    """Validate pricing.py changes."""
    print("Validating pricing.py...")
    try:
        from src.codex_monitor.core.pricing import PricingCalculator

        calc = PricingCalculator()

        # Test Claude model pricing exists
        claude_models = [
            "claude-3-opus",
            "claude-3-sonnet",
            "claude-3.5-sonnet",
            "claude-3-haiku",
            "claude-2.1",
            "claude-2.0",
        ]

        for model in claude_models:
            pricing = calc.get_model_pricing(model)
            assert "prompt" in pricing
            assert "completion" in pricing
            assert "cached_prompt" in pricing
            print(f"  ✓ {model} pricing exists")

        # Test cached cost calculation
        cost, savings = calc.calculate_cached_cost(
            model="claude-3-sonnet",
            prompt_tokens=5000,
            completion_tokens=1000,
            cached_tokens=20000,
        )
        assert cost > 0
        assert savings > 0
        assert savings < cost
        print(f"  ✓ Cached cost calculation works (cost: ${cost:.4f}, savings: ${savings:.4f})")

        # Test supports_caching
        assert calc.supports_caching("claude-3-sonnet") == True
        assert calc.supports_caching("gpt-4") == False
        print("  ✓ Cache support detection works")

        print("✓ All pricing validated successfully!\n")
        return True
    except Exception as e:
        print(f"✗ Pricing validation failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def validate_alerts():
    """Validate alerts.py implementation."""
    print("Validating alerts.py...")
    try:
        from src.codex_monitor.core.alerts import AlertSystem
        from src.codex_monitor.core.models import (
            PlanLimits,
            UsageStats,
            BurnRate,
            MonitorState,
        )

        # Create plan limits
        plan = PlanLimits(
            name="Test Plan",
            token_limit=1_000_000,
            cost_limit=100.0,
        )

        # Create alert system
        alert_system = AlertSystem(plan)
        print("  ✓ AlertSystem initialized")

        # Test usage alerts
        stats = UsageStats(total_tokens=800_000, total_cost=80.0)
        burn_rate = BurnRate(
            tokens_per_minute=2000,
            cost_per_minute=0.2,
            confidence=0.85,
        )

        alerts = alert_system.check_usage_alerts(stats, burn_rate)
        assert len(alerts) > 0
        print(f"  ✓ Generated {len(alerts)} alerts")

        # Test predictions
        predicted_cost, confidence = alert_system.predict_cost(burn_rate, hours_ahead=2)
        assert predicted_cost > 0
        assert 0 <= confidence <= 1
        print(f"  ✓ Cost prediction works (${predicted_cost:.2f} in 2 hours)")

        predicted_tokens, confidence = alert_system.predict_tokens(burn_rate, hours_ahead=2)
        assert predicted_tokens > 0
        print(f"  ✓ Token prediction works ({predicted_tokens:,} in 2 hours)")

        # Test session health
        monitor_state = MonitorState(
            daily_stats=stats,
            burn_rate=burn_rate,
            plan_limits=plan,
        )
        health = alert_system.get_session_health_score(monitor_state)
        assert 0 <= health <= 100
        print(f"  ✓ Session health score works ({health:.1f}/100)")

        # Test reset recommendation
        should_reset, reason = alert_system.should_reset_session(stats, monitor_state)
        assert isinstance(should_reset, bool)
        print(f"  ✓ Reset recommendation works (should_reset: {should_reset})")

        # Test alert formatting
        summary = alert_system.format_alert_summary()
        assert isinstance(summary, str)
        assert len(summary) > 0
        print("  ✓ Alert formatting works")

        # Test critical alerts filter
        critical = alert_system.get_critical_alerts()
        assert isinstance(critical, list)
        print(f"  ✓ Critical alerts filter works ({len(critical)} critical)")

        print("✓ All alerts validated successfully!\n")
        return True
    except Exception as e:
        print(f"✗ Alerts validation failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def validate_integration():
    """Validate complete integration."""
    print("Validating complete integration...")
    try:
        from src.codex_monitor.core.alerts import AlertSystem
        from src.codex_monitor.core.models import (
            APICall,
            CachedTokenUsage,
            PlanLimits,
            TokenUsage,
            UsageStats,
            BurnRate,
            MonitorState,
        )
        from src.codex_monitor.core.pricing import PricingCalculator

        # Setup
        calc = PricingCalculator()
        plan = PlanLimits(name="Test", token_limit=100_000, cost_limit=10.0)
        alert_system = AlertSystem(plan)

        # Create API call with cached tokens
        call = APICall(
            timestamp=datetime.now(),
            model="claude-3-sonnet",
            tokens=TokenUsage(prompt_tokens=1000, completion_tokens=500),
            cost=0.0,
            cached_tokens=CachedTokenUsage(
                cached_tokens=5000,
                cache_hit_rate=0.83,
                savings=0.135,
            ),
        )

        # Calculate cost
        cost, savings = calc.calculate_cached_cost(
            model=call.model,
            prompt_tokens=call.tokens.prompt_tokens,
            completion_tokens=call.tokens.completion_tokens,
            cached_tokens=call.cached_tokens.cached_tokens,
        )
        call.cost = cost

        # Update stats
        stats = UsageStats(total_tokens=85_000, total_cost=8.5)
        stats.update_from_call(call)

        # Check alerts
        burn_rate = BurnRate(tokens_per_minute=1000, cost_per_minute=0.1)
        alerts = alert_system.check_usage_alerts(stats, burn_rate)

        # Verify everything worked
        assert call.cost > 0
        assert stats.total_cached_tokens > 0
        assert stats.total_cache_savings > 0
        assert len(alerts) > 0

        print("  ✓ End-to-end workflow works")
        print(f"    - API call cost: ${call.cost:.4f}")
        print(f"    - Cache savings: ${savings:.4f}")
        print(f"    - Total cached tokens: {stats.total_cached_tokens:,}")
        print(f"    - Alerts generated: {len(alerts)}")

        print("✓ Integration validated successfully!\n")
        return True
    except Exception as e:
        print(f"✗ Integration validation failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validations."""
    print("=" * 60)
    print("VALIDATING CACHE & ALERTS IMPLEMENTATION")
    print("=" * 60 + "\n")

    results = []
    results.append(("Models", validate_models()))
    results.append(("Pricing", validate_pricing()))
    results.append(("Alerts", validate_alerts()))
    results.append(("Integration", validate_integration()))

    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name:20s} {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 ALL VALIDATIONS PASSED! Implementation is complete and working.\n")
        return 0
    else:
        print("\n⚠️  SOME VALIDATIONS FAILED. Please check the errors above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

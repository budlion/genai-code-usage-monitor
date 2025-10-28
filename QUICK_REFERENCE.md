# Quick Reference: Cache & Alerts

## 30-Second Quick Start

```python
from genai_code_usage_monitor.core.alerts import AlertSystem
from genai_code_usage_monitor.core.models import PlanLimits, UsageStats, BurnRate
from genai_code_usage_monitor.core.pricing import PricingCalculator

# 1. Setup
calc = PricingCalculator()
plan = PlanLimits(name="Pro", token_limit=1_000_000, cost_limit=100.0)
alerts = AlertSystem(plan)

# 2. Calculate cost with cache
cost, savings = calc.calculate_cached_cost(
    model="claude-3-sonnet",
    prompt_tokens=5000,
    completion_tokens=1000,
    cached_tokens=50000
)
print(f"Cost: ${cost:.4f}, Saved: ${savings:.4f}")

# 3. Check alerts
stats = UsageStats(total_tokens=850_000, total_cost=85.0)
burn_rate = BurnRate(tokens_per_minute=3000, cost_per_minute=0.3)
active_alerts = alerts.check_usage_alerts(stats, burn_rate)
print(alerts.format_alert_summary())
```

## Alert Thresholds

| Level | Threshold | Color | Action |
|-------|-----------|-------|--------|
| INFO | 50% | Blue | Monitor |
| WARNING | 75% | Yellow | Review |
| CRITICAL | 90% | Red | Plan reset |
| DANGER | 95% | Magenta | Reset NOW |

## Claude Pricing (per 1M tokens)

| Model | Prompt | Completion | Cached |
|-------|--------|------------|--------|
| Opus | $15 | $75 | $1.50 |
| Sonnet | $3 | $15 | $0.30 |
| Haiku | $0.25 | $1.25 | $0.025 |

## Common Tasks

### Check if model supports caching
```python
calc.supports_caching("claude-3-sonnet")  # True
```

### Get current alert level
```python
level = AlertLevel.from_usage_percentage(85)  # WARNING
```

### Predict future cost
```python
predicted, confidence = alerts.predict_cost(burn_rate, hours_ahead=4)
```

### Check session health
```python
health = alerts.get_session_health_score(monitor_state)  # 0-100
```

### Should reset?
```python
should_reset, reason = alerts.should_reset_session(stats, monitor_state)
```

## File Locations

- **Models**: `src/genai_code_usage_monitor/core/models.py`
- **Pricing**: `src/genai_code_usage_monitor/core/pricing.py`
- **Alerts**: `src/genai_code_usage_monitor/core/alerts.py`
- **Demo**: `examples/cache_and_alerts_demo.py`
- **Full Docs**: `docs/CACHE_AND_ALERTS.md`

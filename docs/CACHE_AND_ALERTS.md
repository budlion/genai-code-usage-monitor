# Cache Token Calculation and Multi-Level Alert System

This document describes the new caching token calculation and multi-level warning system implemented in the GenAI Code Usage Monitor.

## Overview

The system provides:
1. **Cached Token Tracking** - Monitor and calculate costs for cached tokens (90% discount)
2. **Multi-Level Alerts** - 4-tier alert system (INFO, WARNING, CRITICAL, DANGER)
3. **Real-Time Predictions** - Predict future costs and token usage
4. **Burn Rate Monitoring** - Track consumption rates and estimate time to limits
5. **Session Health Scoring** - Get health scores and reset recommendations

## Features

### 1. Cached Token Support

#### CachedTokenUsage Model

Tracks cached token usage with the following fields:

```python
from genai_code_usage_monitor.core.models import CachedTokenUsage

cached = CachedTokenUsage(
    cached_tokens=50000,        # Number of cached tokens used
    cache_hit_rate=0.87,        # Cache hit rate (0-1)
    savings=0.54                # Cost savings in USD
)

print(f"Cache hit: {cached.cache_hit_percentage:.1f}%")  # 87.0%
```

#### Pricing Calculator Enhancements

The `PricingCalculator` now supports:
- Claude model pricing (Opus, Sonnet, Haiku, 2.0, 2.1, 3.5)
- 90% discount for cached tokens
- Cost savings calculation

```python
from genai_code_usage_monitor.core.pricing import PricingCalculator

calc = PricingCalculator()

# Calculate cost with cached tokens
total_cost, savings = calc.calculate_cached_cost(
    model="claude-3-sonnet",
    prompt_tokens=5000,          # New tokens
    completion_tokens=1000,      # Response tokens
    cached_tokens=50000          # Cached tokens
)

print(f"Total cost: ${total_cost:.4f}")
print(f"Savings: ${savings:.4f}")

# Check if model supports caching
if calc.supports_caching("claude-3-sonnet"):
    print("Model supports caching!")
```

#### Claude Model Pricing

| Model | Prompt (per 1M) | Completion (per 1M) | Cached Prompt (per 1M) |
|-------|----------------|---------------------|------------------------|
| Claude 3 Opus | $15.00 | $75.00 | $1.50 (90% off) |
| Claude 3 Sonnet | $3.00 | $15.00 | $0.30 (90% off) |
| Claude 3.5 Sonnet | $3.00 | $15.00 | $0.30 (90% off) |
| Claude 3 Haiku | $0.25 | $1.25 | $0.025 (90% off) |
| Claude 2.1 | $8.00 | $24.00 | $0.80 (90% off) |
| Claude 2.0 | $8.00 | $24.00 | $0.80 (90% off) |

### 2. Multi-Level Alert System

#### Alert Levels

Four alert levels based on usage percentage:

```python
from genai_code_usage_monitor.core.models import AlertLevel

# Alert thresholds
INFO = 50%      # Blue - Informational
WARNING = 75%   # Yellow - Monitor closely
CRITICAL = 90%  # Red - Plan to reset
DANGER = 95%    # Magenta - Immediate action required
```

Each alert level has:
- `threshold`: Usage percentage that triggers the level
- `color_code`: ANSI color code for terminal display
- `formatted_message`: Color-coded message output

```python
level = AlertLevel.from_usage_percentage(92)
print(level)  # AlertLevel.CRITICAL
print(level.threshold)  # 90.0
print(level.formatted_message)  # Color-coded output
```

#### Alert Model

```python
from genai_code_usage_monitor.core.models import Alert, AlertLevel
from datetime import datetime

alert = Alert(
    level=AlertLevel.WARNING,
    message="Cost usage at 78.5%",
    timestamp=datetime.now(),
    severity=78,
    metric_type="cost_usage",
    current_value=78.50,
    threshold_value=75.0,
    recommended_action="Monitor usage closely. Consider implementing rate limiting."
)

print(alert.formatted_message)  # Color-coded output
print(f"Is critical: {alert.is_critical}")  # False
```

### 3. Alert System

The `AlertSystem` class provides comprehensive monitoring and alerting:

```python
from genai_code_usage_monitor.core.alerts import AlertSystem
from genai_code_usage_monitor.core.models import PlanLimits, UsageStats, BurnRate

# Set up plan limits
plan_limits = PlanLimits(
    name="Professional Plan",
    token_limit=1_000_000,
    cost_limit=100.0
)

# Initialize alert system
alert_system = AlertSystem(plan_limits)

# Current usage
stats = UsageStats(
    total_tokens=850_000,
    total_cost=85.0
)

# Current burn rate
burn_rate = BurnRate(
    tokens_per_minute=3000,
    cost_per_minute=0.3,
    estimated_time_to_limit=50.0
)

# Check for alerts
alerts = alert_system.check_usage_alerts(stats, burn_rate)

# Display alerts
print(alert_system.format_alert_summary())

# Get only critical alerts
critical_alerts = alert_system.get_critical_alerts()
```

#### Alert Types

The system monitors:

1. **Token Usage Alerts**
   - Triggered when token usage exceeds thresholds (50%, 75%, 90%, 95%)
   - Includes time-to-limit estimation
   - Provides actionable recommendations

2. **Cost Usage Alerts**
   - Triggered when cost exceeds thresholds
   - Estimates remaining time based on burn rate
   - Suggests optimization strategies

3. **Burn Rate Alerts**
   - High token consumption (>10,000 tokens/min)
   - High cost burn rate (>$1/min)
   - Rapid consumption warnings

### 4. Real-Time Predictions

#### Cost Prediction

```python
# Predict cost for next N hours
predicted_cost, confidence = alert_system.predict_cost(
    burn_rate=burn_rate,
    hours_ahead=4.0
)

print(f"Predicted cost in 4 hours: ${predicted_cost:.2f}")
print(f"Confidence: {confidence * 100:.0f}%")
```

#### Token Prediction

```python
# Predict token usage for next N hours
predicted_tokens, confidence = alert_system.predict_tokens(
    burn_rate=burn_rate,
    hours_ahead=4.0
)

print(f"Predicted tokens in 4 hours: {predicted_tokens:,}")
print(f"Confidence: {confidence * 100:.0f}%")
```

### 5. Session Management

#### Session Health Score

Get a health score (0-100) for the current session:

```python
from genai_code_usage_monitor.core.models import MonitorState

monitor_state = MonitorState(
    daily_stats=stats,
    burn_rate=burn_rate,
    plan_limits=plan_limits
)

health_score = alert_system.get_session_health_score(monitor_state)
print(f"Session Health: {health_score:.1f}/100")

# 100 = Healthy
# 60-80 = Monitor
# 30-60 = Warning
# 0-30 = Critical
```

#### Session Reset Recommendations

Automatically determine if session should be reset:

```python
should_reset, reason = alert_system.should_reset_session(
    current_stats=stats,
    monitor_state=monitor_state
)

if should_reset:
    print(f"RECOMMENDATION: Reset session")
    print(f"Reason: {reason}")
```

Reset is recommended when:
- DANGER level alert is triggered
- Approaching limits (>90%) with high burn rate
- Less than 30 minutes until limit reached

### 6. Enhanced Usage Statistics

The `UsageStats` model now tracks cache statistics:

```python
stats = UsageStats(
    total_tokens=100_000,
    total_cost=10.0,
    total_cached_tokens=50_000,      # NEW: Total cached tokens
    total_cache_savings=4.50          # NEW: Total savings from cache
)

# Calculate average cache hit rate
hit_rate = stats.average_cache_hit_rate
print(f"Average cache hit rate: {hit_rate * 100:.1f}%")

# Update from API call with cached tokens
from genai_code_usage_monitor.core.models import APICall, TokenUsage, CachedTokenUsage

call = APICall(
    timestamp=datetime.now(),
    model="claude-3-sonnet",
    tokens=TokenUsage(prompt_tokens=5000, completion_tokens=1000),
    cost=0.06,
    cached_tokens=CachedTokenUsage(
        cached_tokens=20000,
        cache_hit_rate=0.8,
        savings=0.54
    )
)

stats.update_from_call(call)  # Automatically updates cache stats
```

## Usage Examples

### Example 1: Basic Cache Tracking

```python
from genai_code_usage_monitor.core.pricing import PricingCalculator
from genai_code_usage_monitor.core.models import CachedTokenUsage

calc = PricingCalculator()

# API call with cached tokens
model = "claude-3-sonnet"
prompt_tokens = 3000
completion_tokens = 1000
cached_tokens = 20000

# Calculate cost
total_cost, savings = calc.calculate_cached_cost(
    model=model,
    prompt_tokens=prompt_tokens,
    completion_tokens=completion_tokens,
    cached_tokens=cached_tokens
)

# Create cache usage record
cache_usage = CachedTokenUsage(
    cached_tokens=cached_tokens,
    cache_hit_rate=cached_tokens / (cached_tokens + prompt_tokens),
    savings=savings
)

print(f"Cost: ${total_cost:.4f} (Saved: ${savings:.4f})")
print(f"Cache hit rate: {cache_usage.cache_hit_percentage:.1f}%")
```

### Example 2: Complete Monitoring Setup

```python
from genai_code_usage_monitor.core.alerts import AlertSystem
from genai_code_usage_monitor.core.models import (
    PlanLimits, UsageStats, BurnRate, MonitorState
)

# Set up monitoring
plan_limits = PlanLimits(
    name="Professional",
    token_limit=1_000_000,
    cost_limit=100.0
)

alert_system = AlertSystem(plan_limits)

# Current state
stats = UsageStats(total_tokens=850_000, total_cost=85.0)
burn_rate = BurnRate(
    tokens_per_minute=3000,
    cost_per_minute=0.3,
    estimated_time_to_limit=50.0,
    confidence=0.85
)

# Check alerts
alerts = alert_system.check_usage_alerts(stats, burn_rate)

# Display status
print(alert_system.format_alert_summary())

# Predictions
predicted_cost, conf = alert_system.predict_cost(burn_rate, hours_ahead=4)
print(f"\nPredicted cost in 4 hours: ${predicted_cost:.2f} ({conf*100:.0f}% confidence)")

# Health check
monitor_state = MonitorState(
    daily_stats=stats,
    burn_rate=burn_rate,
    plan_limits=plan_limits
)

health = alert_system.get_session_health_score(monitor_state)
should_reset, reason = alert_system.should_reset_session(stats, monitor_state)

print(f"\nSession Health: {health:.1f}/100")
if should_reset:
    print(f"⚠️  RECOMMENDATION: Reset session - {reason}")
```

### Example 3: Alert Response Handling

```python
# Check alerts and take action
alerts = alert_system.check_usage_alerts(stats, burn_rate)

for alert in alerts:
    print(alert.formatted_message)

    if alert.is_critical:
        # Critical or danger level
        print(f"⚠️  {alert.recommended_action}")

        if alert.level == AlertLevel.DANGER:
            # Immediate action required
            print("🚨 STOPPING CURRENT SESSION")
            # Implement session stop logic

    elif alert.level == AlertLevel.WARNING:
        # Warning level - monitor closely
        print(f"ℹ️  {alert.recommended_action}")

    else:
        # Info level - just log
        print(f"📊 {alert.message}")
```

## API Reference

### Models

#### CachedTokenUsage
- `cached_tokens: int` - Number of cached tokens
- `cache_hit_rate: float` - Hit rate (0-1)
- `savings: float` - Cost savings in USD
- `cache_hit_percentage: float` - Hit rate as percentage (property)

#### AlertLevel (Enum)
- `INFO` - 50% threshold
- `WARNING` - 75% threshold
- `CRITICAL` - 90% threshold
- `DANGER` - 95% threshold

Methods:
- `from_usage_percentage(percentage)` - Get level from percentage
- `threshold` - Get threshold percentage (property)
- `color_code` - Get ANSI color code (property)

#### Alert
- `level: AlertLevel` - Alert severity level
- `message: str` - Alert message
- `timestamp: datetime` - When alert was created
- `severity: int` - Severity score (0-100)
- `metric_type: str` - Type of metric (usage, cost, rate)
- `current_value: float` - Current metric value
- `threshold_value: float` - Threshold that was exceeded
- `recommended_action: Optional[str]` - Recommended action

Properties:
- `is_critical: bool` - True if CRITICAL or DANGER
- `formatted_message: str` - Color-coded message

### PricingCalculator

#### Methods

**calculate_cached_cost(model, prompt_tokens, completion_tokens, cached_tokens=0)**
- Calculate cost with cached tokens
- Returns: `tuple[float, float]` - (total_cost, savings)

**supports_caching(model)**
- Check if model supports caching
- Returns: `bool`

**get_model_pricing(model)**
- Get pricing for a model
- Returns: `dict` with prompt, completion, and optional cached_prompt prices

### AlertSystem

#### Methods

**check_usage_alerts(current_stats, burn_rate)**
- Check for usage alerts
- Returns: `List[Alert]`

**predict_cost(burn_rate, hours_ahead=1.0)**
- Predict future cost
- Returns: `tuple[float, float]` - (predicted_cost, confidence)

**predict_tokens(burn_rate, hours_ahead=1.0)**
- Predict future token usage
- Returns: `tuple[int, float]` - (predicted_tokens, confidence)

**should_reset_session(current_stats, monitor_state)**
- Check if session should be reset
- Returns: `tuple[bool, str]` - (should_reset, reason)

**get_session_health_score(monitor_state)**
- Calculate session health score
- Returns: `float` - Score from 0-100

**format_alert_summary()**
- Format all alerts as string
- Returns: `str`

**get_critical_alerts()**
- Get only critical/danger alerts
- Returns: `List[Alert]`

**clear_alerts()**
- Clear all current alerts

## Best Practices

1. **Monitor Cache Hit Rates**
   - Track cache hit rates over time
   - Optimize prompts for better caching
   - Use cached tokens for repeated queries

2. **Respond to Alerts Promptly**
   - INFO: Monitor and log
   - WARNING: Review usage patterns
   - CRITICAL: Plan session reset
   - DANGER: Take immediate action

3. **Use Predictions**
   - Check predicted costs before long operations
   - Estimate remaining time regularly
   - Plan breaks based on burn rate

4. **Session Management**
   - Check health score periodically
   - Follow reset recommendations
   - Don't exceed DANGER threshold

5. **Custom Thresholds**
   - Adjust thresholds based on your needs
   - Use stricter limits for production
   - Set up custom alerts for specific scenarios

## Troubleshooting

### Cache Not Working
- Verify model supports caching: `calc.supports_caching(model)`
- Check Claude model name matches exactly
- Ensure cached_tokens is passed correctly

### No Alerts Triggered
- Verify plan limits are set
- Check usage is being tracked correctly
- Confirm burn rate is calculated

### Inaccurate Predictions
- Low confidence indicates insufficient data
- Burn rate needs stable measurement period
- Check for outlier API calls

## Future Enhancements

Planned features:
- Historical alert tracking and analysis
- Email/webhook notifications
- Custom alert rules and conditions
- Multi-session aggregation
- Advanced caching analytics
- Auto-scaling recommendations

## See Also

- [Main Documentation](../README.md)
- [Example Usage](../examples/cache_and_alerts_demo.py)
- [API Reference](API_REFERENCE.md)
- [Pricing Guide](PRICING_GUIDE.md)

# Platform Abstraction Layer - Quick Reference

## Installation

```bash
# The platform layer is included in the package
pip install -e .
```

## Basic Usage

### Import

```python
from genai_code_usage_monitor.platforms import CodexPlatform, ClaudePlatform
```

### Initialize Platforms

```python
# OpenAI Codex (default: ~/.genai-code-usage-monitor/)
codex = CodexPlatform()

# Claude Code (default: ~/.claude-monitor/)
claude = ClaudePlatform()

# Custom storage location
codex = CodexPlatform(data_directory="/custom/path")
```

## Core Methods

### 1. Get Usage Data

```python
stats = platform.get_usage_data()
# Returns: UsageStats with total_tokens, total_cost, total_calls
```

### 2. Get Session Info

```python
session = platform.get_session_info()
# Returns: Optional[SessionData] with session details
```

### 3. Calculate Cost

```python
# Regular tokens
cost = platform.calculate_cost(10000, "gpt-4", is_prompt=True)

# Cached tokens (Claude only)
cost = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)
```

### 4. Get Platform Name

```python
name = platform.get_platform_name()
# Returns: "OpenAI Codex" or "Claude Code"
```

## Platform-Specific Methods

### CodexPlatform

```python
# Log API call
call = codex.log_api_call(
    model="gpt-4",
    prompt_tokens=100,
    completion_tokens=50
)

# Get usage summary
summary = codex.get_usage_summary()
# Returns: {"today": {...}, "week": {...}, "month": {...}}
```

### ClaudePlatform

```python
# Log API call with caching
call = claude.log_api_call(
    model="claude-sonnet-4",
    prompt_tokens=100,
    completion_tokens=50,
    cached_tokens=1000  # 90% discount
)

# Get usage summary
summary = claude.get_usage_summary()
```

## Pricing Reference

### OpenAI Codex (per 1M tokens)

| Model | Prompt | Completion |
|-------|--------|------------|
| GPT-4 | $30.00 | $60.00 |
| GPT-4 Turbo | $10.00 | $30.00 |
| GPT-3.5 Turbo | $0.50 | $1.50 |

### Claude Code (per 1M tokens)

| Model | Prompt | Completion | Cached |
|-------|--------|------------|--------|
| Sonnet 4 | $3.00 | $15.00 | $0.30 |
| Opus 3 | $15.00 | $75.00 | $1.50 |

**Note**: Cached tokens receive 90% discount on Claude

## Cost Examples

```python
# 10,000 tokens on GPT-4 (prompt)
codex.calculate_cost(10000, "gpt-4", is_prompt=True)
# → $0.3000

# 10,000 tokens on Claude Sonnet (regular prompt)
claude.calculate_cost(10000, "claude-sonnet-4", is_prompt=True)
# → $0.0300

# 10,000 tokens on Claude Sonnet (cached)
claude.calculate_cost(10000, "claude-sonnet-4", is_cached=True)
# → $0.0030 (90% discount!)
```

## Usage Stats Structure

```python
stats = platform.get_usage_data()

# Available fields:
stats.total_tokens      # int: Total tokens used
stats.total_cost        # float: Total cost in USD
stats.total_calls       # int: Number of API calls
stats.prompt_tokens     # int: Prompt tokens
stats.completion_tokens # int: Completion tokens
stats.models            # dict: Model -> token count mapping
stats.date              # datetime: Stats date
stats.api_calls         # list: Individual API call records
```

## Session Data Structure

```python
session = platform.get_session_info()

# Available fields (if session exists):
session.session_id      # str: Unique session ID
session.start_time      # datetime: Session start
session.end_time        # datetime: Session end
session.total_tokens    # int: Total tokens in session
session.total_cost      # float: Total cost in session
session.api_calls       # list: All API calls
session.models_used     # dict: Model usage counts
session.is_active       # bool: Whether session is active
session.duration        # float: Session duration in seconds
```

## Common Patterns

### Compare Platforms

```python
platforms = [CodexPlatform(), ClaudePlatform()]

for platform in platforms:
    cost = platform.calculate_cost(100000, "default")
    print(f"{platform.get_platform_name()}: ${cost:.2f}")
```

### Track Daily Usage

```python
def check_daily_usage(platform):
    stats = platform.get_usage_data()
    print(f"Today: {stats.total_tokens:,} tokens (${stats.total_cost:.2f})")

check_daily_usage(codex)
check_daily_usage(claude)
```

### Calculate Cache Savings (Claude)

```python
regular = claude.calculate_cost(100000, "claude-sonnet-4", is_prompt=True)
cached = claude.calculate_cost(100000, "claude-sonnet-4", is_cached=True)
savings = regular - cached

print(f"Regular: ${regular:.2f}")
print(f"Cached: ${cached:.2f}")
print(f"Savings: ${savings:.2f} (90%)")
```

### Get Model Information

```python
info = platform.get_model_info("claude-sonnet-4")

print(f"Model: {info['name']}")
print(f"Prompt: ${info['prompt_price_per_1m']:.2f}/1M")
print(f"Completion: ${info['completion_price_per_1m']:.2f}/1M")

# Claude-specific
if 'cached_prompt_price_per_1m' in info:
    print(f"Cached: ${info['cached_prompt_price_per_1m']:.2f}/1M")
```

## Error Handling

```python
try:
    stats = platform.get_usage_data()
except RuntimeError as e:
    print(f"Error accessing data: {e}")
except FileNotFoundError:
    print("No data files found yet")
except ValueError as e:
    print(f"Invalid parameter: {e}")
```

## Testing

```bash
# Run demo
python examples/platform_demo.py

# Run tests
pytest tests/test_platforms.py -v --no-cov

# Run specific test class
pytest tests/test_platforms.py::TestClaudePlatform -v
```

## Files Overview

```
src/genai_code_usage_monitor/platforms/
├── __init__.py          # Public API
├── base.py              # Abstract Platform class
├── codex.py             # OpenAI Codex adapter
├── claude.py            # Claude Code adapter
└── README.md            # Full documentation

examples/
└── platform_demo.py     # Demo script

tests/
└── test_platforms.py    # Unit tests
```

## Key Differences Between Platforms

| Feature | CodexPlatform | ClaudePlatform |
|---------|--------------|----------------|
| Default Storage | ~/.genai-code-usage-monitor/ | ~/.claude-monitor/ |
| Prompt Caching | ❌ No | ✅ Yes (90% discount) |
| Cache Parameter | Ignored | Required for discount |
| Pricing Model | Prompt/Completion | Prompt/Completion/Cached |
| Models | GPT-3.5, GPT-4 | Sonnet, Opus |
| Integration | UsageTracker | Custom storage |

## Tips

1. **Use caching with Claude**: Pass `is_cached=True` to get 90% discount
2. **Custom directories**: Use for testing or multi-environment setups
3. **Check session info**: Returns `None` if no data available
4. **Model names**: Use exact names for accurate pricing
5. **Error handling**: Always wrap in try-except for production

## Quick Links

- Full Documentation: `src/genai_code_usage_monitor/platforms/README.md`
- Demo Script: `examples/platform_demo.py`
- Tests: `tests/test_platforms.py`
- Summary: `PLATFORM_LAYER_SUMMARY.md`

## Support

For issues or questions about the platform abstraction layer:
1. Check the README: `src/genai_code_usage_monitor/platforms/README.md`
2. Run the demo: `python examples/platform_demo.py`
3. Review tests: `tests/test_platforms.py`

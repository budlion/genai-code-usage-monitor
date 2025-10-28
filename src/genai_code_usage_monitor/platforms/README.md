# Platform Abstraction Layer

A unified interface for tracking usage and costs across multiple AI platforms (OpenAI Codex and Claude Code).

## Overview

The platform abstraction layer provides a consistent API for working with different AI platforms, each with their own pricing models, token systems, and data storage formats.

## Architecture

```
platforms/
├── __init__.py       # Public API exports
├── base.py           # Abstract Platform interface
├── codex.py          # OpenAI Codex implementation
└── claude.py         # Claude Code implementation
```

## Key Features

- **Unified Interface**: All platforms implement the same `Platform` abstract base class
- **Type Safety**: Full Pydantic validation for all data models
- **Platform-Specific Features**: Support for unique features like Claude's prompt caching
- **Flexible Storage**: Customizable data directories for each platform
- **Comprehensive Docstrings**: Detailed documentation with examples

## Platform Interface

All platform adapters implement these core methods:

### Core Methods

```python
class Platform(ABC):
    @abstractmethod
    def get_usage_data(self) -> UsageStats:
        """Get current usage statistics"""

    @abstractmethod
    def get_session_info(self) -> Optional[SessionData]:
        """Get current session information"""

    @abstractmethod
    def calculate_cost(self, tokens: int, model: str,
                      is_prompt: bool = True,
                      is_cached: bool = False) -> float:
        """Calculate cost for token usage"""

    @abstractmethod
    def get_platform_name(self) -> str:
        """Get platform name"""
```

## Supported Platforms

### 1. OpenAI Codex (`CodexPlatform`)

**Models Supported:**
- GPT-4 (all variants)
- GPT-3.5 Turbo
- Legacy Codex models

**Features:**
- Integration with existing `UsageTracker` and `PricingCalculator`
- Separate pricing for prompt and completion tokens
- Default storage: `~/.genai-code-usage-monitor/`

**Example:**
```python
from genai_code_usage_monitor.platforms import CodexPlatform

platform = CodexPlatform()

# Get usage statistics
stats = platform.get_usage_data()
print(f"Total cost: ${stats.total_cost:.2f}")

# Calculate cost for a specific model
cost = platform.calculate_cost(10000, "gpt-4", is_prompt=True)
print(f"Cost for 10K tokens: ${cost:.4f}")

# Log an API call
call = platform.log_api_call("gpt-4", prompt_tokens=100, completion_tokens=50)
```

**Pricing (per 1M tokens):**
- GPT-4: $30 (prompt) / $60 (completion)
- GPT-4 Turbo: $10 (prompt) / $30 (completion)
- GPT-3.5 Turbo: $0.50 (prompt) / $1.50 (completion)

### 2. Claude Code (`ClaudePlatform`)

**Models Supported:**
- Claude Sonnet 4 / 3.5
- Claude Opus 3

**Features:**
- **Prompt Caching**: 90% discount on cached prompt tokens
- Extended context windows (up to 200K tokens)
- Default storage: `~/.claude-monitor/`

**Example:**
```python
from genai_code_usage_monitor.platforms import ClaudePlatform

platform = ClaudePlatform()

# Regular prompt tokens
cost1 = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=True)
print(f"Regular: ${cost1:.4f}")  # $0.0300

# Cached prompt tokens (90% discount)
cost2 = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)
print(f"Cached: ${cost2:.4f}")   # $0.0030

# Log an API call with caching
call = platform.log_api_call(
    "claude-sonnet-4",
    prompt_tokens=1000,
    completion_tokens=500,
    cached_tokens=5000  # 90% discount applied
)
```

**Pricing (per 1M tokens):**
- Claude Sonnet: $3 (prompt) / $15 (completion) / $0.30 (cached)
- Claude Opus: $15 (prompt) / $75 (completion) / $1.50 (cached)

## Usage Examples

### Basic Usage

```python
from genai_code_usage_monitor.platforms import CodexPlatform, ClaudePlatform

# Initialize platforms
codex = CodexPlatform()
claude = ClaudePlatform()

# Get usage from both platforms
codex_stats = codex.get_usage_data()
claude_stats = claude.get_usage_data()

print(f"Codex cost: ${codex_stats.total_cost:.2f}")
print(f"Claude cost: ${claude_stats.total_cost:.2f}")
```

### Working with Multiple Platforms

```python
from genai_code_usage_monitor.platforms import CodexPlatform, ClaudePlatform

platforms = [
    CodexPlatform(),
    ClaudePlatform(),
]

# Compare costs across platforms
for platform in platforms:
    cost = platform.calculate_cost(100000, "default", is_prompt=True)
    print(f"{platform.get_platform_name()}: ${cost:.4f}")
```

### Custom Storage Locations

```python
from genai_code_usage_monitor.platforms import CodexPlatform, ClaudePlatform

# Use custom data directories
codex = CodexPlatform(data_directory="/custom/path/codex")
claude = ClaudePlatform(data_directory="/custom/path/claude")
```

### Session Tracking

```python
from genai_code_usage_monitor.platforms import ClaudePlatform

platform = ClaudePlatform()

# Get current session info
session = platform.get_session_info()

if session:
    print(f"Session: {session.session_id}")
    print(f"Duration: {session.duration:.0f} seconds")
    print(f"Total cost: ${session.total_cost:.4f}")
    print(f"Models used: {list(session.models_used.keys())}")
```

### Getting Model Information

```python
from genai_code_usage_monitor.platforms import ClaudePlatform

platform = ClaudePlatform()

# Get detailed model info
info = platform.get_model_info("claude-sonnet-4")

print(f"Model: {info['name']}")
print(f"Prompt price: ${info['prompt_price_per_1m']:.2f}")
print(f"Cached price: ${info['cached_prompt_price_per_1m']:.2f}")
print(f"Cache discount: {info['cache_discount']}")
```

## Data Models

All platforms use consistent Pydantic models from `genai_code_usage_monitor.core.models`:

### UsageStats
```python
class UsageStats(BaseModel):
    total_tokens: int
    total_cost: float
    total_calls: int
    prompt_tokens: int
    completion_tokens: int
    models: Dict[str, int]
    date: Optional[datetime]
    api_calls: List[APICall]
```

### SessionData
```python
class SessionData(BaseModel):
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    total_tokens: int
    total_cost: float
    api_calls: List[APICall]
    models_used: Dict[str, int]
```

### APICall
```python
class APICall(BaseModel):
    timestamp: datetime
    model: str
    tokens: TokenUsage
    cost: float
    request_id: Optional[str]
    status: str
    error: Optional[str]
```

## Adding New Platforms

To add support for a new AI platform:

1. Create a new file (e.g., `gemini.py`)
2. Inherit from the `Platform` base class
3. Implement all abstract methods
4. Add platform-specific features
5. Export from `__init__.py`

Example:
```python
from genai_code_usage_monitor.platforms.base import Platform

class GeminiPlatform(Platform):
    def get_usage_data(self) -> UsageStats:
        # Implementation

    def get_session_info(self) -> Optional[SessionData]:
        # Implementation

    def calculate_cost(self, tokens: int, model: str,
                      is_prompt: bool = True,
                      is_cached: bool = False) -> float:
        # Implementation

    def get_platform_name(self) -> str:
        return "Google Gemini"
```

## Error Handling

All platforms raise consistent exceptions:

- `RuntimeError`: Unable to access or parse data files
- `FileNotFoundError`: Required data files are missing
- `ValueError`: Invalid model names or parameters
- `ValidationError`: Pydantic validation failures

Example:
```python
from genai_code_usage_monitor.platforms import ClaudePlatform

platform = ClaudePlatform()

try:
    stats = platform.get_usage_data()
except RuntimeError as e:
    print(f"Error accessing usage data: {e}")
except FileNotFoundError as e:
    print(f"Data files not found: {e}")
```

## Testing

Run the demo script to test the platform abstraction layer:

```bash
python examples/platform_demo.py
```

## Best Practices

1. **Use Type Hints**: All methods use proper type hints for IDE support
2. **Handle Missing Data**: Check for `None` when getting session info
3. **Custom Storage**: Use custom directories in production environments
4. **Error Handling**: Always wrap platform calls in try-except blocks
5. **Model Names**: Use exact model names for accurate pricing

## Future Enhancements

Potential improvements for the platform abstraction layer:

- [ ] Add support for Google Gemini
- [ ] Add support for AWS Bedrock
- [ ] Implement rate limiting per platform
- [ ] Add async/await support for concurrent operations
- [ ] Implement platform-specific health checks
- [ ] Add automatic platform detection
- [ ] Support for batch cost calculations
- [ ] Historical usage comparison across platforms

## License

This module is part of the genai-code-usage-monitor project and follows the same license.

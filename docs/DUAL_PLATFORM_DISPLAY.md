# Dual-Platform Display System

## Overview

The dual-platform display system allows simultaneous monitoring of multiple AI platforms (Codex and Claude) in a split-screen format. Each platform has its own independent display area with platform-specific styling and information.

## Features

### 1. Independent Platform Displays
- **Codex Display** (Cyan theme)
  - Token usage tracking
  - Cost monitoring
  - Session information
  - API call history

- **Claude Display** (Magenta theme)
  - All Codex features PLUS
  - Cache hit rate statistics
  - Cache cost savings
  - Cache efficiency indicators

### 2. Layout Options

#### Horizontal Split (Side-by-Side)
```
┌─────────────────────┬─────────────────────┐
│   CODEX (Cyan)      │   CLAUDE (Magenta)  │
│                     │                     │
│   - Header          │   - Header          │
│   - Usage Panel     │   - Usage Panel     │
│   - Session Info    │   - Cache Info      │
│                     │   - Session Info    │
└─────────────────────┴─────────────────────┘
```

Best for: Wide terminals (>160 columns)

#### Vertical Split (Top-Bottom)
```
┌─────────────────────────────────────────┐
│          CODEX (Cyan)                   │
│                                         │
│          - Header                       │
│          - Usage Panel                  │
│          - Session Info                 │
├─────────────────────────────────────────┤
│          CLAUDE (Magenta)               │
│                                         │
│          - Header                       │
│          - Usage Panel                  │
│          - Cache Info                   │
│          - Session Info                 │
└─────────────────────────────────────────┘
```

Best for: Standard terminals (80-120 columns)

### 3. Multi-Platform Comparison View
An alternative layout showing aggregate statistics across all platforms with compact individual breakdowns.

## Architecture

### Core Models

#### Platform Enum (`core/models.py`)
```python
class Platform(str, Enum):
    CODEX = "codex"
    CLAUDE = "claude"

    @property
    def display_name(self) -> str:
        """Returns: 'Codex' or 'Claude'"""

    @property
    def theme_color(self) -> str:
        """Returns: 'cyan' or 'magenta'"""
```

#### MonitorState
Enhanced with `platform` field to identify which platform the state belongs to:
```python
class MonitorState(BaseModel):
    # ... existing fields ...
    platform: Platform = Field(default=Platform.CODEX)
```

#### MultiPlatformState
New model for managing multiple platforms:
```python
class MultiPlatformState(BaseModel):
    codex_state: Optional[MonitorState] = None
    claude_state: Optional[MonitorState] = None
    last_update: datetime

    @property
    def total_cost(self) -> float:
        """Aggregate cost across platforms"""

    @property
    def total_tokens(self) -> int:
        """Aggregate tokens across platforms"""
```

### UI Components

#### Platform-Specific Header (`ui/components.py`)
```python
def create_platform_header(
    self,
    platform: Platform,
    state: MonitorState,
    plan_manager: Optional[PlanManager] = None,
    timestamp: str = "",
) -> Panel:
    """Creates a header with platform-specific styling."""
```

**Visual Output:**
- Codex: Cyan border with "Codex API Monitor" title
- Claude: Magenta border with "Claude API Monitor" title

#### Cache Info Panel (`ui/components.py`)
```python
def create_cache_info_panel(self, state: MonitorState) -> Panel:
    """Creates cache statistics panel (Claude-only feature)."""
```

**Displays:**
- Cache hit rate with colored indicator
- Total cached tokens
- Cost savings from cache
- Visual efficiency gauge
- Performance recommendations

### Layout Management

#### Dual-Platform Layout (`ui/layouts.py`)
```python
def create_dual_platform_layout(
    self,
    codex_state: MonitorState,
    claude_state: MonitorState,
    codex_plan_manager: PlanManager,
    claude_plan_manager: PlanManager,
    codex_session: Optional[SessionData] = None,
    claude_session: Optional[SessionData] = None,
    refresh_rate: int = 5,
    split_orientation: str = "horizontal",
) -> Layout:
    """Creates split-screen layout for two platforms."""
```

**Parameters:**
- `codex_state`: Monitor state for Codex platform
- `claude_state`: Monitor state for Claude platform
- `codex_plan_manager`: Plan limits for Codex
- `claude_plan_manager`: Plan limits for Claude
- `codex_session`: Optional session data for Codex
- `claude_session`: Optional session data for Claude
- `refresh_rate`: Display refresh rate in seconds
- `split_orientation`: "horizontal" or "vertical"

#### Internal Helper
```python
def _create_platform_display(
    self,
    platform: Platform,
    state: MonitorState,
    plan_manager: PlanManager,
    session: Optional[SessionData] = None,
    timestamp: str = "",
    include_cache: bool = False,
) -> Layout:
    """Creates display for a single platform."""
```

**Conditional Cache Display:**
- When `include_cache=True` and `platform=Platform.CLAUDE`, adds cache info panel
- Codex displays skip cache panel entirely

### Theme System

#### Platform Colors (`ui/themes.py`)
```python
class PlatformColors:
    CODEX_COLORS = {
        "primary": "cyan",
        "accent": "bright_cyan",
        "border": "cyan",
        "header": "bold cyan",
        "text": "cyan",
        "dim": "dim cyan",
    }

    CLAUDE_COLORS = {
        "primary": "magenta",
        "accent": "bright_magenta",
        "border": "magenta",
        "header": "bold magenta",
        "text": "magenta",
        "dim": "dim magenta",
    }
```

#### Platform-Specific Theme Variants
```python
@staticmethod
def get_platform_theme_variant(
    platform: str, base_theme: ColorScheme
) -> ColorScheme:
    """Creates platform-specific theme variant."""
```

## Usage Examples

### Basic Dual-Platform Display

```python
from genai_code_usage_monitor.core.models import MonitorState, Platform, PlanLimits
from genai_code_usage_monitor.core.plans import PlanManager
from genai_code_usage_monitor.ui.layouts import LayoutManager

# Create states for both platforms
codex_state = MonitorState(
    plan_limits=PlanLimits(name="Codex Pro", token_limit=10_000),
    platform=Platform.CODEX,
)

claude_state = MonitorState(
    plan_limits=PlanLimits(name="Claude Team", token_limit=15_000),
    platform=Platform.CLAUDE,
)

# Create plan managers
codex_plan = PlanManager("tier1")
claude_plan = PlanManager("tier2")

# Create layout
layout_manager = LayoutManager(theme="dark")
dual_layout = layout_manager.create_dual_platform_layout(
    codex_state=codex_state,
    claude_state=claude_state,
    codex_plan_manager=codex_plan,
    claude_plan_manager=claude_plan,
    split_orientation="horizontal",
)

# Display
from rich.console import Console
console = Console()
console.print(dual_layout)
```

### Multi-Platform Comparison

```python
from genai_code_usage_monitor.core.models import MultiPlatformState

# Create multi-platform state
multi_state = MultiPlatformState(
    codex_state=codex_state,
    claude_state=claude_state,
)

# Create comparison layout
comparison_layout = layout_manager.create_multi_platform_comparison_layout(
    multi_state=multi_state,
    codex_plan_manager=codex_plan,
    claude_plan_manager=claude_plan,
)

console.print(comparison_layout)
```

### Live Updating Display

```python
from rich.live import Live
import time

with Live(dual_layout, refresh_per_second=0.2) as live:
    while True:
        # Update states with new data
        # ... update codex_state and claude_state ...

        # Recreate layout with updated states
        updated_layout = layout_manager.create_dual_platform_layout(
            codex_state=codex_state,
            claude_state=claude_state,
            codex_plan_manager=codex_plan,
            claude_plan_manager=claude_plan,
            split_orientation="horizontal",
        )

        live.update(updated_layout)
        time.sleep(5)  # Update every 5 seconds
```

## Display Differences Between Platforms

### Codex Display Components
1. Platform-specific header (Cyan)
2. Warning banner (if applicable)
3. Usage overview panel
4. Session information panel
5. Footer

### Claude Display Components
1. Platform-specific header (Magenta)
2. Warning banner (if applicable)
3. Usage overview panel
4. **Cache statistics panel** (unique to Claude)
5. Session information panel
6. Footer

## Accessibility

All platform-specific colors maintain WCAG 2.1 AA compliance:

- **Codex Cyan**: Maintains 4.5:1 contrast ratio (light theme) / 7:1 (dark theme)
- **Claude Magenta**: Maintains 4.5:1 contrast ratio (light theme) / 7:1 (dark theme)

Platform differentiation is achieved through:
1. Color coding (primary method)
2. Explicit platform labels in headers
3. Different information panels (cache for Claude)

## Best Practices

### 1. Terminal Size Recommendations
- **Horizontal split**: Minimum 160 columns, 40+ rows
- **Vertical split**: Minimum 80 columns, 60+ rows
- **Comparison view**: Minimum 100 columns, 30+ rows

### 2. Layout Selection
Choose layout based on:
- Terminal size
- User preference
- Information density needs
- Screen aspect ratio

### 3. State Management
- Keep platform states completely independent
- Never mix API calls from different platforms in the same state
- Use `MultiPlatformState` for aggregate operations

### 4. Performance Considerations
- Limit refresh rate to 0.2-1 updates per second
- Cache layout components when possible
- Use Rich's `Live` context for smooth updates

## API Reference

### LayoutManager Methods

#### `create_dual_platform_layout()`
Creates split-screen layout for two platforms.

**Returns:** `Layout` object ready for display

#### `create_multi_platform_comparison_layout()`
Creates aggregate comparison view.

**Returns:** `Layout` object with compact platform summaries

#### `_create_platform_display()` (Internal)
Helper method for creating single platform display.

**Returns:** `Layout` for one platform

#### `_create_compact_platform_summary()` (Internal)
Helper method for compact platform summary.

**Returns:** `Panel` with platform statistics

### UIComponents Methods

#### `create_platform_header()`
Creates platform-specific header with appropriate styling.

**Returns:** `Panel` with platform header

#### `create_cache_info_panel()`
Creates cache statistics panel (Claude-specific).

**Returns:** `Panel` with cache information

### PlatformColors Methods

#### `get_platform_colors()`
Returns color dictionary for specified platform.

**Returns:** `Dict[str, str]` of color mappings

#### `get_platform_theme_variant()`
Creates platform-specific theme variant.

**Returns:** `ColorScheme` with platform colors

## Migration Guide

### From Single-Platform to Dual-Platform

**Before:**
```python
# Single platform display
layout = layout_manager.create_realtime_layout(
    state=state,
    plan_manager=plan_manager,
)
```

**After:**
```python
# Dual platform display
layout = layout_manager.create_dual_platform_layout(
    codex_state=codex_state,
    claude_state=claude_state,
    codex_plan_manager=codex_plan,
    claude_plan_manager=claude_plan,
)
```

### Adding Platform Field to Existing States

```python
# Update existing MonitorState objects
state.platform = Platform.CODEX  # or Platform.CLAUDE
```

## Troubleshooting

### Issue: Displays overlap or look cramped
**Solution:** Increase terminal size or switch to vertical orientation

### Issue: Cache panel not showing for Claude
**Check:**
1. `platform` field is set to `Platform.CLAUDE`
2. `total_cached_tokens > 0` in usage stats
3. Using `create_dual_platform_layout()` (not old methods)

### Issue: Colors not showing correctly
**Check:**
1. Terminal supports 256 colors or true color
2. Theme is set correctly (`LayoutManager(theme="dark")`)
3. Platform field is set on states

### Issue: Platform headers look identical
**Check:**
1. States have correct `platform` field values
2. Using `create_platform_header()` (not old `create_header()`)

## Future Enhancements

Potential future additions:
1. Support for more than 2 platforms
2. Draggable panel resizing
3. Platform-specific graphs and charts
4. Export to HTML/PDF with preserved layouts
5. Custom platform color schemes
6. Interactive platform selection

## See Also

- [Examples: dual_platform_display_example.py](../examples/dual_platform_display_example.py)
- [Core Models Documentation](./MODELS.md)
- [Theme System Documentation](./THEMES.md)
- [UI Components Guide](./UI_COMPONENTS.md)

# GenAI Code Usage Monitor - Visualization Components Guide

## Overview

This guide describes the enhanced visualization components added to GenAI Code Usage Monitor, including advanced progress bars, charts, and data visualizations using Unicode characters.

## Enhanced Progress Bars

### Features Added

#### 1. Gradient Color Support (Green → Yellow → Orange → Red)

Progress bars now automatically adjust their color based on usage percentage:

- **0-25%**: Green (Safe)
- **25-50%**: Green-Yellow (Low)
- **50-75%**: Yellow (Medium)
- **75-90%**: Orange (High)
- **90-100%**: Red (Critical)

```python
from genai_code_usage_monitor.ui.progress_bars import TokenProgressBar

token_bar = TokenProgressBar(width=50)
print(token_bar.render(85.5))
# Output: 🟠 [████████████████████████████████░░░░] 85.50% [HIGH]
```

#### 2. Pulse Animation Effect

When usage exceeds 85%, the progress bar pulses to draw attention:

```python
# The bar will cycle through different brightness levels
# ▓ → █ → ▓ (repeating animation)
```

The pulse effect uses time-based cycling to create a smooth animation when the terminal refreshes.

#### 3. 3D Visual Effects

Progress bars now have a subtle 3D appearance with:
- Lighter edges on the left (highlight)
- Darker edges on the right (shadow)
- Normal brightness in the middle

#### 4. Precise Decimal Percentages

All percentages now display to 2 decimal places for precision:

```python
# Old: 85.5%
# New: 85.50% [HIGH]
```

### Usage Examples

#### Token Progress Bar

```python
from genai_code_usage_monitor.ui.progress_bars import TokenProgressBar

token_bar = TokenProgressBar(width=50)

# Different usage levels
print(token_bar.render(25.75))   # 🟢 [...] 25.75% [LOW]
print(token_bar.render(65.33))   # 🟡 [...] 65.33% [MEDIUM]
print(token_bar.render(92.12))   # 🔴 [...] 92.12% [CRITICAL] (pulsing)
```

#### Cost Progress Bar

```python
from genai_code_usage_monitor.ui.progress_bars import CostProgressBar

cost_bar = CostProgressBar(width=50)

# Shows cost with gradient and status
print(cost_bar.render(45.67, 100.0))
# Output: 💲 [...] $45.6700 / $100.00 (45.67%) [SAFE]
```

## New Visualization Components

### 1. MiniChart - Trend Visualization

Uses Unicode block characters (▁▂▃▄▅▆▇█) to display trends.

#### Features

- Compact trend visualization
- Sparklines for inline display
- Auto-scaling to fit data range
- Min/max value display

#### Usage

```python
from genai_code_usage_monitor.ui.visualizations import MiniChart

chart = MiniChart(width=30, height=8)

# Token usage over last 30 API calls
data = [100, 150, 120, 180, 200, 220, 250, ...]

# Full chart with title and values
chart_text = chart.render(
    data,
    title="Token Usage Trend",
    color="cyan",
    show_values=True,
)
console.print(chart_text)
```

Output:
```
Token Usage Trend
▁▂▃▄▅▆▇█▇█▇█▇█▇█▇█▇█▇█
Min: 100.00 | Max: 250.00
```

#### Sparklines

```python
# Compact single-line sparkline
sparkline = chart.render_sparkline(data, color="green")
print(f"Trend: {sparkline}")
# Output: Trend: ▁▂▃▄▅▆▇█▇█▇█▇█
```

### 2. GaugeChart - Circular Progress Display

Displays progress as a visual gauge with rotating indicators.

#### Features

- Circular gauge visualization
- Color-coded by percentage
- Multiple display formats
- Icon indicators

#### Usage

```python
from genai_code_usage_monitor.ui.visualizations import GaugeChart

gauge = GaugeChart(width=40)

# Simple gauge
gauge_text = gauge.render(
    percentage=75.5,
    label="Token Usage",
    show_percentage=True,
)
console.print(gauge_text)
```

Output:
```
Token Usage: 🟡 ◐◓◑◒◐◓◑◒◐◓◑◒◐◓◑○○○○○ 75.5%
```

#### Semi-circle Gauge

```python
# Multi-line semicircle display
lines = gauge.render_semicircle(percentage=65.0, width=30)
for line in lines:
    console.print(line)
```

Output:
```
  ▄▄▄▄▄▄▄▄▄▄▄▄▄░░
 █            █
  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀
      65.0%
```

### 3. HeatMap - Time-based Usage Patterns

Visualizes usage intensity across time periods.

#### Features

- 24-hour usage visualization
- Configurable time resolution
- Color-coded intensity levels
- Automatic time bucketing

#### Usage

```python
from genai_code_usage_monitor.ui.visualizations import HeatMap
from datetime import datetime, timedelta

heat_map = HeatMap(hours=24, resolution=12)

# Build time-series data
data = {}
now = datetime.now()
for i in range(100):
    timestamp = now - timedelta(minutes=i * 10)
    data[timestamp] = float(token_count)

# Render heat map
heat_text = heat_map.render(
    data,
    title="24-Hour Usage Pattern"
)
console.print(heat_text)
```

Output:
```
24-Hour Usage Pattern
00:00 ::::::::::::::::::::::::::::::::::::::::::::::::
02:00 --------========================================
04:00 ....::::::::::::::::::::::::::::::::::::::::::::
...
22:00 ################################################

Intensity: Low ░░░ Medium ░░░ High
```

Intensity characters:
- ` ` (space): No activity
- `.`: Very low
- `:`: Low
- `-`: Medium-low
- `=`: Medium
- `+`: Medium-high
- `*`: High
- `#`: Very high
- `█`: Maximum

### 4. WaterfallChart - Cost Breakdown

Shows hierarchical breakdown of costs or values.

#### Features

- Waterfall visualization
- Component contribution display
- Running total tracking
- Currency formatting

#### Usage

```python
from genai_code_usage_monitor.ui.visualizations import WaterfallChart

waterfall = WaterfallChart(width=50)

# Cost breakdown by model
components = [
    ("claude-3-opus", 5.4321),
    ("claude-3-sonnet", 2.1234),
    ("claude-3-haiku", 0.8765),
    ("gpt-4", 1.2345),
]

# Full waterfall chart
chart_text = waterfall.render(
    components,
    total_label="Total Cost",
    currency=True,
)
console.print(chart_text)
```

Output:
```
Cost Breakdown
──────────────────────────────────────────────────────
├─ claude-3-opus         ████████████████████  $5.4321  (56.7%)
├─ claude-3-sonnet       ████████              $2.1234  (22.1%)
├─ claude-3-haiku        ███                   $0.8765  (9.1%)
└─ gpt-4                 ████                  $1.2345  (12.9%)
──────────────────────────────────────────────────────
   Total Cost                                  $9.6665
```

#### Compact Waterfall

```python
# Single stacked bar visualization
compact = waterfall.render_compact(components, width=40)
console.print(compact)
```

Output:
```
┌────────────────────────────────────────┐
│████████████████████████████████        │
└────────────────────────────────────────┘
  █ claude-3-opus: $5.4321 (56.7%)
  █ claude-3-sonnet: $2.1234 (22.1%)
  █ claude-3-haiku: $0.8765 (9.1%)
  █ gpt-4: $1.2345 (12.9%)
```

## Enhanced UI Components

### New Component Methods

#### 1. create_trend_panel()

Creates a panel with mini charts showing usage trends.

```python
ui = UIComponents()
trend_panel = ui.create_trend_panel(state)
console.print(trend_panel)
```

#### 2. create_gauge_panel()

Creates a panel with gauge visualizations for token and cost usage.

```python
gauge_panel = ui.create_gauge_panel(state, limits)
console.print(gauge_panel)
```

#### 3. create_heat_map_panel()

Creates a heat map showing 24-hour usage patterns.

```python
heat_panel = ui.create_heat_map_panel(state)
console.print(heat_panel)
```

#### 4. create_cost_breakdown_panel()

Creates a waterfall chart showing cost breakdown by model.

```python
cost_panel = ui.create_cost_breakdown_panel(state)
console.print(cost_panel)
```

#### 5. create_enhanced_overview()

Creates an enhanced overview with decorative elements and progress indicators.

```python
overview = ui.create_enhanced_overview(state, limits)
console.print(overview)
```

Example output:
```
╔══════════════════════════════════════════════════╗
║           USAGE OVERVIEW                         ║
╚══════════════════════════════════════════════════╝

📊 Token Usage
   [████████████████████████░░░░░░] 75.00%
   750.00K / 1.00M tokens

💰 Cost Usage
   [████████████████░░░░░░░░░░░░░░] 45.67%
   $45.6700 / $100.00

🔄 API Activity
   150 API calls
   Avg: 5000 tokens/call, $0.3045/call

🤖 Model Distribution
   claude-3-sonnet          ████████████░░░░░░░░ 60.0%
   claude-3-haiku           ████░░░░░░░░░░░░░░░░ 26.7%
   gpt-4                    ███░░░░░░░░░░░░░░░░░ 13.3%
```

#### 6. create_compact_dashboard()

Creates a compact table with multiple visualizations.

```python
dashboard = ui.create_compact_dashboard(state, limits)
console.print(dashboard)
```

## Helper Functions

### format_large_number()

Formats large numbers with SI suffixes.

```python
from genai_code_usage_monitor.ui.visualizations import format_large_number

print(format_large_number(1500))        # "1.50K"
print(format_large_number(2500000))     # "2.50M"
print(format_large_number(3500000000))  # "3.50B"
```

### create_progress_indicator()

Creates a simple progress indicator bar.

```python
from genai_code_usage_monitor.ui.visualizations import create_progress_indicator

indicator = create_progress_indicator(
    current=750,
    target=1000,
    width=30,
    show_overage=True
)
print(indicator)
# Output: [███████████████████████░░░░░░░] 75.0%
```

## Color Themes

All visualizations support WCAG 2.1 AA compliant themes (when theme support is available):

- **Light Theme**: Higher contrast colors for bright backgrounds
- **Dark Theme**: Softer colors for dark backgrounds
- **Classic Theme**: Traditional terminal colors

Colors automatically adjust based on:
- Usage percentage
- Critical thresholds
- Data intensity
- Component importance

## Best Practices

### 1. Progress Bars

- Use gradient bars for percentage-based metrics
- Enable pulse animation for critical alerts
- Display precise decimals for detailed monitoring

### 2. Mini Charts

- Keep data points to 20-30 for readability
- Use sparklines for inline trend indicators
- Show min/max values for context

### 3. Gauges

- Use for at-a-glance status checks
- Combine with precise numbers
- Color-code by threshold levels

### 4. Heat Maps

- Best for 24-hour usage patterns
- Adjust resolution based on data density
- Use appropriate time buckets (5-10 min intervals)

### 5. Waterfall Charts

- Sort components by value (descending)
- Show percentages for contribution context
- Use compact version for space-constrained displays

## Integration Examples

### Dashboard Layout

```python
from rich.layout import Layout
from rich.console import Console

console = Console()
layout = Layout()

# Split screen into sections
layout.split_column(
    Layout(name="header", size=3),
    Layout(name="main"),
    Layout(name="footer", size=3),
)

layout["main"].split_row(
    Layout(name="left"),
    Layout(name="right"),
)

# Add visualizations
ui = UIComponents()
layout["header"].update(ui.create_header("Professional", "realtime"))
layout["left"].update(ui.create_trend_panel(state))
layout["right"].update(ui.create_gauge_panel(state, limits))
layout["footer"].update(ui.create_footer())

console.print(layout)
```

### Real-time Animation

```python
import time
from rich.live import Live

with Live(console=console, refresh_per_second=2) as live:
    while True:
        # Update visualizations
        overview = ui.create_enhanced_overview(state, limits)
        live.update(overview)
        time.sleep(0.5)
```

## Performance Considerations

- **Mini Charts**: O(n) where n is data points (recommended: < 50 points)
- **Heat Maps**: O(n) where n is time buckets (optimized for 24h with 12 buckets/hour)
- **Waterfall Charts**: O(n log n) due to sorting (recommended: < 20 components)
- **Gauges**: O(1) constant time rendering

## Accessibility

All visualizations follow accessibility best practices:

- WCAG 2.1 AA color contrast ratios
- Unicode characters widely supported
- Text-based fallbacks available
- Screen reader friendly content structure

## Demo Script

Run the included demo to see all visualizations in action:

```bash
python examples/visualization_demo.py
```

This will showcase:
- All progress bar variations
- Mini chart examples
- Gauge chart displays
- Heat map visualization
- Waterfall chart examples
- Enhanced UI components

## Future Enhancements

Planned additions:
- Interactive drill-down capabilities
- Export to HTML/SVG
- Custom color palettes
- Animation speed controls
- More chart types (pie, line, area)

## Support

For issues or questions about visualizations:
- Check the examples directory
- Review the source code documentation
- Open an issue on the project repository

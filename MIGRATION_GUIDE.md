# Migration Guide: v1.0.0 to v2.0.0

## Table of Contents

- [Overview](#overview)
- [Why Upgrade](#why-upgrade)
- [Backward Compatibility](#backward-compatibility)
- [Breaking Changes](#breaking-changes)
- [Migration Steps](#migration-steps)
- [New Features Guide](#new-features-guide)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Troubleshooting](#troubleshooting)

---

## Overview

Welcome to the GenAI Code Usage Monitor v2.0.0 migration guide! This document will help you smoothly transition from v1.0.0 to v2.0.0, which introduces exciting new features while maintaining backward compatibility for most use cases.

### What's New in v2.0.0

Version 2.0.0 brings several major enhancements:

1. **Dual Platform Support** - Monitor both OpenAI Codex/GPT and Claude Code usage
2. **WCAG 2.1 AA Compliant Theme System** - Light, dark, and classic themes with accessibility support
3. **Cached Token Cost Calculation** - 90% discount support for Claude's prompt caching
4. **Advanced Warning System** - Multi-level alerts with cost and time predictions
5. **Enhanced Visualizations** - Gradient progress bars, pulse animations, and 3D effects
6. **Improved Architecture** - Platform abstraction layer for extensibility

### Release Information

- **Version**: v2.0.0
- **Release Date**: 2025-10-28
- **Python Support**: 3.9, 3.10, 3.11, 3.12+
- **License**: MIT

---

## Why Upgrade

### Key Benefits

#### 1. Multi-Platform Support
Track usage across multiple AI platforms from a single tool:
- Monitor OpenAI Codex/GPT API usage
- Track Claude Code conversations
- Compare costs between platforms
- Unified interface for all monitoring needs

#### 2. Cost Optimization
Save money with intelligent cost tracking:
- **Claude cache support**: 90% discount on cached tokens
- **Real-time cost analysis**: Know your spend instantly
- **Cross-platform comparison**: Choose the most cost-effective option
- **Budget alerts**: Get warned before exceeding limits

#### 3. Accessibility & User Experience
Enhanced visual experience for all users:
- **WCAG 2.1 AA compliant** color schemes
- **Auto-detection** of terminal background
- **High contrast** modes (4.5:1 to 13:1 ratios)
- **Color-blind friendly** palettes

#### 4. Better Monitoring
More powerful analytics and visualization:
- **Gradient progress bars** with smooth color transitions
- **Pulse animations** for critical alerts
- **Mini charts** for trend analysis
- **Heat maps** for 24-hour usage patterns
- **Waterfall charts** for cost breakdown

---

## Backward Compatibility

### Guaranteed Compatibility

v2.0.0 maintains **backward compatibility** for:

✅ **Configuration Files**
- All v1.0.0 configuration files work without changes
- Settings are preserved during upgrade
- Automatic migration of legacy configs

✅ **Command-Line Interface**
- All v1.0.0 CLI commands remain functional
- New flags are optional
- Aliases unchanged (`genai-code-usage-monitor`, `cxmonitor`, `cxm`)

✅ **Data Storage**
- Existing usage data is fully compatible
- No data conversion required
- Historical data remains accessible

✅ **API Compatibility**
- Core API methods remain unchanged
- Existing integrations continue to work
- Python API maintains same interface

### What's Changed (Non-Breaking)

The following changes are **additive** and don't break existing functionality:

| Feature | v1.0.0 | v2.0.0 | Impact |
|---------|--------|--------|---------|
| Platforms | OpenAI only | OpenAI + Claude | New optional flag |
| Themes | Classic only | Light/Dark/Classic | Auto-detection |
| Cache Support | N/A | Claude caching | Automatic |
| Progress Bars | Static | Animated gradients | Visual enhancement |
| Storage | `~/.genai-code-usage-monitor/` | Platform-specific | Backwards compatible |

---

## Breaking Changes

### Important: No Breaking Changes for Standard Usage

For most users, **no code changes are required**. The upgrade is seamless.

### Advanced Users: API Changes

If you're using the Python API directly, note these changes:

#### 1. Platform Abstraction Layer

**Before (v1.0.0):**
```python
from genai_code_usage_monitor.data.api_client import UsageTracker
from genai_code_usage_monitor.core.pricing import PricingCalculator

tracker = UsageTracker()
pricing = PricingCalculator()
cost = pricing.calculate_cost(tokens, model)
```

**After (v2.0.0):**
```python
from genai_code_usage_monitor.platforms import CodexPlatform, ClaudePlatform

# For OpenAI Codex
codex = CodexPlatform()
cost = codex.calculate_cost(tokens, model, is_prompt=True)

# For Claude Code
claude = ClaudePlatform()
cost = claude.calculate_cost(tokens, model, is_cached=True)
```

**Migration**: The old API still works, but new code should use the platform layer.

#### 2. Theme System Integration

**Before (v1.0.0):**
```python
from genai_code_usage_monitor.ui.progress_bars import TokenProgressBar

bar = TokenProgressBar()
print(bar.render(75.0))
```

**After (v2.0.0):**
```python
from genai_code_usage_monitor.ui import TokenProgressBar, set_theme, ThemeType

# Set theme (optional, auto-detected by default)
set_theme(ThemeType.AUTO)

bar = TokenProgressBar()
print(bar.render(75.0))  # Automatically uses current theme
```

**Migration**: Theme is now auto-detected; no changes required unless you want to override.

#### 3. Cost Calculation with Cache Support

**Before (v1.0.0):**
```python
# No cache support in v1.0.0
cost = pricing.calculate_cost(tokens=10000, model="gpt-4")
```

**After (v2.0.0):**
```python
# Claude cache support (90% discount)
platform = ClaudePlatform()

# Regular tokens
regular_cost = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=True)
# $0.0300

# Cached tokens (90% discount!)
cached_cost = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)
# $0.0030 - saves $0.0270
```

**Migration**: Add `is_cached=True` parameter for Claude cached tokens.

---

## Migration Steps

### Step 1: Backup Your Configuration

Before upgrading, backup your configuration and data:

```bash
# Backup configuration
cp -r ~/.genai-code-usage-monitor ~/.genai-code-usage-monitor.backup

# If using Claude
cp -r ~/.claude-monitor ~/.claude-monitor.backup
```

### Step 2: Upgrade the Package

Choose your preferred installation method:

#### Using uv (Recommended)

```bash
# Upgrade to v2.0.0
uv tool upgrade genai-code-usage-monitor

# Verify installation
genai-code-usage-monitor --version
# Expected output: genai-code-usage-monitor v2.0.0
```

#### Using pip

```bash
# Upgrade to v2.0.0
pip install --upgrade genai-code-usage-monitor

# Verify installation
genai-code-usage-monitor --version
```

#### Using pipx

```bash
# Upgrade to v2.0.0
pipx upgrade genai-code-usage-monitor

# Verify installation
genai-code-usage-monitor --version
```

### Step 3: Verify Installation

Run a basic test to ensure everything works:

```bash
# Test basic functionality
genai-code-usage-monitor --help

# Test with your existing configuration
genai-code-usage-monitor --plan custom --refresh-rate 10
```

### Step 4: Explore New Features

Try out the new capabilities:

```bash
# Test dual platform support
genai-code-usage-monitor --platform codex    # OpenAI Codex/GPT
genai-code-usage-monitor --platform claude   # Claude Code

# Test theme system
genai-code-usage-monitor --theme dark        # Dark theme
genai-code-usage-monitor --theme light       # Light theme
genai-code-usage-monitor --theme auto        # Auto-detection (default)

# Run visualization demo
python -m genai_code_usage_monitor.examples.visualization_demo
```

### Step 5: Update Your Scripts (If Any)

If you have custom scripts using the Python API:

**Before:**
```python
#!/usr/bin/env python3
from genai_code_usage_monitor.data.api_client import UsageTracker

tracker = UsageTracker()
stats = tracker.get_today_usage()
print(f"Total tokens: {stats.total_tokens}")
```

**After:**
```python
#!/usr/bin/env python3
from genai_code_usage_monitor.platforms import CodexPlatform

# Use platform abstraction
platform = CodexPlatform()
stats = platform.get_usage_data()
print(f"Total tokens: {stats.total_tokens}")
```

### Step 6: Configure New Features (Optional)

Set up new features based on your needs:

#### Enable Claude Platform Support

```bash
# Monitor Claude Code usage
genai-code-usage-monitor --platform claude --data-dir ~/.claude-monitor
```

#### Configure Preferred Theme

```bash
# Light theme for bright environments
genai-code-usage-monitor --theme light

# Dark theme for night coding
genai-code-usage-monitor --theme dark
```

#### Enable Advanced Visualizations

The new visualizations are enabled by default. To customize:

```python
from genai_code_usage_monitor.ui.visualizations import MiniChart, GaugeChart

# Create mini chart for trends
chart = MiniChart(width=40, height=8)
print(chart.render(data=[100, 150, 200, 180, 220]))

# Create gauge chart for current status
gauge = GaugeChart(width=50)
print(gauge.render(percentage=75.5, label="Token Usage"))
```

---

## New Features Guide

### 1. Dual Platform Support

#### What It Does
Monitor multiple AI platforms from a single interface.

#### How to Use

**Command Line:**
```bash
# Monitor OpenAI Codex (default)
genai-code-usage-monitor --platform codex

# Monitor Claude Code
genai-code-usage-monitor --platform claude

# Specify custom data directory
genai-code-usage-monitor --platform claude --data-dir ~/.my-claude-data
```

**Python API:**
```python
from genai_code_usage_monitor.platforms import CodexPlatform, ClaudePlatform

# Initialize platforms
codex = CodexPlatform()
claude = ClaudePlatform()

# Get usage statistics
codex_stats = codex.get_usage_data()
claude_stats = claude.get_usage_data()

# Compare costs
print(f"OpenAI Cost: ${codex_stats.total_cost:.2f}")
print(f"Claude Cost: ${claude_stats.total_cost:.2f}")
```

#### Use Cases

**Scenario 1: Developer using both platforms**
```bash
# Morning: Check OpenAI usage
genai-code-usage-monitor --platform codex --view realtime

# Afternoon: Check Claude usage
genai-code-usage-monitor --platform claude --view daily
```

**Scenario 2: Team cost comparison**
```python
from genai_code_usage_monitor.platforms import CodexPlatform, ClaudePlatform

def compare_platforms():
    codex = CodexPlatform()
    claude = ClaudePlatform()

    # Get statistics
    codex_stats = codex.get_usage_data()
    claude_stats = claude.get_usage_data()

    # Calculate cost per token
    codex_cpt = codex_stats.total_cost / codex_stats.total_tokens if codex_stats.total_tokens > 0 else 0
    claude_cpt = claude_stats.total_cost / claude_stats.total_tokens if claude_stats.total_tokens > 0 else 0

    print(f"OpenAI: ${codex_cpt*1000:.4f} per 1K tokens")
    print(f"Claude: ${claude_cpt*1000:.4f} per 1K tokens")

    # Recommendation
    if claude_cpt < codex_cpt:
        print("Recommendation: Use Claude for cost savings")
    else:
        print("Recommendation: Use OpenAI for better value")
```

---

### 2. WCAG 2.1 AA Compliant Theme System

#### What It Does
Provides accessible, high-contrast color schemes optimized for different environments.

#### Available Themes

| Theme | Contrast Ratio | Best For | WCAG Compliance |
|-------|----------------|----------|-----------------|
| **Light** | 4.5:1 to 13.47:1 | Bright environments, daytime | AA ✓ |
| **Dark** | 7.0:1 to 13.11:1 | Low-light, night coding | AA+ ✓✓ |
| **Classic** | ~3.0:1 | Legacy terminals | - |
| **Auto** | Detected | All environments | Adaptive |

#### How to Use

**Command Line:**
```bash
# Use auto-detection (recommended)
genai-code-usage-monitor --theme auto

# Force dark theme
genai-code-usage-monitor --theme dark

# Force light theme
genai-code-usage-monitor --theme light

# Use classic theme
genai-code-usage-monitor --theme classic
```

**Python API:**
```python
from genai_code_usage_monitor.ui import set_theme, get_theme, ThemeType

# Set global theme
set_theme(ThemeType.DARK)

# Get current theme
theme = get_theme()
info = theme.get_theme_info()
print(f"Current theme: {info['name']}")
print(f"Contrast ratio: {info['contrast_ratio']}:1")
print(f"WCAG compliant: {info['wcag_compliant']}")

# Create custom themed components
from genai_code_usage_monitor.ui import TokenProgressBar, WCAGTheme

custom_theme = WCAGTheme(ThemeType.LIGHT)
bar = TokenProgressBar(theme=custom_theme)
```

#### Theme Auto-Detection

The system automatically detects the best theme based on:

1. **Environment Variables** (`COLORFGBG`)
2. **macOS System Settings** (dark mode)
3. **Terminal Type** (iTerm, VS Code, etc.)
4. **Fallback** (Dark theme)

#### Color Schemes

**Light Theme:**
- Primary: `#0066CC` (Blue, 4.54:1)
- Success: `#006B3D` (Green, 5.24:1)
- Warning: `#E67E00` (Orange, 4.52:1)
- Danger: `#CC0000` (Red, 5.39:1)

**Dark Theme:**
- Primary: `#66B3FF` (Light Blue, 7.53:1)
- Success: `#5FD97A` (Light Green, 9.46:1)
- Warning: `#FFB84D` (Light Orange, 10.39:1)
- Danger: `#FF6B6B` (Light Red, 7.00:1)

---

### 3. Cached Token Cost Calculation

#### What It Does
Supports Claude's prompt caching feature with 90% cost reduction for cached tokens.

#### How It Works

Claude's prompt caching allows reusing previous context:
- **Regular prompt tokens**: $3.00 per 1M tokens (Sonnet 4)
- **Cached prompt tokens**: $0.30 per 1M tokens (90% discount!)
- **Completion tokens**: $15.00 per 1M tokens

#### How to Use

**Command Line:**
The monitor automatically detects and applies cache discounts when using Claude platform.

```bash
# Monitor Claude with automatic cache detection
genai-code-usage-monitor --platform claude
```

**Python API:**
```python
from genai_code_usage_monitor.platforms import ClaudePlatform

platform = ClaudePlatform()

# Calculate cost for regular tokens
regular_cost = platform.calculate_cost(
    tokens=100000,
    model="claude-sonnet-4",
    is_prompt=True,
    is_cached=False
)
print(f"Regular cost: ${regular_cost:.4f}")  # $0.3000

# Calculate cost for cached tokens (90% discount!)
cached_cost = platform.calculate_cost(
    tokens=100000,
    model="claude-sonnet-4",
    is_prompt=True,
    is_cached=True
)
print(f"Cached cost: ${cached_cost:.4f}")   # $0.0300
print(f"Savings: ${regular_cost - cached_cost:.4f}")  # $0.2700

# Log API call with cache information
platform.log_api_call(
    model="claude-sonnet-4",
    prompt_tokens=1000,
    completion_tokens=500,
    cached_tokens=5000  # 90% discount on these
)
```

#### Cost Comparison Example

```python
def compare_cache_savings():
    platform = ClaudePlatform()

    # Scenario: 1M tokens per day
    tokens_per_day = 1_000_000

    # Without caching
    without_cache = platform.calculate_cost(
        tokens_per_day, "claude-sonnet-4", is_prompt=True
    )

    # With 80% cache hit rate
    new_tokens = tokens_per_day * 0.2
    cached_tokens = tokens_per_day * 0.8

    with_cache = (
        platform.calculate_cost(new_tokens, "claude-sonnet-4", is_prompt=True) +
        platform.calculate_cost(cached_tokens, "claude-sonnet-4", is_cached=True)
    )

    savings = without_cache - with_cache
    savings_pct = (savings / without_cache) * 100

    print(f"Without caching: ${without_cache:.2f}/day")
    print(f"With caching:    ${with_cache:.2f}/day")
    print(f"Daily savings:   ${savings:.2f} ({savings_pct:.1f}%)")
    print(f"Monthly savings: ${savings * 30:.2f}")
    print(f"Annual savings:  ${savings * 365:.2f}")

# Output example:
# Without caching: $3.00/day
# With caching:    $0.84/day
# Daily savings:   $2.16 (72.0%)
# Monthly savings: $64.80
# Annual savings:  $788.40
```

---

### 4. Advanced Warning System

#### What It Does
Provides multi-level alerts with intelligent predictions before you hit limits.

#### Alert Levels

| Level | Threshold | Color | Action |
|-------|-----------|-------|--------|
| **SAFE** | 0-50% | Green | Normal operation |
| **LOW** | 50-70% | Yellow | Monitor usage |
| **MEDIUM** | 70-85% | Orange | Reduce activity |
| **HIGH** | 85-95% | Red | Critical warning |
| **CRITICAL** | 95-100% | Red (Pulsing) | Immediate action |

#### Features

- **Cost predictions** based on burn rate
- **Time-to-limit** calculations
- **Visual pulse animation** at critical levels (≥85%)
- **Detailed warnings** with actionable recommendations

#### How to Use

**Command Line:**
Warnings are automatically displayed in real-time view:

```bash
# Monitor with warnings (default)
genai-code-usage-monitor --view realtime --refresh-rate 5

# Output example:
# Token Usage: 87.5% [HIGH] - Approaching limit!
# Cost: $8.50/$10.00 [HIGH] - $1.50 remaining
# Estimated time to limit: 2.3 hours at current burn rate
# Recommendation: Reduce usage or increase limit
```

**Python API:**
```python
from genai_code_usage_monitor.core.models import MonitorState, PlanLimits

def check_warnings(state: MonitorState, limits: PlanLimits):
    """Check usage and display warnings."""

    # Calculate usage percentages
    token_pct = (state.total_tokens / limits.max_tokens) * 100
    cost_pct = (state.total_cost / limits.max_cost) * 100

    # Determine warning level
    max_pct = max(token_pct, cost_pct)

    if max_pct >= 95:
        level = "CRITICAL"
        color = "red bold"
        action = "STOP: Approaching limit!"
    elif max_pct >= 85:
        level = "HIGH"
        color = "red"
        action = "WARNING: Reduce usage immediately"
    elif max_pct >= 70:
        level = "MEDIUM"
        color = "orange"
        action = "CAUTION: Monitor usage closely"
    elif max_pct >= 50:
        level = "LOW"
        color = "yellow"
        action = "INFO: Usage increasing"
    else:
        level = "SAFE"
        color = "green"
        action = "OK: Normal operation"

    # Calculate predictions
    if state.burn_rate > 0:
        tokens_remaining = limits.max_tokens - state.total_tokens
        time_to_limit = tokens_remaining / state.burn_rate

        print(f"[{color}]{level}[/{color}]: {action}")
        print(f"Time to limit: {time_to_limit:.1f} hours")
    else:
        print(f"[{color}]{level}[/{color}]: {action}")
```

---

### 5. Enhanced Visualizations

#### What's New

v2.0.0 introduces several new visualization components:

1. **Gradient Progress Bars** - Smooth color transitions
2. **Pulse Animations** - Attention-grabbing for critical states
3. **3D Effects** - Subtle depth with shading
4. **Mini Charts** - Compact trend visualizations
5. **Gauge Charts** - Circular progress indicators
6. **Heat Maps** - 24-hour usage patterns
7. **Waterfall Charts** - Cost breakdown by component

#### Progress Bar Enhancements

**Features:**
- Gradient colors (Green → Yellow → Orange → Red)
- Pulse animation at ≥85% usage
- 3D shading effects
- Precise percentages (2 decimal places)
- Status indicators

**Example:**
```python
from genai_code_usage_monitor.ui import TokenProgressBar

bar = TokenProgressBar(width=50)

# Different usage levels
print(bar.render(25.0))   # Green (SAFE)
print(bar.render(60.0))   # Yellow (MEDIUM)
print(bar.render(80.0))   # Orange (HIGH)
print(bar.render(92.5))   # Red + Pulsing (CRITICAL)
```

#### Mini Charts

**Purpose:** Display trends using Unicode block characters.

```python
from genai_code_usage_monitor.ui.visualizations import MiniChart

chart = MiniChart(width=40, height=8)

# Token usage over last 30 calls
data = [100, 120, 115, 130, 125, 140, 135, 150, 145, 160]
print(chart.render(data, title="Token Trend", color="cyan"))

# Output:
# Token Trend
# ▁▂▃▄▅▆▇█▇█
# Min: 100.00 | Max: 160.00
```

#### Gauge Charts

**Purpose:** Circular progress indicators.

```python
from genai_code_usage_monitor.ui.visualizations import GaugeChart

gauge = GaugeChart(width=50)

# Token usage gauge
print(gauge.render(75.5, label="Token Usage"))

# Output:
# Token Usage: 🟡 ◐◓◑◒◐◓◑◒◐◓◑◒◐◓◑○○○○○ 75.5%
```

#### Heat Maps

**Purpose:** Visualize 24-hour usage patterns.

```python
from genai_code_usage_monitor.ui.visualizations import HeatMap
from datetime import datetime, timedelta

heatmap = HeatMap(hours=24, resolution=12)

# Generate sample data
data = {}
now = datetime.now()
for i in range(288):  # 24 hours * 12 (5-minute intervals)
    time = now - timedelta(minutes=i*5)
    data[time] = 100 + (i % 50)  # Simulated token usage

print(heatmap.render(data, title="24-Hour Usage Pattern"))

# Output:
# 24-Hour Usage Pattern
# 00:00 ::::::::::::::::::::::::::::::::::::::::::::::::
# 02:00 --------========================================
# 04:00 ....::::::::::::::::::::::::::::::::::::::::::::
# ...
# 22:00 ################################################
```

#### Waterfall Charts

**Purpose:** Break down costs by component.

```python
from genai_code_usage_monitor.ui.visualizations import WaterfallChart

waterfall = WaterfallChart(width=60)

# Cost breakdown by model
components = [
    ("claude-3-opus", 5.4321),
    ("claude-3-sonnet", 2.1234),
    ("gpt-4", 1.2345),
    ("claude-3-haiku", 0.8765),
]

print(waterfall.render(components, total_label="Total Cost", currency=True))

# Output:
# Cost Breakdown
# ──────────────────────────────────────────────────────
# ├─ claude-3-opus         ████████████████████  $5.4321  (56.7%)
# ├─ claude-3-sonnet       ████████              $2.1234  (22.1%)
# ├─ gpt-4                 ████                  $1.2345  (12.9%)
# └─ claude-3-haiku        ███                   $0.8765  (9.1%)
# ──────────────────────────────────────────────────────
#    Total Cost                                  $9.6665
```

---

## Frequently Asked Questions

### General Questions

#### Q: Do I need to change my existing configuration?
**A:** No. All v1.0.0 configurations work with v2.0.0 without changes.

#### Q: Will my historical data be preserved?
**A:** Yes. All existing usage data is fully compatible and remains accessible.

#### Q: Can I still use the old command-line options?
**A:** Yes. All v1.0.0 CLI options continue to work in v2.0.0.

---

### Platform Support

#### Q: Do I need to use both platforms?
**A:** No. You can continue using only OpenAI (Codex) if preferred. Claude support is optional.

#### Q: Can I monitor both platforms simultaneously?
**A:** Not in the same session, but you can easily switch:
```bash
# Terminal 1: Monitor OpenAI
genai-code-usage-monitor --platform codex

# Terminal 2: Monitor Claude
genai-code-usage-monitor --platform claude
```

#### Q: Where is Claude data stored?
**A:** By default in `~/.claude-monitor/`, separate from OpenAI data in `~/.genai-code-usage-monitor/`.

#### Q: How do I migrate from Codex-only to dual platform?
**A:** Just add the `--platform` flag:
```bash
# Continue OpenAI monitoring (no change needed)
genai-code-usage-monitor

# Add Claude monitoring (new)
genai-code-usage-monitor --platform claude
```

---

### Theme System

#### Q: What if I prefer the old color scheme?
**A:** Use the classic theme:
```bash
genai-code-usage-monitor --theme classic
```

#### Q: Can I disable theme auto-detection?
**A:** Yes, specify a theme explicitly:
```bash
genai-code-usage-monitor --theme dark  # Always use dark theme
```

#### Q: Do themes affect functionality?
**A:** No. Themes only change colors; all features work the same in all themes.

#### Q: My terminal doesn't support the new colors. What should I do?
**A:** Use the classic theme, which works on all terminals:
```bash
genai-code-usage-monitor --theme classic
```

---

### Cost Calculation

#### Q: How does cached token pricing work?
**A:** For Claude, cached tokens receive a 90% discount:
- Regular: $3.00 per 1M tokens
- Cached: $0.30 per 1M tokens (saves $2.70)

#### Q: Does the monitor automatically detect cached tokens?
**A:** Yes, when using the Claude platform with proper API logging.

#### Q: Can I see cache savings in the UI?
**A:** Yes, the cost breakdown shows separate entries for regular and cached tokens.

#### Q: Do OpenAI models support caching?
**A:** No, prompt caching is currently a Claude-specific feature.

---

### Performance

#### Q: Does v2.0.0 use more resources than v1.0.0?
**A:** No. v2.0.0 maintains the same performance profile while adding features.

#### Q: Are the new animations resource-intensive?
**A:** No. Animations use minimal CPU and are optimized for efficiency.

#### Q: Can I disable animations for better performance?
**A:** Animations are lightweight, but you can use classic theme for simpler visuals:
```bash
genai-code-usage-monitor --theme classic
```

---

### Data Migration

#### Q: Do I need to export/import data?
**A:** No. Data migration is automatic and seamless.

#### Q: What happens to my custom plan settings?
**A:** They are preserved automatically. No action needed.

#### Q: Can I rollback to v1.0.0 if needed?
**A:** Yes, using your backup:
```bash
# Uninstall v2.0.0
pip uninstall genai-code-usage-monitor

# Install v1.0.0
pip install genai-code-usage-monitor==1.0.0

# Restore backup
rm -rf ~/.genai-code-usage-monitor
mv ~/.genai-code-usage-monitor.backup ~/.genai-code-usage-monitor
```

---

### Configuration

#### Q: How do I set a default theme?
**A:** Set the `CODEX_MONITOR_THEME` environment variable:
```bash
# In ~/.bashrc or ~/.zshrc
export CODEX_MONITOR_THEME=dark
```

#### Q: Can I use different themes for different platforms?
**A:** Yes, via separate terminal sessions or shell functions:
```bash
# Shell function in ~/.bashrc
monitor_codex() {
    genai-code-usage-monitor --platform codex --theme light
}

monitor_claude() {
    genai-code-usage-monitor --platform claude --theme dark
}
```

#### Q: How do I persist theme settings?
**A:** Create a configuration file:
```yaml
# ~/.genai-code-usage-monitor/config.yaml
theme: dark
platform: codex
refresh_rate: 10
```

---

## Troubleshooting

### Installation Issues

#### Issue: "Module not found" error after upgrade

**Symptoms:**
```
ModuleNotFoundError: No module named 'genai_code_usage_monitor.platforms'
```

**Solution:**
```bash
# Completely uninstall and reinstall
pip uninstall genai-code-usage-monitor -y
pip cache purge
pip install genai-code-usage-monitor==2.0.0

# Or use uv (recommended)
uv tool uninstall genai-code-usage-monitor
uv tool install genai-code-usage-monitor
```

---

#### Issue: Version shows v1.0.0 after upgrade

**Symptoms:**
```bash
genai-code-usage-monitor --version
# Output: genai-code-usage-monitor v1.0.0
```

**Solution:**
```bash
# Check for multiple installations
which -a genai-code-usage-monitor
pip list | grep genai-code-usage-monitor

# Force reinstall to specific location
pip install --force-reinstall --user genai-code-usage-monitor==2.0.0

# Update PATH if needed
export PATH="$HOME/.local/bin:$PATH"
```

---

### Theme Issues

#### Issue: Colors not displaying correctly

**Symptoms:**
- Incorrect colors in progress bars
- Theme doesn't match terminal background

**Solution:**
```bash
# Try different theme
genai-code-usage-monitor --theme light

# Check terminal color support
echo $TERM
# Should be: xterm-256color or similar

# Set explicitly if needed
export TERM=xterm-256color
```

---

#### Issue: Auto-detection selects wrong theme

**Symptoms:**
- Dark theme on light terminal (or vice versa)

**Solution:**
```bash
# Override auto-detection
genai-code-usage-monitor --theme light  # or dark

# Set environment variable
export CODEX_MONITOR_THEME=light

# Check detection
python3 << EOF
from genai_code_usage_monitor.ui import get_theme
theme = get_theme()
print(theme.get_theme_info())
EOF
```

---

### Platform Issues

#### Issue: Claude platform not found

**Symptoms:**
```
Error: Platform 'claude' not available
```

**Solution:**
```bash
# Verify installation
python3 -c "from genai_code_usage_monitor.platforms import ClaudePlatform; print('OK')"

# Reinstall if needed
pip install --force-reinstall genai-code-usage-monitor

# Check for data directory
mkdir -p ~/.claude-monitor
genai-code-usage-monitor --platform claude --data-dir ~/.claude-monitor
```

---

#### Issue: Cost calculations incorrect for Claude

**Symptoms:**
- Cached tokens not showing discount
- Incorrect pricing

**Solution:**
```python
# Verify platform is correct
from genai_code_usage_monitor.platforms import ClaudePlatform

platform = ClaudePlatform()
print(platform.get_platform_name())  # Should be "Claude Code"

# Test cost calculation
regular = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=True, is_cached=False)
cached = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=True, is_cached=True)

print(f"Regular: ${regular:.4f}")  # Should be $0.0300
print(f"Cached: ${cached:.4f}")    # Should be $0.0030
print(f"Discount: {((regular - cached) / regular * 100):.1f}%")  # Should be 90.0%
```

---

### Data Issues

#### Issue: Usage data not showing

**Symptoms:**
- Empty statistics
- No historical data

**Solution:**
```bash
# Check data directory exists
ls -la ~/.genai-code-usage-monitor/
ls -la ~/.claude-monitor/

# Verify file permissions
chmod 755 ~/.genai-code-usage-monitor
chmod 644 ~/.genai-code-usage-monitor/*.jsonl

# Check file format
head -1 ~/.genai-code-usage-monitor/api_calls.jsonl
# Should be valid JSON

# Reset if corrupted
mv ~/.genai-code-usage-monitor ~/.genai-code-usage-monitor.old
mkdir ~/.genai-code-usage-monitor
genai-code-usage-monitor
```

---

### Performance Issues

#### Issue: High CPU usage with animations

**Symptoms:**
- Excessive CPU usage
- Slow rendering

**Solution:**
```bash
# Reduce refresh rate
genai-code-usage-monitor --refresh-rate 30 --refresh-per-second 0.5

# Use classic theme (no animations)
genai-code-usage-monitor --theme classic

# Disable file logging if enabled
genai-code-usage-monitor --log-level WARNING
```

---

#### Issue: Slow startup time

**Symptoms:**
- Long delay before display appears

**Solution:**
```bash
# Check for data corruption
python3 << EOF
from genai_code_usage_monitor.platforms import CodexPlatform
import time

start = time.time()
platform = CodexPlatform()
stats = platform.get_usage_data()
print(f"Loaded in {time.time() - start:.2f}s")
EOF

# If slow, check data file size
du -h ~/.genai-code-usage-monitor/api_calls.jsonl

# Archive old data if too large (>10MB)
cd ~/.genai-code-usage-monitor
mv api_calls.jsonl api_calls.$(date +%Y%m%d).jsonl.backup
touch api_calls.jsonl
```

---

### Common Errors

#### Error: "JSONDecodeError"

**Cause:** Corrupted data file

**Solution:**
```bash
# Backup and reset data
mv ~/.genai-code-usage-monitor/api_calls.jsonl ~/.genai-code-usage-monitor/api_calls.jsonl.backup
touch ~/.genai-code-usage-monitor/api_calls.jsonl
genai-code-usage-monitor
```

---

#### Error: "PermissionError"

**Cause:** Insufficient file permissions

**Solution:**
```bash
# Fix permissions
chmod -R u+rw ~/.genai-code-usage-monitor
chmod -R u+rw ~/.claude-monitor

# Or change data directory
genai-code-usage-monitor --data-dir ~/my-monitor-data
```

---

#### Error: "No module named 'pydantic'"

**Cause:** Missing dependencies

**Solution:**
```bash
# Reinstall with dependencies
pip install --force-reinstall genai-code-usage-monitor[dev]

# Or install dependencies manually
pip install pydantic>=2.0.0 pydantic-settings>=2.0.0
```

---

### Getting Help

If you encounter issues not covered in this guide:

1. **Check Documentation**
   - [README.md](README.md) - Project overview
   - [THEME_SYSTEM.md](THEME_SYSTEM.md) - Theme details
   - [PLATFORM_LAYER_SUMMARY.md](PLATFORM_LAYER_SUMMARY.md) - Platform architecture

2. **Search Issues**
   - GitHub Issues: [https://github.com/yourusername/genai-code-usage-monitor/issues](https://github.com/yourusername/genai-code-usage-monitor/issues)

3. **Report a Bug**
   - Include version: `genai-code-usage-monitor --version`
   - Describe steps to reproduce
   - Attach error messages
   - Mention your environment (OS, Python version)

4. **Ask the Community**
   - Discussions: [https://github.com/yourusername/genai-code-usage-monitor/discussions](https://github.com/yourusername/genai-code-usage-monitor/discussions)

---

## Summary Checklist

Use this checklist to ensure a smooth migration:

### Pre-Migration
- [ ] Backup configuration: `~/.genai-code-usage-monitor`
- [ ] Note current version: `genai-code-usage-monitor --version`
- [ ] Document custom settings
- [ ] Save any custom scripts

### Migration
- [ ] Upgrade package: `pip install --upgrade genai-code-usage-monitor`
- [ ] Verify version: `genai-code-usage-monitor --version` shows v2.0.0
- [ ] Test basic functionality: `genai-code-usage-monitor --help`
- [ ] Confirm data preserved: check historical statistics

### Post-Migration
- [ ] Explore new features: `genai-code-usage-monitor --theme auto`
- [ ] Test platform support: `genai-code-usage-monitor --platform codex`
- [ ] Update custom scripts (if any)
- [ ] Set preferred theme: `genai-code-usage-monitor --theme <preference>`
- [ ] Configure environment variables (optional)

### Validation
- [ ] Run visualization demo: `python -m genai_code_usage_monitor.examples.visualization_demo`
- [ ] Test theme switching: Try all three themes
- [ ] Verify cost calculations: Check Claude cache support
- [ ] Monitor real usage: Run for at least one session

---

## Conclusion

Congratulations on migrating to v2.0.0! You now have access to:

- **Dual platform support** for comprehensive monitoring
- **WCAG-compliant themes** for better accessibility
- **Cached token optimization** for cost savings
- **Enhanced visualizations** for clearer insights
- **Advanced warnings** for proactive management

For questions or issues, consult the [Troubleshooting](#troubleshooting) section or reach out to the community.

**Happy monitoring!**

---

**Document Version:** 1.0
**Last Updated:** 2025-10-28
**For:** GenAI Code Usage Monitor v2.0.0
**License:** MIT

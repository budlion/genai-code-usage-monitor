# 🎯 GenAI Code Usage Monitor

[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/genai-code-usage-monitor/)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Dual Platform](https://img.shields.io/badge/platform-Codex%20%2B%20Claude-blueviolet.svg)](https://github.com/yourusername/genai-code-usage-monitor)
[![WCAG 2.1 AA](https://img.shields.io/badge/WCAG-2.1%20AA-green.svg)](https://www.w3.org/WAI/WCAG2AA-Conformance)

A beautiful real-time terminal monitoring tool for **OpenAI Codex/GPT** and **Claude Code** APIs with advanced analytics, machine learning-based predictions, WCAG-compliant theming, and Rich UI visualizations. Track your token consumption (including cached tokens with 90% discount), burn rate, cost analysis, and get intelligent predictions about usage limits with a 4-level alert system.

**Inspired by** [Claude Code Usage Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) with full feature parity adapted for both OpenAI and Claude APIs.

---

## 📑 Table of Contents

- [🎉 What's New](#-whats-new)
- [✨ Key Features](#-key-features)
- [🚀 Quick Start](#-quick-start)
- [🚀 Installation](#-installation)
- [📖 Usage](#-usage)
- [🔧 Configuration](#-configuration)
- [📊 Features & How It Works](#-features--how-it-works)
- [🚀 Usage Examples](#-usage-examples)
- [🔍 Architecture](#-architecture)
- [📚 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

## 🎉 What's New

### Latest Enhancements

- **🌐 Dual Platform Support** - Monitor both OpenAI Codex/GPT and Claude Code APIs from a single tool with unified interface and platform abstraction layer
- **🎨 WCAG-Compliant Themes** - Three accessible themes (Light/Dark/Classic) with automatic terminal background detection and WCAG 2.1 AA compliance (4.5:1+ contrast ratios)
- **📊 Advanced Visualizations** - Interactive charts (trend lines, gauges, heat maps, waterfall charts) using Unicode characters for rich terminal display
- **💾 Cached Token Calculation** - Track Claude's cached tokens with automatic 90% discount calculation, cache hit rate monitoring, and savings analytics
- **⚠️ Multi-Level Alert System** - 4-tier alerting (INFO/WARNING/CRITICAL/DANGER) with smart thresholds, color-coded warnings, and actionable recommendations
- **🔮 Enhanced Predictions** - Intelligent cost and token forecasting based on burn rate analysis with confidence scores and time-to-limit estimation

### Why These Features Matter

**Dual Platform Support**: Switch seamlessly between OpenAI and Claude APIs without changing your workflow. Compare costs and performance across platforms.

**WCAG Compliance**: Accessible to all users with proper contrast ratios and screen reader friendly output. Works great in both light and dark environments.

**Cached Tokens**: Save up to 90% on Claude API costs by tracking and optimizing cached prompt usage. See real-time savings.

**Smart Alerts**: Know exactly when to take action with progressive alert levels. Never exceed your budget unexpectedly.

## ✨ Key Features

### 🚀 **v1.0.0 - Full Feature Release**

- **🔮 ML-based predictions** - P90 percentile calculations and intelligent session limit detection
- **🔄 Real-time monitoring** - Configurable refresh rates (1-60s) with intelligent display updates (0.1-20 Hz)
- **📊 Advanced Rich UI** - Beautiful color-coded progress bars, tables, and layouts with WCAG-compliant contrast
- **🤖 Smart auto-detection** - Automatic plan switching with custom limit discovery
- **📋 Enhanced plan support** - Multiple plans: Free Tier, Pay-As-You-Go, Tier 1/2, Custom (P90-based)
- **⚠️ Advanced warning system** - Multi-level alerts with cost and time predictions
- **💼 Professional Architecture** - Modular design with Single Responsibility Principle (SRP) compliance
- **🎨 Intelligent theming** - Scientific color schemes with automatic terminal background detection
- **⏰ Advanced scheduling** - Auto-detected system timezone and time format preferences
- **📈 Cost analytics** - Model-specific pricing with comprehensive token calculations
- **🔧 Pydantic validation** - Type-safe configuration with automatic validation
- **📝 Comprehensive logging** - Optional file logging with configurable levels
- **⚡ Performance optimized** - Advanced caching and efficient data processing

### 📋 Default Custom Plan

The **Custom plan** is the default option, designed for flexible usage monitoring. It monitors three critical metrics:
- **Token usage** - Tracks your token consumption
- **API calls** - Monitors number of API requests
- **Cost usage** - The most important metric for budget control

The Custom plan automatically adapts to your usage patterns by analyzing your sessions from the last 192 hours (8 days) and calculating personalized limits based on your actual usage using P90 analysis.

## 🚀 Quick Start

### Single Platform Monitoring

```bash
# Monitor OpenAI Codex/GPT usage (default)
code-monitor

# Monitor Claude Code usage
code-monitor --platform claude

# Auto-detect platform from environment
code-monitor --platform auto
```

### Compare Both Platforms

```bash
# View usage from both platforms side-by-side
code-monitor --platform both

# Export comparison report
code-monitor --platform both --export comparison-report.json
```

### Theme Selection

```bash
# Auto-detect best theme (default)
code-monitor --theme auto

# Use dark theme for dark terminals
code-monitor --theme dark

# Use light theme for bright environments
code-monitor --theme light

# Classic theme for compatibility
code-monitor --theme classic
```

### Quick Verification

After installation, verify everything works:

```bash
# Check version and configuration
code-monitor --version
code-monitor --help

# Test with your API key
export OPENAI_API_KEY="your-key"
code-monitor --plan custom

# Or for Claude
export ANTHROPIC_API_KEY="your-key"
code-monitor --platform claude
```

## 🚀 Installation

### ⚡ Modern Installation with uv (Recommended)

**Why uv is the best choice:**
- ✅ Creates isolated environments automatically (no system conflicts)
- ✅ No Python version issues
- ✅ No "externally-managed-environment" errors
- ✅ Easy updates and uninstallation
- ✅ Works on all platforms

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install from PyPI with uv (easiest)
uv tool install genai-code-usage-monitor

# Run from anywhere
code-monitor
```

### 📦 Installation with pip

```bash
# Install from PyPI
pip install genai-code-usage-monitor

# If code-monitor command is not found, add ~/.local/bin to PATH:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc  # or restart your terminal

# Run from anywhere
code-monitor
```

### 🛠️ Other Package Managers

#### pipx (Isolated Environments)
```bash
pipx install genai-code-usage-monitor
code-monitor
```

#### conda/mamba
```bash
pip install genai-code-usage-monitor
code-monitor
```

### 🔧 Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/genai-code-usage-monitor.git
cd genai-code-usage-monitor

# Install in development mode
pip install -e .

# Run from source
python -m genai_code_usage_monitor
```

## 📖 Usage

### Get Help

```bash
# Show help information
code-monitor --help
```

### Basic Usage

```bash
# Default (Custom plan with auto-detection)
code-monitor

# Exit the monitor
# Press Ctrl+C to gracefully exit
```

### Configuration Options

#### Specify Your Plan

```bash
# Custom plan with P90 auto-detection (Default)
code-monitor --plan custom

# Free tier plan
code-monitor --plan free

# Pay-as-you-go plan
code-monitor --plan payg

# Tier 1 plan (1M tokens/day)
code-monitor --plan tier1

# Tier 2 plan (5M tokens/day)
code-monitor --plan tier2

# Custom plan with explicit token limit
code-monitor --plan custom --custom-limit-tokens 100000

# Custom plan with cost limit
code-monitor --plan custom --custom-limit-cost 50.0
```

#### Usage View Configuration

```bash
# Real-time monitoring with live updates (Default)
code-monitor --view realtime

# Daily token usage aggregated in table format
code-monitor --view daily

# Monthly token usage aggregated in table format
code-monitor --view monthly
```

#### Performance and Display Configuration

```bash
# Adjust refresh rate (1-60 seconds, default: 10)
code-monitor --refresh-rate 5

# Adjust display refresh rate (0.1-20 Hz, default: 0.75)
code-monitor --refresh-per-second 1.0

# Set time format (auto-detected by default)
code-monitor --time-format 24h  # or 12h

# Force specific theme
code-monitor --theme dark  # light, dark, classic, auto

# Clear saved configuration
code-monitor --clear
```

#### Timezone Configuration

```bash
# Use US Eastern Time
code-monitor --timezone America/New_York

# Use Tokyo time
code-monitor --timezone Asia/Tokyo

# Use UTC
code-monitor --timezone UTC

# Use London time
code-monitor --timezone Europe/London
```

#### Logging and Debugging

```bash
# Enable debug logging
code-monitor --debug

# Log to file
code-monitor --log-file ~/.genai-code-usage-monitor/logs/monitor.log

# Set log level
code-monitor --log-level WARNING  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 📊 Features & How It Works

### Current Features

#### 🔄 Advanced Real-time Monitoring
- Configurable update intervals (1-60 seconds)
- High-precision display refresh (0.1-20 Hz)
- Intelligent change detection to minimize CPU usage
- Multi-threaded orchestration with callback system

#### 📊 Rich UI Components
- **Progress Bars**: WCAG-compliant color schemes with scientific contrast ratios
- **Data Tables**: Sortable columns with model-specific statistics
- **Layout Manager**: Responsive design that adapts to terminal size
- **Theme System**: Auto-detects terminal background for optimal readability

#### 📈 Multiple Usage Views
- **Realtime View** (Default): Live monitoring with progress bars, current session data, and burn rate analysis
- **Daily View**: Aggregated daily statistics showing Date, Models, Input/Output tokens, Total tokens, and Cost
- **Monthly View**: Monthly aggregated data for long-term trend analysis and budget planning

#### 🔮 Machine Learning Predictions
- **P90 Calculator**: 90th percentile analysis for intelligent limit detection
- **Burn Rate Analytics**: Multi-session consumption pattern analysis
- **Cost Projections**: Model-specific pricing with token calculations
- **Trend Forecasting**: Predicts usage trends based on historical patterns

### Available Plans

| Plan | Token Limit | Cost Limit | Best For |
|------|-------------|------------|----------|
| **free** | 100,000 | $0 | Free tier users |
| **payg** | Unlimited | $100 (default) | Pay-as-you-go users |
| **tier1** | 1,000,000 | $50 | Medium usage |
| **tier2** | 5,000,000 | $250 | Heavy usage |
| **custom** | P90-based | $50 (default) | Intelligent detection (default) |

### Technical Requirements

#### Dependencies

```toml
# Core dependencies (automatically installed)
openai>=1.0.0               # OpenAI API client
pytz>=2023.3                # Timezone handling
rich>=13.7.0                # Rich terminal UI
pydantic>=2.0.0             # Type validation
pydantic-settings>=2.0.0    # Configuration management
numpy>=1.21.0               # Statistical calculations
requests>=2.31.0            # HTTP requests
pyyaml>=6.0                 # Configuration files
```

#### Python Requirements

- **Minimum**: Python 3.9+
- **Recommended**: Python 3.11+
- **Tested on**: Python 3.9, 3.10, 3.11, 3.12

## 🚀 Usage Examples

### Common Scenarios

#### 🌅 Morning Developer
Start work at 9 AM and want tokens to reset aligned with your schedule.

```bash
# Set custom reset time to 9 AM
code-monitor --reset-hour 9

# With your timezone
code-monitor --reset-hour 9 --timezone US/Eastern
```

#### 🌙 Night Owl Coder
Work past midnight and need flexible reset scheduling.

```bash
# Reset at midnight for clean daily boundaries
code-monitor --reset-hour 0

# Late evening reset (11 PM)
code-monitor --reset-hour 23
```

#### 🔄 Heavy User with Variable Limits
Your usage varies significantly and you need intelligent limit detection.

```bash
# Auto-detect from historical usage
code-monitor --plan custom

# Monitor with custom scheduling
code-monitor --plan custom --reset-hour 6
```

#### 🌍 International User
Working across different timezones or traveling.

```bash
# US East Coast
code-monitor --timezone America/New_York

# Europe
code-monitor --timezone Europe/London

# Asia Pacific
code-monitor --timezone Asia/Singapore

# UTC for international team coordination
code-monitor --timezone UTC --reset-hour 12
```

### Best Practices

#### Setup Best Practices

1. **Start Early in Sessions**
   ```bash
   # Begin monitoring when starting development work
   code-monitor
   ```
   - Gives accurate usage tracking from the start
   - Better cost predictions
   - Early warning for limit approaches

2. **Use Modern Installation (Recommended)**
   ```bash
   # Easy installation and updates with uv
   uv tool install genai-code-usage-monitor
   code-monitor --plan custom
   ```

3. **Monitor Burn Rate**
   - Watch for sudden spikes in token consumption
   - Adjust coding intensity based on remaining budget
   - Plan big projects around reset times

## 🔍 Architecture

### Modular Design (SRP Compliance)

```
genai-code-usage-monitor/
├── src/genai_code_usage_monitor/
│   ├── cli/                # CLI interface layer
│   ├── core/               # Core business logic
│   │   ├── models.py       # Data models
│   │   ├── plans.py        # Plan definitions
│   │   ├── pricing.py      # Pricing calculator
│   │   ├── settings.py     # Configuration
│   │   ├── alerts.py       # Alert system
│   │   └── p90_calculator.py
│   ├── data/               # Data layer
│   │   └── api_client.py   # API interaction
│   ├── platforms/          # Platform abstraction
│   │   ├── base.py         # Platform interface
│   │   ├── codex.py        # OpenAI adapter
│   │   └── claude.py       # Claude adapter
│   ├── ui/                 # UI components
│   │   ├── display.py      # Rich display
│   │   ├── themes.py       # WCAG themes
│   │   ├── progress_bars.py # Enhanced progress
│   │   └── visualizations.py # Charts & graphs
│   └── utils/              # Utilities
│       └── time_utils.py   # Time functions
```

## 📚 Documentation

Comprehensive guides and references for all features:

### Getting Started
- [QUICKSTART.md](QUICKSTART.md) - Fast-track guide for new users
- [INSTALLATION_TEST_REPORT.md](INSTALLATION_TEST_REPORT.md) - Installation validation and troubleshooting
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Complete usage documentation

### Feature Guides
- [PLATFORM_QUICK_REFERENCE.md](PLATFORM_QUICK_REFERENCE.md) - Dual platform support guide
- [VISUALIZATION_GUIDE.md](VISUALIZATION_GUIDE.md) - Charts, graphs, and visual components
- [docs/CACHE_AND_ALERTS.md](docs/CACHE_AND_ALERTS.md) - Cached tokens and alert system
- [docs/THEME_QUICKSTART.md](docs/THEME_QUICKSTART.md) - Theme system and WCAG compliance
- [THEME_SYSTEM.md](THEME_SYSTEM.md) - Complete theming documentation

### Advanced Topics
- [PLATFORM_LAYER_SUMMARY.md](PLATFORM_LAYER_SUMMARY.md) - Platform abstraction architecture
- [src/genai_code_usage_monitor/platforms/README.md](src/genai_code_usage_monitor/platforms/README.md) - Platform API reference
- [VISUAL_EXAMPLES.md](VISUAL_EXAMPLES.md) - Visual demonstrations and examples
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command quick reference

### Project Information
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview and goals
- [CHANGELOG.md](CHANGELOG.md) - Version history and updates
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [FEATURE_CHECKLIST.md](FEATURE_CHECKLIST.md) - Feature implementation status

### Implementation Details
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical implementation overview
- [ENHANCEMENT_SUMMARY.md](ENHANCEMENT_SUMMARY.md) - Enhancement details
- [THEME_ENHANCEMENT_SUMMARY.md](THEME_ENHANCEMENT_SUMMARY.md) - Theme system enhancements
- [OPTIMIZATION_COMPLETE.md](OPTIMIZATION_COMPLETE.md) - Performance optimizations
- [FINAL_REPORT.md](FINAL_REPORT.md) - Comprehensive project report

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

[MIT License](LICENSE) - feel free to use and modify as needed.

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

[Report Bug](https://github.com/yourusername/genai-code-usage-monitor/issues) • [Request Feature](https://github.com/yourusername/genai-code-usage-monitor/issues)

</div>

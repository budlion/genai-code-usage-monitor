<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=A177F7&center=true&vCenter=true&width=940&lines=GenAI+Code+Usage+Monitor;Real-time+AI+API+Monitoring+%F0%9F%9A%80;OpenAI+%2B+Claude+%E2%9C%A8" alt="Typing SVG" />

# 🎯 GenAI Code Usage Monitor

### *The Ultimate Real-Time Terminal Dashboard for Your AI APIs*

<p align="center">
  <strong>Monitor OpenAI Codex & Claude Code APIs with Style and Precision</strong>
</p>

---

### Languages / 语言

**English** | [中文](./README.zh-CN.md)

---

<p>
  <a href="https://pypi.org/project/genai-code-usage-monitor/">
    <img src="https://img.shields.io/badge/pypi-v2.1.0-blue.svg?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI Version"/>
  </a>
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License"/>
  </a>
</p>

<p>
  <a href="http://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge" alt="PRs Welcome"/>
  </a>
  <a href="https://github.com/yourusername/genai-code-usage-monitor">
    <img src="https://img.shields.io/badge/platform-Codex%20%2B%20Claude-blueviolet.svg?style=for-the-badge&logo=openai&logoColor=white" alt="Platform"/>
  </a>
  <a href="https://www.w3.org/WAI/WCAG2AA-Conformance">
    <img src="https://img.shields.io/badge/WCAG-2.1%20AA-green.svg?style=for-the-badge" alt="WCAG"/>
  </a>
</p>

<p>
  <img src="https://img.shields.io/badge/Rich%20UI-Terminal-ff69b4?style=for-the-badge&logo=windowsterminal&logoColor=white" alt="Rich UI"/>
  <img src="https://img.shields.io/badge/Real--time-Monitoring-00d4ff?style=for-the-badge&logo=grafana&logoColor=white" alt="Monitoring"/>
  <img src="https://img.shields.io/badge/ML-Predictions-orange?style=for-the-badge&logo=tensorflow&logoColor=white" alt="ML"/>
</p>

<img src="https://user-images.githubusercontent.com/placeholder/demo.gif" width="800" alt="Demo GIF" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/>

*Experience real-time monitoring with beautiful terminal UI, intelligent alerts, and ML-powered predictions*

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 Why Choose GenAI Code Usage Monitor?

<table>
<tr>
<td width="50%">

### 🎨 **Beautiful & Accessible**
- WCAG 2.1 AA compliant color schemes
- Auto-detects terminal background
- Rich terminal UI with progress bars
- Three stunning themes: Light, Dark, Classic

</td>
<td width="50%">

### 🚀 **Dual Platform Support**
- Monitor OpenAI Codex/GPT APIs
- Track Claude Code usage
- Unified interface for both platforms
- Compare costs across platforms

</td>
</tr>
<tr>
<td width="50%">

### 💰 **Cost Optimization**
- Track cached tokens (90% discount!)
- Real-time burn rate analysis
- Budget alerts & recommendations
- ML-based usage predictions

</td>
<td width="50%">

### ⚡ **Smart & Fast**
- P90 percentile analytics
- 4-level alert system (INFO/WARNING/CRITICAL/DANGER)
- Configurable refresh rates
- Multi-threaded architecture

</td>
</tr>
</table>

---

## ✨ Features

### 🔥 Core Features

```ascii
┌─────────────────────────────────────────────────────────────────┐
│  🎯 Dual Platform Support    │  📊 Advanced Analytics          │
│  🎨 WCAG-Compliant Themes    │  💾 Cached Token Tracking       │
│  ⚠️  4-Level Alert System     │  🔮 ML-Based Predictions        │
│  📈 Multiple View Modes       │  🚀 Real-Time Monitoring        │
└─────────────────────────────────────────────────────────────────┘
```

<details>
<summary>🔍 Click to see all features in detail</summary>

#### 🌐 **Dual Platform Support**
- ✅ OpenAI Codex/GPT API monitoring
- ✅ Claude Code API monitoring
- ✅ Platform auto-detection
- ✅ Side-by-side comparison mode
- ✅ Platform-specific features (cache tracking for Claude)

#### 📊 **Advanced Analytics**
- ✅ Token usage tracking (input/output/cached)
- ✅ Cost calculation with model-specific pricing
- ✅ Burn rate analysis
- ✅ P90 percentile calculations
- ✅ Session limit predictions

#### 🎨 **Professional UI**
- ✅ Rich terminal layouts with color-coded progress bars
- ✅ Three WCAG-compliant themes (Light/Dark/Classic)
- ✅ Automatic terminal background detection
- ✅ Responsive design that adapts to terminal size
- ✅ Unicode charts and visualizations

#### ⚠️ **Intelligent Alerts**
- ✅ 4-tier alerting: INFO → WARNING → CRITICAL → DANGER
- ✅ Smart threshold detection
- ✅ Actionable recommendations
- ✅ Time-to-limit estimation

#### 💾 **Cache Optimization** (Claude)
- ✅ Cached token tracking with 90% discount
- ✅ Cache hit rate monitoring
- ✅ Real-time savings analytics
- ✅ Cache efficiency recommendations

#### 🔮 **ML Predictions**
- ✅ Usage trend forecasting
- ✅ Cost projections
- ✅ Confidence scores
- ✅ Intelligent limit detection

</details>

---

## 🚀 Quick Start

### ⚡ Installation (Choose One)

<table>
<tr>
<td width="33%">

#### 🎯 **uv (Recommended)**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install tool
uv tool install genai-code-usage-monitor

# Run
code-monitor
```
✅ Isolated environment
✅ No conflicts
✅ Easy updates

</td>
<td width="33%">

#### 📦 **pip**
```bash
# Install
pip install genai-code-usage-monitor

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Run
code-monitor
```
✅ Simple
✅ Familiar
✅ Works everywhere

</td>
<td width="33%">

#### 🍺 **Homebrew**
```bash
# Install
brew install code-monitor

# Run
code-monitor
```
✅ Native macOS
✅ Auto-updates
✅ Clean uninstall

</td>
</tr>
</table>

### 🎬 First Run

```bash
# Set your API key
export OPENAI_API_KEY="sk-..."
# or
export ANTHROPIC_API_KEY="sk-ant-..."

# Launch monitor
code-monitor

# 🎉 That's it! Monitor is running
```

---

## 📸 Screenshots & Demos

> 🎬 **Live Demo**: See the monitor in action below or [contribute screenshots](docs/SCREENSHOTS.md)!

<div align="center">

### 🌙 Dark Theme - Real-time Monitoring

```
┌─────────────────────── GenAI Code Usage Monitor ────────────────────────┐
│                                                                          │
│  Platform: OpenAI Codex          Theme: Dark          View: Realtime   │
│                                                                          │
│  📊 Current Session                                                      │
│  ├─ Input Tokens:     12,450  ████████████████████░░░░░  62%          │
│  ├─ Output Tokens:     8,320  ██████████████░░░░░░░░░░░  41%          │
│  ├─ Total Tokens:     20,770  ████████████████░░░░░░░░░  52%          │
│  └─ Cost:              $0.42  █████████████████░░░░░░░░  84%          │
│                                                                          │
│  ⚠️  WARNING: You've used 84% of your budget                             │
│                                                                          │
│  🔮 Predictions                                                          │
│  ├─ Estimated limit reach: ~2.5 hours                                  │
│  ├─ Recommended action: Reduce token usage                             │
│  └─ Burn rate: $0.17/hour                                              │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

*Beautiful WCAG-compliant dark theme with real-time progress tracking*

### ☀️ Light Theme - Daily Statistics

```
┌─────────────────────── Daily Usage Report ──────────────────────────┐
│                                                                      │
│  Date        Models    Input     Output    Total      Cost         │
│  ─────────── ───────── ───────── ───────── ────────── ────────────│
│  2025-10-28  GPT-4     45.2K     32.1K     77.3K      $1.55        │
│  2025-10-27  GPT-4     38.7K     28.4K     67.1K      $1.34        │
│  2025-10-26  GPT-3.5   52.3K     39.2K     91.5K      $0.18        │
│                                                                      │
│  📈 7-Day Average: $1.02/day    📊 Total: $7.14                     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

*Clean light theme perfect for bright environments*

### 🎨 Dual Platform - Split Screen

```
┌──────────── OpenAI Codex ────────────┬──────────── Claude Code ─────────────┐
│                                      │                                      │
│  📊 Usage: 52% ████████████░░░░░░░  │  📊 Usage: 38% ████████░░░░░░░░░░  │
│  💰 Cost:  $0.42                     │  💰 Cost:  $0.28                     │
│  📈 Tokens: 20.7K                    │  📈 Tokens: 15.2K                    │
│                                      │  💾 Cache Hit Rate: 45%              │
│                                      │  💰 Cache Savings: $0.12 (90% off)  │
│                                      │                                      │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

*Monitor both platforms simultaneously with platform-specific metrics*

</div>

### 🎥 Want to See Real Screenshots?

<div align="center">

| Action | Description |
|:------:|:------------|
| 🚀 **[Try It Now](#-quick-start)** | Install and run the monitor yourself |
| 📸 **[Screenshot Guide](docs/SCREENSHOTS.md)** | Learn how to capture beautiful screenshots |
| 🤝 **[Contribute](CONTRIBUTING.md)** | Add your screenshots to the project |

**Help us showcase the project!** We welcome screenshot contributions. See the [Screenshot Guide](docs/SCREENSHOTS.md) for details.

</div>

---

## 💡 Usage Examples

### 🎯 **Single Platform**

```bash
# Monitor OpenAI (default)
code-monitor

# Monitor Claude
code-monitor --platform claude

# Auto-detect from environment
code-monitor --platform auto
```

### 🔄 **Dual Platform**

```bash
# Monitor both platforms side-by-side
code-monitor --platform both

# Export comparison report
code-monitor --platform both --export comparison.json
```

### 🎨 **Theme Selection**

```bash
# Auto-detect (recommended)
code-monitor --theme auto

# Specific themes
code-monitor --theme dark
code-monitor --theme light
code-monitor --theme classic
```

### ⚙️ **Advanced Configuration**

```bash
# Custom plan with token limit
code-monitor --plan custom --custom-limit-tokens 100000

# Fast refresh for active development
code-monitor --refresh-rate 5

# Debug mode with logging
code-monitor --debug --log-file monitor.log

# Different timezone
code-monitor --timezone America/New_York
```

---

## 📊 Monitoring Plans

<div align="center">

| Plan | Token Limit | Cost Limit | Best For | Command |
|:----:|:-----------:|:----------:|:--------:|:--------|
| 🆓 **Free** | 100,000 | $0 | Free tier users | `--plan free` |
| 💳 **Pay-As-You-Go** | Unlimited | $100 | Flexible usage | `--plan payg` |
| 🥉 **Tier 1** | 1,000,000 | $50 | Medium usage | `--plan tier1` |
| 🥇 **Tier 2** | 5,000,000 | $250 | Heavy usage | `--plan tier2` |
| 🎯 **Custom** | P90-based | $50 | Intelligent detection | `--plan custom` ⭐ |

</div>

> 💡 **Tip**: The Custom plan (default) automatically learns from your usage patterns using P90 analysis!

---

## 🏗️ Architecture

<div align="center">

```mermaid
graph TB
    A[🎯 CLI Interface] --> B[📊 Display Controller]
    A --> C[🔧 Configuration]

    B --> D[🎨 UI Layer]
    B --> E[📈 Data Layer]

    D --> F[Rich Layouts]
    D --> G[Progress Bars]
    D --> H[Themes]

    E --> I[🌐 Platform Layer]

    I --> J[OpenAI Adapter]
    I --> K[Claude Adapter]

    J --> L[OpenAI API]
    K --> M[Claude API]

    style A fill:#a177f7,stroke:#7c3aed,stroke-width:3px,color:#fff
    style B fill:#60a5fa,stroke:#3b82f6,stroke-width:2px,color:#fff
    style I fill:#34d399,stroke:#10b981,stroke-width:2px,color:#fff
    style L fill:#f97316,stroke:#ea580c,stroke-width:2px,color:#fff
    style M fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff
```

</div>

### 📦 Project Structure

```
genai-code-usage-monitor/
├── 🎯 cli/                    # Command-line interface
├── 🧠 core/                   # Business logic
│   ├── models.py              # Data models
│   ├── plans.py               # Plan definitions
│   ├── pricing.py             # Cost calculator
│   ├── alerts.py              # Alert system
│   └── p90_calculator.py      # ML analytics
├── 🌐 platforms/              # Platform abstraction
│   ├── base.py                # Platform interface
│   ├── codex.py               # OpenAI adapter
│   └── claude.py              # Claude adapter
├── 🎨 ui/                     # UI components
│   ├── display.py             # Rich display
│   ├── themes.py              # WCAG themes
│   └── visualizations.py      # Charts & graphs
└── 🛠️ utils/                  # Utilities
    └── time_utils.py          # Time functions
```

---

## 📚 Documentation

<div align="center">

### 📖 Comprehensive Guides

| Category | Document | Description |
|:--------:|:---------|:------------|
| 🚀 | [QUICKSTART.md](QUICKSTART.md) | Fast-track guide for new users |
| 📘 | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Complete usage documentation |
| 🌐 | [PLATFORM_QUICK_REFERENCE.md](PLATFORM_QUICK_REFERENCE.md) | Dual platform support guide |
| 🎨 | [THEME_SYSTEM.md](THEME_SYSTEM.md) | Complete theming documentation |
| 💾 | [docs/CACHE_AND_ALERTS.md](docs/CACHE_AND_ALERTS.md) | Cached tokens & alert system |
| 📊 | [VISUALIZATION_GUIDE.md](VISUALIZATION_GUIDE.md) | Charts & visual components |
| 🏗️ | [PLATFORM_LAYER_SUMMARY.md](PLATFORM_LAYER_SUMMARY.md) | Platform architecture |
| 📜 | [CHANGELOG.md](CHANGELOG.md) | Version history & updates |

</div>

---

## 🎓 Learn By Example

<details>
<summary>🌅 <strong>Morning Developer</strong> - Reset at 9 AM</summary>

```bash
# Set custom reset time aligned with work schedule
code-monitor --reset-hour 9 --timezone America/New_York

# Start monitoring when you begin coding
code-monitor --plan custom --refresh-rate 5
```

</details>

<details>
<summary>🌙 <strong>Night Owl</strong> - Late night coding sessions</summary>

```bash
# Reset at midnight for clean daily boundaries
code-monitor --reset-hour 0

# Or late evening reset
code-monitor --reset-hour 23 --timezone UTC
```

</details>

<details>
<summary>🔄 <strong>Heavy User</strong> - Variable usage patterns</summary>

```bash
# Auto-detect from historical usage
code-monitor --plan custom

# Monitor with custom scheduling
code-monitor --plan custom --reset-hour 6 --refresh-rate 3
```

</details>

<details>
<summary>🌍 <strong>International Team</strong> - Multiple timezones</summary>

```bash
# US East Coast
code-monitor --timezone America/New_York

# Europe
code-monitor --timezone Europe/London

# Asia Pacific
code-monitor --timezone Asia/Tokyo

# UTC for coordination
code-monitor --timezone UTC --reset-hour 12
```

</details>

---

## 🔧 Advanced Features

### 🎯 Alert System

```bash
# 4-Level Progressive Alerts
┌──────────────┬─────────────┬──────────────────────────────┐
│ Level        │ Threshold   │ Action                       │
├──────────────┼─────────────┼──────────────────────────────┤
│ 📘 INFO      │ < 50%       │ Continue normally            │
│ ⚠️  WARNING   │ 50-75%      │ Monitor usage                │
│ 🔶 CRITICAL  │ 75-90%      │ Reduce consumption           │
│ 🔴 DANGER    │ > 90%       │ Immediate action required    │
└──────────────┴─────────────┴──────────────────────────────┘
```

### 💾 Cache Optimization (Claude)

```bash
# Track cached tokens with 90% discount
code-monitor --platform claude

# View cache statistics
# • Cache Hit Rate: 45%
# • Savings: $12.50 (90% discount)
# • Cached Tokens: 125,000
# • Cache Efficiency: High ✅
```

### 🔮 ML Predictions

```python
# Intelligent forecasting based on:
• Historical usage patterns (8 days)
• P90 percentile analysis
• Burn rate trends
• Session patterns

# Predictions include:
• Cost projections with confidence scores
• Time to limit estimation
• Usage trend analysis
• Smart limit recommendations
```

---

## 🛠️ Technical Requirements

### 📋 Dependencies

All dependencies are automatically installed:

```toml
openai>=1.0.0                 # OpenAI API client
rich>=13.7.0                  # Terminal UI framework
pydantic>=2.0.0               # Data validation
pydantic-settings>=2.0.0      # Configuration
numpy>=1.21.0                 # Statistical analysis
pytz>=2023.3                  # Timezone support
requests>=2.31.0              # HTTP client
pyyaml>=6.0                   # Configuration files
```

### 🐍 Python Support

<div align="center">

| Version | Status | Recommended |
|:-------:|:------:|:-----------:|
| 3.9 | ✅ Supported | |
| 3.10 | ✅ Supported | |
| 3.11 | ✅ Supported | ⭐ |
| 3.12 | ✅ Supported | ⭐ |

</div>

### 💻 Platform Support

<div align="center">

| OS | Status | Notes |
|:--:|:------:|:------|
| 🐧 Linux | ✅ Full Support | All distributions |
| 🍎 macOS | ✅ Full Support | Intel & Apple Silicon |
| 🪟 Windows | ✅ Full Support | Windows Terminal recommended |

</div>

---

## 🤝 Contributing

We welcome contributions! 🎉

<div align="center">

### 🌟 Ways to Contribute

| Type | Description | How to Help |
|:----:|:------------|:------------|
| 🐛 | Bug Reports | [Open an issue](https://github.com/yourusername/genai-code-usage-monitor/issues) |
| 💡 | Feature Requests | [Start a discussion](https://github.com/yourusername/genai-code-usage-monitor/discussions) |
| 📝 | Documentation | Improve guides and examples |
| 🔧 | Code | Submit pull requests |
| 🌍 | Translations | Help translate documentation |

</div>

### 🚀 Quick Contribution Guide

```bash
# 1. Fork and clone
git clone https://github.com/yourusername/genai-code-usage-monitor.git
cd genai-code-usage-monitor

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install development dependencies
pip install -e ".[dev]"

# 4. Create feature branch
git checkout -b feature/amazing-feature

# 5. Make changes and test
pytest tests/

# 6. Commit and push
git commit -m "feat: Add amazing feature"
git push origin feature/amazing-feature

# 7. Open Pull Request 🎉
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Project Stats

<div align="center">

<img src="https://img.shields.io/github/stars/yourusername/genai-code-usage-monitor?style=social" alt="Stars"/>
<img src="https://img.shields.io/github/forks/yourusername/genai-code-usage-monitor?style=social" alt="Forks"/>
<img src="https://img.shields.io/github/watchers/yourusername/genai-code-usage-monitor?style=social" alt="Watchers"/>

<img src="https://img.shields.io/github/issues/yourusername/genai-code-usage-monitor" alt="Issues"/>
<img src="https://img.shields.io/github/issues-pr/yourusername/genai-code-usage-monitor" alt="Pull Requests"/>
<img src="https://img.shields.io/github/last-commit/yourusername/genai-code-usage-monitor" alt="Last Commit"/>

<img src="https://img.shields.io/github/languages/top/yourusername/genai-code-usage-monitor" alt="Top Language"/>
<img src="https://img.shields.io/github/languages/code-size/yourusername/genai-code-usage-monitor" alt="Code Size"/>
<img src="https://img.shields.io/tokei/lines/github/yourusername/genai-code-usage-monitor" alt="Lines of Code"/>

</div>

---

## 📄 License

<div align="center">

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License - Free to use, modify, and distribute
✅ Commercial use  ✅ Modification  ✅ Distribution  ✅ Private use
```

</div>

---

## 💖 Acknowledgments

<div align="center">

### 🙏 Special Thanks

This project is inspired by [Claude Code Usage Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor)

### 🛠️ Built With Amazing Tools

<img src="https://img.shields.io/badge/Rich-Terminal-ff69b4?style=for-the-badge&logo=windowsterminal&logoColor=white" alt="Rich"/>
<img src="https://img.shields.io/badge/OpenAI-API-00a67e?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"/>
<img src="https://img.shields.io/badge/Claude-API-8b5cf6?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude"/>
<img src="https://img.shields.io/badge/Python-3.9+-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Pydantic-V2-e92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic"/>

</div>

---

## 🌟 Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/genai-code-usage-monitor&type=Date)](https://star-history.com/#yourusername/genai-code-usage-monitor&Date)

</div>

---

## 🔗 Links

<div align="center">

### 📌 Quick Links

[🏠 Homepage](https://github.com/yourusername/genai-code-usage-monitor) •
[📦 PyPI](https://pypi.org/project/genai-code-usage-monitor/) •
[📖 Documentation](https://github.com/yourusername/genai-code-usage-monitor#readme) •
[🐛 Issues](https://github.com/yourusername/genai-code-usage-monitor/issues) •
[💬 Discussions](https://github.com/yourusername/genai-code-usage-monitor/discussions) •
[📜 Changelog](CHANGELOG.md)

</div>

---

<div align="center">

## ⭐ Star Us!

**If you find this project useful, please consider giving it a star!**

<a href="https://github.com/yourusername/genai-code-usage-monitor/stargazers">
  <img src="https://img.shields.io/github/stars/yourusername/genai-code-usage-monitor?style=social" alt="Star on GitHub"/>
</a>

### 🚀 Happy Monitoring!

Made with ❤️ by the GenAI Monitor Team

---

<sub>🌐 <a href="./README.zh-CN.md">中文文档</a> | English</sub>

</div>

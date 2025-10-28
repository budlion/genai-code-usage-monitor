# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-27

### Added
- Initial release of GenAI Code Usage Monitor
- Real-time monitoring with configurable refresh rates (1-60s, 0.1-20 Hz)
- Multiple view modes: realtime, daily, and monthly
- ML-based P90 analysis and predictions
- Rich terminal UI with themes (light, dark, classic, auto)
- Multiple plan support (free, payg, tier1, tier2, custom)
- OpenAI API integration for usage tracking
- Configuration persistence with Pydantic
- Timezone and time format auto-detection
- Custom token and cost limits
- Model-specific pricing calculations
- Burn rate analysis and forecasting
- Advanced warning system with multi-level alerts
- Comprehensive logging with file output support
- Command aliases: genai-code-usage-monitor, genai-code-usage-monitor, cxmonitor, cxm
- Complete test suite with 70%+ coverage
- Full documentation with examples

### Features
- 🔮 ML-based predictions using P90 percentile calculations
- 🔄 Real-time monitoring with intelligent display updates
- 📊 Advanced Rich UI with WCAG-compliant color schemes
- 🤖 Smart auto-detection for plan limits
- 📋 Support for multiple usage plans
- ⚠️ Multi-level alert system
- 💼 Modular architecture following SRP
- 🎨 Intelligent theming with terminal detection
- ⏰ Advanced timezone handling
- 📈 Comprehensive cost analytics
- 🔧 Type-safe configuration management
- 📝 Flexible logging options
- ⚡ Performance optimized caching

## [Unreleased]

### Planned Features
- Integration with OpenAI official usage API
- WebSocket support for real-time updates
- Dashboard web interface
- Export usage reports (CSV, JSON, PDF)
- Budget alerts via email/Slack/Discord
- Multi-user support with team dashboards
- Historical data visualization charts
- Custom alerting rules engine
- Integration with CI/CD pipelines
- Docker containerization
- Kubernetes deployment support
- GraphQL API for programmatic access

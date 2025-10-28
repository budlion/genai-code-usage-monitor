# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD workflows
- Comprehensive test suite (154 tests, 32.85% coverage)
- Security scanning with CodeQL
- Automated dependency updates with Dependabot
- PR templates and issue templates
- Contributing guidelines
- Code quality tools (ruff, black, isort, mypy)

## [2.1.0] - 2025-10-28

### Added
- Alert system tests (23 tests, 50% coverage)
- P90 calculator tests (27 tests, 95% coverage)
- CLI integration tests (41 tests, 35% coverage)
- Test documentation and matrices
- Bug fix: severity capping at 100 in alerts.py

### Changed
- Improved test coverage from 21.22% to 32.85%
- Enhanced project structure with test organization

## [2.0.0] - 2025-10-27

### Added
- Dual platform support (OpenAI + Claude)
- WCAG-compliant themes (Light/Dark/Classic)
- 4-level alert system (INFO/WARNING/CRITICAL/DANGER)
- ML-based predictions (P90 percentile)
- Cached token tracking for Claude (90% discount)
- Multiple view modes (realtime/daily/monthly/compact/limits)
- Real-time monitoring with configurable refresh
- Advanced analytics and burn rate tracking

### Changed
- Project renamed from codex-usage-monitor to genai-code-usage-monitor
- Command renamed to code-monitor
- Complete architecture refactor for dual-platform support

### Fixed
- Various bug fixes and stability improvements

## [1.0.0] - Initial Release

### Added
- Basic OpenAI API usage monitoring
- Simple terminal UI
- Token and cost tracking

---

[Unreleased]: https://github.com/budlion/genai-code-usage-monitor/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/budlion/genai-code-usage-monitor/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/budlion/genai-code-usage-monitor/releases/tag/v2.0.0

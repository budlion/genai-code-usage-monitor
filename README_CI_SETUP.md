# CI/CD Setup Guide

## 🚀 GitHub Actions Workflows

This project uses GitHub Actions for CI/CD, following best practices from popular Python projects like pytest, requests, and rich.

### 📋 Workflows Overview

#### 1. **Tests Workflow** (`.github/workflows/tests.yml`)
Runs on every push and pull request to `main` and `develop` branches.

**Features**:
- ✅ Multi-OS testing (Ubuntu, macOS, Windows)
- ✅ Multi-Python version (3.9, 3.10, 3.11, 3.12)
- ✅ Coverage reporting to Codecov
- ✅ Dependency caching for faster builds

**Jobs**:
- `tests`: Run pytest across all OS/Python combinations
- `lint`: Code quality checks (ruff, black, isort, mypy)
- `coverage`: Generate and upload coverage reports
- `docs`: Validate documentation

#### 2. **Release Workflow** (`.github/workflows/release.yml`)
Triggered on version tags (`v*.*.*`).

**Features**:
- ✅ Automated package building
- ✅ PyPI publishing
- ✅ GitHub Release creation with artifacts

#### 3. **CodeQL Analysis** (`.github/workflows/codeql.yml`)
Security scanning for vulnerabilities.

**Schedule**: Weekly on Mondays + on push to main

#### 4. **Dependency Review** (`.github/workflows/dependency-review.yml`)
Reviews dependencies in pull requests for security issues.

#### 5. **PR Labeler** (`.github/workflows/pr-labeler.yml`)
Automatically labels PRs based on changed files.

### 🔧 Setup Requirements

#### 1. Enable GitHub Actions
GitHub Actions are enabled by default. No setup required.

#### 2. Set Up Codecov (Optional but Recommended)
1. Go to [codecov.io](https://codecov.io/)
2. Sign in with GitHub
3. Add your repository
4. Copy the upload token
5. Add as repository secret: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`
   - Name: `CODECOV_TOKEN`
   - Value: Your Codecov token

#### 3. Set Up PyPI Publishing (For Releases)
1. Create account on [PyPI](https://pypi.org/)
2. Generate API token: `Account settings` → `API tokens`
3. Add as repository secret:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI token

#### 4. Configure Dependabot
Dependabot is configured in `.github/dependabot.yml` and will:
- ✅ Automatically check for dependency updates weekly
- ✅ Create PRs for outdated dependencies
- ✅ Group related dependencies

### 📊 Badges

Add these badges to your README.md:

```markdown
[![Tests](https://github.com/budlion/genai-code-usage-monitor/actions/workflows/tests.yml/badge.svg)](https://github.com/budlion/genai-code-usage-monitor/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/budlion/genai-code-usage-monitor/branch/main/graph/badge.svg)](https://codecov.io/gh/budlion/genai-code-usage-monitor)
[![Python Version](https://img.shields.io/pypi/pyversions/genai-code-usage-monitor.svg)](https://pypi.org/project/genai-code-usage-monitor/)
[![PyPI version](https://badge.fury.io/py/genai-code-usage-monitor.svg)](https://badge.fury.io/py/genai-code-usage-monitor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

### 🎯 CI/CD Features

#### ✨ Highlights
- **Multi-environment testing**: Linux, macOS, Windows
- **Multiple Python versions**: 3.9 through 3.12
- **Code quality enforcement**: ruff, black, isort, mypy
- **Security scanning**: CodeQL + dependency review
- **Automated releases**: Tag → Build → PyPI + GitHub Release
- **Coverage tracking**: Integrated with Codecov
- **Smart caching**: Dependencies cached for faster builds

#### 🔒 Security
- **CodeQL**: Continuous security analysis
- **Dependency Review**: PR dependency scanning
- **Dependabot**: Automated security updates

#### 📈 Quality Gates
Tests workflow requires:
- ✅ All tests passing
- ✅ Linting checks passing (with continue-on-error for gradual adoption)
- ✅ Documentation validation
- ⚠️ Coverage reporting (informational)

### 🚢 Release Process

1. **Update version** in `pyproject.toml`
2. **Commit and tag**:
   ```bash
   git commit -am "chore: bump version to 2.2.0"
   git tag v2.2.0
   git push origin main --tags
   ```
3. **GitHub Actions automatically**:
   - Builds distribution packages
   - Runs all tests
   - Publishes to PyPI
   - Creates GitHub Release with artifacts

### 🏃 Running CI Checks Locally

Before pushing, run these locally:

```bash
# Run tests
pytest tests/ -v --cov

# Run linters
ruff check src/ tests/
black --check src/ tests/
isort --check-only src/ tests/
mypy src/

# Format code
black src/ tests/
isort src/ tests/

# Build package
python -m build
twine check dist/*
```

### 📝 Contributing

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for detailed contribution guidelines.

### 🔍 Monitoring

- **Actions Tab**: View all workflow runs
- **Codecov Dashboard**: Track coverage over time
- **Security Tab**: Review CodeQL alerts
- **Insights → Dependency graph**: Monitor dependencies

### 🎓 Best Practices Applied

Based on popular Python projects:
- ✅ **pytest**: Multi-OS testing, extensive coverage
- ✅ **requests**: Clear contribution guidelines, automated releases
- ✅ **rich**: Modern CI/CD with matrix builds
- ✅ **FastAPI**: Comprehensive linting and type checking
- ✅ **Django**: Security scanning and dependency management

---

**Setup Date**: 2025-10-28
**Status**: ✅ Ready to use

## 🎨 Adding CI Badges to README

Already added to README.md! The badges include:
- [![Tests](https://github.com/budlion/genai-code-usage-monitor/actions/workflows/tests.yml/badge.svg)](https://github.com/budlion/genai-code-usage-monitor/actions/workflows/tests.yml)
- [![codecov](https://codecov.io/gh/budlion/genai-code-usage-monitor/branch/main/graph/badge.svg)](https://codecov.io/gh/budlion/genai-code-usage-monitor)
- [![PyPI version](https://img.shields.io/pypi/v/genai-code-usage-monitor.svg)](https://pypi.org/project/genai-code-usage-monitor/)
- [![Python Versions](https://img.shields.io/pypi/pyversions/genai-code-usage-monitor.svg)](https://pypi.org/project/genai-code-usage-monitor/)
- [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

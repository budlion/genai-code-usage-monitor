# Contributing to GenAI Code Usage Monitor

🎉 Thank you for considering contributing to GenAI Code Usage Monitor!

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/genai-code-usage-monitor.git
   cd genai-code-usage-monitor
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/budlion/genai-code-usage-monitor.git
   ```

## Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Verify installation**:
   ```bash
   pytest tests/ -v
   ```

## Making Changes

1. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes**

3. **Run tests**:
   ```bash
   pytest tests/ -v --cov
   ```

4. **Run linters**:
   ```bash
   ruff check src/ tests/
   black src/ tests/
   isort src/ tests/
   mypy src/
   ```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_core/test_alerts.py -v

# Run with coverage
pytest tests/ --cov=src/genai_code_usage_monitor --cov-report=html

# Run in parallel
pytest tests/ -n auto
```

### Writing Tests

- Place tests in appropriate `tests/` subdirectory
- Follow the naming convention: `test_*.py`
- Use descriptive test names
- Include docstrings explaining what the test validates
- Aim for >70% code coverage for new code

Example:
```python
def test_alert_system_danger_level():
    """Test that DANGER level alerts trigger at >95% usage."""
    # Test implementation
```

## Code Style

We follow these style guidelines:

- **PEP 8** for Python code
- **Black** for code formatting (line length: 100)
- **isort** for import sorting
- **ruff** for linting
- **Type hints** for function signatures

### Format your code

```bash
# Format with black
black src/ tests/

# Sort imports
isort src/ tests/

# Check with ruff
ruff check src/ tests/
```

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
feat(alerts): add support for custom alert thresholds

Add ability to configure custom alert thresholds via settings.
This allows users to define their own WARNING/CRITICAL levels.

Closes #123
```

```bash
fix(cli): correct argument parsing for --platform option

Fixed issue where --platform=all wasn't properly initializing
both platforms simultaneously.

Fixes #456
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** (if applicable)
5. **Create pull request** with clear description
6. **Link related issues**
7. **Wait for review**

### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG updated (if applicable)
- [ ] No new warnings
- [ ] Coverage maintained or improved

## Questions?

- Open a [Discussion](https://github.com/budlion/genai-code-usage-monitor/discussions)
- Ask in an [Issue](https://github.com/budlion/genai-code-usage-monitor/issues)

---

Thank you for contributing! 🙌

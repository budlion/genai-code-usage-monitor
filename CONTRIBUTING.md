# Contributing to GenAI Code Usage Monitor

Thank you for your interest in contributing to GenAI Code Usage Monitor! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your changes
4. Make your changes
5. Push to your fork and submit a pull request

## Development Setup

### Prerequisites

- Python 3.9 or higher
- uv (recommended) or pip
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/yourusername/genai-code-usage-monitor.git
cd genai-code-usage-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-view` - For new features
- `fix/calculation-bug` - For bug fixes
- `docs/update-readme` - For documentation changes
- `refactor/improve-performance` - For refactoring

### Commit Messages

Follow the conventional commits format:

```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(ui): add monthly view with aggregated statistics

- Implement monthly aggregation logic
- Add Rich table for monthly display
- Include model-specific breakdowns

Closes #123
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=genai_code_usage_monitor --cov-report=html

# Run specific test file
pytest tests/test_core/test_models.py

# Run with verbosity
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Mirror the source structure in tests
- Use descriptive test names
- Include docstrings explaining what is being tested
- Aim for >70% code coverage

Example:
```python
def test_pricing_calculator_with_gpt4():
    """Test pricing calculation for GPT-4 model."""
    calc = PricingCalculator()
    cost = calc.calculate_cost("gpt-4", 1000, 500)
    assert cost > 0
    assert isinstance(cost, float)
```

## Submitting Changes

### Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Create a pull request with a clear description

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new features
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented if unavoidable)
```

## Style Guidelines

### Python Code Style

We follow PEP 8 with some modifications:

- Line length: 88 characters (Black default)
- Use type hints for function signatures
- Use docstrings for all public functions and classes
- Use f-strings for string formatting

### Code Formatting

We use these tools (configured in `pyproject.toml`):

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Linting
- **mypy**: Type checking

Run formatting:
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/
```

### Documentation Style

- Use Google-style docstrings
- Include type information in docstrings
- Provide examples for complex functions
- Keep README.md up to date

Example docstring:
```python
def calculate_cost(
    self, model: str, prompt_tokens: int, completion_tokens: int
) -> float:
    """
    Calculate cost for an API call.

    Args:
        model: Model name (e.g., "gpt-4")
        prompt_tokens: Number of prompt tokens
        completion_tokens: Number of completion tokens

    Returns:
        Total cost in USD

    Example:
        >>> calc = PricingCalculator()
        >>> cost = calc.calculate_cost("gpt-4", 1000, 500)
        >>> print(f"${cost:.2f}")
        $0.07
    """
```

## Questions?

Feel free to open an issue for questions or discussion before starting work on a significant change.

Thank you for contributing! 🎉

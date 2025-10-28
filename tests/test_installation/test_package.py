"""Tests for package installation and setup."""

import importlib
import subprocess
import sys
from pathlib import Path

import pytest


class TestPackageStructure:
    """Test package structure and imports."""

    def test_package_can_be_imported(self):
        """Test that the package can be imported."""
        import genai_code_usage_monitor

        assert genai_code_usage_monitor is not None

    def test_version_exists(self):
        """Test that version information is available."""
        import genai_code_usage_monitor

        assert hasattr(genai_code_usage_monitor, "__version__")
        assert genai_code_usage_monitor.__version__ is not None

    def test_version_format(self):
        """Test that version follows semantic versioning."""
        import genai_code_usage_monitor

        version = genai_code_usage_monitor.__version__
        parts = version.split(".")
        assert len(parts) >= 2, f"Version {version} should have at least 2 parts"
        assert parts[0].isdigit(), f"Major version should be numeric: {parts[0]}"
        assert parts[1].isdigit(), f"Minor version should be numeric: {parts[1]}"

    def test_main_module_exists(self):
        """Test that __main__ module exists."""
        import genai_code_usage_monitor.__main__

        assert genai_code_usage_monitor.__main__ is not None
        assert hasattr(genai_code_usage_monitor.__main__, "main")

    def test_cli_module_exists(self):
        """Test that CLI module exists."""
        from genai_code_usage_monitor.cli import main

        assert main is not None

    def test_core_modules_exist(self):
        """Test that core modules can be imported."""
        from genai_code_usage_monitor.core import alerts
        from genai_code_usage_monitor.core import models
        from genai_code_usage_monitor.core import p90_calculator
        from genai_code_usage_monitor.core import plans
        from genai_code_usage_monitor.core import pricing

        assert alerts is not None
        assert models is not None
        assert p90_calculator is not None
        assert plans is not None
        assert pricing is not None

    def test_ui_modules_exist(self):
        """Test that UI modules can be imported."""
        from genai_code_usage_monitor.ui import components
        from genai_code_usage_monitor.ui import display
        from genai_code_usage_monitor.ui import themes

        assert components is not None
        assert display is not None
        assert themes is not None

    def test_platform_modules_exist(self):
        """Test that platform modules can be imported."""
        from genai_code_usage_monitor.platforms import base
        from genai_code_usage_monitor.platforms import claude
        from genai_code_usage_monitor.platforms import codex

        assert base is not None
        assert claude is not None
        assert codex is not None


class TestCommandAliases:
    """Test command aliases installation."""

    @pytest.fixture
    def venv_bin_path(self):
        """Get the venv bin path."""
        # Find the venv bin directory
        if sys.platform == "win32":
            scripts_dir = Path(sys.prefix) / "Scripts"
        else:
            scripts_dir = Path(sys.prefix) / "bin"

        return scripts_dir

    def test_code_monitor_command_exists(self, venv_bin_path):
        """Test that code-monitor command exists."""
        cmd_path = venv_bin_path / "code-monitor"
        if sys.platform == "win32":
            cmd_path = venv_bin_path / "code-monitor.exe"

        assert cmd_path.exists(), f"code-monitor not found at {cmd_path}"

    def test_genai_monitor_command_exists(self, venv_bin_path):
        """Test that genai-monitor command exists."""
        cmd_path = venv_bin_path / "genai-monitor"
        if sys.platform == "win32":
            cmd_path = venv_bin_path / "genai-monitor.exe"

        assert cmd_path.exists(), f"genai-monitor not found at {cmd_path}"

    def test_gm_command_exists(self, venv_bin_path):
        """Test that gm command exists."""
        cmd_path = venv_bin_path / "gm"
        if sys.platform == "win32":
            cmd_path = venv_bin_path / "gm.exe"

        assert cmd_path.exists(), f"gm not found at {cmd_path}"

    def test_code_monitor_help(self, venv_bin_path):
        """Test that code-monitor --help works."""
        cmd = str(venv_bin_path / "code-monitor")
        result = subprocess.run(
            [cmd, "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        assert "usage: code-monitor" in result.stdout

    def test_genai_monitor_help(self, venv_bin_path):
        """Test that genai-monitor --help works."""
        cmd = str(venv_bin_path / "genai-monitor")
        result = subprocess.run(
            [cmd, "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        assert "usage: genai-monitor" in result.stdout

    def test_gm_help(self, venv_bin_path):
        """Test that gm --help works."""
        cmd = str(venv_bin_path / "gm")
        result = subprocess.run(
            [cmd, "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        assert "usage: gm" in result.stdout

    def test_version_command(self, venv_bin_path):
        """Test that --version command works."""
        cmd = str(venv_bin_path / "code-monitor")
        result = subprocess.run(
            [cmd, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        # Should output version information
        output = result.stdout + result.stderr
        assert len(output) > 0


class TestPackageMetadata:
    """Test package metadata."""

    def test_package_name(self):
        """Test that package name is correct."""
        import genai_code_usage_monitor

        metadata = importlib.metadata.metadata("genai-code-usage-monitor")
        assert metadata["Name"] == "genai-code-usage-monitor"

    def test_package_version(self):
        """Test that package version matches."""
        import genai_code_usage_monitor

        metadata_version = importlib.metadata.version("genai-code-usage-monitor")
        code_version = genai_code_usage_monitor.__version__
        assert metadata_version == code_version

    def test_package_author(self):
        """Test that package author is set."""
        metadata = importlib.metadata.metadata("genai-code-usage-monitor")
        assert "Author-Email" in metadata or "Author" in metadata

    def test_package_description(self):
        """Test that package description exists."""
        metadata = importlib.metadata.metadata("genai-code-usage-monitor")
        assert "Summary" in metadata
        assert len(metadata["Summary"]) > 0

    def test_package_entry_points(self):
        """Test that entry points are registered."""
        eps = importlib.metadata.entry_points()

        # Get console_scripts group
        if hasattr(eps, "select"):
            # Python 3.10+
            console_scripts = eps.select(group="console_scripts")
        else:
            # Python 3.9
            console_scripts = eps.get("console_scripts", [])

        # Convert to list of names
        script_names = [ep.name for ep in console_scripts]

        assert "code-monitor" in script_names
        assert "genai-monitor" in script_names
        assert "gm" in script_names


class TestDependencies:
    """Test package dependencies."""

    def test_required_dependencies_installed(self):
        """Test that all required dependencies are installed."""
        required_packages = [
            "openai",
            "numpy",
            "pydantic",
            "pydantic-settings",
            "pyyaml",
            "pytz",
            "rich",
            "requests",
        ]

        for package in required_packages:
            try:
                importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                pytest.fail(f"Required package '{package}' is not installed")

    def test_dependencies_can_be_imported(self):
        """Test that dependencies can be imported."""
        import numpy
        import openai
        import pydantic
        import pytz
        import requests
        import rich
        import yaml

        assert numpy is not None
        assert openai is not None
        assert pydantic is not None
        assert pytz is not None
        assert requests is not None
        assert rich is not None
        assert yaml is not None


class TestDevDependencies:
    """Test development dependencies."""

    def test_dev_dependencies_exist(self):
        """Test that dev dependencies exist when installed."""
        dev_packages = [
            "pytest",
            "pytest-cov",
            "ruff",
            "black",
            "isort",
            "mypy",
        ]

        missing = []
        for package in dev_packages:
            try:
                importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                missing.append(package)

        if missing:
            pytest.skip(f"Dev dependencies not installed: {', '.join(missing)}")

"""Comprehensive tests for CLI main entry point.

Tests command-line interface features mentioned in README:
- Platform selection (codex/claude/all)
- View modes (realtime/daily/monthly/compact/limits)
- Theme selection (auto/light/dark/classic)
- Plan configuration
"""

import argparse
from unittest.mock import Mock, patch, MagicMock
import pytest

from genai_code_usage_monitor.cli.main import create_parser
from genai_code_usage_monitor.core.plans import PLANS


class TestArgumentParser:
    """Test argument parser configuration and defaults."""

    def test_parser_creation(self):
        """Test that parser can be created."""
        parser = create_parser()
        
        assert parser is not None
        assert isinstance(parser, argparse.ArgumentParser)

    def test_default_values(self):
        """Test default argument values match README."""
        parser = create_parser()
        args = parser.parse_args([])
        
        # Default values from README
        assert args.platform == "all"
        assert args.plan == "custom"
        assert args.view == "realtime"
        assert args.theme == "auto"

    def test_platform_choices(self):
        """Test valid platform choices: codex, claude, all."""
        parser = create_parser()
        
        # Valid choices should parse successfully
        args_codex = parser.parse_args(["--platform", "codex"])
        assert args_codex.platform == "codex"
        
        args_claude = parser.parse_args(["--platform", "claude"])
        assert args_claude.platform == "claude"
        
        args_all = parser.parse_args(["--platform", "all"])
        assert args_all.platform == "all"

    def test_invalid_platform(self):
        """Test that invalid platform choice raises error."""
        parser = create_parser()
        
        with pytest.raises(SystemExit):
            parser.parse_args(["--platform", "invalid"])

    def test_view_mode_choices(self):
        """Test valid view mode choices."""
        parser = create_parser()
        
        valid_views = ["realtime", "daily", "monthly", "compact", "limits"]
        
        for view in valid_views:
            args = parser.parse_args(["--view", view])
            assert args.view == view

    def test_invalid_view_mode(self):
        """Test that invalid view mode raises error."""
        parser = create_parser()
        
        with pytest.raises(SystemExit):
            parser.parse_args(["--view", "invalid"])

    def test_theme_choices(self):
        """Test valid theme choices: auto, light, dark, classic."""
        parser = create_parser()
        
        valid_themes = ["auto", "light", "dark", "classic"]
        
        for theme in valid_themes:
            args = parser.parse_args(["--theme", theme])
            assert args.theme == theme

    def test_invalid_theme(self):
        """Test that invalid theme raises error."""
        parser = create_parser()
        
        with pytest.raises(SystemExit):
            parser.parse_args(["--theme", "neon"])

    def test_plan_choices(self):
        """Test that all PLANS are valid choices."""
        parser = create_parser()
        
        for plan_name in PLANS.keys():
            args = parser.parse_args(["--plan", plan_name])
            assert args.plan == plan_name

    def test_custom_token_limit(self):
        """Test custom token limit argument."""
        parser = create_parser()
        args = parser.parse_args(["--custom-limit-tokens", "50000"])
        
        assert args.custom_limit_tokens == 50000

    def test_custom_cost_limit(self):
        """Test custom cost limit argument."""
        parser = create_parser()
        args = parser.parse_args(["--custom-limit-cost", "25.50"])
        
        assert args.custom_limit_cost == 25.5

    def test_timezone_option(self):
        """Test timezone configuration option."""
        parser = create_parser()
        args = parser.parse_args(["--timezone", "America/New_York"])
        
        assert args.timezone == "America/New_York"

    def test_reset_hour_option(self):
        """Test daily reset hour option."""
        parser = create_parser()
        args = parser.parse_args(["--reset-hour", "6"])
        
        assert args.reset_hour == 6


class TestPlatformSelection:
    """Test platform selection logic."""

    def test_codex_only_selection(self):
        """Test --platform=codex selects OpenAI only."""
        parser = create_parser()
        args = parser.parse_args(["--platform", "codex"])
        
        assert args.platform == "codex"

    def test_claude_only_selection(self):
        """Test --platform=claude selects Claude only."""
        parser = create_parser()
        args = parser.parse_args(["--platform", "claude"])
        
        assert args.platform == "claude"

    def test_dual_platform_selection(self):
        """Test --platform=all selects both platforms."""
        parser = create_parser()
        args = parser.parse_args(["--platform", "all"])
        
        assert args.platform == "all"

    def test_default_is_all_platforms(self):
        """Test that default platform is 'all' (both)."""
        parser = create_parser()
        args = parser.parse_args([])
        
        assert args.platform == "all"


class TestPlanIntegration:
    """Test plan configuration."""

    def test_free_plan(self):
        """Test free plan selection."""
        parser = create_parser()
        args = parser.parse_args(["--plan", "free"])
        
        assert args.plan == "free"
        assert "free" in PLANS

    def test_pay_as_you_go_plan(self):
        """Test pay-as-you-go plan selection."""
        parser = create_parser()
        args = parser.parse_args(["--plan", "payg"])

        assert args.plan == "payg"

    def test_custom_plan_with_limits(self):
        """Test custom plan with custom limits."""
        parser = create_parser()
        args = parser.parse_args([
            "--plan", "custom",
            "--custom-limit-tokens", "100000",
            "--custom-limit-cost", "50.0"
        ])
        
        assert args.plan == "custom"
        assert args.custom_limit_tokens == 100000
        assert args.custom_limit_cost == 50.0


class TestViewModes:
    """Test view mode configuration."""

    def test_realtime_view(self):
        """Test realtime view mode (default)."""
        parser = create_parser()
        args = parser.parse_args(["--view", "realtime"])
        
        assert args.view == "realtime"

    def test_daily_view(self):
        """Test daily aggregated view."""
        parser = create_parser()
        args = parser.parse_args(["--view", "daily"])
        
        assert args.view == "daily"

    def test_monthly_view(self):
        """Test monthly aggregated view."""
        parser = create_parser()
        args = parser.parse_args(["--view", "monthly"])
        
        assert args.view == "monthly"

    def test_compact_view(self):
        """Test compact view mode."""
        parser = create_parser()
        args = parser.parse_args(["--view", "compact"])
        
        assert args.view == "compact"

    def test_limits_view(self):
        """Test limits-focused view."""
        parser = create_parser()
        args = parser.parse_args(["--view", "limits"])
        
        assert args.view == "limits"


class TestComplexArgumentCombinations:
    """Test complex combinations of arguments."""

    def test_codex_with_dark_theme_realtime(self):
        """Test codex + dark theme + realtime view."""
        parser = create_parser()
        args = parser.parse_args([
            "--platform", "codex",
            "--theme", "dark",
            "--view", "realtime"
        ])
        
        assert args.platform == "codex"
        assert args.theme == "dark"
        assert args.view == "realtime"

    def test_claude_with_light_theme_daily(self):
        """Test claude + light theme + daily view."""
        parser = create_parser()
        args = parser.parse_args([
            "--platform", "claude",
            "--theme", "light",
            "--view", "daily"
        ])
        
        assert args.platform == "claude"
        assert args.theme == "light"
        assert args.view == "daily"

    def test_all_platforms_with_custom_plan(self):
        """Test both platforms + custom plan with limits."""
        parser = create_parser()
        args = parser.parse_args([
            "--platform", "all",
            "--plan", "custom",
            "--custom-limit-tokens", "200000",
            "--custom-limit-cost", "100.0",
            "--view", "compact",
            "--theme", "classic"
        ])
        
        assert args.platform == "all"
        assert args.plan == "custom"
        assert args.custom_limit_tokens == 200000
        assert args.custom_limit_cost == 100.0
        assert args.view == "compact"
        assert args.theme == "classic"


class TestTimeConfiguration:
    """Test time-related configuration options."""

    def test_timezone_auto_detection(self):
        """Test auto timezone detection (default)."""
        parser = create_parser()
        args = parser.parse_args([])
        
        assert args.timezone == "auto"

    def test_custom_timezone(self):
        """Test custom timezone setting."""
        parser = create_parser()
        args = parser.parse_args(["--timezone", "Europe/London"])
        
        assert args.timezone == "Europe/London"

    def test_12_hour_format(self):
        """Test 12-hour time format."""
        parser = create_parser()
        args = parser.parse_args(["--time-format", "12h"])
        
        assert args.time_format == "12h"

    def test_24_hour_format(self):
        """Test 24-hour time format."""
        parser = create_parser()
        args = parser.parse_args(["--time-format", "24h"])
        
        assert args.time_format == "24h"

    def test_auto_time_format(self):
        """Test auto time format detection (default)."""
        parser = create_parser()
        args = parser.parse_args([])
        
        assert args.time_format == "auto"

    def test_custom_reset_hour(self):
        """Test custom daily reset hour."""
        parser = create_parser()
        
        # Test valid hours (0-23)
        for hour in [0, 6, 12, 18, 23]:
            args = parser.parse_args(["--reset-hour", str(hour)])
            assert args.reset_hour == hour

    def test_default_reset_hour(self):
        """Test default reset hour is midnight (0)."""
        parser = create_parser()
        args = parser.parse_args([])
        
        assert args.reset_hour == 0


class TestHelp:
    """Test help text and documentation."""

    def test_help_includes_platform_description(self):
        """Test that help text includes platform choices."""
        parser = create_parser()
        help_text = parser.format_help()
        
        assert "platform" in help_text.lower()
        assert "codex" in help_text.lower()
        assert "claude" in help_text.lower()

    def test_help_includes_view_modes(self):
        """Test that help text includes view mode choices."""
        parser = create_parser()
        help_text = parser.format_help()
        
        assert "view" in help_text.lower()
        assert "realtime" in help_text.lower()
        assert "daily" in help_text.lower()

    def test_help_includes_themes(self):
        """Test that help text includes theme choices."""
        parser = create_parser()
        help_text = parser.format_help()
        
        assert "theme" in help_text.lower()
        assert "light" in help_text.lower()
        assert "dark" in help_text.lower()


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_arguments(self):
        """Test with no arguments uses all defaults."""
        parser = create_parser()
        args = parser.parse_args([])
        
        # Should not raise and should have defaults
        assert args.platform == "all"
        assert args.view == "realtime"
        assert args.theme == "auto"
        assert args.plan == "custom"

    def test_negative_custom_limits_accepted(self):
        """Test that parser accepts negative values (validation elsewhere)."""
        parser = create_parser()
        
        # Parser doesn't validate ranges, just types
        args = parser.parse_args(["--custom-limit-tokens", "-1000"])
        assert args.custom_limit_tokens == -1000

    def test_very_large_custom_limits(self):
        """Test with very large custom limits."""
        parser = create_parser()
        args = parser.parse_args([
            "--custom-limit-tokens", "10000000",
            "--custom-limit-cost", "10000.0"
        ])
        
        assert args.custom_limit_tokens == 10000000
        assert args.custom_limit_cost == 10000.0

    def test_zero_custom_limits(self):
        """Test with zero custom limits."""
        parser = create_parser()
        args = parser.parse_args([
            "--custom-limit-tokens", "0",
            "--custom-limit-cost", "0.0"
        ])
        
        assert args.custom_limit_tokens == 0
        assert args.custom_limit_cost == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

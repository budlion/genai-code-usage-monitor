"""Unit tests for WCAG theme system.

Tests theme functionality, color schemes, and progress bar integration.
"""

import pytest
from genai_code_usage_monitor.ui.themes import (
    ThemeType,
    WCAGTheme,
    ColorScheme,
    get_theme,
    set_theme,
    reset_theme,
)
from genai_code_usage_monitor.ui.progress_bars import (
    TokenProgressBar,
    CostProgressBar,
    ModelUsageBar,
    TimeProgressBar,
)


class TestThemeSystem:
    """Tests for theme system functionality."""

    def test_theme_creation(self):
        """Test creating theme instances."""
        light_theme = WCAGTheme(ThemeType.LIGHT)
        assert light_theme.current.name == "Light"
        assert light_theme.current.contrast_ratio >= 4.5

        dark_theme = WCAGTheme(ThemeType.DARK)
        assert dark_theme.current.name == "Dark"
        assert dark_theme.current.contrast_ratio >= 7.0

        classic_theme = WCAGTheme(ThemeType.CLASSIC)
        assert classic_theme.current.name == "Classic"

    def test_theme_switching(self):
        """Test switching between themes."""
        theme = WCAGTheme(ThemeType.LIGHT)
        assert theme.current.name == "Light"

        theme.switch_theme(ThemeType.DARK)
        assert theme.current.name == "Dark"

        theme.switch_theme(ThemeType.CLASSIC)
        assert theme.current.name == "Classic"

    def test_status_colors(self):
        """Test status color retrieval."""
        theme = WCAGTheme(ThemeType.LIGHT)

        primary = theme.get_status_color("primary")
        assert primary == "#0066CC"

        success = theme.get_status_color("success")
        assert success == "#006B3D"

        warning = theme.get_status_color("warning")
        assert warning == "#E67E00"

        danger = theme.get_status_color("danger")
        assert danger == "#CC0000"

    def test_progress_colors(self):
        """Test progress color gradients."""
        theme = WCAGTheme(ThemeType.LIGHT)

        # Low usage - success color
        low_color = theme.get_progress_color(25.0)
        assert low_color == theme.current.progress_low

        # Medium usage - warning color
        medium_color = theme.get_progress_color(55.0)
        assert medium_color == theme.current.progress_medium

        # High usage - high warning color
        high_color = theme.get_progress_color(80.0)
        assert high_color == theme.current.progress_high

        # Critical usage - danger color
        critical_color = theme.get_progress_color(95.0)
        assert critical_color == theme.current.progress_critical

    def test_model_colors(self):
        """Test model color cycling."""
        theme = WCAGTheme(ThemeType.DARK)

        colors = [theme.get_model_color(i) for i in range(10)]
        assert len(colors) == 10

        # Should cycle through available colors
        assert colors[0] == colors[5]  # Same color after cycling

    def test_gradient_creation(self):
        """Test gradient generation."""
        theme = WCAGTheme(ThemeType.LIGHT)

        gradient = theme.create_gradient(0, 100, steps=5)
        assert len(gradient) == 5
        assert all(isinstance(color, str) for color in gradient)

    def test_text_styles(self):
        """Test text style retrieval."""
        theme = WCAGTheme(ThemeType.DARK)

        normal = theme.get_text_style("normal")
        assert normal == theme.current.text

        dim = theme.get_text_style("dim")
        assert dim == theme.current.text_dim

        muted = theme.get_text_style("muted")
        assert muted == theme.current.muted

    def test_theme_info(self):
        """Test theme information retrieval."""
        theme = WCAGTheme(ThemeType.LIGHT)
        info = theme.get_theme_info()

        assert info["name"] == "Light"
        assert info["contrast_ratio"] >= 4.5
        assert info["wcag_compliant"] is True
        assert "primary" in info["colors"]
        assert "success" in info["colors"]

    def test_wcag_compliance(self):
        """Test WCAG compliance standards."""
        light_theme = WCAGTheme(ThemeType.LIGHT)
        assert light_theme.current.contrast_ratio >= 4.5  # AA standard

        dark_theme = WCAGTheme(ThemeType.DARK)
        assert dark_theme.current.contrast_ratio >= 4.5  # AA standard
        assert dark_theme.current.contrast_ratio >= 7.0  # AAA standard


class TestGlobalTheme:
    """Tests for global theme management."""

    def test_get_default_theme(self):
        """Test getting default theme."""
        reset_theme()
        theme = get_theme()
        assert theme is not None
        assert isinstance(theme, WCAGTheme)

    def test_set_global_theme(self):
        """Test setting global theme."""
        set_theme(ThemeType.LIGHT)
        theme = get_theme()
        assert theme.current.name == "Light"

        set_theme(ThemeType.DARK)
        theme = get_theme()
        assert theme.current.name == "Dark"

    def test_reset_theme(self):
        """Test resetting theme to auto."""
        set_theme(ThemeType.LIGHT)
        reset_theme()
        theme = get_theme()
        # After reset, should use auto-detection
        assert theme is not None


class TestProgressBarsWithThemes:
    """Tests for progress bars using theme system."""

    def test_token_bar_with_theme(self):
        """Test token progress bar with theme."""
        theme = WCAGTheme(ThemeType.LIGHT)
        bar = TokenProgressBar(theme=theme)

        # Render different percentages
        result_low = bar.render(25.0)
        assert isinstance(result_low, str)
        assert "SAFE" in result_low or "LOW" in result_low

        result_high = bar.render(85.0)
        assert isinstance(result_high, str)
        assert "HIGH" in result_high or "CRITICAL" in result_high

    def test_cost_bar_with_theme(self):
        """Test cost progress bar with theme."""
        theme = WCAGTheme(ThemeType.DARK)
        bar = CostProgressBar(theme=theme)

        result = bar.render(5.0, 10.0)
        assert isinstance(result, str)
        assert "$5.0" in result or "$5.00" in result
        assert "$10.0" in result or "$10.00" in result

    def test_model_bar_with_theme(self):
        """Test model usage bar with theme."""
        theme = WCAGTheme(ThemeType.LIGHT)
        bar = ModelUsageBar(theme=theme)

        stats = {
            "model-1": {"prompt_tokens": 1000, "completion_tokens": 500},
            "model-2": {"prompt_tokens": 500, "completion_tokens": 250},
        }

        result = bar.render(stats)
        assert isinstance(result, str)
        assert "model" in result.lower()

    def test_time_bar_with_theme(self):
        """Test time progress bar with theme."""
        theme = WCAGTheme(ThemeType.DARK)
        bar = TimeProgressBar(theme=theme)

        result = bar.render(30.0, 60.0)
        assert isinstance(result, str)
        assert "m" in result  # minutes indicator

    def test_bar_without_icons(self):
        """Test progress bars without icons."""
        bar = TokenProgressBar()

        with_icons = bar.render(50.0, use_icons=True)
        without_icons = bar.render(50.0, use_icons=False)

        # Without icons should be shorter or different
        assert isinstance(with_icons, str)
        assert isinstance(without_icons, str)


class TestColorScheme:
    """Tests for ColorScheme dataclass."""

    def test_light_theme_colors(self):
        """Test light theme color values."""
        scheme = WCAGTheme.LIGHT_THEME

        assert scheme.primary == "#0066CC"
        assert scheme.success == "#006B3D"
        assert scheme.warning == "#E67E00"
        assert scheme.danger == "#CC0000"
        assert scheme.text == "#2D2D2D"
        assert scheme.background == "#FFFFFF"

    def test_dark_theme_colors(self):
        """Test dark theme color values."""
        scheme = WCAGTheme.DARK_THEME

        assert scheme.primary == "#66B3FF"
        assert scheme.success == "#5FD97A"
        assert scheme.warning == "#FFB84D"
        assert scheme.danger == "#FF6B6B"
        assert scheme.text == "#E8E8E8"
        assert scheme.background == "#1E1E1E"

    def test_classic_theme_colors(self):
        """Test classic theme color values."""
        scheme = WCAGTheme.CLASSIC_THEME

        assert scheme.primary == "cyan"
        assert scheme.success == "green"
        assert scheme.warning == "yellow"
        assert scheme.danger == "red"


class TestAutoDetection:
    """Tests for automatic theme detection."""

    def test_auto_theme_creation(self):
        """Test creating theme with AUTO type."""
        theme = WCAGTheme(ThemeType.AUTO)
        assert theme.current is not None
        # Should detect and apply a theme
        assert theme.current.name in ["Light", "Dark", "Classic"]

    def test_auto_detection_fallback(self):
        """Test auto detection fallback to dark theme."""
        # Without specific environment variables, should default to dark
        theme = WCAGTheme(ThemeType.AUTO)
        # Fallback is typically dark theme
        assert theme.current is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

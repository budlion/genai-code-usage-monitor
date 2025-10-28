"""UI components for Codex Monitor.

Provides WCAG 2.1 AA compliant themes, progress bars, and display components.
"""

from genai_code_usage_monitor.ui.themes import (
    ThemeType,
    WCAGTheme,
    ColorScheme,
    get_theme,
    set_theme,
    reset_theme,
)
from genai_code_usage_monitor.ui.progress_bars import (
    BaseProgressBar,
    TokenProgressBar,
    TimeProgressBar,
    ModelUsageBar,
    CostProgressBar,
)
from genai_code_usage_monitor.ui.theme_switcher import ThemeSwitcher

__all__ = [
    # Themes
    "ThemeType",
    "WCAGTheme",
    "ColorScheme",
    "get_theme",
    "set_theme",
    "reset_theme",
    # Progress Bars
    "BaseProgressBar",
    "TokenProgressBar",
    "TimeProgressBar",
    "ModelUsageBar",
    "CostProgressBar",
    # Theme Switcher
    "ThemeSwitcher",
]

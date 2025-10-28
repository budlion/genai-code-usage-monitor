"""Progress bar components for Codex Monitor.

Provides token usage, time progress, and model usage progress bars with enhanced visuals.
Supports WCAG 2.1 AA compliant themes, gradients, and animations.
"""

import time
from typing import Any, Dict, Optional

from genai_code_usage_monitor.ui.themes import get_theme, WCAGTheme


class BaseProgressBar:
    """Base class for progress bars with gradient and 3D effects.

    Features:
    - WCAG-compliant color schemes
    - Gradient color transitions
    - Pulse animations for critical states
    - 3D visual effects
    """

    def __init__(self, width: int = 50, theme: Optional[WCAGTheme] = None):
        """Initialize progress bar.

        Args:
            width: Width of progress bar in characters
            theme: Optional theme instance (uses global theme if None)
        """
        self.width = width
        self.theme = theme or get_theme()
        self._last_render_time = 0

    def _calculate_filled(self, percentage: float) -> int:
        """Calculate filled segments."""
        bounded = max(0, min(percentage, 100.0))
        return int(self.width * bounded / 100.0)

    def _get_gradient_color(self, percentage: float) -> str:
        """Get gradient color based on percentage using WCAG theme.

        Uses theme's progress color scheme which is automatically selected
        based on current theme (light/dark/classic).

        Args:
            percentage: Progress percentage

        Returns:
            WCAG-compliant color code
        """
        return self.theme.get_progress_color(percentage)

    def _should_pulse(self, percentage: float) -> bool:
        """Determine if bar should pulse (when approaching limits).

        Args:
            percentage: Progress percentage

        Returns:
            True if should pulse
        """
        return percentage >= 85.0

    def _get_pulse_char(self, percentage: float) -> str:
        """Get pulsing character based on time for animation effect.

        Args:
            percentage: Progress percentage

        Returns:
            Character to use for filled bar
        """
        if not self._should_pulse(percentage):
            return "█"

        # Create pulse effect by cycling through different brightness levels
        pulse_cycle = int(time.time() * 2) % 3
        pulse_chars = ["▓", "█", "▓"]
        return pulse_chars[pulse_cycle]

    def _render_bar_with_gradient(
        self,
        percentage: float,
        filled: int,
        empty_char: str = "░",
        empty_style: str = None,
    ) -> str:
        """Render progress bar with gradient effect and 3D appearance.

        Args:
            percentage: Current percentage
            filled: Number of filled segments
            empty_char: Character for empty portion
            empty_style: Style for empty portion

        Returns:
            Rendered bar string with Rich markup
        """
        # Get gradient color
        main_color = self._get_gradient_color(percentage)
        filled_char = self._get_pulse_char(percentage)

        # Create 3D effect with different shading
        filled_segments = []
        for i in range(filled):
            # Add subtle 3D effect by varying brightness
            if i == 0:
                # Left edge - lighter for 3D effect
                filled_segments.append(f"[bold {main_color}]{filled_char}[/]")
            elif i == filled - 1:
                # Right edge - darker for 3D effect
                filled_segments.append(f"[dim {main_color}]{filled_char}[/]")
            else:
                # Middle - normal
                filled_segments.append(f"[{main_color}]{filled_char}[/]")

        filled_bar = "".join(filled_segments)
        empty_bar = empty_char * (self.width - filled)

        if empty_style:
            empty_bar = f"[{empty_style}]{empty_bar}[/]"

        return f"{filled_bar}{empty_bar}"

    def _render_bar(
        self,
        filled: int,
        filled_char: str = "█",
        empty_char: str = "░",
        filled_style: str = None,
        empty_style: str = None,
    ) -> str:
        """Render progress bar (legacy method for compatibility).

        Args:
            filled: Number of filled segments
            filled_char: Character for filled portion
            empty_char: Character for empty portion
            filled_style: Style for filled portion
            empty_style: Style for empty portion

        Returns:
            Rendered bar string
        """
        filled_bar = filled_char * filled
        empty_bar = empty_char * (self.width - filled)

        if filled_style:
            filled_bar = f"[{filled_style}]{filled_bar}[/]"
        if empty_style:
            empty_bar = f"[{empty_style}]{empty_bar}[/]"

        return f"{filled_bar}{empty_bar}"


class TokenProgressBar(BaseProgressBar):
    """Token usage progress bar with WCAG-compliant gradient colors and pulse animation.

    Features:
    - Automatic theme-based coloring
    - Smooth gradient transitions
    - Pulse animation for critical states (>=85%)
    - 3D visual effects
    - WCAG 2.1 AA compliant contrast
    """

    def render(self, percentage: float, use_icons: bool = True) -> str:
        """Render token usage progress bar with enhanced visuals.

        Args:
            percentage: Usage percentage (can be > 100)
            use_icons: Whether to include status icons (default: True)

        Returns:
            Formatted progress bar string with WCAG-compliant colors
        """
        filled = self._calculate_filled(min(percentage, 100.0))

        # Use gradient rendering with 3D effect
        bar = self._render_bar_with_gradient(percentage, filled, empty_style="dim")

        # Determine icon and status based on usage level
        if percentage >= 90.0:
            icon = "🔴" if use_icons else ""
            status = "CRITICAL"
            status_color = self.theme.get_status_color("danger")
        elif percentage >= 75.0:
            icon = "🟠" if use_icons else ""
            status = "HIGH"
            status_color = self.theme.get_status_color("warning")
        elif percentage >= 50.0:
            icon = "🟡" if use_icons else ""
            status = "MEDIUM"
            status_color = self.theme.get_status_color("warning")
        elif percentage >= 25.0:
            icon = "🟢" if use_icons else ""
            status = "LOW"
            status_color = self.theme.get_status_color("success")
        else:
            icon = "🟢" if use_icons else ""
            status = "SAFE"
            status_color = self.theme.get_status_color("success")

        # Precise decimal display with theme colors
        if percentage >= 100.0:
            pct_color = self.theme.get_status_color("danger")
            pct_display = f"[bold {pct_color}]{percentage:.2f}%[/]"
        elif percentage >= 90.0:
            pct_color = self.theme.get_status_color("danger")
            pct_display = f"[{pct_color}]{percentage:.2f}%[/]"
        else:
            pct_display = f"{percentage:.2f}%"

        icon_part = f"{icon} " if icon else ""
        return f"{icon_part}[{bar}] {pct_display} [[{status_color}]{status}[/]]"


class TimeProgressBar(BaseProgressBar):
    """Time progress bar for session duration with theme support."""

    def render(self, elapsed_minutes: float, total_minutes: float, use_icons: bool = True) -> str:
        """Render time progress bar.

        Args:
            elapsed_minutes: Minutes elapsed
            total_minutes: Total minutes in session
            use_icons: Whether to include time icon (default: True)

        Returns:
            Formatted time progress bar with theme colors
        """
        if total_minutes <= 0:
            percentage = 0
        else:
            percentage = min(100, (elapsed_minutes / total_minutes) * 100)

        filled = self._calculate_filled(percentage)

        # Use theme primary color for time
        primary_color = self.theme.get_status_color("primary")
        bar = self._render_bar(filled, filled_style=primary_color, empty_style="dim")

        remaining_minutes = max(0, total_minutes - elapsed_minutes)
        hours = int(remaining_minutes // 60)
        mins = int(remaining_minutes % 60)
        remaining_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

        icon = "⏰ " if use_icons else ""
        return f"{icon}[{bar}] {remaining_str}"


class ModelUsageBar(BaseProgressBar):
    """Model usage distribution bar with WCAG-compliant theme colors.

    Displays token distribution across different models with distinct colors
    from the current theme's model color palette.
    """

    def render(self, per_model_stats: Dict[str, Any], use_icons: bool = True) -> str:
        """Render model usage bar with theme colors.

        Args:
            per_model_stats: Model statistics dictionary
            use_icons: Whether to include robot icon (default: True)

        Returns:
            Formatted model usage bar with theme-based colors
        """
        icon = "🤖 " if use_icons else ""

        if not per_model_stats:
            empty_bar = self._render_bar(0, empty_style="dim")
            return f"{icon}[{empty_bar}] No models used"

        # Calculate tokens per model
        model_tokens = {}
        total_tokens = 0

        for model, stats in per_model_stats.items():
            if isinstance(stats, dict):
                tokens = stats.get("prompt_tokens", 0) + stats.get("completion_tokens", 0)
                if tokens > 0:
                    model_tokens[model] = tokens
                    total_tokens += tokens

        if total_tokens == 0:
            empty_bar = self._render_bar(0, empty_style="dim")
            return f"{icon}[{empty_bar}] No tokens used"

        # Build bar segments using theme model colors
        bar_segments = []

        for idx, (model, tokens) in enumerate(model_tokens.items()):
            percentage = (tokens / total_tokens) * 100
            filled = int(self.width * tokens / total_tokens)

            if filled > 0:
                # Use theme's model colors for consistency and accessibility
                color = self.theme.get_model_color(idx)
                segment = f"[{color}]{'█' * filled}[/]"
                bar_segments.append(segment)

        bar_display = "".join(bar_segments)

        # Pad if needed
        total_filled = sum(int(self.width * t / total_tokens) for t in model_tokens.values())
        if total_filled < self.width:
            bar_display += "░" * (self.width - total_filled)

        # Create summary
        if len(model_tokens) == 1:
            model_name = list(model_tokens.keys())[0]
            summary = f"{model_name} 100%"
        else:
            top_model = max(model_tokens.items(), key=lambda x: x[1])
            pct = (top_model[1] / total_tokens) * 100
            summary = f"{top_model[0]} {pct:.1f}%"

        return f"{icon}[{bar_display}] {summary}"


class CostProgressBar(BaseProgressBar):
    """Cost usage progress bar with WCAG-compliant gradient and pulse effects.

    Features:
    - Theme-based gradient colors
    - Pulse animation for high usage (>=85%)
    - 3D visual effects
    - Precise cost display with appropriate warnings
    """

    def render(self, cost: float, limit: float, use_icons: bool = True) -> str:
        """Render cost progress bar with enhanced visuals.

        Args:
            cost: Current cost
            limit: Cost limit
            use_icons: Whether to include cost icons (default: True)

        Returns:
            Formatted cost progress bar with WCAG-compliant gradient colors
        """
        if limit <= 0:
            percentage = 0
        else:
            percentage = (cost / limit) * 100

        filled = self._calculate_filled(min(percentage, 100.0))

        # Use gradient rendering with 3D effect
        bar = self._render_bar_with_gradient(percentage, filled, empty_style="dim")

        # Determine icon and status based on usage level with theme colors
        if percentage >= 90.0:
            icon = "💰" if use_icons else ""
            status = "CRITICAL"
            status_color = self.theme.get_status_color("danger")
        elif percentage >= 75.0:
            icon = "💵" if use_icons else ""
            status = "HIGH"
            status_color = self.theme.get_status_color("warning")
        else:
            icon = "💲" if use_icons else ""
            status = "SAFE"
            status_color = self.theme.get_status_color("success")

        # Precise decimal display with theme-aware coloring
        cost_display = f"${cost:.4f}"
        limit_display = f"${limit:.2f}"

        if percentage >= 90.0:
            pct_color = self.theme.get_status_color("danger")
            pct_display = f"[{pct_color}]{percentage:.2f}%[/]"
        else:
            pct_display = f"{percentage:.2f}%"

        icon_part = f"{icon} " if icon else ""
        return f"{icon_part}[{bar}] {cost_display} / {limit_display} ({pct_display}) [[{status_color}]{status}[/]]"

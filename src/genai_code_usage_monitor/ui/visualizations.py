"""Advanced visualization components for Codex Monitor.

Provides mini charts, gauge charts, heat maps, and waterfall charts using Unicode characters.
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from rich.text import Text


class MiniChart:
    """Mini trend chart using Unicode block characters."""

    BLOCKS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]

    def __init__(self, width: int = 20, height: int = 8):
        """Initialize mini chart.

        Args:
            width: Number of data points to display
            height: Visual height using block characters
        """
        self.width = width
        self.height = height

    def render(
        self,
        data: List[float],
        title: str = "",
        color: str = "cyan",
        show_values: bool = False,
    ) -> Text:
        """Render mini chart from data.

        Args:
            data: List of numeric values
            title: Optional chart title
            color: Color style for chart
            show_values: Show min/max values

        Returns:
            Rich Text object with chart
        """
        if not data:
            return Text("No data", style="dim")

        # Normalize data to fit in height range
        min_val = min(data)
        max_val = max(data)
        value_range = max_val - min_val if max_val != min_val else 1

        # Take last N points
        display_data = data[-self.width :] if len(data) > self.width else data

        # Build chart
        chart_text = Text()

        if title:
            chart_text.append(f"{title}\n", style="bold")

        # Render bars
        chart_line = ""
        for value in display_data:
            normalized = (value - min_val) / value_range
            block_index = int(normalized * (len(self.BLOCKS) - 1))
            block_index = max(0, min(block_index, len(self.BLOCKS) - 1))
            chart_line += self.BLOCKS[block_index]

        chart_text.append(chart_line, style=color)

        # Show min/max if requested
        if show_values and data:
            chart_text.append(f"\n[dim]Min: {min_val:.2f} | Max: {max_val:.2f}[/]")

        return chart_text

    def render_sparkline(self, data: List[float], color: str = "cyan") -> str:
        """Render compact sparkline (single line).

        Args:
            data: List of numeric values
            color: Color style

        Returns:
            Formatted sparkline string
        """
        if not data:
            return "[dim]━━━━━━━━━━[/]"

        min_val = min(data)
        max_val = max(data)
        value_range = max_val - min_val if max_val != min_val else 1

        display_data = data[-self.width :] if len(data) > self.width else data

        chart = ""
        for value in display_data:
            normalized = (value - min_val) / value_range
            block_index = int(normalized * (len(self.BLOCKS) - 1))
            block_index = max(0, min(block_index, len(self.BLOCKS) - 1))
            chart += self.BLOCKS[block_index]

        return f"[{color}]{chart}[/]"


class GaugeChart:
    """Circular gauge chart for displaying progress."""

    def __init__(self, width: int = 40):
        """Initialize gauge chart.

        Args:
            width: Total width of gauge display
        """
        self.width = width

    def render(
        self,
        percentage: float,
        label: str = "",
        show_percentage: bool = True,
    ) -> Text:
        """Render gauge chart.

        Args:
            percentage: Value from 0-100
            label: Optional label
            show_percentage: Display percentage value

        Returns:
            Rich Text object with gauge
        """
        # Clamp percentage
        percentage = max(0, min(100, percentage))

        # Determine color based on percentage
        if percentage >= 90:
            color = "red"
            icon = "🔴"
        elif percentage >= 75:
            color = "dark_orange"
            icon = "🟠"
        elif percentage >= 50:
            color = "yellow"
            icon = "🟡"
        else:
            color = "green"
            icon = "🟢"

        gauge_text = Text()

        # Build gauge using arc characters
        gauge_chars = "◐◓◑◒"
        filled_segments = int((percentage / 100) * 20)

        gauge_line = ""
        for i in range(20):
            if i < filled_segments:
                char_index = i % len(gauge_chars)
                gauge_line += gauge_chars[char_index]
            else:
                gauge_line += "○"

        # Format output
        if label:
            gauge_text.append(f"{label}: ", style="bold")

        gauge_text.append(icon + " ")
        gauge_text.append(gauge_line, style=color)

        if show_percentage:
            gauge_text.append(f" {percentage:.1f}%", style="bold")

        return gauge_text

    def render_semicircle(
        self,
        percentage: float,
        width: int = 30,
    ) -> List[str]:
        """Render semicircle gauge (multi-line).

        Args:
            percentage: Value from 0-100
            width: Width of gauge

        Returns:
            List of strings representing each line
        """
        percentage = max(0, min(100, percentage))

        # Determine color
        if percentage >= 90:
            color = "red"
        elif percentage >= 75:
            color = "dark_orange"
        elif percentage >= 50:
            color = "yellow"
        else:
            color = "green"

        # Create arc segments
        arc_segments = []
        total_segments = width // 2

        filled_segments = int((percentage / 100) * total_segments)

        # Top arc
        top_line = "  "
        for i in range(total_segments):
            if i < filled_segments:
                top_line += f"[{color}]▄[/]"
            else:
                top_line += "░"

        # Middle lines
        left_fill = "█" if percentage > 25 else "░"
        right_fill = "█" if percentage > 75 else "░"
        middle_line = f" [{color}]{left_fill}[/]"
        middle_line += " " * (total_segments - 2)
        middle_line += f"[{color}]{right_fill}[/]"

        # Bottom line with percentage
        bottom_line = "  "
        bottom_line += f"[{color}]{'▀' * total_segments}[/]"

        # Center percentage
        pct_line = f"  {percentage:.1f}%".center(width)

        return [top_line, middle_line, bottom_line, pct_line]


class HeatMap:
    """Heat map visualization for time-based data."""

    def __init__(self, hours: int = 24, resolution: int = 12):
        """Initialize heat map.

        Args:
            hours: Number of hours to display
            resolution: Time blocks per hour
        """
        self.hours = hours
        self.resolution = resolution

    def render(
        self,
        data: Dict[datetime, float],
        title: str = "Usage Heat Map",
    ) -> Text:
        """Render heat map from timestamped data.

        Args:
            data: Dictionary mapping timestamps to values
            title: Chart title

        Returns:
            Rich Text object with heat map
        """
        if not data:
            return Text("No data available", style="dim")

        heat_text = Text()
        heat_text.append(f"{title}\n", style="bold cyan")

        # Create time buckets
        now = datetime.now()
        start_time = now - timedelta(hours=self.hours)
        bucket_minutes = 60 // self.resolution
        total_buckets = self.hours * self.resolution

        # Initialize buckets
        buckets = [0.0] * total_buckets

        # Fill buckets with data
        for timestamp, value in data.items():
            if timestamp >= start_time:
                minutes_diff = int((timestamp - start_time).total_seconds() / 60)
                bucket_idx = min(minutes_diff // bucket_minutes, total_buckets - 1)
                buckets[bucket_idx] += value

        # Normalize to 0-1 range
        max_value = max(buckets) if buckets else 1
        if max_value > 0:
            normalized = [v / max_value for v in buckets]
        else:
            normalized = buckets

        # Heat characters (intensity levels)
        heat_chars = [" ", ".", ":", "-", "=", "+", "*", "#", "█"]

        # Render heat map in rows
        blocks_per_row = 48
        for row_start in range(0, total_buckets, blocks_per_row):
            row_data = normalized[row_start : row_start + blocks_per_row]

            # Time label
            hours_offset = row_start // self.resolution
            time_label = (start_time + timedelta(hours=hours_offset)).strftime("%H:%M")
            heat_text.append(f"{time_label} ", style="dim")

            # Heat blocks
            for value in row_data:
                char_idx = int(value * (len(heat_chars) - 1))
                char = heat_chars[char_idx]

                # Color based on intensity
                if value >= 0.8:
                    color = "red"
                elif value >= 0.6:
                    color = "dark_orange"
                elif value >= 0.4:
                    color = "yellow"
                elif value >= 0.2:
                    color = "green"
                else:
                    color = "dim"

                heat_text.append(char, style=color)

            heat_text.append("\n")

        # Legend
        heat_text.append("\n[dim]Intensity: ", style="dim")
        heat_text.append("Low ", style="green")
        heat_text.append("░░░ ", style="dim")
        heat_text.append("Medium ", style="yellow")
        heat_text.append("░░░ ", style="dim")
        heat_text.append("High", style="red")
        heat_text.append("[/]")

        return heat_text


class WaterfallChart:
    """Waterfall chart for cost breakdown visualization."""

    def __init__(self, width: int = 50):
        """Initialize waterfall chart.

        Args:
            width: Maximum bar width
        """
        self.width = width

    def render(
        self,
        components: List[Tuple[str, float]],
        total_label: str = "Total",
        currency: bool = True,
    ) -> Text:
        """Render waterfall chart showing cost breakdown.

        Args:
            components: List of (label, value) tuples
            total_label: Label for total row
            currency: Format values as currency

        Returns:
            Rich Text object with waterfall chart
        """
        if not components:
            return Text("No data", style="dim")

        chart_text = Text()
        chart_text.append("Cost Breakdown\n", style="bold cyan")
        chart_text.append("─" * (self.width + 30) + "\n", style="dim")

        # Calculate total and max for scaling
        total = sum(value for _, value in components)
        max_value = max(value for _, value in components) if components else 1

        running_total = 0

        for label, value in components:
            # Calculate bar length
            bar_length = int((value / max_value) * self.width) if max_value > 0 else 0
            bar_length = max(1, bar_length)  # Minimum 1 char

            # Determine color based on contribution
            contribution_pct = (value / total * 100) if total > 0 else 0
            if contribution_pct >= 50:
                color = "red"
            elif contribution_pct >= 25:
                color = "yellow"
            else:
                color = "green"

            # Format value
            if currency:
                value_str = f"${value:.4f}"
            else:
                value_str = f"{value:.2f}"

            # Build bar with running total
            running_total += value
            bar = "█" * bar_length
            connector = "├" if running_total < total else "└"

            # Format line
            chart_text.append(f"{connector}─ ", style="dim")
            chart_text.append(f"{label:<20}", style="cyan")
            chart_text.append(f" [{color}]{bar}[/] ", style=color)
            chart_text.append(f"{value_str:>12}", style="bold")
            chart_text.append(f"  ({contribution_pct:.1f}%)\n", style="dim")

        # Total line
        chart_text.append("─" * (self.width + 30) + "\n", style="dim")

        if currency:
            total_str = f"${total:.4f}"
        else:
            total_str = f"{total:.2f}"

        chart_text.append("  ", style="dim")
        chart_text.append(f"{total_label:<20}", style="bold green")
        chart_text.append(" " * (self.width + 1))
        chart_text.append(f"{total_str:>12}", style="bold green")
        chart_text.append("\n")

        return chart_text

    def render_compact(
        self,
        components: List[Tuple[str, float]],
        width: int = 40,
    ) -> Text:
        """Render compact waterfall chart (single stacked bar).

        Args:
            components: List of (label, value) tuples
            width: Total bar width

        Returns:
            Rich Text object with compact chart
        """
        if not components:
            return Text("No data", style="dim")

        chart_text = Text()
        total = sum(value for _, value in components)

        if total == 0:
            return Text("No costs", style="dim")

        # Color palette
        colors = ["green", "cyan", "blue", "magenta", "yellow", "dark_orange", "red"]

        # Build stacked bar
        chart_text.append("┌" + "─" * width + "┐\n", style="dim")
        chart_text.append("│", style="dim")

        for idx, (label, value) in enumerate(components):
            segment_width = int((value / total) * width)
            if segment_width > 0:
                color = colors[idx % len(colors)]
                chart_text.append("█" * segment_width, style=color)

        chart_text.append("│", style="dim")
        chart_text.append("\n")
        chart_text.append("└" + "─" * width + "┘\n", style="dim")

        # Legend
        for idx, (label, value) in enumerate(components):
            color = colors[idx % len(colors)]
            pct = (value / total * 100) if total > 0 else 0
            chart_text.append("  ")
            chart_text.append("█", style=color)
            chart_text.append(f" {label}: ${value:.4f} ({pct:.1f}%)\n", style="dim")

        return chart_text


# Helper function to format numbers with SI suffixes
def format_large_number(num: float) -> str:
    """Format large numbers with SI suffixes (K, M, B).

    Args:
        num: Number to format

    Returns:
        Formatted string
    """
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return f"{num:.2f}"


# Helper function to create progress indicators
def create_progress_indicator(
    current: float,
    target: float,
    width: int = 20,
    show_overage: bool = True,
) -> str:
    """Create a simple progress indicator.

    Args:
        current: Current value
        target: Target/limit value
        width: Indicator width
        show_overage: Show if over target

    Returns:
        Formatted progress string
    """
    if target <= 0:
        return "[dim]No limit[/]"

    percentage = (current / target) * 100
    filled = int((min(percentage, 100) / 100) * width)

    if percentage >= 100 and show_overage:
        color = "red"
        indicator = f"[{color}]{'█' * width} OVER[/]"
    elif percentage >= 90:
        color = "red"
        indicator = f"[{color}]{'█' * filled}{'░' * (width - filled)}[/]"
    elif percentage >= 75:
        color = "yellow"
        indicator = f"[{color}]{'█' * filled}{'░' * (width - filled)}[/]"
    else:
        color = "green"
        indicator = f"[{color}]{'█' * filled}{'░' * (width - filled)}[/]"

    return f"{indicator} {percentage:.1f}%"

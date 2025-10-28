"""Reusable UI components for Codex Monitor.

Provides common UI elements like alerts, status indicators, and formatted displays.
Enhanced with advanced visualizations including mini charts, gauges, and heat maps.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple

from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.columns import Columns

from genai_code_usage_monitor.core.models import MonitorState, PlanLimits, Platform
from genai_code_usage_monitor.ui.progress_bars import (
    CostProgressBar,
    ModelUsageBar,
    TokenProgressBar,
)
from genai_code_usage_monitor.ui.visualizations import (
    MiniChart,
    GaugeChart,
    HeatMap,
    WaterfallChart,
    format_large_number,
    create_progress_indicator,
)


class UIComponents:
    """Collection of reusable UI components."""

    def __init__(self):
        """Initialize UI components with enhanced visualizations."""
        self.token_bar = TokenProgressBar(width=50)
        self.cost_bar = CostProgressBar(width=50)
        self.model_bar = ModelUsageBar(width=50)

        # Advanced visualization components
        self.mini_chart = MiniChart(width=30, height=8)
        self.gauge_chart = GaugeChart(width=40)
        self.heat_map = HeatMap(hours=24, resolution=12)
        self.waterfall_chart = WaterfallChart(width=50)

    def create_header(
        self, plan_name: str, view: str = "realtime", timestamp: str = ""
    ) -> Panel:
        """Create application header.

        Args:
            plan_name: Current plan name
            view: Current view mode
            timestamp: Current timestamp

        Returns:
            Header panel
        """
        title = Text()
        title.append("Codex Usage Monitor", style="bold cyan")

        info = Text()
        info.append("Plan: ", style="dim")
        info.append(plan_name, style="bold yellow")
        info.append(" | ", style="dim")
        info.append("View: ", style="dim")
        info.append(view, style="bold green")
        if timestamp:
            info.append(" | ", style="dim")
            info.append(timestamp, style="dim cyan")

        content = Text()
        content.append_text(title)
        content.append("\n")
        content.append_text(info)

        return Panel(
            Align.center(content),
            border_style="cyan",
            padding=(0, 2),
        )

    def create_usage_overview_panel(
        self, state: MonitorState, limits: PlanLimits
    ) -> Panel:
        """Create usage overview panel with progress bars.

        Args:
            state: Current monitor state
            limits: Plan limits

        Returns:
            Usage overview panel
        """
        stats = state.daily_stats

        content = Text()

        # Token usage bar
        if limits.token_limit:
            token_pct = (stats.total_tokens / limits.token_limit) * 100
            token_bar_str = self.token_bar.render(token_pct)
            # Parse Rich markup properly
            content.append(Text.from_markup(token_bar_str))
            content.append("\n")
        else:
            content.append(
                f"🟢 Tokens: {stats.total_tokens:,} (unlimited)\n", style="green"
            )

        # Cost usage bar
        if limits.cost_limit:
            cost_bar_str = self.cost_bar.render(stats.total_cost, limits.cost_limit)
            # Parse Rich markup properly
            content.append(Text.from_markup(cost_bar_str))
            content.append("\n")
        else:
            content.append(f"💲 Cost: ${stats.total_cost:.4f}\n", style="green")

        # Model usage bar
        if stats.models:
            # Convert models dict to per_model_stats format for progress bar
            per_model_stats = {
                model: {"prompt_tokens": 0, "completion_tokens": tokens}
                for model, tokens in stats.models.items()
            }
            model_bar_str = self.model_bar.render(per_model_stats)
            # Parse Rich markup properly
            content.append(Text.from_markup(model_bar_str))

        return Panel(
            content,
            title="[bold]Usage Overview[/bold]",
            border_style="blue",
        )

    def create_limits_panel(self, limits: PlanLimits) -> Panel:
        """Create limits information panel.

        Args:
            limits: Plan limits

        Returns:
            Limits panel
        """
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Label", style="cyan")
        table.add_column("Value", style="green", justify="right")

        # Token limit
        if limits.token_limit:
            table.add_row("Token Limit", f"{limits.token_limit:,}")
        else:
            table.add_row("Token Limit", "Unlimited")

        # Cost limit
        if limits.cost_limit:
            table.add_row("Cost Limit", f"${limits.cost_limit:.2f}")
        else:
            table.add_row("Cost Limit", "Unlimited")

        # Warnings (75% threshold)
        if limits.token_limit:
            warning_tokens = int(limits.token_limit * 0.75)
            table.add_row(
                "Token Warning", f"{warning_tokens:,} (75%)"
            )

        if limits.cost_limit:
            warning_cost = limits.cost_limit * 0.75
            table.add_row(
                "Cost Warning", f"${warning_cost:.2f} (75%)"
            )

        return Panel(
            table,
            title=f"[bold]{limits.name}[/bold]",
            border_style="yellow",
        )

    def create_alert_panel(
        self, message: str, alert_type: str = "info"
    ) -> Panel:
        """Create alert panel.

        Args:
            message: Alert message
            alert_type: Type of alert (info, warning, error, success)

        Returns:
            Alert panel
        """
        styles = {
            "info": ("cyan", "ℹ"),
            "warning": ("yellow", "⚠"),
            "error": ("red", "❌"),
            "success": ("green", "✅"),
        }

        color, icon = styles.get(alert_type, styles["info"])

        content = Text()
        content.append(f"{icon} ", style=f"bold {color}")
        content.append(message, style=color)

        return Panel(
            content,
            border_style=color,
            padding=(0, 1),
        )

    def create_stats_summary(self, state: MonitorState) -> Table:
        """Create compact statistics summary table.

        Args:
            state: Current monitor state

        Returns:
            Statistics summary table
        """
        stats = state.daily_stats

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Metric", style="bold cyan")
        table.add_column("Value", style="green", justify="right")

        table.add_row("Total Tokens", f"{stats.total_tokens:,}")
        table.add_row("Prompt Tokens", f"{stats.prompt_tokens:,}")
        table.add_row("Completion Tokens", f"{stats.completion_tokens:,}")
        table.add_row("Total Cost", f"${stats.total_cost:.4f}")
        table.add_row("API Calls", f"{stats.total_calls}")

        if stats.total_calls > 0:
            table.add_row("Avg Tokens/Call", f"{stats.total_tokens / stats.total_calls:.0f}")
            table.add_row("Avg Cost/Call", f"${stats.total_cost / stats.total_calls:.4f}")

        return table

    def create_quick_stats_line(self, state: MonitorState) -> Text:
        """Create single-line quick statistics.

        Args:
            state: Current monitor state

        Returns:
            Text with quick statistics
        """
        stats = state.daily_stats

        text = Text()
        text.append("📊 ", style="bold")
        text.append(f"Tokens: {stats.total_tokens:,}", style="cyan")
        text.append(" | ", style="dim")
        text.append(f"Cost: ${stats.total_cost:.4f}", style="green")
        text.append(" | ", style="dim")
        text.append(f"Calls: {stats.total_calls}", style="yellow")

        return text

    def create_warning_banner(self, state: MonitorState, limits: PlanLimits) -> Optional[Panel]:
        """Create warning banner if approaching limits.

        Args:
            state: Current monitor state
            limits: Plan limits

        Returns:
            Warning panel if warnings exist, None otherwise
        """
        warnings = []
        stats = state.daily_stats

        # Calculate thresholds (75% warning, 90% critical)
        warning_threshold = 0.75
        critical_threshold = 0.90

        # Check token warnings
        if limits.token_limit:
            token_pct = (stats.total_tokens / limits.token_limit) * 100
            if token_pct >= critical_threshold * 100:
                warnings.append(f"🔴 Token usage CRITICAL at {token_pct:.1f}%")
            elif token_pct >= warning_threshold * 100:
                warnings.append(f"Token usage at {token_pct:.1f}%")

        # Check cost warnings
        if limits.cost_limit:
            cost_pct = (stats.total_cost / limits.cost_limit) * 100
            if cost_pct >= critical_threshold * 100:
                warnings.append(f"🔴 Cost CRITICAL at {cost_pct:.1f}%")
            elif cost_pct >= warning_threshold * 100:
                warnings.append(f"Cost at {cost_pct:.1f}%")

        if not warnings:
            return None

        content = Text()
        content.append("⚠ WARNING: ", style="bold yellow")
        content.append(" | ".join(warnings), style="yellow")

        return Panel(
            content,
            border_style="yellow",
            padding=(0, 1),
        )

    def create_footer(self, refresh_rate: int = 5) -> Text:
        """Create footer with instructions.

        Args:
            refresh_rate: Refresh rate in seconds

        Returns:
            Footer text
        """
        text = Text()
        text.append("Press ", style="dim")
        text.append("Ctrl+C", style="bold cyan")
        text.append(" to exit", style="dim")
        text.append(" | ", style="dim")
        text.append(f"Refreshing every {refresh_rate}s", style="dim italic")

        return text

    def create_trend_panel(self, state: MonitorState) -> Panel:
        """Create trend visualization panel with mini charts.

        Args:
            state: Current monitor state

        Returns:
            Panel with trend visualizations
        """
        content = Text()

        # Extract token usage over time from API calls
        token_history = []
        cost_history = []

        if state.daily_stats.api_calls:
            for call in state.daily_stats.api_calls[-30:]:  # Last 30 calls
                token_history.append(float(call.tokens.total_tokens))
                cost_history.append(call.cost)

        # Token trend
        if token_history:
            content.append("Token Usage Trend\n", style="bold cyan")
            token_chart = self.mini_chart.render(
                token_history,
                color="green",
                show_values=True,
            )
            content.append_text(token_chart)
            content.append("\n\n")

        # Cost trend
        if cost_history:
            content.append("Cost Trend\n", style="bold yellow")
            cost_chart = self.mini_chart.render(
                cost_history,
                color="yellow",
                show_values=True,
            )
            content.append_text(cost_chart)

        if not token_history and not cost_history:
            content.append("No trend data available", style="dim")

        return Panel(
            content,
            title="[bold]Usage Trends[/bold]",
            border_style="cyan",
        )

    def create_gauge_panel(self, state: MonitorState, limits: PlanLimits) -> Panel:
        """Create gauge visualization panel.

        Args:
            state: Current monitor state
            limits: Plan limits

        Returns:
            Panel with gauge visualizations
        """
        content = Text()

        # Token usage gauge
        if limits.token_limit:
            token_pct = (state.daily_stats.total_tokens / limits.token_limit) * 100
            content.append("Token Usage\n", style="bold")
            gauge = self.gauge_chart.render(token_pct, show_percentage=True)
            content.append_text(gauge)
            content.append("\n")
            content.append(
                f"  {format_large_number(state.daily_stats.total_tokens)} / "
                f"{format_large_number(limits.token_limit)} tokens\n\n",
                style="dim",
            )

        # Cost usage gauge
        if limits.cost_limit:
            cost_pct = (state.daily_stats.total_cost / limits.cost_limit) * 100
            content.append("Cost Usage\n", style="bold")
            gauge = self.gauge_chart.render(cost_pct, show_percentage=True)
            content.append_text(gauge)
            content.append("\n")
            content.append(
                f"  ${state.daily_stats.total_cost:.4f} / ${limits.cost_limit:.2f}\n",
                style="dim",
            )

        if not limits.token_limit and not limits.cost_limit:
            content.append("No limits configured", style="dim")

        return Panel(
            content,
            title="[bold]Usage Gauges[/bold]",
            border_style="magenta",
        )

    def create_heat_map_panel(self, state: MonitorState) -> Panel:
        """Create heat map panel for hourly usage.

        Args:
            state: Current monitor state

        Returns:
            Panel with heat map visualization
        """
        # Build time-series data from API calls
        time_series: Dict[datetime, float] = {}

        if state.daily_stats.api_calls:
            for call in state.daily_stats.api_calls:
                # Round to nearest 5 minutes for bucketing
                rounded_time = call.timestamp.replace(
                    minute=(call.timestamp.minute // 5) * 5,
                    second=0,
                    microsecond=0,
                )
                if rounded_time in time_series:
                    time_series[rounded_time] += call.tokens.total_tokens
                else:
                    time_series[rounded_time] = float(call.tokens.total_tokens)

        heat_map = self.heat_map.render(time_series, title="24-Hour Usage Pattern")

        return Panel(
            heat_map,
            title="[bold]Usage Heat Map[/bold]",
            border_style="red",
        )

    def create_cost_breakdown_panel(self, state: MonitorState) -> Panel:
        """Create cost breakdown waterfall chart.

        Args:
            state: Current monitor state

        Returns:
            Panel with waterfall chart
        """
        # Build cost breakdown by model
        cost_components: List[Tuple[str, float]] = []

        if state.daily_stats.models:
            # Calculate cost per model (simplified - would need pricing data)
            for model, tokens in state.daily_stats.models.items():
                # Find total cost for this model from API calls
                model_cost = 0.0
                for call in state.daily_stats.api_calls:
                    if call.model == model:
                        model_cost += call.cost

                if model_cost > 0:
                    cost_components.append((model, model_cost))

        # Sort by cost descending
        cost_components.sort(key=lambda x: x[1], reverse=True)

        if cost_components:
            waterfall = self.waterfall_chart.render(
                cost_components,
                total_label="Total Cost",
                currency=True,
            )
        else:
            waterfall = Text("No cost data available", style="dim")

        return Panel(
            waterfall,
            title="[bold]Cost Breakdown[/bold]",
            border_style="yellow",
        )

    def create_enhanced_overview(
        self, state: MonitorState, limits: PlanLimits
    ) -> Panel:
        """Create enhanced overview with sparklines and indicators.

        Args:
            state: Current monitor state
            limits: Plan limits

        Returns:
            Enhanced overview panel
        """
        content = Text()

        stats = state.daily_stats

        # Header with icon decorations
        content.append("╔══════════════════════════════════════════════════╗\n", style="cyan")
        content.append("║           ", style="cyan")
        content.append("USAGE OVERVIEW", style="bold cyan")
        content.append("                        ║\n", style="cyan")
        content.append("╚══════════════════════════════════════════════════╝\n", style="cyan")
        content.append("\n")

        # Token metrics with sparkline
        content.append("📊 ", style="bold")
        content.append("Token Usage\n", style="bold cyan")

        if limits.token_limit:
            token_pct = (stats.total_tokens / limits.token_limit) * 100
            indicator = create_progress_indicator(
                stats.total_tokens, limits.token_limit, width=30
            )
            content.append(f"   {indicator}\n", style="")
            content.append(
                f"   {format_large_number(stats.total_tokens)} / "
                f"{format_large_number(limits.token_limit)} tokens\n\n",
                style="dim",
            )
        else:
            content.append(
                f"   {format_large_number(stats.total_tokens)} tokens (unlimited)\n\n",
                style="green",
            )

        # Cost metrics
        content.append("💰 ", style="bold")
        content.append("Cost Usage\n", style="bold yellow")

        if limits.cost_limit:
            cost_pct = (stats.total_cost / limits.cost_limit) * 100
            indicator = create_progress_indicator(
                stats.total_cost, limits.cost_limit, width=30
            )
            content.append(f"   {indicator}\n", style="")
            content.append(
                f"   ${stats.total_cost:.4f} / ${limits.cost_limit:.2f}\n\n",
                style="dim",
            )
        else:
            content.append(f"   ${stats.total_cost:.4f} (unlimited)\n\n", style="green")

        # API calls
        content.append("🔄 ", style="bold")
        content.append("API Activity\n", style="bold magenta")
        content.append(f"   {stats.total_calls:,} API calls\n", style="dim")

        if stats.total_calls > 0:
            avg_tokens = stats.total_tokens / stats.total_calls
            avg_cost = stats.total_cost / stats.total_calls
            content.append(
                f"   Avg: {avg_tokens:.0f} tokens/call, ${avg_cost:.4f}/call\n",
                style="dim",
            )

        content.append("\n")

        # Model distribution
        if stats.models:
            content.append("🤖 ", style="bold")
            content.append("Model Distribution\n", style="bold blue")

            total_tokens = sum(stats.models.values())
            for model, tokens in sorted(
                stats.models.items(), key=lambda x: x[1], reverse=True
            ):
                pct = (tokens / total_tokens * 100) if total_tokens > 0 else 0
                bar_width = int(pct / 5)  # 20 chars max
                bar = "█" * bar_width + "░" * (20 - bar_width)
                content.append(f"   {model:<25} ", style="dim")
                content.append(f"[cyan]{bar}[/]")
                content.append(f" {pct:.1f}%\n", style="dim")

        return Panel(
            content,
            border_style="bold cyan",
            padding=(1, 2),
        )

    def create_compact_dashboard(
        self, state: MonitorState, limits: PlanLimits
    ) -> Table:
        """Create compact dashboard with multiple visualizations.

        Args:
            state: Current monitor state
            limits: Plan limits

        Returns:
            Table with compact visualizations
        """
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Visual", style="cyan")
        table.add_column("Data", style="white")

        stats = state.daily_stats

        # Token gauge
        if limits.token_limit:
            token_pct = (stats.total_tokens / limits.token_limit) * 100
            gauge = self.gauge_chart.render(token_pct, label="Tokens")
            table.add_row("", gauge)

        # Cost gauge
        if limits.cost_limit:
            cost_pct = (stats.total_cost / limits.cost_limit) * 100
            gauge = self.gauge_chart.render(cost_pct, label="Cost")
            table.add_row("", gauge)

        # Token history sparkline
        if stats.api_calls:
            token_history = [
                float(call.tokens.total_tokens) for call in stats.api_calls[-20:]
            ]
            sparkline = self.mini_chart.render_sparkline(token_history, color="green")
            label = Text("Token Trend: ", style="bold")
            label.append_text(Text.from_markup(sparkline))
            table.add_row("", label)

        return table

    def create_platform_header(
        self,
        platform: Platform,
        state: MonitorState,
        plan_manager: Optional["PlanManager"] = None,
        timestamp: str = "",
    ) -> Panel:
        """Create platform-specific header.

        Args:
            platform: Platform type (Codex or Claude)
            state: Current monitor state
            plan_manager: Plan manager (optional)
            timestamp: Current timestamp

        Returns:
            Platform-specific header panel
        """
        title = Text()
        title.append(platform.display_name, style=f"bold {platform.theme_color}")
        title.append(" API Monitor", style="bold white")

        info = Text()
        if plan_manager:
            info.append("Plan: ", style="dim")
            info.append(plan_manager.plan_name, style="bold yellow")
            info.append(" | ", style="dim")

        info.append("Platform: ", style="dim")
        info.append(platform.display_name, style=f"bold {platform.theme_color}")

        if timestamp:
            info.append(" | ", style="dim")
            info.append(timestamp, style="dim cyan")

        content = Text()
        content.append_text(title)
        content.append("\n")
        content.append_text(info)

        return Panel(
            Align.center(content),
            border_style=platform.theme_color,
            padding=(0, 2),
        )

    def create_cache_info_panel(self, state: MonitorState) -> Panel:
        """Create cache information panel (Claude-specific).

        Args:
            state: Current monitor state

        Returns:
            Panel with cache statistics
        """
        content = Text()
        stats = state.daily_stats

        # Check if cache data is available
        if stats.total_cached_tokens == 0:
            content.append("No cache data available", style="dim italic")
        else:
            # Cache hit rate
            cache_hit_rate = stats.average_cache_hit_rate
            content.append("Cache Performance\n\n", style="bold cyan")

            # Hit rate gauge
            hit_rate_pct = cache_hit_rate * 100
            if hit_rate_pct >= 75:
                color = "green"
                icon = "✓"
            elif hit_rate_pct >= 50:
                color = "yellow"
                icon = "◐"
            else:
                color = "red"
                icon = "✗"

            content.append(f"{icon} Hit Rate: ", style="dim")
            content.append(f"{hit_rate_pct:.1f}%\n", style=f"bold {color}")

            # Cached tokens
            content.append("Cached Tokens: ", style="dim")
            content.append(f"{stats.total_cached_tokens:,}\n", style="cyan")

            # Cost savings
            content.append("Cost Savings: ", style="dim")
            content.append(f"${stats.total_cache_savings:.4f}\n", style="green")

            # Visual progress bar for cache efficiency
            bar_width = 30
            filled = int((hit_rate_pct / 100) * bar_width)
            bar = "█" * filled + "░" * (bar_width - filled)
            content.append(f"\n{bar}\n", style="cyan")

            # Interpretation
            if hit_rate_pct >= 75:
                content.append("\nExcellent cache efficiency!", style="bold green")
            elif hit_rate_pct >= 50:
                content.append("\nGood cache performance", style="bold yellow")
            else:
                content.append("\nConsider optimizing cache usage", style="bold red")

        return Panel(
            content,
            title="[bold magenta]Cache Statistics[/bold magenta]",
            border_style="magenta",
        )

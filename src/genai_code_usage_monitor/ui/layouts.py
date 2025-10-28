"""Screen layout management for Codex Monitor.

Provides different layout configurations for various view modes.
"""

from datetime import datetime
from typing import Optional

from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from genai_code_usage_monitor.core.models import MonitorState, SessionData, Platform, MultiPlatformState
from genai_code_usage_monitor.core.plans import PlanManager
from genai_code_usage_monitor.ui.components import UIComponents
from genai_code_usage_monitor.ui.session_display import SessionDisplay
from genai_code_usage_monitor.ui.table_views import TableViews


class LayoutManager:
    """Manages screen layouts for different view modes."""

    def __init__(self, theme: str = "dark"):
        """Initialize layout manager.

        Args:
            theme: Display theme
        """
        self.theme = theme
        self.components = UIComponents()
        self.session_display = SessionDisplay()
        self.table_views = TableViews()

    def create_realtime_layout(
        self,
        state: MonitorState,
        plan_manager: PlanManager,
        session: Optional[SessionData] = None,
        refresh_rate: int = 5,
    ) -> Layout:
        """Create real-time monitoring layout.

        Args:
            state: Current monitor state
            plan_manager: Plan manager
            session: Current session data
            refresh_rate: Refresh rate in seconds

        Returns:
            Layout for real-time view
        """
        layout = Layout()

        # Create header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = self.components.create_header(
            plan_name=plan_manager.plan_name,
            view="realtime",
            timestamp=timestamp,
        )

        # Create warning banner if needed
        warning = self.components.create_warning_banner(state, plan_manager.limits)

        # Create main content
        usage_panel = self.components.create_usage_overview_panel(
            state, plan_manager.limits
        )

        # Create session info
        session_panel = self.session_display.create_session_info_panel(
            state, session
        )

        # Create footer
        footer = self.components.create_footer(refresh_rate)

        # Assemble layout
        if warning:
            layout.split_column(
                Layout(header, size=5),
                Layout(warning, size=3),
                Layout(usage_panel, size=10),
                Layout(session_panel, size=8),
                Layout(Panel(footer, border_style="dim"), size=3),
            )
        else:
            layout.split_column(
                Layout(header, size=5),
                Layout(usage_panel, size=10),
                Layout(session_panel, size=8),
                Layout(Panel(footer, border_style="dim"), size=3),
            )

        return layout

    def create_daily_layout(
        self,
        state: MonitorState,
        plan_manager: PlanManager,
        refresh_rate: int = 5,
    ) -> Layout:
        """Create daily summary layout.

        Args:
            state: Current monitor state
            plan_manager: Plan manager
            refresh_rate: Refresh rate in seconds

        Returns:
            Layout for daily view
        """
        layout = Layout()

        # Create header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = self.components.create_header(
            plan_name=plan_manager.plan_name,
            view="daily",
            timestamp=timestamp,
        )

        # Create warning banner if needed
        warning = self.components.create_warning_banner(state, plan_manager.limits)

        # Create daily summary table
        daily_table = self.table_views.create_daily_summary_table(state.daily_stats)

        # Create hourly breakdown
        hourly_table = self.table_views.create_hourly_breakdown_table(
            state.daily_stats.api_calls
        )

        # Create footer
        footer = self.components.create_footer(refresh_rate)

        # Assemble layout
        if warning:
            layout.split_column(
                Layout(header, size=5),
                Layout(warning, size=3),
                Layout(daily_table),
                Layout(hourly_table),
                Layout(Panel(footer, border_style="dim"), size=3),
            )
        else:
            layout.split_column(
                Layout(header, size=5),
                Layout(daily_table),
                Layout(hourly_table),
                Layout(Panel(footer, border_style="dim"), size=3),
            )

        return layout

    def create_monthly_layout(
        self,
        state: MonitorState,
        plan_manager: PlanManager,
        monthly_stats: dict,
        refresh_rate: int = 5,
    ) -> Layout:
        """Create monthly summary layout.

        Args:
            state: Current monitor state
            plan_manager: Plan manager
            monthly_stats: Monthly statistics dictionary
            refresh_rate: Refresh rate in seconds

        Returns:
            Layout for monthly view
        """
        layout = Layout()

        # Create header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = self.components.create_header(
            plan_name=plan_manager.plan_name,
            view="monthly",
            timestamp=timestamp,
        )

        # Create monthly summary table
        monthly_table = self.table_views.create_monthly_summary_table(monthly_stats)

        # Create cost breakdown
        current_month_stats = state.daily_stats
        cost_table = self.table_views.create_cost_breakdown_table(current_month_stats)

        # Create footer
        footer = self.components.create_footer(refresh_rate)

        # Assemble layout
        layout.split_column(
            Layout(header, size=5),
            Layout(monthly_table),
            Layout(cost_table),
            Layout(Panel(footer, border_style="dim"), size=3),
        )

        return layout

    def create_compact_layout(
        self,
        state: MonitorState,
        plan_manager: PlanManager,
    ) -> Layout:
        """Create compact layout for smaller terminals.

        Args:
            state: Current monitor state
            plan_manager: Plan manager

        Returns:
            Compact layout
        """
        layout = Layout()

        # Create compact header
        header = self.components.create_header(
            plan_name=plan_manager.plan_name,
            view="compact",
        )

        # Create quick stats
        quick_stats = self.components.create_quick_stats_line(state)

        # Create usage panel
        usage_panel = self.components.create_usage_overview_panel(
            state, plan_manager.limits
        )

        # Assemble layout
        layout.split_column(
            Layout(header, size=5),
            Layout(Panel(quick_stats, border_style="cyan"), size=3),
            Layout(usage_panel, size=8),
        )

        return layout

    def create_limits_layout(
        self,
        state: MonitorState,
        plan_manager: PlanManager,
    ) -> Layout:
        """Create limits information layout.

        Args:
            state: Current monitor state
            plan_manager: Plan manager

        Returns:
            Limits layout
        """
        layout = Layout()

        # Create header
        header = self.components.create_header(
            plan_name=plan_manager.plan_name,
            view="limits",
        )

        # Create limits panel
        limits_panel = self.components.create_limits_panel(plan_manager.limits)

        # Create usage overview
        usage_panel = self.components.create_usage_overview_panel(
            state, plan_manager.limits
        )

        # Create stats summary
        stats_table = self.components.create_stats_summary(state)

        # Create warning if needed
        warning = self.components.create_warning_banner(state, plan_manager.limits)

        # Assemble layout
        if warning:
            layout.split_column(
                Layout(header, size=5),
                Layout(warning, size=3),
                Layout().split_row(
                    Layout(limits_panel),
                    Layout(usage_panel),
                ),
                Layout(stats_table),
            )
        else:
            layout.split_column(
                Layout(header, size=5),
                Layout().split_row(
                    Layout(limits_panel),
                    Layout(usage_panel),
                ),
                Layout(stats_table),
            )

        return layout

    def create_dual_platform_layout(
        self,
        codex_state: MonitorState,
        claude_state: MonitorState,
        codex_plan_manager: PlanManager,
        claude_plan_manager: PlanManager,
        codex_session: Optional[SessionData] = None,
        claude_session: Optional[SessionData] = None,
        refresh_rate: int = 5,
        split_orientation: str = "horizontal",
    ) -> Layout:
        """Create dual-platform split-screen layout.

        Displays Codex and Claude platforms side-by-side (horizontal) or
        top-bottom (vertical) with independent display areas.

        Args:
            codex_state: Codex monitor state
            claude_state: Claude monitor state
            codex_plan_manager: Codex plan manager
            claude_plan_manager: Claude plan manager
            codex_session: Codex session data (optional)
            claude_session: Claude session data (optional)
            refresh_rate: Refresh rate in seconds
            split_orientation: "horizontal" (left/right) or "vertical" (top/bottom)

        Returns:
            Layout for dual-platform display
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create Codex display
        codex_layout = self._create_platform_display(
            platform=Platform.CODEX,
            state=codex_state,
            plan_manager=codex_plan_manager,
            session=codex_session,
            timestamp=timestamp,
        )

        # Create Claude display
        claude_layout = self._create_platform_display(
            platform=Platform.CLAUDE,
            state=claude_state,
            plan_manager=claude_plan_manager,
            session=claude_session,
            timestamp=timestamp,
            include_cache=True,  # Claude has cache info
        )

        # Create footer
        footer = self.components.create_footer(refresh_rate)
        footer_panel = Panel(footer, border_style="dim")

        # Assemble dual-platform layout
        main_layout = Layout()

        if split_orientation == "horizontal":
            # Left: Codex, Right: Claude
            main_layout.split_column(
                Layout().split_row(
                    Layout(codex_layout, name="codex"),
                    Layout(claude_layout, name="claude"),
                ),
                Layout(footer_panel, size=3, name="footer"),
            )
        else:
            # Top: Codex, Bottom: Claude
            main_layout.split_column(
                Layout(codex_layout, name="codex"),
                Layout(claude_layout, name="claude"),
                Layout(footer_panel, size=3, name="footer"),
            )

        return main_layout

    def _create_platform_display(
        self,
        platform: Platform,
        state: MonitorState,
        plan_manager: PlanManager,
        session: Optional[SessionData] = None,
        timestamp: str = "",
        include_cache: bool = False,
    ) -> Layout:
        """Create display for a single platform.

        Args:
            platform: Platform type
            state: Monitor state
            plan_manager: Plan manager
            session: Session data (optional)
            timestamp: Current timestamp
            include_cache: Whether to include cache info panel (Claude only)

        Returns:
            Layout for single platform
        """
        layout = Layout()

        # Create platform-specific header
        header = self.components.create_platform_header(
            platform=platform,
            state=state,
            plan_manager=plan_manager,
            timestamp=timestamp,
        )

        # Create warning banner if needed
        warning = self.components.create_warning_banner(state, plan_manager.limits)

        # Create usage overview panel
        usage_panel = self.components.create_usage_overview_panel(
            state, plan_manager.limits
        )

        # Create session info panel
        session_panel = self.session_display.create_session_info_panel(state, session)

        # Build layout components list
        components = [Layout(header, size=5)]

        if warning:
            components.append(Layout(warning, size=3))

        components.append(Layout(usage_panel, size=10))

        # Add cache info panel for Claude
        if include_cache and platform == Platform.CLAUDE:
            cache_panel = self.components.create_cache_info_panel(state)
            components.append(Layout(cache_panel, size=12))

        components.append(Layout(session_panel, size=8))

        # Assemble platform layout
        layout.split_column(*components)

        return layout

    def create_multi_platform_comparison_layout(
        self,
        multi_state: MultiPlatformState,
        codex_plan_manager: Optional[PlanManager] = None,
        claude_plan_manager: Optional[PlanManager] = None,
        refresh_rate: int = 5,
    ) -> Layout:
        """Create multi-platform comparison layout.

        Alternative layout that shows aggregate statistics across platforms
        with individual platform breakdowns.

        Args:
            multi_state: Multi-platform state
            codex_plan_manager: Codex plan manager (optional)
            claude_plan_manager: Claude plan manager (optional)
            refresh_rate: Refresh rate in seconds

        Returns:
            Layout for multi-platform comparison
        """
        layout = Layout()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create header showing total cost/tokens across platforms
        header_text = Text()
        header_text.append("Multi-Platform Monitor", style="bold white")
        header_text.append("\n")
        header_text.append("Total Cost: ", style="dim")
        header_text.append(f"${multi_state.total_cost:.4f}", style="bold green")
        header_text.append(" | ", style="dim")
        header_text.append("Total Tokens: ", style="dim")
        header_text.append(f"{multi_state.total_tokens:,}", style="bold cyan")
        header_text.append(" | ", style="dim")
        header_text.append(timestamp, style="dim cyan")

        header = Panel(
            Align.center(header_text),
            border_style="white",
            padding=(0, 2),
        )

        # Create individual platform panels side by side
        platform_panels = []

        if multi_state.codex_state and codex_plan_manager:
            codex_content = self._create_compact_platform_summary(
                Platform.CODEX,
                multi_state.codex_state,
                codex_plan_manager,
            )
            platform_panels.append(codex_content)

        if multi_state.claude_state and claude_plan_manager:
            claude_content = self._create_compact_platform_summary(
                Platform.CLAUDE,
                multi_state.claude_state,
                claude_plan_manager,
            )
            platform_panels.append(claude_content)

        # Create footer
        footer = self.components.create_footer(refresh_rate)

        # Assemble layout
        if len(platform_panels) == 2:
            layout.split_column(
                Layout(header, size=5),
                Layout().split_row(
                    Layout(platform_panels[0]),
                    Layout(platform_panels[1]),
                ),
                Layout(Panel(footer, border_style="dim"), size=3),
            )
        elif len(platform_panels) == 1:
            layout.split_column(
                Layout(header, size=5),
                Layout(platform_panels[0]),
                Layout(Panel(footer, border_style="dim"), size=3),
            )
        else:
            # No active platforms
            empty_msg = Panel(
                "No active platforms detected",
                border_style="red",
            )
            layout.split_column(
                Layout(header, size=5),
                Layout(empty_msg),
                Layout(Panel(footer, border_style="dim"), size=3),
            )

        return layout

    def _create_compact_platform_summary(
        self,
        platform: Platform,
        state: MonitorState,
        plan_manager: PlanManager,
    ) -> Panel:
        """Create compact summary for a single platform.

        Args:
            platform: Platform type
            state: Monitor state
            plan_manager: Plan manager

        Returns:
            Panel with platform summary
        """
        content = Text()
        stats = state.daily_stats

        # Platform title
        content.append(f"{platform.display_name}\n\n", style=f"bold {platform.theme_color}")

        # Plan info
        content.append("Plan: ", style="dim")
        content.append(f"{plan_manager.plan_name}\n\n", style="yellow")

        # Token usage
        content.append("Tokens: ", style="dim")
        content.append(f"{stats.total_tokens:,}", style="cyan")
        if plan_manager.limits.token_limit:
            token_pct = (stats.total_tokens / plan_manager.limits.token_limit) * 100
            content.append(f" ({token_pct:.1f}%)", style="dim")
        content.append("\n")

        # Cost
        content.append("Cost: ", style="dim")
        content.append(f"${stats.total_cost:.4f}", style="green")
        if plan_manager.limits.cost_limit:
            cost_pct = (stats.total_cost / plan_manager.limits.cost_limit) * 100
            content.append(f" ({cost_pct:.1f}%)", style="dim")
        content.append("\n")

        # API calls
        content.append("API Calls: ", style="dim")
        content.append(f"{stats.total_calls}\n\n", style="yellow")

        # Cache info for Claude
        if platform == Platform.CLAUDE and stats.total_cached_tokens > 0:
            cache_hit_rate = stats.average_cache_hit_rate * 100
            content.append("Cache Hit Rate: ", style="dim")
            content.append(f"{cache_hit_rate:.1f}%\n", style="magenta")
            content.append("Cache Savings: ", style="dim")
            content.append(f"${stats.total_cache_savings:.4f}\n", style="green")

        # Warning indicator
        warning_level = "normal"
        if plan_manager.limits.token_limit:
            token_pct = (stats.total_tokens / plan_manager.limits.token_limit) * 100
            if token_pct >= 90:
                warning_level = "critical"
            elif token_pct >= 75:
                warning_level = "warning"

        if warning_level == "critical":
            content.append("\n⚠ CRITICAL USAGE LEVEL", style="bold red")
        elif warning_level == "warning":
            content.append("\n⚠ High usage", style="bold yellow")

        return Panel(
            content,
            border_style=platform.theme_color,
            padding=(1, 2),
        )

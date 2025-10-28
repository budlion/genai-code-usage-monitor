"""Display controller for Codex Monitor.

Main orchestrator for UI rendering and real-time updates.
"""

import time
from datetime import datetime
from typing import Dict, Optional

from rich.console import Console
from rich.live import Live

from genai_code_usage_monitor.core.models import MonitorState, MultiPlatformState, Platform, SessionData
from genai_code_usage_monitor.core.plans import PlanManager
from genai_code_usage_monitor.data.api_client import UsageTracker
from genai_code_usage_monitor.platforms.base import Platform as PlatformAdapter
from genai_code_usage_monitor.ui.layouts import LayoutManager


class DisplayController:
    """Controls the display and rendering of the monitor UI."""

    def __init__(
        self,
        theme: str = "dark",
        view: str = "realtime",
        refresh_rate: int = 5,
    ):
        """Initialize display controller.

        Args:
            theme: Display theme
            view: View mode (realtime, daily, monthly, compact, limits)
            refresh_rate: Refresh rate in seconds
        """
        self.console = Console()
        self.theme = theme
        self.view = view
        self.refresh_rate = refresh_rate
        self.layout_manager = LayoutManager(theme=theme)
        self.current_session: Optional[SessionData] = None

    def start_session(self, session_id: str = None) -> None:
        """Start a new monitoring session.

        Args:
            session_id: Optional session ID
        """
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.current_session = SessionData(
            session_id=session_id,
            start_time=datetime.now(),
            end_time=None,
            total_tokens=0,
            total_cost=0.0,
            api_calls=[],  # Empty list of APICall objects
        )

    def end_session(self) -> None:
        """End the current monitoring session."""
        if self.current_session:
            self.current_session.end_time = datetime.now()

    def update_session(self, state: MonitorState) -> None:
        """Update session with current state.

        Args:
            state: Current monitor state
        """
        if self.current_session:
            self.current_session.total_tokens = state.daily_stats.total_tokens
            self.current_session.total_cost = state.daily_stats.total_cost
            self.current_session.api_calls = state.daily_stats.api_calls  # List of APICall objects

    def render_view(
        self,
        state: MonitorState,
        plan_manager: PlanManager,
        monthly_stats: dict = None,
    ):
        """Render the current view.

        Args:
            state: Current monitor state
            plan_manager: Plan manager
            monthly_stats: Monthly statistics (for monthly view)

        Returns:
            Layout to render
        """
        if self.view == "realtime":
            return self.layout_manager.create_realtime_layout(
                state=state,
                plan_manager=plan_manager,
                session=self.current_session,
                refresh_rate=self.refresh_rate,
            )
        elif self.view == "daily":
            return self.layout_manager.create_daily_layout(
                state=state,
                plan_manager=plan_manager,
                refresh_rate=self.refresh_rate,
            )
        elif self.view == "monthly":
            if monthly_stats is None:
                monthly_stats = {}
            return self.layout_manager.create_monthly_layout(
                state=state,
                plan_manager=plan_manager,
                monthly_stats=monthly_stats,
                refresh_rate=self.refresh_rate,
            )
        elif self.view == "compact":
            return self.layout_manager.create_compact_layout(
                state=state,
                plan_manager=plan_manager,
            )
        elif self.view == "limits":
            return self.layout_manager.create_limits_layout(
                state=state,
                plan_manager=plan_manager,
            )
        else:
            # Default to realtime
            return self.layout_manager.create_realtime_layout(
                state=state,
                plan_manager=plan_manager,
                session=self.current_session,
                refresh_rate=self.refresh_rate,
            )

    def display_static(
        self,
        state: MonitorState,
        plan_manager: PlanManager,
        monthly_stats: dict = None,
    ) -> None:
        """Display a static (non-updating) view.

        Args:
            state: Current monitor state
            plan_manager: Plan manager
            monthly_stats: Monthly statistics (for monthly view)
        """
        layout = self.render_view(state, plan_manager, monthly_stats)
        self.console.print(layout)

    def display_live(
        self,
        tracker: UsageTracker,
        plan_manager: PlanManager,
    ) -> None:
        """Display live updating view.

        Args:
            tracker: Usage tracker
            plan_manager: Plan manager
        """
        # Start session if not already started
        if self.current_session is None:
            self.start_session()

        # Get initial state
        daily_stats = tracker.get_daily_stats()
        monthly_stats = None
        if self.view == "monthly":
            monthly_stats = tracker.get_monthly_stats()

        state = MonitorState(
            daily_stats=daily_stats,
            plan_limits=plan_manager.limits,
        )

        # Render initial layout
        initial_layout = self.render_view(state, plan_manager, monthly_stats)

        # Display with live updates
        try:
            with Live(
                initial_layout,
                console=self.console,
                refresh_per_second=1 / self.refresh_rate,
                screen=True,
            ) as live:
                # Keep updating
                while True:
                    time.sleep(self.refresh_rate)

                    # Get current stats
                    daily_stats = tracker.get_daily_stats()

                    # Get monthly stats if in monthly view
                    monthly_stats = None
                    if self.view == "monthly":
                        monthly_stats = tracker.get_monthly_stats()

                    # Create state
                    state = MonitorState(
                        daily_stats=daily_stats,
                        plan_limits=plan_manager.limits,
                    )

                    # Update session
                    self.update_session(state)

                    # Render view
                    layout = self.render_view(state, plan_manager, monthly_stats)

                    # Update display
                    live.update(layout)

        except KeyboardInterrupt:
            self.end_session()
            self.console.print("\n[yellow]Monitor stopped by user[/yellow]")

    def display_live_multiplatform(
        self,
        platform_adapters: Dict[str, PlatformAdapter],
        plan_manager: PlanManager,
    ) -> None:
        """Display live updating view for multiple platforms.

        Args:
            platform_adapters: Dictionary of platform name -> platform adapter
            plan_manager: Plan manager for limits
        """
        # Start session if not already started
        if self.current_session is None:
            self.start_session()

        # Create multi-platform state
        multi_state = MultiPlatformState()

        # Initialize states for each platform
        for platform_name, adapter in platform_adapters.items():
            try:
                # Get usage data from platform
                usage_stats = adapter.get_usage_data()

                # Create MonitorState for this platform
                platform_enum = Platform.CODEX if platform_name == "codex" else Platform.CLAUDE
                state = MonitorState(
                    daily_stats=usage_stats,
                    plan_limits=plan_manager.limits,
                    platform=platform_enum,
                )

                # Update multi-platform state
                multi_state.update_state(platform_name, state)

            except Exception as e:
                self.display_error(f"Error initializing {platform_name}: {str(e)}")

        # Render initial layout
        if not (multi_state.codex_state or multi_state.claude_state):
            self.display_error("No platforms available")
            return

        # Use dual-platform layout if both platforms are active
        if multi_state.codex_state and multi_state.claude_state:
            initial_layout = self.layout_manager.create_dual_platform_layout(
                codex_state=multi_state.codex_state,
                claude_state=multi_state.claude_state,
                codex_plan_manager=plan_manager,
                claude_plan_manager=plan_manager,
                split_orientation="vertical",  # Default to vertical for most terminals
                refresh_rate=self.refresh_rate,
            )
        else:
            # Single platform - use existing render_view
            primary_state = multi_state.codex_state or multi_state.claude_state
            initial_layout = self.render_view(primary_state, plan_manager, None)

        # Display with live updates
        try:
            with Live(
                initial_layout,
                console=self.console,
                refresh_per_second=1 / self.refresh_rate,
                screen=True,
            ) as live:
                # Keep updating
                while True:
                    time.sleep(self.refresh_rate)

                    # Update each platform independently
                    for platform_name, adapter in platform_adapters.items():
                        try:
                            # Get current stats
                            usage_stats = adapter.get_usage_data()

                            # Create updated state
                            platform_enum = Platform.CODEX if platform_name == "codex" else Platform.CLAUDE
                            state = MonitorState(
                                daily_stats=usage_stats,
                                plan_limits=plan_manager.limits,
                                platform=platform_enum,
                            )

                            # Update multi-platform state
                            multi_state.update_state(platform_name, state)

                        except Exception as e:
                            # Log error but continue monitoring other platforms
                            if self.view == "realtime":
                                self.display_error(f"Error updating {platform_name}: {str(e)}")

                    # Update session with aggregated data
                    if self.current_session:
                        self.current_session.total_tokens = multi_state.total_tokens
                        self.current_session.total_cost = multi_state.total_cost

                    # Render view - use dual-platform layout if both platforms active
                    if multi_state.codex_state and multi_state.claude_state:
                        layout = self.layout_manager.create_dual_platform_layout(
                            codex_state=multi_state.codex_state,
                            claude_state=multi_state.claude_state,
                            codex_plan_manager=plan_manager,
                            claude_plan_manager=plan_manager,
                            split_orientation="vertical",
                            refresh_rate=self.refresh_rate,
                        )
                        live.update(layout)
                    else:
                        # Single platform
                        primary_state = multi_state.codex_state or multi_state.claude_state
                        if primary_state:
                            layout = self.render_view(primary_state, plan_manager, None)
                            live.update(layout)

        except KeyboardInterrupt:
            self.end_session()
            self.console.print("\n[yellow]Monitor stopped by user[/yellow]")

    def display_info(self, message: str) -> None:
        """Display info message.

        Args:
            message: Info message
        """
        self.console.print(f"[cyan]ℹ[/cyan] {message}")

    def display_warning(self, message: str) -> None:
        """Display warning message.

        Args:
            message: Warning message
        """
        self.console.print(f"[yellow]⚠[/yellow] {message}")

    def display_error(self, message: str) -> None:
        """Display error message.

        Args:
            message: Error message
        """
        self.console.print(f"[red]✗[/red] {message}")

    def display_success(self, message: str) -> None:
        """Display success message.

        Args:
            message: Success message
        """
        self.console.print(f"[green]✓[/green] {message}")

    def clear_screen(self) -> None:
        """Clear the console screen."""
        self.console.clear()

    def print_separator(self, char: str = "─", width: int = 80) -> None:
        """Print a separator line.

        Args:
            char: Character to use for separator
            width: Width of separator
        """
        self.console.print(char * width, style="dim")

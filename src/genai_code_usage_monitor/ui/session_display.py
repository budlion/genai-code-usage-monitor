"""Session display components for Codex Monitor.

Displays session information and status.
"""

from datetime import datetime, timedelta
from typing import Optional

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from genai_code_usage_monitor.core.models import MonitorState, SessionData
from genai_code_usage_monitor.ui.progress_bars import TimeProgressBar


class SessionDisplay:
    """Display session information."""

    def __init__(self):
        """Initialize session display."""
        self.time_bar = TimeProgressBar(width=40)

    def create_session_info_panel(
        self, state: MonitorState, session: Optional[SessionData] = None
    ) -> Panel:
        """Create session information panel.

        Args:
            state: Current monitor state
            session: Current session data

        Returns:
            Panel with session information
        """
        if not session:
            # Create a default session for display
            session = SessionData(
                session_id="current",
                start_time=datetime.now(),
                end_time=None,
                total_tokens=state.daily_stats.total_tokens,
                total_cost=state.daily_stats.total_cost,
                api_calls=state.daily_stats.api_calls,  # Use API calls from daily stats
            )

        # Calculate session duration
        if session.end_time:
            duration = session.end_time - session.start_time
        else:
            duration = datetime.now() - session.start_time

        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        seconds = int(duration.total_seconds() % 60)

        duration_str = f"{hours}h {minutes}m {seconds}s"

        # Format start time
        start_str = session.start_time.strftime("%Y-%m-%d %H:%M:%S")

        content = Text()
        content.append("Session ID: ", style="bold")
        content.append(f"{session.session_id}\n", style="cyan")
        content.append("Started: ", style="bold")
        content.append(f"{start_str}\n", style="green")
        content.append("Duration: ", style="bold")
        content.append(f"{duration_str}\n", style="yellow")
        content.append("API Calls: ", style="bold")
        content.append(f"{len(session.api_calls)}", style="magenta")

        return Panel(
            content,
            title="[bold cyan]Session Info[/bold cyan]",
            border_style="cyan",
        )

    def create_session_timer_panel(
        self, elapsed_minutes: float, session_length_minutes: float = 480
    ) -> Panel:
        """Create session timer panel with progress bar.

        Args:
            elapsed_minutes: Minutes elapsed in session
            session_length_minutes: Total session length (default 8 hours)

        Returns:
            Panel with time progress bar
        """
        time_bar = self.time_bar.render(elapsed_minutes, session_length_minutes)

        return Panel(
            time_bar,
            title="[bold cyan]Session Timer[/bold cyan]",
            border_style="cyan",
        )

    def create_session_stats_table(self, state: MonitorState) -> Table:
        """Create session statistics table.

        Args:
            state: Current monitor state

        Returns:
            Table with session statistics
        """
        table = Table(title="Session Statistics", show_header=True, header_style="bold")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green", justify="right")

        stats = state.daily_stats

        table.add_row("Total Tokens", f"{stats.total_tokens:,}")
        table.add_row("Prompt Tokens", f"{stats.prompt_tokens:,}")
        table.add_row("Completion Tokens", f"{stats.completion_tokens:,}")
        table.add_row("Total Cost", f"${stats.total_cost:.4f}")
        table.add_row("API Calls", f"{stats.total_calls}")

        if stats.total_calls > 0:
            avg_tokens = stats.total_tokens / stats.total_calls
            avg_cost = stats.total_cost / stats.total_calls
            table.add_row("Avg Tokens/Call", f"{avg_tokens:.0f}")
            table.add_row("Avg Cost/Call", f"${avg_cost:.4f}")

        return table


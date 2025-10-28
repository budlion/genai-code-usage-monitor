"""Rich terminal UI display components.

DEPRECATED: This module is kept for backward compatibility.
Use display_controller.py for new implementations.
"""

from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TextColumn
from rich.table import Table

from genai_code_usage_monitor.core.models import MonitorState
from genai_code_usage_monitor.core.plans import PlanManager
from genai_code_usage_monitor.core.pricing import PricingCalculator
from genai_code_usage_monitor.ui.display_controller import DisplayController


class MonitorDisplay:
    """Display monitor information in terminal.

    DEPRECATED: Use DisplayController instead for better component organization.
    This class is maintained for backward compatibility.
    """

    def __init__(self, theme: str = "dark"):
        """
        Initialize display.

        Args:
            theme: Display theme
        """
        self.console = Console()
        self.theme = theme
        self.pricing_calc = PricingCalculator()

        # Use new display controller internally
        self._controller = DisplayController(theme=theme, view="realtime", refresh_rate=5)

    def create_header(self, plan_name: str) -> Panel:
        """Create header panel."""
        return Panel(
            f"[bold cyan]Codex Usage Monitor[/bold cyan]\n"
            f"Plan: [yellow]{plan_name}[/yellow] | "
            f"Time: [green]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/green]",
            border_style="cyan",
        )

    def create_usage_panel(self, state: MonitorState) -> Panel:
        """
        Create usage statistics panel.

        Args:
            state: Current monitor state

        Returns:
            Panel with usage information
        """
        stats = state.daily_stats
        limits = state.plan_limits

        # Create progress bars
        progress = Progress(
            TextColumn("[bold]{task.description}"),
            BarColumn(complete_style="green", finished_style="red"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )

        # Token usage
        if limits.token_limit:
            token_pct = (stats.total_tokens / limits.token_limit) * 100
            color = self._get_color_for_percentage(token_pct)
            progress.add_task(
                f"[{color}]Tokens",
                completed=stats.total_tokens,
                total=limits.token_limit,
            )
        else:
            progress.add_task(
                "[cyan]Tokens", completed=stats.total_tokens, total=100000
            )

        # Cost usage
        if limits.cost_limit:
            cost_pct = (stats.total_cost / limits.cost_limit) * 100
            color = self._get_color_for_percentage(cost_pct)
            progress.add_task(
                f"[{color}]Cost",
                completed=int(stats.total_cost * 100),
                total=int(limits.cost_limit * 100),
            )

        # Format token limit with proper handling
        token_limit_str = f"{limits.token_limit:,}" if limits.token_limit else "unlimited"

        content = f"""[bold]Daily Usage:[/bold]
Tokens: [cyan]{stats.total_tokens:,}[/cyan] / {token_limit_str}
Cost: [green]${stats.total_cost:.2f}[/green] / ${limits.cost_limit or 0:.2f}
API Calls: [yellow]{stats.total_calls}[/yellow]
"""

        return Panel(content, title="Usage Statistics", border_style="blue")

    def create_stats_table(self, state: MonitorState) -> Table:
        """
        Create statistics table.

        Args:
            state: Current monitor state

        Returns:
            Table with statistics
        """
        table = Table(title="Model Usage", show_header=True, header_style="bold magenta")
        table.add_column("Model", style="cyan")
        table.add_column("Tokens", justify="right", style="green")
        table.add_column("Cost", justify="right", style="yellow")

        stats = state.daily_stats
        for model, tokens in stats.models.items():
            cost = self.pricing_calc.calculate_total_cost(model, tokens)
            table.add_row(model, f"{tokens:,}", f"${cost:.3f}")

        return table

    def create_realtime_view(self, state: MonitorState, plan_manager: PlanManager) -> Layout:
        """
        Create real-time monitoring view.

        Args:
            state: Current monitor state
            plan_manager: Plan manager

        Returns:
            Layout for display
        """
        layout = Layout()

        layout.split_column(
            Layout(self.create_header(plan_manager.plan_name), size=3),
            Layout(self.create_usage_panel(state)),
            Layout(self.create_stats_table(state)),
        )

        return layout

    def _get_color_for_percentage(self, percentage: float) -> str:
        """Get color based on usage percentage."""
        if percentage < 50:
            return "green"
        elif percentage < 75:
            return "yellow"
        elif percentage < 90:
            return "orange"
        else:
            return "red"

    def display_realtime(
        self, state: MonitorState, plan_manager: PlanManager
    ) -> None:
        """
        Display real-time monitoring view.

        Args:
            state: Current monitor state
            plan_manager: Plan manager
        """
        layout = self.create_realtime_view(state, plan_manager)
        self.console.print(layout)

    def display_error(self, error_message: str) -> None:
        """
        Display error message.

        Args:
            error_message: Error message to display
        """
        self.console.print(
            Panel(
                f"[bold red]Error:[/bold red] {error_message}",
                border_style="red",
            )
        )

    def display_info(self, message: str) -> None:
        """
        Display info message.

        Args:
            message: Message to display
        """
        self._controller.display_info(message)

    def display_warning(self, message: str) -> None:
        """
        Display warning message.

        Args:
            message: Warning message to display
        """
        self._controller.display_warning(message)

    def display_success(self, message: str) -> None:
        """
        Display success message.

        Args:
            message: Success message to display
        """
        self._controller.display_success(message)

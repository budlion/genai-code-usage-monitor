"""Table views for daily and monthly statistics.

Provides detailed table displays for usage data.
"""

from datetime import datetime, timedelta
from typing import Dict, List

from rich.table import Table
from rich.text import Text

from genai_code_usage_monitor.core.models import APICall, UsageStats


class TableViews:
    """Table view components for usage statistics."""

    def create_daily_summary_table(
        self, stats: UsageStats, date: datetime = None
    ) -> Table:
        """Create daily usage summary table.

        Args:
            stats: Usage statistics
            date: Date for the summary (defaults to today)

        Returns:
            Daily summary table
        """
        if date is None:
            date = datetime.now()

        title = f"Daily Summary - {date.strftime('%Y-%m-%d')}"
        table = Table(title=title, show_header=True, header_style="bold cyan")

        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green", justify="right")

        # Overall statistics
        table.add_row("Total Tokens", f"{stats.total_tokens:,}")
        table.add_row("Prompt Tokens", f"{stats.prompt_tokens:,}")
        table.add_row("Completion Tokens", f"{stats.completion_tokens:,}")
        table.add_row("", "")  # Separator
        table.add_row("Total Cost", f"${stats.total_cost:.4f}")
        table.add_row("API Calls", f"{stats.total_calls}")

        # Averages
        if stats.total_calls > 0:
            table.add_row("", "")  # Separator
            table.add_row(
                "Avg Tokens/Call",
                f"{stats.total_tokens / stats.total_calls:.1f}",
            )
            table.add_row(
                "Avg Cost/Call",
                f"${stats.total_cost / stats.total_calls:.4f}",
            )

        return table


    def create_hourly_breakdown_table(
        self, api_calls: List[APICall], date: datetime = None
    ) -> Table:
        """Create hourly usage breakdown table.

        Args:
            api_calls: List of API calls
            date: Date to analyze (defaults to today)

        Returns:
            Hourly breakdown table
        """
        if date is None:
            date = datetime.now()

        title = f"Hourly Breakdown - {date.strftime('%Y-%m-%d')}"
        table = Table(title=title, show_header=True, header_style="bold cyan")

        table.add_column("Hour", style="cyan", no_wrap=True)
        table.add_column("Calls", justify="right", style="yellow")
        table.add_column("Tokens", justify="right", style="green")
        table.add_column("Cost", justify="right", style="green")
        table.add_column("Activity", style="blue")

        # Group by hour
        hourly_data: Dict[int, Dict] = {}
        for hour in range(24):
            hourly_data[hour] = {
                "calls": 0,
                "tokens": 0,
                "cost": 0.0,
            }

        # Filter calls for the specified date
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        for call in api_calls:
            if start_of_day <= call.timestamp < end_of_day:
                hour = call.timestamp.hour
                hourly_data[hour]["calls"] += 1
                hourly_data[hour]["tokens"] += call.tokens.total_tokens
                hourly_data[hour]["cost"] += call.cost

        # Find max calls for activity bar scaling
        max_calls = max((data["calls"] for data in hourly_data.values()), default=1)

        # Add rows
        for hour in range(24):
            data = hourly_data[hour]
            hour_str = f"{hour:02d}:00-{hour:02d}:59"

            # Create activity bar
            if max_calls > 0 and data["calls"] > 0:
                bar_length = int((data["calls"] / max_calls) * 20)
                activity = "█" * bar_length
            else:
                activity = ""

            table.add_row(
                hour_str,
                str(data["calls"]),
                f"{data['tokens']:,}",
                f"${data['cost']:.4f}",
                activity,
            )

        return table

    def create_monthly_summary_table(
        self, monthly_stats: Dict[str, UsageStats]
    ) -> Table:
        """Create monthly summary table.

        Args:
            monthly_stats: Dictionary of month -> UsageStats

        Returns:
            Monthly summary table
        """
        table = Table(
            title="Monthly Summary",
            show_header=True,
            header_style="bold cyan",
        )

        table.add_column("Month", style="cyan", no_wrap=True)
        table.add_column("Tokens", justify="right", style="green")
        table.add_column("Cost", justify="right", style="green")
        table.add_column("Calls", justify="right", style="yellow")
        table.add_column("Avg/Day", justify="right", style="blue")

        # Sort by month (descending)
        sorted_months = sorted(monthly_stats.items(), reverse=True)

        for month_key, stats in sorted_months:
            # Calculate days in month
            year, month = map(int, month_key.split("-"))
            if month == 12:
                next_month = datetime(year + 1, 1, 1)
            else:
                next_month = datetime(year, month + 1, 1)
            days_in_month = (next_month - datetime(year, month, 1)).days

            avg_cost_per_day = stats.total_cost / days_in_month

            table.add_row(
                month_key,
                f"{stats.total_tokens:,}",
                f"${stats.total_cost:.2f}",
                str(stats.total_calls),
                f"${avg_cost_per_day:.2f}",
            )

        return table


    def create_cost_breakdown_table(self, stats: UsageStats) -> Table:
        """Create cost breakdown table.

        Args:
            stats: Usage statistics

        Returns:
            Cost breakdown table
        """
        table = Table(
            title="Cost Breakdown",
            show_header=True,
            header_style="bold green",
        )

        table.add_column("Model", style="cyan")
        table.add_column("Prompt Cost", justify="right", style="blue")
        table.add_column("Completion Cost", justify="right", style="blue")
        table.add_column("Total Cost", justify="right", style="green")
        table.add_column("% of Total", justify="right", style="yellow")

        total_cost = stats.total_cost or 1  # Avoid division by zero

        # Calculate costs per model
        model_costs: Dict[str, Dict] = {}
        for call in stats.api_calls:
            if call.model not in model_costs:
                model_costs[call.model] = {
                    "prompt": 0.0,
                    "completion": 0.0,
                    "total": 0.0,
                }

            # Estimate prompt vs completion cost (simple approximation)
            prompt_ratio = (
                call.tokens.prompt_tokens / call.tokens.total_tokens
                if call.tokens.total_tokens > 0
                else 0.5
            )
            prompt_cost = call.cost * prompt_ratio
            completion_cost = call.cost * (1 - prompt_ratio)

            model_costs[call.model]["prompt"] += prompt_cost
            model_costs[call.model]["completion"] += completion_cost
            model_costs[call.model]["total"] += call.cost

        # Sort by total cost (descending)
        sorted_costs = sorted(
            model_costs.items(),
            key=lambda x: x[1]["total"],
            reverse=True,
        )

        # Add rows
        for model, costs in sorted_costs:
            percentage = (costs["total"] / total_cost) * 100
            table.add_row(
                model,
                f"${costs['prompt']:.4f}",
                f"${costs['completion']:.4f}",
                f"${costs['total']:.4f}",
                f"{percentage:.1f}%",
            )

        return table

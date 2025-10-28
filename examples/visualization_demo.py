"""Demo script showcasing new visualization components.

This example demonstrates:
- Enhanced progress bars with gradients and pulse animations
- Mini charts for trend visualization
- Gauge charts for usage display
- Heat maps for time-based analysis
- Waterfall charts for cost breakdown
"""

from datetime import datetime, timedelta
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

from genai_code_usage_monitor.core.models import (
    MonitorState,
    UsageStats,
    PlanLimits,
    APICall,
    TokenUsage,
)
from genai_code_usage_monitor.ui.components import UIComponents
from genai_code_usage_monitor.ui.visualizations import (
    MiniChart,
    GaugeChart,
    HeatMap,
    WaterfallChart,
)
from genai_code_usage_monitor.ui.progress_bars import (
    TokenProgressBar,
    CostProgressBar,
)


def demo_progress_bars():
    """Demonstrate enhanced progress bars."""
    console = Console()
    console.print("\n[bold cyan]Enhanced Progress Bars Demo[/bold cyan]\n")

    token_bar = TokenProgressBar(width=50)
    cost_bar = CostProgressBar(width=50)

    # Demo different usage levels
    usage_levels = [
        (25.5, "Low usage"),
        (50.75, "Medium usage"),
        (75.33, "High usage"),
        (90.12, "Critical usage"),
        (100.99, "Over limit"),
    ]

    for percentage, label in usage_levels:
        console.print(f"\n[bold]{label}:[/bold]")
        console.print(token_bar.render(percentage))

    console.print("\n[bold]Cost Progress Bars:[/bold]\n")
    cost_bar.render(8.5432, 10.0)
    console.print(cost_bar.render(8.5432, 10.0))
    console.print(cost_bar.render(9.8765, 10.0))


def demo_mini_charts():
    """Demonstrate mini charts and sparklines."""
    console = Console()
    console.print("\n[bold cyan]Mini Charts Demo[/bold cyan]\n")

    chart = MiniChart(width=30, height=8)

    # Sample data - simulated token usage over time
    data = [
        100, 150, 120, 180, 200, 190, 220, 250, 240, 280,
        300, 290, 320, 350, 340, 380, 400, 390, 420, 450,
        440, 480, 500, 490, 520, 550, 540, 580, 600, 590,
    ]

    # Full chart
    console.print(chart.render(
        data,
        title="Token Usage Trend",
        color="cyan",
        show_values=True,
    ))

    # Sparkline
    console.print("\n[bold]Sparkline:[/bold]")
    sparkline = chart.render_sparkline(data, color="green")
    console.print(f"Usage: {sparkline}")


def demo_gauge_charts():
    """Demonstrate gauge charts."""
    console = Console()
    console.print("\n[bold cyan]Gauge Charts Demo[/bold cyan]\n")

    gauge = GaugeChart(width=40)

    usage_levels = [25, 50, 75, 90, 100]

    for level in usage_levels:
        console.print(gauge.render(
            level,
            label=f"Usage Level",
            show_percentage=True,
        ))
        console.print()


def demo_heat_map():
    """Demonstrate heat map visualization."""
    console = Console()
    console.print("\n[bold cyan]Heat Map Demo[/bold cyan]\n")

    heat_map = HeatMap(hours=24, resolution=6)

    # Generate sample time-series data
    now = datetime.now()
    data = {}

    for i in range(144):  # 24 hours * 6 intervals per hour
        timestamp = now - timedelta(minutes=i * 10)
        # Simulate usage pattern - higher during work hours
        hour = timestamp.hour
        if 9 <= hour <= 17:
            value = 100 + (i % 10) * 20
        else:
            value = 20 + (i % 5) * 10
        data[timestamp] = float(value)

    console.print(heat_map.render(data, title="24-Hour API Usage Pattern"))


def demo_waterfall_chart():
    """Demonstrate waterfall chart."""
    console = Console()
    console.print("\n[bold cyan]Waterfall Chart Demo[/bold cyan]\n")

    waterfall = WaterfallChart(width=50)

    # Sample cost breakdown
    cost_components = [
        ("claude-3-opus", 5.4321),
        ("claude-3-sonnet", 2.1234),
        ("claude-3-haiku", 0.8765),
        ("gpt-4", 1.2345),
        ("gpt-3.5-turbo", 0.3456),
    ]

    console.print(waterfall.render(
        cost_components,
        total_label="Total Daily Cost",
        currency=True,
    ))

    console.print("\n[bold]Compact Version:[/bold]\n")
    console.print(waterfall.render_compact(cost_components, width=50))


def demo_ui_components():
    """Demonstrate enhanced UI components."""
    console = Console()
    console.print("\n[bold cyan]Enhanced UI Components Demo[/bold cyan]\n")

    # Create sample state
    state = create_sample_state()
    limits = PlanLimits(
        name="Professional",
        token_limit=1000000,
        cost_limit=100.0,
    )

    ui = UIComponents()

    # Enhanced overview
    console.print(ui.create_enhanced_overview(state, limits))

    # Trend panel
    console.print("\n")
    console.print(ui.create_trend_panel(state))

    # Gauge panel
    console.print("\n")
    console.print(ui.create_gauge_panel(state, limits))


def create_sample_state() -> MonitorState:
    """Create sample monitor state for demo."""
    now = datetime.now()

    # Create sample API calls
    api_calls = []
    for i in range(50):
        call = APICall(
            timestamp=now - timedelta(minutes=i * 5),
            model="claude-3-sonnet" if i % 2 == 0 else "claude-3-haiku",
            tokens=TokenUsage(
                prompt_tokens=500 + i * 10,
                completion_tokens=1000 + i * 20,
                total_tokens=1500 + i * 30,
            ),
            cost=0.05 + i * 0.001,
            status="completed",
        )
        api_calls.append(call)

    # Create stats
    stats = UsageStats(
        total_tokens=750000,
        total_cost=45.67,
        total_calls=150,
        prompt_tokens=300000,
        completion_tokens=450000,
        models={
            "claude-3-sonnet": 450000,
            "claude-3-haiku": 200000,
            "gpt-4": 100000,
        },
        api_calls=api_calls,
    )

    limits = PlanLimits(
        name="Professional",
        token_limit=1000000,
        cost_limit=100.0,
    )

    state = MonitorState(
        daily_stats=stats,
        plan_limits=limits,
        last_update=now,
    )

    return state


def main():
    """Run all demos."""
    console = Console()

    console.print("\n[bold magenta]═══════════════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]     Codex Monitor - Visualization Components Demo     [/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════════════[/bold magenta]\n")

    # Run demos
    demo_progress_bars()
    console.input("\n[dim]Press Enter to continue...[/dim]")

    demo_mini_charts()
    console.input("\n[dim]Press Enter to continue...[/dim]")

    demo_gauge_charts()
    console.input("\n[dim]Press Enter to continue...[/dim]")

    demo_heat_map()
    console.input("\n[dim]Press Enter to continue...[/dim]")

    demo_waterfall_chart()
    console.input("\n[dim]Press Enter to continue...[/dim]")

    demo_ui_components()

    console.print("\n[bold green]Demo completed![/bold green]\n")


if __name__ == "__main__":
    main()

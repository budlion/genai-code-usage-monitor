#!/usr/bin/env python3
"""
Unified AI Usage Monitor Demo
=============================

Demonstrates all new features integrated:
- Dual platform support (Codex + Claude)
- WCAG-compliant themes
- Enhanced visualizations
- Cache token calculation
- Multi-level alert system
"""

import time
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

# Platform imports
from genai_code_usage_monitor.platforms import CodexPlatform, ClaudePlatform

# Core imports
from genai_code_usage_monitor.core.models import PlanLimits, UsageStats, BurnRate
from genai_code_usage_monitor.core.alerts import AlertSystem

# UI imports
from genai_code_usage_monitor.ui.themes import WCAGTheme, ThemeType, set_theme
from genai_code_usage_monitor.ui.progress_bars import TokenProgressBar, CostProgressBar
from genai_code_usage_monitor.ui.visualizations import MiniChart, GaugeChart, HeatMap, WaterfallChart
from genai_code_usage_monitor.ui.components import UIComponents


def print_section(console: Console, title: str):
    """Print a section header."""
    console.print(f"\n{'='*70}")
    console.print(f"  {title}", style="bold cyan")
    console.print('='*70 + "\n")


def demo_dual_platform(console: Console):
    """Demonstrate dual platform support."""
    print_section(console, "🌐 Dual Platform Support")

    # Initialize both platforms
    codex = CodexPlatform()
    claude = ClaudePlatform()

    # Log some sample usage
    console.print("[dim]Simulating API usage...[/dim]\n")

    # Codex usage
    codex.log_api_call("gpt-4", 1000, 500)
    codex.log_api_call("gpt-3.5-turbo", 2000, 800)

    # Claude usage (with caching)
    claude.log_api_call("claude-sonnet-4", 1500, 600, cached_tokens=5000)
    claude.log_api_call("claude-opus", 2000, 1000, cached_tokens=8000)

    # Create comparison table
    table = Table(title="Platform Comparison", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Codex (OpenAI)", justify="right", style="green")
    table.add_column("Claude", justify="right", style="blue")

    codex_stats = codex.get_usage_data()
    claude_stats = claude.get_usage_data()

    table.add_row(
        "Total Tokens",
        f"{codex_stats.total_tokens:,}",
        f"{claude_stats.total_tokens:,}"
    )
    table.add_row(
        "Total Cost",
        f"${codex_stats.total_cost:.4f}",
        f"${claude_stats.total_cost:.4f}"
    )
    table.add_row(
        "API Calls",
        str(codex_stats.total_calls),
        str(claude_stats.total_calls)
    )
    table.add_row(
        "Cache Savings",
        "N/A",
        f"${claude_stats.total_cache_savings:.4f}"
    )

    console.print(table)


def demo_themes(console: Console):
    """Demonstrate WCAG-compliant themes."""
    print_section(console, "🎨 WCAG-Compliant Themes")

    themes = [
        (ThemeType.LIGHT, "Light Theme (4.5:1+ contrast)"),
        (ThemeType.DARK, "Dark Theme (7:1+ contrast)"),
        (ThemeType.CLASSIC, "Classic Theme (backward compatible)")
    ]

    for theme_type, description in themes:
        console.print(f"\n[bold]{description}[/bold]")
        set_theme(theme_type)

        # Show progress bar in this theme
        bar = TokenProgressBar(width=50)
        console.print("  75% usage: ", bar.render(75.5), sep='')

        time.sleep(0.5)


def demo_enhanced_progress_bars(console: Console):
    """Demonstrate enhanced progress bars with gradients and animation."""
    print_section(console, "📊 Enhanced Progress Bars")

    set_theme(ThemeType.DARK)

    levels = [
        (15.0, "LOW - Safe zone"),
        (45.0, "MEDIUM - Normal usage"),
        (78.0, "HIGH - Watch carefully"),
        (92.0, "CRITICAL - Near limit (pulsing)")
    ]

    token_bar = TokenProgressBar(width=50)
    cost_bar = CostProgressBar(width=50)

    for percentage, description in levels:
        console.print(f"\n{description}:")
        console.print("  Token: ", token_bar.render(percentage), sep='')
        console.print("  Cost:  ", cost_bar.render(percentage * 100, 10000), sep='')

        # Simulate pulsing for critical level
        if percentage >= 90:
            console.print("  [dim italic]Pulsing animation active...[/dim italic]")

        time.sleep(0.8)


def demo_visualizations(console: Console):
    """Demonstrate new visualization components."""
    print_section(console, "📈 Advanced Visualizations")

    # Mini Chart
    console.print("[bold]1. Token Trend (Last 24 hours)[/bold]")
    chart = MiniChart(width=60)
    trend_data = [100, 150, 120, 180, 200, 250, 280, 320,
                  350, 380, 400, 420, 450, 480, 500, 520,
                  550, 580, 600, 620, 650, 680, 700, 750]
    console.print(chart.render(trend_data, title="Tokens (k)"))

    # Gauge Chart
    console.print("\n[bold]2. Usage Gauges[/bold]")
    gauge = GaugeChart()
    console.print("  Token Usage: ", gauge.render(75.5, label="Tokens"), sep='')
    console.print("  Cost Usage:  ", gauge.render(45.2, label="Cost"), sep='')
    console.print("  API Calls:   ", gauge.render(62.8, label="Calls"), sep='')

    # Heat Map
    console.print("\n[bold]3. Usage Heat Map (24h pattern)[/bold]")
    heatmap = HeatMap()
    # Simulate hourly usage data
    hourly_data = {}
    now = datetime.now()
    for hour in range(24):
        timestamp = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        intensity = abs((hour - 12)) / 12 * 100  # Peak at noon
        hourly_data[timestamp] = int(intensity * 10)
    console.print(heatmap.render(hourly_data))

    # Waterfall Chart
    console.print("\n[bold]4. Cost Breakdown[/bold]")
    waterfall = WaterfallChart()
    cost_breakdown = [
        ("claude-sonnet-4", 5.4321),
        ("gpt-4", 3.2100),
        ("claude-opus", 2.1234),
        ("gpt-3.5-turbo", 0.8765)
    ]
    console.print(waterfall.render(cost_breakdown))


def demo_alert_system(console: Console):
    """Demonstrate multi-level alert system."""
    print_section(console, "⚠️  Multi-Level Alert System")

    plan = PlanLimits(
        name="Pro",
        token_limit=1_000_000,
        cost_limit=100.0
    )

    alert_system = AlertSystem(plan)

    # Test different usage levels
    test_cases = [
        (550_000, 55.0, 1000, "Normal Usage"),
        (780_000, 78.0, 1500, "Warning Level"),
        (920_000, 92.0, 2500, "Critical Level"),
        (970_000, 97.0, 3500, "Danger Level")
    ]

    for tokens, cost, burn_tokens, description in test_cases:
        console.print(f"\n[bold cyan]{description}[/bold cyan]")

        stats = UsageStats(
            total_tokens=tokens,
            total_cost=cost,
            total_calls=100
        )

        burn_rate = BurnRate(
            tokens_per_minute=burn_tokens,
            cost_per_minute=cost / tokens * burn_tokens
        )

        alerts = alert_system.check_usage_alerts(stats, burn_rate)

        if alerts:
            console.print(alert_system.format_alert_summary())

            # Show predictions
            future_cost, confidence = alert_system.predict_cost(burn_rate, hours_ahead=1)
            console.print(f"  Predicted cost in 1h: ${future_cost:.2f} (confidence: {confidence:.0%})")
        else:
            console.print("  ✅ All systems normal")

        time.sleep(1)


def demo_cache_calculation(console: Console):
    """Demonstrate cache token calculation."""
    print_section(console, "💾 Cache Token Calculation (Claude)")

    from genai_code_usage_monitor.core.pricing import PricingCalculator

    calc = PricingCalculator()

    console.print("[bold]Scenario: Large prompt with caching[/bold]\n")

    # Without caching
    cost_no_cache = calc.calculate_cost(
        model="claude-sonnet-4",
        prompt_tokens=100_000,
        completion_tokens=5_000
    )

    # With caching
    cost_cached, savings = calc.calculate_cached_cost(
        model="claude-sonnet-4",
        prompt_tokens=5_000,
        completion_tokens=5_000,
        cached_tokens=95_000
    )

    # Create comparison table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Scenario", style="cyan")
    table.add_column("Prompt Tokens", justify="right")
    table.add_column("Cached Tokens", justify="right")
    table.add_column("Cost", justify="right", style="green")
    table.add_column("Savings", justify="right", style="yellow")

    table.add_row(
        "Without Cache",
        "100,000",
        "0",
        f"${cost_no_cache:.4f}",
        "-"
    )
    table.add_row(
        "With Cache (95%)",
        "5,000",
        "95,000",
        f"${cost_cached:.4f}",
        f"${savings:.4f} (90% off)"
    )

    console.print(table)

    savings_pct = (savings / cost_no_cache) * 100
    console.print(f"\n💰 [bold green]Total Savings: {savings_pct:.1f}%[/bold green]")


def demo_integrated_dashboard(console: Console):
    """Show integrated dashboard with all features."""
    print_section(console, "📱 Integrated Dashboard")

    set_theme(ThemeType.DARK)

    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )

    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )

    # Header
    layout["header"].update(
        Panel(
            "[bold cyan]AI Usage Monitor - Unified Dashboard[/bold cyan]",
            style="cyan"
        )
    )

    # Left panel - Progress bars
    token_bar = TokenProgressBar(width=40)
    cost_bar = CostProgressBar(width=40)

    left_content = Panel(
        f"{token_bar.render(75.5)}\n\n{cost_bar.render(4567.89, 10000.0)}",
        title="[bold]Usage Overview[/bold]",
        border_style="blue"
    )
    layout["left"].update(left_content)

    # Right panel - Mini trend
    chart = MiniChart(width=40)
    trend_data = [100, 120, 150, 180, 200, 250, 300, 350]

    right_content = Panel(
        chart.render(trend_data, title="Token Trend"),
        title="[bold]24h Trend[/bold]",
        border_style="green"
    )
    layout["right"].update(right_content)

    # Footer
    layout["footer"].update(
        Panel(
            "[dim]Press Ctrl+C to exit | Refreshing every 5s | Powered by Claude Sonnet 4.5[/dim]",
            style="dim"
        )
    )

    console.print(layout)


def main():
    """Run all demos."""
    console = Console()

    console.clear()
    console.print("\n" + "="*70)
    console.print("       🚀 AI USAGE MONITOR - UNIFIED DEMO 🚀       ", style="bold cyan")
    console.print("  Showcasing Codex + Claude | WCAG Themes | Enhanced UI  ", style="dim")
    console.print("="*70)

    try:
        # Run all demos
        demo_dual_platform(console)
        time.sleep(2)

        demo_themes(console)
        time.sleep(2)

        demo_enhanced_progress_bars(console)
        time.sleep(2)

        demo_visualizations(console)
        time.sleep(2)

        demo_alert_system(console)
        time.sleep(2)

        demo_cache_calculation(console)
        time.sleep(2)

        demo_integrated_dashboard(console)

        # Final message
        console.print("\n" + "="*70)
        console.print("  ✅ Demo Complete! All features working perfectly.  ", style="bold green")
        console.print("="*70 + "\n")

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n\n[red]Error: {e}[/red]")
        raise


if __name__ == "__main__":
    main()

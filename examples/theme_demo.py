#!/usr/bin/env python3
"""Demo script for WCAG-compliant theme system.

Demonstrates:
- Theme switching
- Progress bar rendering with different themes
- WCAG compliance features
- Gradient and animation effects
"""

import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from genai_code_usage_monitor.ui import (
    ThemeType,
    set_theme,
    get_theme,
    TokenProgressBar,
    CostProgressBar,
    ModelUsageBar,
)


def demo_theme(theme_type: ThemeType, console: Console):
    """Demonstrate a specific theme.

    Args:
        theme_type: Theme to demonstrate
        console: Rich console instance
    """
    # Switch to theme
    set_theme(theme_type)
    theme = get_theme()
    info = theme.get_theme_info()

    # Display theme header
    console.print()
    console.print(Panel(
        Text(f"{info['name']} Theme Demo", style="bold cyan", justify="center"),
        border_style=theme.get_status_color("primary")
    ))

    console.print(f"[dim]{info['description']}[/dim]")
    console.print(f"[dim]Contrast Ratio: {info['contrast_ratio']}:1[/dim]")
    console.print()

    # Create progress bars with this theme
    token_bar = TokenProgressBar()
    cost_bar = CostProgressBar()
    model_bar = ModelUsageBar()

    # Demo token usage progression
    console.print("[bold]Token Usage Progression:[/bold]")
    for pct in [15, 35, 55, 75, 85, 95]:
        rendered = token_bar.render(pct)
        console.print(Text.from_markup(rendered))
        time.sleep(0.3)

    console.print()

    # Demo cost tracking
    console.print("[bold]Cost Tracking:[/bold]")
    for cost in [2.5, 5.0, 7.5, 9.0, 9.5]:
        rendered = cost_bar.render(cost, 10.0)
        console.print(Text.from_markup(rendered))
        time.sleep(0.3)

    console.print()

    # Demo model distribution
    console.print("[bold]Model Distribution:[/bold]")
    model_stats = {
        "claude-3-opus": {"prompt_tokens": 5000, "completion_tokens": 3000},
        "claude-3-sonnet": {"prompt_tokens": 2000, "completion_tokens": 1500},
        "claude-3-haiku": {"prompt_tokens": 1000, "completion_tokens": 500},
    }
    rendered = model_bar.render(model_stats)
    console.print(Text.from_markup(rendered))

    console.print()
    console.print("[dim]Press Enter to continue...[/dim]")
    input()


def main():
    """Run theme demonstration."""
    console = Console()

    # Title
    console.clear()
    console.print()
    console.print(Panel(
        Text("Codex Monitor - WCAG 2.1 AA Theme System Demo", style="bold cyan", justify="center"),
        border_style="cyan"
    ))
    console.print()

    # Introduction
    intro = Text()
    intro.append("This demo showcases the WCAG 2.1 AA compliant theme system.\n\n", style="white")
    intro.append("Features:\n", style="bold")
    intro.append("  ✓ Light theme with 4.5:1 contrast ratio\n", style="dim")
    intro.append("  ✓ Dark theme with 7:1+ contrast ratio\n", style="dim")
    intro.append("  ✓ Classic theme for backward compatibility\n", style="dim")
    intro.append("  ✓ Gradient color transitions\n", style="dim")
    intro.append("  ✓ Pulse animations for critical states\n", style="dim")
    intro.append("  ✓ 3D visual effects\n\n", style="dim")

    console.print(Panel(intro, border_style="blue"))
    console.print("[dim]Press Enter to start...[/dim]")
    input()

    # Demo each theme
    themes = [
        (ThemeType.LIGHT, "Light theme optimized for bright environments"),
        (ThemeType.DARK, "Dark theme optimized for low-light conditions"),
        (ThemeType.CLASSIC, "Classic theme using Rich library defaults"),
    ]

    for theme_type, description in themes:
        console.clear()
        demo_theme(theme_type, console)

    # Final summary
    console.clear()
    console.print()
    console.print(Panel(
        Text("Theme Demo Complete!", style="bold green", justify="center"),
        border_style="green"
    ))

    console.print()
    console.print("[bold]Next Steps:[/bold]")
    console.print("  1. Use [cyan]--theme[/cyan] flag to set theme: [dim]--theme light|dark|classic|auto[/dim]")
    console.print("  2. Run theme switcher: [dim]python -m codex_monitor.ui.theme_switcher[/dim]")
    console.print("  3. Preview themes: [dim]python -m codex_monitor.ui.theme_switcher --preview dark[/dim]")
    console.print()

    console.print("[dim]For more information, see the theme documentation.[/dim]")
    console.print()


if __name__ == "__main__":
    main()

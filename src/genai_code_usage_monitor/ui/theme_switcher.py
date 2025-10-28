"""Theme switcher for Codex Monitor UI.

Provides command-line interface and programmatic API for switching between
WCAG-compliant themes (Light, Dark, Classic, Auto).
"""

import argparse
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from genai_code_usage_monitor.ui.themes import (
    ThemeType,
    WCAGTheme,
    get_theme,
    set_theme,
)


class ThemeSwitcher:
    """Interactive theme switcher for Codex Monitor.

    Provides methods to:
    - Display current theme information
    - Switch between available themes
    - Preview themes with sample content
    - Show WCAG compliance details
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize theme switcher.

        Args:
            console: Rich console instance (creates new if None)
        """
        self.console = console or Console()

    def display_current_theme(self):
        """Display information about the current theme."""
        theme = get_theme()
        info = theme.get_theme_info()

        # Create theme info panel
        content = Table(show_header=False, box=None, padding=(0, 1))
        content.add_column("Property", style="cyan")
        content.add_column("Value", style="bold")

        content.add_row("Theme Name", info["name"])
        content.add_row("Type", info["type"])
        content.add_row("Description", info["description"])
        content.add_row("Contrast Ratio", f"{info['contrast_ratio']}:1")

        wcag_status = "✓ WCAG 2.1 AA Compliant" if info["wcag_compliant"] else "⚠ Not WCAG AA compliant"
        wcag_style = "green" if info["wcag_compliant"] else "yellow"
        content.add_row("Accessibility", Text(wcag_status, style=wcag_style))

        # Color preview
        colors = info["colors"]
        color_table = Table(show_header=True, box=None, padding=(0, 1))
        color_table.add_column("Color", style="cyan")
        color_table.add_column("Sample", style="bold")

        for name, color in colors.items():
            sample_text = Text(f"■ {color}", style=color)
            color_table.add_row(name.capitalize(), sample_text)

        self.console.print(Panel(
            content,
            title=f"[bold cyan]Current Theme: {info['name']}[/bold cyan]",
            border_style="cyan"
        ))
        self.console.print()
        self.console.print(Panel(
            color_table,
            title="[bold]Color Palette[/bold]",
            border_style="blue"
        ))

    def list_available_themes(self):
        """List all available themes with descriptions."""
        table = Table(title="Available Themes", show_header=True)
        table.add_column("Theme", style="cyan", no_wrap=True)
        table.add_column("Type", style="magenta")
        table.add_column("Contrast", style="green", justify="right")
        table.add_column("Description", style="white")

        themes = [
            (ThemeType.LIGHT, WCAGTheme.LIGHT_THEME),
            (ThemeType.DARK, WCAGTheme.DARK_THEME),
            (ThemeType.CLASSIC, WCAGTheme.CLASSIC_THEME),
        ]

        for theme_type, scheme in themes:
            wcag_badge = "✓ AA" if scheme.contrast_ratio >= 4.5 else ""
            table.add_row(
                scheme.name,
                theme_type.value,
                f"{scheme.contrast_ratio}:1 {wcag_badge}",
                scheme.description
            )

        self.console.print(table)
        self.console.print()
        self.console.print(
            Text("💡 Tip: Use 'auto' to let the system detect the best theme", style="dim italic")
        )

    def switch_to_theme(self, theme_name: str) -> bool:
        """Switch to specified theme.

        Args:
            theme_name: Theme name or type (light, dark, classic, auto)

        Returns:
            True if theme switch successful, False otherwise
        """
        theme_map = {
            "light": ThemeType.LIGHT,
            "dark": ThemeType.DARK,
            "classic": ThemeType.CLASSIC,
            "auto": ThemeType.AUTO,
        }

        theme_type = theme_map.get(theme_name.lower())
        if not theme_type:
            self.console.print(
                f"[red]Error: Unknown theme '{theme_name}'[/red]"
            )
            self.console.print(
                f"Available themes: {', '.join(theme_map.keys())}"
            )
            return False

        # Switch theme
        set_theme(theme_type)

        # Confirm switch
        new_theme = get_theme()
        info = new_theme.get_theme_info()

        self.console.print(
            Panel(
                Text(f"✓ Switched to {info['name']} theme", style="bold green"),
                border_style="green"
            )
        )

        return True

    def preview_theme(self, theme_name: str):
        """Preview a theme with sample progress bars.

        Args:
            theme_name: Theme name to preview (light, dark, classic)
        """
        # Import here to avoid circular dependency
        from genai_code_usage_monitor.ui.progress_bars import (
            TokenProgressBar,
            CostProgressBar,
            ModelUsageBar,
        )

        theme_map = {
            "light": ThemeType.LIGHT,
            "dark": ThemeType.DARK,
            "classic": ThemeType.CLASSIC,
        }

        theme_type = theme_map.get(theme_name.lower())
        if not theme_type:
            self.console.print(f"[red]Error: Unknown theme '{theme_name}'[/red]")
            return

        # Create temporary theme instance for preview
        preview_theme = WCAGTheme(theme_type)
        info = preview_theme.get_theme_info()

        # Display theme info
        self.console.print(f"\n[bold cyan]Preview: {info['name']} Theme[/bold cyan]")
        self.console.print(f"[dim]{info['description']}[/dim]")
        self.console.print(f"[dim]Contrast Ratio: {info['contrast_ratio']}:1[/dim]\n")

        # Create sample progress bars
        token_bar = TokenProgressBar(theme=preview_theme)
        cost_bar = CostProgressBar(theme=preview_theme)
        model_bar = ModelUsageBar(theme=preview_theme)

        # Sample data
        sample_model_stats = {
            "claude-3-opus": {"prompt_tokens": 5000, "completion_tokens": 3000},
            "claude-3-sonnet": {"prompt_tokens": 2000, "completion_tokens": 1500},
        }

        # Render samples
        samples = [
            ("Safe (25%)", token_bar.render(25.0)),
            ("Medium (55%)", token_bar.render(55.0)),
            ("High (80%)", token_bar.render(80.0)),
            ("Critical (95%)", token_bar.render(95.0)),
            ("Cost Safe", cost_bar.render(2.5, 10.0)),
            ("Cost High", cost_bar.render(8.5, 10.0)),
            ("Model Usage", model_bar.render(sample_model_stats)),
        ]

        table = Table(show_header=True, box=None, padding=(0, 1))
        table.add_column("Sample", style="cyan")
        table.add_column("Preview", style="white")

        for label, preview in samples:
            # Parse Rich markup for display
            table.add_row(label, Text.from_markup(preview))

        self.console.print(table)
        self.console.print()

    def show_accessibility_info(self):
        """Display WCAG accessibility information."""
        panel_content = Text()

        panel_content.append("WCAG 2.1 Accessibility Standards\n\n", style="bold cyan")

        panel_content.append("Contrast Ratios:\n", style="bold")
        panel_content.append("  • ", style="dim")
        panel_content.append("WCAG AA Normal Text: ", style="white")
        panel_content.append("4.5:1 minimum\n", style="green")

        panel_content.append("  • ", style="dim")
        panel_content.append("WCAG AAA Normal Text: ", style="white")
        panel_content.append("7:1 minimum\n", style="green")

        panel_content.append("  • ", style="dim")
        panel_content.append("WCAG AA Large Text: ", style="white")
        panel_content.append("3:1 minimum\n", style="green")

        panel_content.append("\nCodex Monitor Themes:\n", style="bold")

        panel_content.append("  • ", style="dim")
        panel_content.append("Light Theme: ", style="white")
        panel_content.append("4.5:1+ (WCAG AA)\n", style="green")

        panel_content.append("  • ", style="dim")
        panel_content.append("Dark Theme: ", style="white")
        panel_content.append("7.0:1+ (Exceeds WCAG AA)\n", style="bold green")

        panel_content.append("  • ", style="dim")
        panel_content.append("Classic Theme: ", style="white")
        panel_content.append("~3.0:1 (Terminal dependent)\n", style="yellow")

        panel_content.append("\nFeatures:\n", style="bold")
        panel_content.append("  ✓ Color blind friendly palettes\n", style="dim")
        panel_content.append("  ✓ High contrast text\n", style="dim")
        panel_content.append("  ✓ Consistent visual hierarchy\n", style="dim")
        panel_content.append("  ✓ Alternative text indicators\n", style="dim")

        self.console.print(Panel(
            panel_content,
            title="[bold]Accessibility Information[/bold]",
            border_style="cyan"
        ))


def create_cli_parser() -> argparse.ArgumentParser:
    """Create argument parser for theme CLI.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Codex Monitor Theme Manager - WCAG 2.1 AA Compliant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show current theme
  python -m codex_monitor.ui.theme_switcher --show

  # List all themes
  python -m codex_monitor.ui.theme_switcher --list

  # Switch to dark theme
  python -m codex_monitor.ui.theme_switcher --switch dark

  # Preview light theme
  python -m codex_monitor.ui.theme_switcher --preview light

  # Show accessibility info
  python -m codex_monitor.ui.theme_switcher --accessibility
        """
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Show current theme information"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available themes"
    )

    parser.add_argument(
        "--switch",
        metavar="THEME",
        help="Switch to specified theme (light, dark, classic, auto)"
    )

    parser.add_argument(
        "--preview",
        metavar="THEME",
        help="Preview theme with sample progress bars"
    )

    parser.add_argument(
        "--accessibility",
        action="store_true",
        help="Show WCAG accessibility information"
    )

    return parser


def main():
    """Main entry point for theme switcher CLI."""
    parser = create_cli_parser()
    args = parser.parse_args()

    switcher = ThemeSwitcher()

    # If no arguments, show current theme
    if not any(vars(args).values()):
        switcher.display_current_theme()
        return

    # Process commands
    if args.show:
        switcher.display_current_theme()

    if args.list:
        switcher.list_available_themes()

    if args.switch:
        switcher.switch_to_theme(args.switch)

    if args.preview:
        switcher.preview_theme(args.preview)

    if args.accessibility:
        switcher.show_accessibility_info()


if __name__ == "__main__":
    main()

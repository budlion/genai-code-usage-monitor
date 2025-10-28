"""CLI main entry point."""

import argparse
import sys
import time
from pathlib import Path

from genai_code_usage_monitor._version import __version__
from genai_code_usage_monitor.core.models import BurnRate
from genai_code_usage_monitor.core.models import MonitorState
from genai_code_usage_monitor.core.models import MultiPlatformState
from genai_code_usage_monitor.core.models import Platform
from genai_code_usage_monitor.core.models import UsageStats
from genai_code_usage_monitor.core.plans import PlanManager
from genai_code_usage_monitor.core.plans import PLANS
from genai_code_usage_monitor.core.settings import Settings
from genai_code_usage_monitor.data.api_client import UsageTracker
from genai_code_usage_monitor.platforms import CodexPlatform
from genai_code_usage_monitor.platforms import ClaudePlatform
from genai_code_usage_monitor.ui.display import MonitorDisplay
from genai_code_usage_monitor.ui.display_controller import DisplayController


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Codex Usage Monitor - Real-time monitoring for OpenAI API usage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Platform options
    parser.add_argument(
        "--platform",
        type=str,
        default="all",
        choices=["codex", "claude", "all"],
        help="Platform to monitor: codex (OpenAI), claude (Anthropic), or all (both platforms, default)",
    )

    # Plan options
    parser.add_argument(
        "--plan",
        type=str,
        default="custom",
        choices=list(PLANS.keys()),
        help="Usage plan (default: custom)",
    )
    parser.add_argument(
        "--custom-limit-tokens",
        type=int,
        help="Custom token limit (for custom plan)",
    )
    parser.add_argument(
        "--custom-limit-cost",
        type=float,
        help="Custom cost limit in USD (default: 50.0)",
    )

    # Display options
    parser.add_argument(
        "--view",
        type=str,
        default="realtime",
        choices=["realtime", "daily", "monthly", "compact", "limits"],
        help="View mode (default: realtime)",
    )
    parser.add_argument(
        "--theme",
        type=str,
        default="auto",
        choices=["auto", "light", "dark", "classic"],
        help="Display theme (default: auto)",
    )

    # Time options
    parser.add_argument(
        "--timezone",
        type=str,
        default="auto",
        help="Timezone (default: auto-detect)",
    )
    parser.add_argument(
        "--time-format",
        type=str,
        default="auto",
        choices=["auto", "12h", "24h"],
        help="Time format (default: auto)",
    )
    parser.add_argument(
        "--reset-hour",
        type=int,
        default=0,
        help="Daily reset hour 0-23 (default: 0)",
    )

    # Refresh options
    parser.add_argument(
        "--refresh-rate",
        type=int,
        default=10,
        help="Data refresh rate in seconds (default: 10)",
    )
    parser.add_argument(
        "--refresh-per-second",
        type=float,
        default=0.75,
        help="Display refresh rate in Hz (default: 0.75)",
    )

    # Logging options
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: INFO)",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        help="Log file path",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    # Other options
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear saved configuration",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Codex Monitor v{__version__}",
    )

    return parser


def run_monitor(args: argparse.Namespace) -> int:
    """
    Run the monitor.

    Args:
        args: Parsed arguments

    Returns:
        Exit code
    """
    # Initialize settings
    settings = Settings(
        plan=args.plan,
        view=args.view,
        theme=args.theme,
        timezone=args.timezone,
        time_format=args.time_format,
        reset_hour=args.reset_hour,
        refresh_rate=args.refresh_rate,
        refresh_per_second=args.refresh_per_second,
        log_level=args.log_level,
        log_file=args.log_file,
        debug=args.debug,
    )

    # Initialize plan manager
    plan_manager = PlanManager(args.plan)

    if args.custom_limit_tokens:
        plan_manager.set_custom_limits(token_limit=args.custom_limit_tokens)
    if args.custom_limit_cost:
        plan_manager.set_custom_limits(cost_limit=args.custom_limit_cost)

    # Initialize platforms based on --platform argument
    platform_adapters = {}
    platform_names = []

    try:
        if args.platform in ["codex", "all"]:
            codex_platform = CodexPlatform()
            platform_adapters["codex"] = codex_platform
            platform_names.append("OpenAI Codex")

        if args.platform in ["claude", "all"]:
            claude_platform = ClaudePlatform()
            platform_adapters["claude"] = claude_platform
            platform_names.append("Claude Code")
    except Exception as e:
        print(f"Error initializing platform(s): {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1

    # Initialize usage tracker (for backward compatibility with Codex)
    tracker = UsageTracker(settings.config_dir)

    # Initialize display controller with new component system
    controller = DisplayController(
        theme=settings.theme,
        view=args.view,
        refresh_rate=args.refresh_rate,
    )

    # Show startup message
    controller.display_info(f"Starting Codex Monitor v{__version__}")
    controller.display_info(f"Platform(s): {', '.join(platform_names)}")
    controller.display_info(f"Plan: {plan_manager.plan_name}")
    controller.display_info(f"Config directory: {settings.config_dir}")
    controller.display_info("Press Ctrl+C to exit")
    controller.console.print()  # Blank line

    try:
        # Start live monitoring with multi-platform support
        if len(platform_adapters) == 1:
            # Single platform mode - use existing display_live
            controller.display_live(tracker, plan_manager)
        else:
            # Multi-platform mode - use new multi-platform display
            controller.display_live_multiplatform(platform_adapters, plan_manager)
        return 0

    except KeyboardInterrupt:
        controller.display_info("\nMonitoring stopped by user")
        return 0
    except Exception as e:
        controller.display_error(f"Unexpected error: {str(e)}")
        if args.debug:
            import traceback

            traceback.print_exc()
        return 1


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args()

    # Handle clear config
    if args.clear:
        settings = Settings()
        if settings.config_file.exists():
            settings.config_file.unlink()
            print("Configuration cleared")
        return 0

    return run_monitor(args)


if __name__ == "__main__":
    sys.exit(main())

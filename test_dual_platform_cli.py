#!/usr/bin/env python3
"""Test dual-platform CLI display."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rich.console import Console
from genai_code_usage_monitor.platforms import CodexPlatform, ClaudePlatform
from genai_code_usage_monitor.core.models import MonitorState, MultiPlatformState, Platform
from genai_code_usage_monitor.core.plans import PlanManager
from genai_code_usage_monitor.ui.layouts import LayoutManager

console = Console()

console.print("[bold cyan]Testing Dual-Platform CLI Display[/bold cyan]\n")

# Initialize platforms
console.print("1. Initializing platforms...")
codex = CodexPlatform()
claude = ClaudePlatform()

# Log some test data
console.print("2. Logging test API calls...")
codex.log_api_call("gpt-4", 1000, 500)
codex.log_api_call("gpt-3.5-turbo", 2000, 800)
claude.log_api_call("claude-sonnet-4", 1500, 600, cached_tokens=5000)
claude.log_api_call("claude-opus", 2000, 1000, cached_tokens=8000)

# Get usage data
console.print("3. Getting usage data...")
codex_stats = codex.get_usage_data()
claude_stats = claude.get_usage_data()

# Create states
console.print("4. Creating monitor states...")
plan_manager = PlanManager("tier1")

codex_state = MonitorState(
    daily_stats=codex_stats,
    plan_limits=plan_manager.limits,
    platform=Platform.CODEX,
)

claude_state = MonitorState(
    daily_stats=claude_stats,
    plan_limits=plan_manager.limits,
    platform=Platform.CLAUDE,
)

# Create layout
console.print("5. Creating dual-platform layout...\n")
layout_manager = LayoutManager(theme="dark")

layout = layout_manager.create_dual_platform_layout(
    codex_state=codex_state,
    claude_state=claude_state,
    codex_plan_manager=plan_manager,
    claude_plan_manager=plan_manager,
    split_orientation="vertical",
    refresh_rate=5,
)

# Display
console.print(layout)
console.print("\n[bold green]✅ Dual-platform display test successful![/bold green]")
console.print(f"Codex: {codex_stats.total_tokens:,} tokens, ${codex_stats.total_cost:.4f}")
console.print(f"Claude: {claude_stats.total_tokens:,} tokens, ${claude_stats.total_cost:.4f}")
console.print(f"Claude cache savings: ${claude_stats.total_cache_savings:.4f}")

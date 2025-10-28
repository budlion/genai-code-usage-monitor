"""Example: Dual-Platform Display for Codex and Claude.

This example demonstrates how to use the new dual-platform layout system
to display Codex and Claude API usage side-by-side or top-bottom in a
split-screen format.

The dual-platform display shows:
- Independent displays for each platform
- Platform-specific headers with distinct colors (cyan for Codex, magenta for Claude)
- Cache information for Claude (since Claude supports caching)
- Different usage patterns and limits per platform
- Warnings and alerts specific to each platform
"""

from datetime import datetime, timedelta
from rich.console import Console
from rich.live import Live

from genai_code_usage_monitor.core.models import (
    MonitorState,
    Platform,
    PlanLimits,
    UsageStats,
    APICall,
    TokenUsage,
    CachedTokenUsage,
    SessionData,
)
from genai_code_usage_monitor.core.plans import PlanManager
from genai_code_usage_monitor.ui.layouts import LayoutManager


def create_sample_codex_state() -> MonitorState:
    """Create sample Codex monitor state with realistic data."""
    # Create sample API calls
    api_calls = []
    base_time = datetime.now() - timedelta(hours=2)

    for i in range(15):
        call = APICall(
            timestamp=base_time + timedelta(minutes=i * 8),
            model="gpt-4",
            tokens=TokenUsage(
                prompt_tokens=150 + (i * 10),
                completion_tokens=75 + (i * 5),
                total_tokens=225 + (i * 15),
            ),
            cost=0.015 + (i * 0.001),
            request_id=f"codex-req-{i:04d}",
            status="completed",
        )
        api_calls.append(call)

    # Create usage stats
    usage_stats = UsageStats(
        total_tokens=sum(call.tokens.total_tokens for call in api_calls),
        total_cost=sum(call.cost for call in api_calls),
        total_calls=len(api_calls),
        prompt_tokens=sum(call.tokens.prompt_tokens for call in api_calls),
        completion_tokens=sum(call.tokens.completion_tokens for call in api_calls),
        models={"gpt-4": sum(call.tokens.total_tokens for call in api_calls)},
        api_calls=api_calls,
    )

    # Create plan limits
    plan_limits = PlanLimits(
        name="Codex Pro",
        token_limit=10_000,
        cost_limit=5.0,
        rate_limit_rpm=100,
        rate_limit_tpm=50_000,
    )

    # Create session data
    session = SessionData(
        session_id="codex-session-001",
        start_time=base_time,
        end_time=None,
        total_tokens=usage_stats.total_tokens,
        total_cost=usage_stats.total_cost,
        api_calls=api_calls,
        models_used=usage_stats.models,
    )

    return MonitorState(
        current_session=session,
        daily_stats=usage_stats,
        monthly_stats=usage_stats,
        plan_limits=plan_limits,
        platform=Platform.CODEX,
    )


def create_sample_claude_state() -> MonitorState:
    """Create sample Claude monitor state with cache data."""
    # Create sample API calls with cache information
    api_calls = []
    base_time = datetime.now() - timedelta(hours=1, minutes=30)

    for i in range(12):
        # Simulate cache hits on some calls
        has_cache = i % 3 == 0  # Every 3rd call uses cache
        cached_tokens_count = 100 if has_cache else 0

        cached_tokens = CachedTokenUsage(
            cached_tokens=cached_tokens_count,
            cache_hit_rate=0.4 if has_cache else 0.0,
            savings=0.003 if has_cache else 0.0,
        ) if has_cache else None

        call = APICall(
            timestamp=base_time + timedelta(minutes=i * 7),
            model="claude-3-opus",
            tokens=TokenUsage(
                prompt_tokens=200 + (i * 12),
                completion_tokens=100 + (i * 8),
                total_tokens=300 + (i * 20),
            ),
            cost=0.025 + (i * 0.002),
            request_id=f"claude-req-{i:04d}",
            status="completed",
            cached_tokens=cached_tokens,
        )
        api_calls.append(call)

    # Calculate total cached tokens and savings
    total_cached = sum(
        call.cached_tokens.cached_tokens
        for call in api_calls
        if call.cached_tokens
    )
    total_savings = sum(
        call.cached_tokens.savings
        for call in api_calls
        if call.cached_tokens
    )

    # Create usage stats
    usage_stats = UsageStats(
        total_tokens=sum(call.tokens.total_tokens for call in api_calls),
        total_cost=sum(call.cost for call in api_calls),
        total_calls=len(api_calls),
        prompt_tokens=sum(call.tokens.prompt_tokens for call in api_calls),
        completion_tokens=sum(call.tokens.completion_tokens for call in api_calls),
        models={"claude-3-opus": sum(call.tokens.total_tokens for call in api_calls)},
        api_calls=api_calls,
        total_cached_tokens=total_cached,
        total_cache_savings=total_savings,
    )

    # Create plan limits
    plan_limits = PlanLimits(
        name="Claude Team",
        token_limit=15_000,
        cost_limit=10.0,
        rate_limit_rpm=150,
        rate_limit_tpm=75_000,
    )

    # Create session data
    session = SessionData(
        session_id="claude-session-001",
        start_time=base_time,
        end_time=None,
        total_tokens=usage_stats.total_tokens,
        total_cost=usage_stats.total_cost,
        api_calls=api_calls,
        models_used=usage_stats.models,
    )

    return MonitorState(
        current_session=session,
        daily_stats=usage_stats,
        monthly_stats=usage_stats,
        plan_limits=plan_limits,
        platform=Platform.CLAUDE,
    )


def main():
    """Run dual-platform display example."""
    console = Console()

    # Print introduction
    console.print("\n[bold cyan]Dual-Platform Display Example[/bold cyan]")
    console.print("Displaying Codex and Claude API usage simultaneously\n")

    # Create sample states
    codex_state = create_sample_codex_state()
    claude_state = create_sample_claude_state()

    # Create plan managers
    codex_plan = PlanManager("tier1")
    codex_plan.set_custom_limits(token_limit=10_000, cost_limit=5.0)

    claude_plan = PlanManager("tier2")
    claude_plan.set_custom_limits(token_limit=15_000, cost_limit=10.0)

    # Create layout manager
    layout_manager = LayoutManager(theme="dark")

    # Demonstration 1: Horizontal split (side-by-side)
    console.print("[bold white]1. Horizontal Split Layout (Side-by-Side)[/bold white]")
    console.print("[dim]Left: Codex | Right: Claude[/dim]\n")

    horizontal_layout = layout_manager.create_dual_platform_layout(
        codex_state=codex_state,
        claude_state=claude_state,
        codex_plan_manager=codex_plan,
        claude_plan_manager=claude_plan,
        codex_session=codex_state.current_session,
        claude_session=claude_state.current_session,
        refresh_rate=5,
        split_orientation="horizontal",
    )

    console.print(horizontal_layout)
    console.print("\n" + "=" * 80 + "\n")

    # Demonstration 2: Vertical split (top-bottom)
    console.print("[bold white]2. Vertical Split Layout (Top-Bottom)[/bold white]")
    console.print("[dim]Top: Codex | Bottom: Claude[/dim]\n")

    vertical_layout = layout_manager.create_dual_platform_layout(
        codex_state=codex_state,
        claude_state=claude_state,
        codex_plan_manager=codex_plan,
        claude_plan_manager=claude_plan,
        codex_session=codex_state.current_session,
        claude_session=claude_state.current_session,
        refresh_rate=5,
        split_orientation="vertical",
    )

    console.print(vertical_layout)
    console.print("\n" + "=" * 80 + "\n")

    # Demonstration 3: Multi-platform comparison layout
    from genai_code_usage_monitor.core.models import MultiPlatformState

    console.print("[bold white]3. Multi-Platform Comparison Layout[/bold white]")
    console.print("[dim]Aggregate view with individual platform breakdowns[/dim]\n")

    multi_state = MultiPlatformState(
        codex_state=codex_state,
        claude_state=claude_state,
    )

    comparison_layout = layout_manager.create_multi_platform_comparison_layout(
        multi_state=multi_state,
        codex_plan_manager=codex_plan,
        claude_plan_manager=claude_plan,
        refresh_rate=5,
    )

    console.print(comparison_layout)
    console.print("\n" + "=" * 80 + "\n")

    # Print summary
    console.print("[bold green]Key Features:[/bold green]")
    console.print("  1. Platform-specific colors (Cyan for Codex, Magenta for Claude)")
    console.print("  2. Independent displays with separate headers and panels")
    console.print("  3. Cache information shown only for Claude")
    console.print("  4. Flexible split orientation (horizontal or vertical)")
    console.print("  5. Multi-platform aggregate view option")
    console.print("  6. WCAG-compliant color schemes for accessibility")
    console.print("\n[bold yellow]Usage:[/bold yellow]")
    console.print("  - Use horizontal split for wide terminals (>160 columns)")
    console.print("  - Use vertical split for standard terminals")
    console.print("  - Use comparison layout for quick overview of both platforms\n")


if __name__ == "__main__":
    main()

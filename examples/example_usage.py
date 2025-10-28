"""Example usage of Codex Monitor programmatically."""

from datetime import datetime
from pathlib import Path

from genai_code_usage_monitor.core.models import UsageStats
from genai_code_usage_monitor.core.plans import PlanManager
from genai_code_usage_monitor.core.pricing import PricingCalculator
from genai_code_usage_monitor.data.api_client import UsageTracker


def main():
    """Demonstrate programmatic usage of Codex Monitor."""

    # Initialize components
    print("🎯 Codex Monitor - Programmatic Usage Example\n")

    # 1. Initialize pricing calculator
    print("1. Initializing pricing calculator...")
    pricing = PricingCalculator()

    # Calculate some costs
    gpt4_cost = pricing.calculate_cost("gpt-4", 1000, 500)
    gpt35_cost = pricing.calculate_cost("gpt-3.5-turbo", 1000, 500)

    print(f"   GPT-4 cost (1000 prompt + 500 completion tokens): ${gpt4_cost:.4f}")
    print(f"   GPT-3.5 cost (1000 prompt + 500 completion tokens): ${gpt35_cost:.4f}\n")

    # 2. Initialize plan manager
    print("2. Setting up plan manager...")
    plan_manager = PlanManager("custom")
    plan_manager.set_custom_limits(token_limit=100000, cost_limit=50.0)

    print(f"   Plan: {plan_manager.current_plan.name}")
    print(f"   Token limit: {plan_manager.current_plan.token_limit:,}")
    print(f"   Cost limit: ${plan_manager.current_plan.cost_limit:.2f}\n")

    # 3. Initialize usage tracker
    print("3. Initializing usage tracker...")
    storage_dir = Path.home() / ".codex-monitor" / "examples"
    tracker = UsageTracker(storage_dir)

    print(f"   Storage directory: {storage_dir}")
    print(f"   Logging usage data...\n")

    # 4. Log some sample API calls
    print("4. Logging sample API calls...")

    # Simulate some API calls
    calls = [
        ("gpt-4", 800, 400),
        ("gpt-4", 1200, 600),
        ("gpt-3.5-turbo", 500, 300),
        ("gpt-4-turbo", 1500, 800),
        ("gpt-3.5-turbo", 700, 400),
    ]

    for model, prompt_tokens, completion_tokens in calls:
        call = tracker.log_api_call(model, prompt_tokens, completion_tokens)
        print(f"   Logged: {model} - {call.tokens.total_tokens:,} tokens (${call.cost:.4f})")

    print()

    # 5. Get usage summary
    print("5. Retrieving usage summary...")
    summary = tracker.get_usage_summary()

    print(f"   Today's usage:")
    print(f"     Tokens: {summary['today']['tokens']:,}")
    print(f"     Cost: ${summary['today']['cost']:.4f}")
    print(f"     Calls: {summary['today']['calls']}")
    print()

    # 6. Check limit status
    print("6. Checking limit status...")
    status = plan_manager.check_limit_status(
        summary['today']['tokens'],
        summary['today']['cost']
    )

    print(f"   Warning level: {status['warning_level']}")
    if 'percentage' in status['tokens']:
        print(f"   Token usage: {status['tokens']['percentage']:.1f}%")
    if 'percentage' in status['cost']:
        print(f"   Cost usage: {status['cost']['percentage']:.1f}%")

    print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    main()

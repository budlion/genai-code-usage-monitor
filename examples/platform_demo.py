"""Demo script showing the platform abstraction layer usage.

This script demonstrates how to use the platform abstraction layer
to work with multiple AI platforms (Codex and Claude) through a
unified interface.
"""

from genai_code_usage_monitor.platforms import ClaudePlatform, CodexPlatform


def demo_codex_platform():
    """Demonstrate OpenAI Codex platform usage."""
    print("=" * 60)
    print("OpenAI Codex Platform Demo")
    print("=" * 60)

    # Initialize Codex platform
    platform = CodexPlatform()
    print(f"\nPlatform: {platform.get_platform_name()}")
    print(f"Storage: {platform.storage_path}")

    # Get model info
    model_info = platform.get_model_info("gpt-4")
    print(f"\nGPT-4 Model Info:")
    print(f"  - Prompt price: ${model_info['prompt_price_per_1m']:.2f} per 1M tokens")
    print(f"  - Completion price: ${model_info['completion_price_per_1m']:.2f} per 1M tokens")

    # Calculate costs
    prompt_cost = platform.calculate_cost(10000, "gpt-4", is_prompt=True)
    completion_cost = platform.calculate_cost(10000, "gpt-4", is_prompt=False)
    print(f"\nCost for 10,000 tokens:")
    print(f"  - Prompt tokens: ${prompt_cost:.4f}")
    print(f"  - Completion tokens: ${completion_cost:.4f}")

    # Get usage data
    try:
        stats = platform.get_usage_data()
        print(f"\nToday's Usage:")
        print(f"  - Total tokens: {stats.total_tokens:,}")
        print(f"  - Total cost: ${stats.total_cost:.4f}")
        print(f"  - Total calls: {stats.total_calls}")
    except Exception as e:
        print(f"\nNo usage data available yet: {e}")


def demo_claude_platform():
    """Demonstrate Claude Code platform usage."""
    print("\n" + "=" * 60)
    print("Claude Code Platform Demo")
    print("=" * 60)

    # Initialize Claude platform
    platform = ClaudePlatform()
    print(f"\nPlatform: {platform.get_platform_name()}")
    print(f"Storage: {platform.storage_path}")

    # Get model info
    model_info = platform.get_model_info("claude-sonnet-4")
    print(f"\nClaude Sonnet 4 Model Info:")
    print(f"  - Prompt price: ${model_info['prompt_price_per_1m']:.2f} per 1M tokens")
    print(f"  - Completion price: ${model_info['completion_price_per_1m']:.2f} per 1M tokens")
    print(f"  - Cached prompt price: ${model_info['cached_prompt_price_per_1m']:.2f} per 1M tokens")
    print(f"  - Cache discount: {model_info['cache_discount']}")

    # Calculate costs with and without caching
    regular_cost = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=True)
    cached_cost = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)
    completion_cost = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=False)

    print(f"\nCost for 10,000 tokens:")
    print(f"  - Regular prompt tokens: ${regular_cost:.4f}")
    print(f"  - Cached prompt tokens: ${cached_cost:.4f} (90% discount!)")
    print(f"  - Completion tokens: ${completion_cost:.4f}")

    # Get usage data
    try:
        stats = platform.get_usage_data()
        print(f"\nToday's Usage:")
        print(f"  - Total tokens: {stats.total_tokens:,}")
        print(f"  - Total cost: ${stats.total_cost:.4f}")
        print(f"  - Total calls: {stats.total_calls}")
    except Exception as e:
        print(f"\nNo usage data available yet")


def demo_unified_interface():
    """Demonstrate unified platform interface."""
    print("\n" + "=" * 60)
    print("Unified Platform Interface Demo")
    print("=" * 60)

    platforms = [
        CodexPlatform(),
        ClaudePlatform(),
    ]

    print("\nComparing platforms for 100,000 prompt tokens:\n")
    print(f"{'Platform':<20} {'Regular':<15} {'Cached':<15}")
    print("-" * 50)

    for platform in platforms:
        regular = platform.calculate_cost(100000, "default", is_prompt=True)
        cached = platform.calculate_cost(100000, "default", is_cached=True)
        print(f"{platform.get_platform_name():<20} ${regular:<14.4f} ${cached:<14.4f}")


if __name__ == "__main__":
    demo_codex_platform()
    demo_claude_platform()
    demo_unified_interface()

    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)

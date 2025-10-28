"""Unit tests for platform abstraction layer.

Tests the Platform interface and implementations for both CodexPlatform
and ClaudePlatform.
"""

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from genai_code_usage_monitor.platforms import ClaudePlatform, CodexPlatform, Platform
from genai_code_usage_monitor.core.models import UsageStats


class TestPlatformInterface:
    """Test the Platform abstract base class."""

    def test_platform_is_abstract(self):
        """Platform cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Platform()


class TestCodexPlatform:
    """Test CodexPlatform implementation."""

    def test_initialization(self):
        """Test CodexPlatform initialization."""
        platform = CodexPlatform()
        assert platform.get_platform_name() == "OpenAI Codex"
        assert platform.storage_path.exists()

    def test_custom_data_directory(self):
        """Test CodexPlatform with custom data directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            platform = CodexPlatform(data_directory=tmpdir)
            assert platform.storage_path == Path(tmpdir)

    def test_calculate_cost_prompt(self):
        """Test cost calculation for prompt tokens."""
        platform = CodexPlatform()
        cost = platform.calculate_cost(10000, "gpt-4", is_prompt=True)
        # GPT-4 prompt: $30 per 1M tokens
        assert cost == pytest.approx(0.30, rel=1e-4)

    def test_calculate_cost_completion(self):
        """Test cost calculation for completion tokens."""
        platform = CodexPlatform()
        cost = platform.calculate_cost(10000, "gpt-4", is_prompt=False)
        # GPT-4 completion: $60 per 1M tokens
        assert cost == pytest.approx(0.60, rel=1e-4)

    def test_calculate_cost_gpt35(self):
        """Test cost calculation for GPT-3.5."""
        platform = CodexPlatform()
        cost = platform.calculate_cost(10000, "gpt-3.5-turbo", is_prompt=True)
        # GPT-3.5 prompt: $0.50 per 1M tokens
        assert cost == pytest.approx(0.005, rel=1e-4)

    def test_get_usage_data_empty(self):
        """Test getting usage data when no data exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            platform = CodexPlatform(data_directory=tmpdir)
            stats = platform.get_usage_data()
            assert isinstance(stats, UsageStats)
            assert stats.total_tokens == 0
            assert stats.total_cost == 0.0

    def test_get_session_info_empty(self):
        """Test getting session info when no data exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            platform = CodexPlatform(data_directory=tmpdir)
            session = platform.get_session_info()
            assert session is None

    def test_log_api_call(self):
        """Test logging an API call."""
        with tempfile.TemporaryDirectory() as tmpdir:
            platform = CodexPlatform(data_directory=tmpdir)
            call = platform.log_api_call("gpt-4", prompt_tokens=100, completion_tokens=50)

            assert call.model == "gpt-4"
            assert call.tokens.prompt_tokens == 100
            assert call.tokens.completion_tokens == 50
            assert call.tokens.total_tokens == 150
            assert call.cost > 0

    def test_get_model_info(self):
        """Test getting model information."""
        platform = CodexPlatform()
        info = platform.get_model_info("gpt-4")

        assert info["name"] == "gpt-4"
        assert info["platform"] == "OpenAI Codex"
        assert info["prompt_price_per_1m"] == 30.0
        assert info["completion_price_per_1m"] == 60.0


class TestClaudePlatform:
    """Test ClaudePlatform implementation."""

    def test_initialization(self):
        """Test ClaudePlatform initialization."""
        platform = ClaudePlatform()
        assert platform.get_platform_name() == "Claude Code"
        assert platform.storage_path.exists()

    def test_custom_data_directory(self):
        """Test ClaudePlatform with custom data directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            platform = ClaudePlatform(data_directory=tmpdir)
            assert platform.storage_path == Path(tmpdir)

    def test_calculate_cost_prompt(self):
        """Test cost calculation for prompt tokens."""
        platform = ClaudePlatform()
        cost = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=True)
        # Claude Sonnet prompt: $3 per 1M tokens
        assert cost == pytest.approx(0.03, rel=1e-4)

    def test_calculate_cost_cached(self):
        """Test cost calculation for cached tokens (90% discount)."""
        platform = ClaudePlatform()
        cost = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)
        # Claude Sonnet cached: $0.30 per 1M tokens (90% discount)
        assert cost == pytest.approx(0.003, rel=1e-4)

    def test_calculate_cost_completion(self):
        """Test cost calculation for completion tokens."""
        platform = ClaudePlatform()
        cost = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=False)
        # Claude Sonnet completion: $15 per 1M tokens
        assert cost == pytest.approx(0.15, rel=1e-4)

    def test_calculate_cost_opus(self):
        """Test cost calculation for Claude Opus."""
        platform = ClaudePlatform()
        cost = platform.calculate_cost(10000, "claude-opus", is_prompt=True)
        # Claude Opus prompt: $15 per 1M tokens
        assert cost == pytest.approx(0.15, rel=1e-4)

    def test_cache_discount(self):
        """Test that cached tokens are 90% cheaper."""
        platform = ClaudePlatform()
        regular = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=True)
        cached = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)

        # Cached should be 10% of regular (90% discount)
        assert cached == pytest.approx(regular * 0.1, rel=1e-4)

    def test_get_usage_data_empty(self):
        """Test getting usage data when no data exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            platform = ClaudePlatform(data_directory=tmpdir)
            stats = platform.get_usage_data()
            assert isinstance(stats, UsageStats)
            assert stats.total_tokens == 0
            assert stats.total_cost == 0.0

    def test_get_session_info_empty(self):
        """Test getting session info when no data exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            platform = ClaudePlatform(data_directory=tmpdir)
            session = platform.get_session_info()
            assert session is None

    def test_log_api_call(self):
        """Test logging an API call."""
        with tempfile.TemporaryDirectory() as tmpdir:
            platform = ClaudePlatform(data_directory=tmpdir)
            call = platform.log_api_call(
                "claude-sonnet-4",
                prompt_tokens=1000,
                completion_tokens=500,
                cached_tokens=5000
            )

            assert call.model == "claude-sonnet-4"
            # Total prompt tokens includes cached
            assert call.tokens.prompt_tokens == 6000
            assert call.tokens.completion_tokens == 500
            assert call.tokens.total_tokens == 6500
            assert call.cost > 0

    def test_log_api_call_with_cache_discount(self):
        """Test that logged API call applies cache discount correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            platform = ClaudePlatform(data_directory=tmpdir)

            # Log call with caching
            call = platform.log_api_call(
                "claude-sonnet-4",
                prompt_tokens=0,
                completion_tokens=0,
                cached_tokens=10000
            )

            # Should use cached pricing ($0.30 per 1M tokens)
            expected_cost = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)
            assert call.cost == pytest.approx(expected_cost, rel=1e-4)

    def test_get_model_info(self):
        """Test getting model information."""
        platform = ClaudePlatform()
        info = platform.get_model_info("claude-sonnet-4")

        assert info["name"] == "claude-sonnet-4"
        assert info["platform"] == "Claude Code"
        assert info["prompt_price_per_1m"] == 3.0
        assert info["completion_price_per_1m"] == 15.0
        assert info["cached_prompt_price_per_1m"] == 0.30
        assert info["cache_discount"] == "90%"
        assert info["supports_caching"] is True


class TestPlatformComparison:
    """Test comparing different platforms."""

    def test_codex_vs_claude_pricing(self):
        """Compare pricing between Codex and Claude."""
        codex = CodexPlatform()
        claude = ClaudePlatform()

        # For 100K prompt tokens
        codex_cost = codex.calculate_cost(100000, "gpt-4", is_prompt=True)
        claude_cost = claude.calculate_cost(100000, "claude-sonnet-4", is_prompt=True)

        # GPT-4 ($30/1M) should be more expensive than Claude Sonnet ($3/1M)
        assert codex_cost > claude_cost

    def test_claude_cache_benefit(self):
        """Test Claude's caching benefit."""
        claude = ClaudePlatform()

        regular = claude.calculate_cost(100000, "claude-sonnet-4", is_prompt=True)
        cached = claude.calculate_cost(100000, "claude-sonnet-4", is_cached=True)

        # Regular: $0.30, Cached: $0.03
        assert regular == pytest.approx(0.30, rel=1e-4)
        assert cached == pytest.approx(0.03, rel=1e-4)

    def test_unified_interface(self):
        """Test that both platforms implement the same interface."""
        platforms = [CodexPlatform(), ClaudePlatform()]

        for platform in platforms:
            # All platforms should have these methods
            assert hasattr(platform, "get_usage_data")
            assert hasattr(platform, "get_session_info")
            assert hasattr(platform, "calculate_cost")
            assert hasattr(platform, "get_platform_name")
            assert hasattr(platform, "get_model_info")

            # All should return a string name
            assert isinstance(platform.get_platform_name(), str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

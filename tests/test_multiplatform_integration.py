"""Integration tests for multi-platform monitoring.

Tests the complete data flow and state management for monitoring
multiple AI platforms (Codex and Claude) simultaneously, ensuring:
- Data independence between platforms
- No cross-platform contamination
- Efficient refresh cycles
- Proper error handling if one platform fails
"""

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from genai_code_usage_monitor.core.models import (
    MonitorState,
    MultiPlatformState,
    Platform,
    UsageStats,
)
from genai_code_usage_monitor.core.plans import PlanManager
from genai_code_usage_monitor.platforms import ClaudePlatform, CodexPlatform


class TestSinglePlatformMode:
    """Test monitoring in single platform mode (Codex only)."""

    def test_codex_only_initialization(self, tmp_path):
        """Test that Codex platform initializes correctly."""
        # Create platform with temporary storage
        platform = CodexPlatform(data_directory=str(tmp_path))

        # Verify platform name
        assert platform.get_platform_name() == "OpenAI Codex"

        # Get usage data (should be empty initially)
        stats = platform.get_usage_data()
        assert isinstance(stats, UsageStats)
        assert stats.total_tokens == 0
        assert stats.total_cost == 0.0
        assert stats.total_calls == 0

    def test_codex_only_data_tracking(self, tmp_path):
        """Test that Codex platform tracks usage correctly."""
        platform = CodexPlatform(data_directory=str(tmp_path))

        # Log some API calls
        call1 = platform.log_api_call("gpt-4", 100, 50)
        assert call1.tokens.prompt_tokens == 100
        assert call1.tokens.completion_tokens == 50
        assert call1.cost > 0

        call2 = platform.log_api_call("gpt-3.5-turbo", 200, 100)
        assert call2.cost > 0

        # Get aggregated stats
        stats = platform.get_usage_data()
        assert stats.total_tokens == 450  # 100+50+200+100
        assert stats.total_calls == 2
        assert stats.total_cost > 0

    def test_codex_only_state_creation(self, tmp_path):
        """Test MonitorState creation for Codex only."""
        platform = CodexPlatform(data_directory=str(tmp_path))
        plan_manager = PlanManager("custom")
        plan_manager.set_custom_limits(token_limit=100000, cost_limit=50.0)

        # Log some usage
        platform.log_api_call("gpt-4", 1000, 500)

        # Create MonitorState
        stats = platform.get_usage_data()
        state = MonitorState(
            daily_stats=stats,
            plan_limits=plan_manager.limits,
            platform=Platform.CODEX,
        )

        assert state.platform == Platform.CODEX
        assert state.daily_stats.total_tokens == 1500
        assert state.token_usage_percentage is not None
        assert state.token_usage_percentage > 0


class TestClaudeOnlyMode:
    """Test monitoring in single platform mode (Claude only)."""

    def test_claude_only_initialization(self, tmp_path):
        """Test that Claude platform initializes correctly."""
        # Create platform with temporary storage
        platform = ClaudePlatform(data_directory=str(tmp_path))

        # Verify platform name
        assert platform.get_platform_name() == "Claude Code"

        # Get usage data (should be empty initially)
        stats = platform.get_usage_data()
        assert isinstance(stats, UsageStats)
        assert stats.total_tokens == 0
        assert stats.total_cost == 0.0
        assert stats.total_calls == 0

    def test_claude_only_data_tracking(self, tmp_path):
        """Test that Claude platform tracks usage correctly."""
        platform = ClaudePlatform(data_directory=str(tmp_path))

        # Log API calls with cache support
        call1 = platform.log_api_call(
            "claude-sonnet-4", prompt_tokens=1000, completion_tokens=500, cached_tokens=5000
        )
        assert call1.tokens.prompt_tokens == 6000  # includes cached
        assert call1.tokens.completion_tokens == 500
        assert call1.cost > 0

        # Get aggregated stats
        stats = platform.get_usage_data()
        assert stats.total_tokens == 6500
        assert stats.total_calls == 1
        assert stats.total_cost > 0

    def test_claude_cache_discount(self, tmp_path):
        """Test that Claude applies cache discount correctly."""
        platform = ClaudePlatform(data_directory=str(tmp_path))

        # Calculate cost without cache
        regular_cost = platform.calculate_cost(10000, "claude-sonnet-4", is_prompt=True)

        # Calculate cost with cache (90% discount)
        cached_cost = platform.calculate_cost(10000, "claude-sonnet-4", is_cached=True)

        # Cached cost should be 10% of regular cost
        assert abs(cached_cost - (regular_cost * 0.1)) < 0.0001

    def test_claude_only_state_creation(self, tmp_path):
        """Test MonitorState creation for Claude only."""
        platform = ClaudePlatform(data_directory=str(tmp_path))
        plan_manager = PlanManager("custom")
        plan_manager.set_custom_limits(token_limit=100000, cost_limit=50.0)

        # Log some usage
        platform.log_api_call("claude-sonnet-4", 1000, 500)

        # Create MonitorState
        stats = platform.get_usage_data()
        state = MonitorState(
            daily_stats=stats,
            plan_limits=plan_manager.limits,
            platform=Platform.CLAUDE,
        )

        assert state.platform == Platform.CLAUDE
        assert state.daily_stats.total_tokens == 1500
        assert state.token_usage_percentage is not None


class TestDualPlatformMode:
    """Test monitoring in dual platform mode (both Codex and Claude)."""

    def test_dual_platform_initialization(self, tmp_path):
        """Test that both platforms can be initialized simultaneously."""
        codex_dir = tmp_path / "codex"
        claude_dir = tmp_path / "claude"

        codex_platform = CodexPlatform(data_directory=str(codex_dir))
        claude_platform = ClaudePlatform(data_directory=str(claude_dir))

        assert codex_platform.get_platform_name() == "OpenAI Codex"
        assert claude_platform.get_platform_name() == "Claude Code"

    def test_data_isolation(self, tmp_path):
        """Test that data is isolated between platforms."""
        codex_dir = tmp_path / "codex"
        claude_dir = tmp_path / "claude"

        codex_platform = CodexPlatform(data_directory=str(codex_dir))
        claude_platform = ClaudePlatform(data_directory=str(claude_dir))

        # Log to Codex only
        codex_platform.log_api_call("gpt-4", 1000, 500)

        # Log to Claude only
        claude_platform.log_api_call("claude-sonnet-4", 2000, 1000)

        # Verify data isolation
        codex_stats = codex_platform.get_usage_data()
        claude_stats = claude_platform.get_usage_data()

        assert codex_stats.total_tokens == 1500
        assert claude_stats.total_tokens == 3000

        # Verify models are tracked separately
        assert "gpt-4" in codex_stats.models
        assert "claude-sonnet-4" not in codex_stats.models

        assert "claude-sonnet-4" in claude_stats.models
        assert "gpt-4" not in claude_stats.models

    def test_multiplatform_state(self, tmp_path):
        """Test MultiPlatformState aggregation."""
        codex_dir = tmp_path / "codex"
        claude_dir = tmp_path / "claude"

        codex_platform = CodexPlatform(data_directory=str(codex_dir))
        claude_platform = ClaudePlatform(data_directory=str(claude_dir))
        plan_manager = PlanManager("custom")
        plan_manager.set_custom_limits(token_limit=100000, cost_limit=50.0)

        # Log usage to both platforms
        codex_platform.log_api_call("gpt-4", 1000, 500)
        claude_platform.log_api_call("claude-sonnet-4", 2000, 1000)

        # Create states for each platform
        codex_stats = codex_platform.get_usage_data()
        codex_state = MonitorState(
            daily_stats=codex_stats,
            plan_limits=plan_manager.limits,
            platform=Platform.CODEX,
        )

        claude_stats = claude_platform.get_usage_data()
        claude_state = MonitorState(
            daily_stats=claude_stats,
            plan_limits=plan_manager.limits,
            platform=Platform.CLAUDE,
        )

        # Create multi-platform state
        multi_state = MultiPlatformState(
            codex_state=codex_state,
            claude_state=claude_state,
        )

        # Verify aggregation
        assert multi_state.total_tokens == 4500  # 1500 + 3000
        assert multi_state.total_cost > 0
        assert "codex" in multi_state.active_platforms
        assert "claude" in multi_state.active_platforms

    def test_independent_refresh_cycles(self, tmp_path):
        """Test that platforms can be refreshed independently."""
        codex_dir = tmp_path / "codex"
        claude_dir = tmp_path / "claude"

        codex_platform = CodexPlatform(data_directory=str(codex_dir))
        claude_platform = ClaudePlatform(data_directory=str(claude_dir))
        plan_manager = PlanManager("custom")

        # Initial state
        multi_state = MultiPlatformState()

        # Update Codex state only
        codex_platform.log_api_call("gpt-4", 1000, 500)
        codex_stats = codex_platform.get_usage_data()
        codex_state = MonitorState(
            daily_stats=codex_stats,
            plan_limits=plan_manager.limits,
            platform=Platform.CODEX,
        )
        multi_state.update_state("codex", codex_state)

        assert multi_state.codex_state is not None
        assert multi_state.claude_state is None

        # Update Claude state independently
        claude_platform.log_api_call("claude-sonnet-4", 2000, 1000)
        claude_stats = claude_platform.get_usage_data()
        claude_state = MonitorState(
            daily_stats=claude_stats,
            plan_limits=plan_manager.limits,
            platform=Platform.CLAUDE,
        )
        multi_state.update_state("claude", claude_state)

        assert multi_state.codex_state is not None
        assert multi_state.claude_state is not None

        # Verify independence: update Codex again
        codex_platform.log_api_call("gpt-3.5-turbo", 500, 250)
        codex_stats = codex_platform.get_usage_data()
        codex_state = MonitorState(
            daily_stats=codex_stats,
            plan_limits=plan_manager.limits,
            platform=Platform.CODEX,
        )
        multi_state.update_state("codex", codex_state)

        # Claude state should remain unchanged
        assert multi_state.claude_state.daily_stats.total_tokens == 3000
        # Codex state should be updated
        assert multi_state.codex_state.daily_stats.total_tokens == 2250

    def test_error_handling_one_platform_fails(self, tmp_path):
        """Test that system continues if one platform fails."""
        codex_dir = tmp_path / "codex"
        claude_dir = tmp_path / "claude"

        codex_platform = CodexPlatform(data_directory=str(codex_dir))
        claude_platform = ClaudePlatform(data_directory=str(claude_dir))
        plan_manager = PlanManager("custom")

        # Log to Codex successfully
        codex_platform.log_api_call("gpt-4", 1000, 500)

        # Create multi-platform state
        multi_state = MultiPlatformState()

        # Update Codex state (should succeed)
        try:
            codex_stats = codex_platform.get_usage_data()
            codex_state = MonitorState(
                daily_stats=codex_stats,
                plan_limits=plan_manager.limits,
                platform=Platform.CODEX,
            )
            multi_state.update_state("codex", codex_state)
        except Exception as e:
            pytest.fail(f"Codex platform should not fail: {e}")

        # Simulate Claude failure (corrupt storage)
        invalid_claude_dir = tmp_path / "nonexistent"
        claude_platform_invalid = ClaudePlatform(data_directory=str(invalid_claude_dir))

        # Try to update Claude state (may fail, but shouldn't affect Codex)
        try:
            claude_stats = claude_platform_invalid.get_usage_data()
            claude_state = MonitorState(
                daily_stats=claude_stats,
                plan_limits=plan_manager.limits,
                platform=Platform.CLAUDE,
            )
            multi_state.update_state("claude", claude_state)
        except Exception:
            # Claude failed, but that's okay
            pass

        # Verify Codex data is still intact
        assert multi_state.codex_state is not None
        assert multi_state.codex_state.daily_stats.total_tokens == 1500

    def test_multiplatform_state_helpers(self):
        """Test MultiPlatformState helper methods."""
        multi_state = MultiPlatformState()

        # Initially no platforms
        assert len(multi_state.active_platforms) == 0
        assert not multi_state.has_platform("codex")
        assert not multi_state.has_platform("claude")

        # Add Codex state
        plan_manager = PlanManager("custom")
        codex_state = MonitorState(
            daily_stats=UsageStats(),
            plan_limits=plan_manager.limits,
            platform=Platform.CODEX,
        )
        multi_state.update_state("codex", codex_state)

        assert len(multi_state.active_platforms) == 1
        assert multi_state.has_platform("codex")
        assert not multi_state.has_platform("claude")
        assert multi_state.get_state("codex") is not None
        assert multi_state.get_state("claude") is None

        # Add Claude state
        claude_state = MonitorState(
            daily_stats=UsageStats(),
            plan_limits=plan_manager.limits,
            platform=Platform.CLAUDE,
        )
        multi_state.update_state("claude", claude_state)

        assert len(multi_state.active_platforms) == 2
        assert multi_state.has_platform("codex")
        assert multi_state.has_platform("claude")


class TestErrorRecovery:
    """Test error recovery and resilience."""

    def test_corrupted_data_recovery(self, tmp_path):
        """Test that system recovers from corrupted data files."""
        platform = CodexPlatform(data_directory=str(tmp_path))

        # Create corrupted data file
        usage_file = tmp_path / "usage_log.jsonl"
        usage_file.write_text("corrupted data\n{invalid json}\n")

        # Should still be able to get stats (empty)
        stats = platform.get_usage_data()
        assert stats.total_tokens == 0

        # Should be able to log new calls
        call = platform.log_api_call("gpt-4", 100, 50)
        assert call.tokens.total_tokens == 150

    def test_missing_storage_directory(self, tmp_path):
        """Test initialization with missing storage directory."""
        nonexistent_dir = tmp_path / "nonexistent" / "nested" / "path"

        # Should create directories automatically
        platform = CodexPlatform(data_directory=str(nonexistent_dir))
        assert nonexistent_dir.exists()

        # Should work normally
        call = platform.log_api_call("gpt-4", 100, 50)
        assert call.tokens.total_tokens == 150


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

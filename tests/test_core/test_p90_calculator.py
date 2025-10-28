"""Comprehensive tests for P90 Calculator.

Tests ML-based predictions mentioned in README:
- P90 percentile calculations
- Trend analysis (increasing/decreasing/stable)
- Confidence calculations
- Recommended limit calculations
"""

from datetime import datetime, timedelta
import pytest
import numpy as np

from genai_code_usage_monitor.core.p90_calculator import P90Calculator
from genai_code_usage_monitor.core.models import (
    APICall,
    SessionData,
    TokenUsage,
)


@pytest.fixture
def calculator():
    """Create P90 calculator with default settings."""
    return P90Calculator(time_window_hours=192)


@pytest.fixture
def sample_sessions():
    """Create sample session data for testing."""
    base_time = datetime.now() - timedelta(hours=100)
    sessions = []
    
    for i in range(20):
        session = SessionData(
            session_id=f"session-{i}",
            start_time=base_time + timedelta(hours=i*5),
            end_time=base_time + timedelta(hours=i*5 + 1),
            total_tokens=1000 + (i * 100),  # Increasing pattern
            total_cost=0.1 + (i * 0.01),
            api_calls=[],
        )
        sessions.append(session)
    
    return sessions


@pytest.fixture
def sample_calls():
    """Create sample API call data for testing."""
    base_time = datetime.now() - timedelta(hours=50)
    calls = []
    
    for i in range(50):
        call = APICall(
            model="gpt-4",
            timestamp=base_time + timedelta(hours=i),
            tokens=TokenUsage(
                prompt_tokens=100 + (i * 10),
                completion_tokens=50 + (i * 5),
                total_tokens=150 + (i * 15),
            ),
            cost=0.015 + (i * 0.002),
        )
        calls.append(call)
    
    return calls


class TestP90Calculation:
    """Test basic P90 percentile calculations."""

    def test_p90_with_sufficient_data(self, calculator, sample_sessions, sample_calls):
        """Test P90 calculation with 100+ samples."""
        result = calculator.calculate_p90(sample_sessions, sample_calls)
        
        assert result is not None
        assert result.p90_tokens > 0
        assert result.p90_cost > 0
        assert result.sample_size > 0
        assert result.confidence > 0

    def test_p90_with_minimal_data(self, calculator):
        """Test P90 calculation with minimal data (2-10 samples)."""
        base_time = datetime.now() - timedelta(hours=10)
        sessions = [
            SessionData(
                session_id="s1",
                start_time=base_time,
                end_time=base_time + timedelta(hours=1),
                total_tokens=1000,
                total_cost=0.1,
                api_calls=[],
            ),
            SessionData(
                session_id="s2",
                start_time=base_time + timedelta(hours=2),
                end_time=base_time + timedelta(hours=3),
                total_tokens=2000,
                total_cost=0.2,
                api_calls=[],
            ),
        ]
        
        result = calculator.calculate_p90(sessions, [])
        
        assert result is not None
        assert result.sample_size == 2
        # Confidence should be low with few samples
        assert result.confidence < 0.1

    def test_p90_with_empty_data(self, calculator):
        """Test P90 calculation with no data returns None."""
        result = calculator.calculate_p90([], [])
        
        assert result is None

    def test_p90_tokens_accuracy(self, calculator):
        """Test P90 tokens calculation accuracy."""
        # Create controlled dataset
        base_time = datetime.now() - timedelta(hours=50)
        values = list(range(100, 201))  # 100 to 200 tokens
        sessions = []
        
        for i, tokens in enumerate(values):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i),
                end_time=base_time + timedelta(hours=i+1),
                total_tokens=tokens,
                total_cost=tokens * 0.001,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_p90(sessions, [])
        
        # P90 of 100-200 should be around 190
        expected_p90 = int(np.percentile(values, 90))
        assert result.p90_tokens == expected_p90

    def test_p90_cost_accuracy(self, calculator):
        """Test P90 cost calculation accuracy."""
        base_time = datetime.now() - timedelta(hours=50)
        cost_values = [i * 0.01 for i in range(1, 101)]  # $0.01 to $1.00
        sessions = []
        
        for i, cost in enumerate(cost_values):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i),
                end_time=base_time + timedelta(hours=i+1),
                total_tokens=1000,
                total_cost=cost,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_p90(sessions, [])
        
        expected_p90 = float(np.percentile(cost_values, 90))
        assert abs(result.p90_cost - expected_p90) < 0.01

    def test_p90_calls_accuracy(self, calculator):
        """Test P90 calls calculation accuracy."""
        base_time = datetime.now() - timedelta(hours=50)
        sessions = []

        for i in range(100):
            # Vary number of calls per session
            num_calls = (i % 10) + 1
            # Create fake APICall objects (just count them)
            api_calls = []
            for j in range(num_calls):
                call = APICall(
                    model="gpt-4",
                    timestamp=base_time + timedelta(hours=i),
                    tokens=TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150),
                    cost=0.015,
                )
                api_calls.append(call)

            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i),
                end_time=base_time + timedelta(hours=i+1),
                total_tokens=1000,
                total_cost=0.1,
                api_calls=api_calls,
            )
            sessions.append(session)

        result = calculator.calculate_p90(sessions, [])

        assert result.p90_calls > 0
        assert result.p90_calls <= 10  # Max is 10 in our data


class TestConfidenceCalculation:
    """Test confidence calculation based on sample size."""

    def test_confidence_with_zero_samples(self, calculator):
        """Test confidence with 0 samples returns None."""
        result = calculator.calculate_p90([], [])
        
        assert result is None

    def test_confidence_with_50_samples(self, calculator):
        """Test confidence with 50 samples is ~50%."""
        base_time = datetime.now() - timedelta(hours=50)
        sessions = []
        
        for i in range(50):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i),
                end_time=base_time + timedelta(hours=i+1),
                total_tokens=1000 + i,
                total_cost=0.1,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_p90(sessions, [])
        
        # Confidence formula: min(0.95, sample_size / 100)
        assert result.confidence == pytest.approx(0.50, rel=0.01)

    def test_confidence_with_100_plus_samples(self, calculator):
        """Test confidence with 100+ samples caps at 95%."""
        base_time = datetime.now() - timedelta(hours=150)
        sessions = []
        
        for i in range(150):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i),
                end_time=base_time + timedelta(hours=i+1),
                total_tokens=1000 + i,
                total_cost=0.1,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_p90(sessions, [])
        
        # Should cap at 95%
        assert result.confidence == 0.95

    def test_confidence_formula(self, calculator):
        """Test confidence formula: min(0.95, sample_size/100)."""
        test_cases = [
            (10, 0.10),
            (25, 0.25),
            (75, 0.75),
            (100, 0.95),
            (200, 0.95),  # Capped
        ]
        
        for sample_size, expected_confidence in test_cases:
            base_time = datetime.now() - timedelta(hours=sample_size)
            sessions = []
            
            for i in range(sample_size):
                session = SessionData(
                    session_id=f"s{i}",
                    start_time=base_time + timedelta(hours=i),
                    end_time=base_time + timedelta(hours=i+1),
                    total_tokens=1000,
                    total_cost=0.1,
                    api_calls=[],
                )
                sessions.append(session)
            
            result = calculator.calculate_p90(sessions, [])
            assert result.confidence == expected_confidence


class TestRecommendedLimit:
    """Test recommended limit calculation with 10% buffer."""

    def test_10_percent_buffer(self, calculator):
        """Test recommended limit is P90 * 1.1 (10% buffer)."""
        base_time = datetime.now() - timedelta(hours=50)
        sessions = []
        
        # Create data where P90 will be 1800 tokens
        for i in range(100):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i),
                end_time=base_time + timedelta(hours=i+1),
                total_tokens=1000 + (i * 10),  # 1000 to 1990
                total_cost=0.1,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_p90(sessions, [])
        
        # Recommended limit should be P90 * 1.1
        expected_limit = int(result.p90_tokens * 1.1)
        assert result.recommended_limit == expected_limit

    def test_recommended_limit_is_integer(self, calculator, sample_sessions):
        """Test recommended limit is always an integer."""
        result = calculator.calculate_p90(sample_sessions, [])
        
        assert isinstance(result.recommended_limit, int)


class TestTimeWindow:
    """Test time window filtering."""

    def test_default_192_hour_window(self, calculator):
        """Test default 192-hour (8 days) window."""
        assert calculator.time_window_hours == 192

    def test_custom_time_window(self):
        """Test custom time windows."""
        calc_24h = P90Calculator(time_window_hours=24)
        calc_168h = P90Calculator(time_window_hours=168)
        
        assert calc_24h.time_window_hours == 24
        assert calc_168h.time_window_hours == 168

    def test_filters_old_data(self, calculator):
        """Test that data outside window is filtered."""
        base_time = datetime.now()
        
        # Create old session (outside 192-hour window)
        old_session = SessionData(
            session_id="old",
            start_time=base_time - timedelta(hours=300),
            end_time=base_time - timedelta(hours=299),
            total_tokens=10000,  # Very high value
            total_cost=1.0,
            api_calls=[],
        )
        
        # Create recent sessions (inside window)
        recent_sessions = []
        for i in range(10):
            session = SessionData(
                session_id=f"recent-{i}",
                start_time=base_time - timedelta(hours=i*10),
                end_time=base_time - timedelta(hours=i*10 - 1),
                total_tokens=1000,  # Normal values
                total_cost=0.1,
                api_calls=[],
            )
            recent_sessions.append(session)
        
        all_sessions = [old_session] + recent_sessions
        result = calculator.calculate_p90(all_sessions, [])
        
        # P90 should reflect recent data only, not the old high value
        assert result.p90_tokens < 5000
        assert result.sample_size == 10  # Only recent sessions counted

    def test_mixing_sessions_and_calls(self, calculator, sample_sessions, sample_calls):
        """Test mixing sessions and calls in time window."""
        result = calculator.calculate_p90(sample_sessions, sample_calls)
        
        # Should combine data from both sources
        assert result.sample_size == len(sample_sessions) + len(sample_calls)


class TestTrendAnalysis:
    """Test trend analysis (increasing/decreasing/stable)."""

    def test_increasing_trend(self, calculator):
        """Test detecting increasing trend (>10% change)."""
        base_time = datetime.now() - timedelta(days=5)
        sessions = []
        
        # First half: low values
        for i in range(10):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i*12),
                end_time=base_time + timedelta(hours=i*12 + 1),
                total_tokens=1000,  # Low
                total_cost=0.1,
                api_calls=[],
            )
            sessions.append(session)
        
        # Second half: high values (>10% increase)
        for i in range(10, 20):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i*12),
                end_time=base_time + timedelta(hours=i*12 + 1),
                total_tokens=1200,  # 20% higher
                total_cost=0.12,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_trend(sessions, period_days=7)
        
        assert result["trend"] == "increasing"
        assert result["change_percentage"] > 10

    def test_decreasing_trend(self, calculator):
        """Test detecting decreasing trend (<-10% change)."""
        base_time = datetime.now() - timedelta(days=5)
        sessions = []
        
        # First half: high values
        for i in range(10):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i*12),
                end_time=base_time + timedelta(hours=i*12 + 1),
                total_tokens=1200,
                total_cost=0.12,
                api_calls=[],
            )
            sessions.append(session)
        
        # Second half: low values (>10% decrease)
        for i in range(10, 20):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i*12),
                end_time=base_time + timedelta(hours=i*12 + 1),
                total_tokens=1000,  # ~17% lower
                total_cost=0.10,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_trend(sessions, period_days=7)
        
        assert result["trend"] == "decreasing"
        assert result["change_percentage"] < -10

    def test_stable_trend(self, calculator):
        """Test detecting stable trend (-10% to +10%)."""
        base_time = datetime.now() - timedelta(days=5)
        sessions = []
        
        # Consistent values throughout
        for i in range(20):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i*12),
                end_time=base_time + timedelta(hours=i*12 + 1),
                total_tokens=1000 + (i % 3) * 50,  # Small variation
                total_cost=0.1,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_trend(sessions, period_days=7)
        
        assert result["trend"] == "stable"
        assert -10 <= result["change_percentage"] <= 10

    def test_insufficient_data_for_trend(self, calculator):
        """Test trend with insufficient data (<2 sessions)."""
        session = SessionData(
            session_id="s1",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            total_tokens=1000,
            total_cost=0.1,
            api_calls=[],
        )
        
        result = calculator.calculate_trend([session], period_days=7)
        
        assert result["trend"] == "neutral"
        assert result["change_percentage"] == 0.0

    def test_empty_sessions_trend(self, calculator):
        """Test trend with no sessions."""
        result = calculator.calculate_trend([], period_days=7)
        
        assert result["trend"] == "neutral"
        assert result["change_percentage"] == 0.0

    def test_change_percentage_calculation(self, calculator):
        """Test change percentage is calculated correctly."""
        base_time = datetime.now() - timedelta(days=5)
        sessions = []
        
        # First half: exactly 1000 tokens
        for i in range(10):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i*12),
                end_time=base_time + timedelta(hours=i*12 + 1),
                total_tokens=1000,
                total_cost=0.1,
                api_calls=[],
            )
            sessions.append(session)
        
        # Second half: exactly 1300 tokens (30% increase)
        for i in range(10, 20):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i*12),
                end_time=base_time + timedelta(hours=i*12 + 1),
                total_tokens=1300,
                total_cost=0.13,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_trend(sessions, period_days=7)
        
        # Should be approximately 30% increase
        assert result["change_percentage"] == pytest.approx(30.0, rel=0.01)
        assert result["first_half_avg"] == 1000
        assert result["second_half_avg"] == 1300


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_all_same_values(self, calculator):
        """Test with all sessions having identical values."""
        base_time = datetime.now() - timedelta(hours=50)
        sessions = []
        
        for i in range(100):
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i),
                end_time=base_time + timedelta(hours=i+1),
                total_tokens=1000,  # Always same
                total_cost=0.1,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_p90(sessions, [])
        
        assert result.p90_tokens == 1000
        assert result.p90_cost == pytest.approx(0.1, rel=0.01)

    def test_highly_variable_data(self, calculator):
        """Test with highly variable data."""
        base_time = datetime.now() - timedelta(hours=50)
        sessions = []
        
        values = [100, 10000, 200, 9000, 300, 8000, 400, 7000]
        for i, tokens in enumerate(values * 12):  # Repeat to get 96 samples
            session = SessionData(
                session_id=f"s{i}",
                start_time=base_time + timedelta(hours=i),
                end_time=base_time + timedelta(hours=i+1),
                total_tokens=tokens,
                total_cost=tokens * 0.001,
                api_calls=[],
            )
            sessions.append(session)
        
        result = calculator.calculate_p90(sessions, [])
        
        # P90 should be in the higher range
        assert result.p90_tokens > 7000

    def test_sessions_no_calls(self, calculator, sample_sessions):
        """Test with sessions but no API calls."""
        result = calculator.calculate_p90(sample_sessions, [])
        
        assert result is not None
        assert result.sample_size == len(sample_sessions)

    def test_calls_no_sessions(self, calculator, sample_calls):
        """Test with API calls but no sessions."""
        result = calculator.calculate_p90([], sample_calls)
        
        assert result is not None
        assert result.sample_size == len(sample_calls)
        # P90 calls should be 0 when no sessions provided
        assert result.p90_calls == 0

    def test_zero_tokens_costs(self, calculator):
        """Test with sessions having zero tokens/costs."""
        base_time = datetime.now() - timedelta(hours=10)
        sessions = [
            SessionData(
                session_id="s1",
                start_time=base_time,
                end_time=base_time + timedelta(hours=1),
                total_tokens=0,
                total_cost=0.0,
                api_calls=[],
            )
        ]
        
        # This should return None as there's no meaningful data
        result = calculator.calculate_p90(sessions, [])
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

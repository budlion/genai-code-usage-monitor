"""P90 percentile calculator for usage analysis."""

from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional

import numpy as np

from genai_code_usage_monitor.core.models import APICall
from genai_code_usage_monitor.core.models import P90Analysis
from genai_code_usage_monitor.core.models import SessionData


class P90Calculator:
    """Calculate P90 percentile statistics for usage prediction."""

    def __init__(self, time_window_hours: int = 192):
        """
        Initialize P90 calculator.

        Args:
            time_window_hours: Time window for analysis in hours (default: 192 = 8 days)
        """
        self.time_window_hours = time_window_hours

    def calculate_p90(
        self, sessions: List[SessionData], calls: List[APICall]
    ) -> Optional[P90Analysis]:
        """
        Calculate P90 statistics from historical data.

        Args:
            sessions: List of session data
            calls: List of API calls

        Returns:
            P90Analysis object or None if insufficient data
        """
        if not sessions and not calls:
            return None

        cutoff_time = datetime.now() - timedelta(hours=self.time_window_hours)

        # Filter recent sessions and calls
        recent_sessions = [s for s in sessions if s.start_time >= cutoff_time]
        recent_calls = [c for c in calls if c.timestamp >= cutoff_time]

        if not recent_sessions and not recent_calls:
            return None

        # Extract metrics
        token_values = []
        cost_values = []
        call_counts = []

        # From sessions
        for session in recent_sessions:
            if session.total_tokens > 0:
                token_values.append(session.total_tokens)
                cost_values.append(session.total_cost)
                call_counts.append(len(session.api_calls))

        # From individual calls
        for call in recent_calls:
            token_values.append(call.tokens.total_tokens)
            cost_values.append(call.cost)

        if not token_values:
            return None

        # Calculate P90
        p90_tokens = int(np.percentile(token_values, 90))
        p90_cost = float(np.percentile(cost_values, 90)) if cost_values else 0.0
        p90_calls = int(np.percentile(call_counts, 90)) if call_counts else 0

        # Calculate confidence based on sample size
        sample_size = len(token_values)
        confidence = min(0.95, (sample_size / 100))  # Max 95% confidence with 100+ samples

        # Recommend limit based on P90 with buffer
        recommended_limit = int(p90_tokens * 1.1)  # 10% buffer

        return P90Analysis(
            p90_tokens=p90_tokens,
            p90_cost=p90_cost,
            p90_calls=p90_calls,
            sample_size=sample_size,
            time_window_hours=self.time_window_hours,
            confidence=confidence,
            recommended_limit=recommended_limit,
        )

    def calculate_trend(
        self, sessions: List[SessionData], period_days: int = 7
    ) -> dict:
        """
        Calculate usage trends over a period.

        Args:
            sessions: List of session data
            period_days: Number of days to analyze

        Returns:
            Dictionary with trend information
        """
        if not sessions:
            return {"trend": "neutral", "change_percentage": 0.0}

        cutoff_time = datetime.now() - timedelta(days=period_days)
        recent_sessions = [s for s in sessions if s.start_time >= cutoff_time]

        if len(recent_sessions) < 2:
            return {"trend": "neutral", "change_percentage": 0.0}

        # Split into first and second half
        mid_point = len(recent_sessions) // 2
        first_half = recent_sessions[:mid_point]
        second_half = recent_sessions[mid_point:]

        first_avg = sum(s.total_tokens for s in first_half) / len(first_half)
        second_avg = sum(s.total_tokens for s in second_half) / len(second_half)

        if first_avg == 0:
            return {"trend": "neutral", "change_percentage": 0.0}

        change_percentage = ((second_avg - first_avg) / first_avg) * 100

        if change_percentage > 10:
            trend = "increasing"
        elif change_percentage < -10:
            trend = "decreasing"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "change_percentage": change_percentage,
            "first_half_avg": first_avg,
            "second_half_avg": second_avg,
        }

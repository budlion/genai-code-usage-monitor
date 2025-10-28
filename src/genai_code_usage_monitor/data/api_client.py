"""OpenAI API client for usage monitoring."""

import json
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from genai_code_usage_monitor.core.models import APICall
from genai_code_usage_monitor.core.models import TokenUsage
from genai_code_usage_monitor.core.models import UsageStats
from genai_code_usage_monitor.core.pricing import PricingCalculator


class UsageTracker:
    """Track and store API usage locally."""

    def __init__(self, storage_dir: Path):
        """
        Initialize usage tracker.

        Args:
            storage_dir: Directory for storing usage data
        """
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.usage_file = self.storage_dir / "usage_log.jsonl"
        self.pricing_calc = PricingCalculator()

    def log_api_call(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        request_id: Optional[str] = None,
    ) -> APICall:
        """
        Log an API call.

        Args:
            model: Model name
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            request_id: Optional request ID

        Returns:
            APICall object
        """
        tokens = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )

        cost = self.pricing_calc.calculate_cost(model, prompt_tokens, completion_tokens)

        call = APICall(
            timestamp=datetime.now(),
            model=model,
            tokens=tokens,
            cost=cost,
            request_id=request_id,
            status="completed",
        )

        # Save to file
        self._save_call(call)

        return call

    def _save_call(self, call: APICall) -> None:
        """Save API call to storage."""
        with open(self.usage_file, "a") as f:
            f.write(call.model_dump_json() + "\n")

    def get_recent_calls(self, hours: int = 24) -> List[APICall]:
        """
        Get recent API calls.

        Args:
            hours: Number of hours to look back

        Returns:
            List of APICall objects
        """
        if not self.usage_file.exists():
            return []

        cutoff_time = datetime.now() - timedelta(hours=hours)
        calls = []

        with open(self.usage_file, "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    call = APICall(**data)
                    if call.timestamp >= cutoff_time:
                        calls.append(call)
                except Exception:
                    continue

        return calls

    def get_daily_stats(self, date: Optional[datetime] = None) -> UsageStats:
        """
        Get usage statistics for a specific day.

        Args:
            date: Date to get stats for (default: today)

        Returns:
            UsageStats object
        """
        if date is None:
            date = datetime.now()

        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        calls = self.get_recent_calls(hours=720)  # Get up to 30 days
        daily_calls = [
            c for c in calls if start_of_day <= c.timestamp < end_of_day
        ]

        stats = UsageStats(date=start_of_day)
        for call in daily_calls:
            stats.update_from_call(call)

        return stats

    def get_monthly_stats(self, year: int, month: int) -> UsageStats:
        """
        Get usage statistics for a specific month.

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            UsageStats object
        """
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        calls = self.get_recent_calls(hours=720)  # Get up to 30 days
        monthly_calls = [
            c for c in calls if start_date <= c.timestamp < end_date
        ]

        stats = UsageStats(date=start_date)
        for call in monthly_calls:
            stats.update_from_call(call)

        return stats

    def get_usage_summary(self) -> Dict[str, any]:
        """
        Get overall usage summary.

        Returns:
            Dictionary with summary statistics
        """
        today = self.get_daily_stats()
        week_calls = self.get_recent_calls(hours=168)  # 7 days
        month_calls = self.get_recent_calls(hours=720)  # 30 days

        week_tokens = sum(c.tokens.total_tokens for c in week_calls)
        week_cost = sum(c.cost for c in week_calls)
        month_tokens = sum(c.tokens.total_tokens for c in month_calls)
        month_cost = sum(c.cost for c in month_calls)

        return {
            "today": {
                "tokens": today.total_tokens,
                "cost": today.total_cost,
                "calls": today.total_calls,
            },
            "week": {"tokens": week_tokens, "cost": week_cost, "calls": len(week_calls)},
            "month": {
                "tokens": month_tokens,
                "cost": month_cost,
                "calls": len(month_calls),
            },
        }

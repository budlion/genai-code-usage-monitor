"""Core data models for Codex Monitor."""

from datetime import datetime
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class Platform(str, Enum):
    """API platform types."""

    CODEX = "codex"
    CLAUDE = "claude"

    @property
    def display_name(self) -> str:
        """Get display name for the platform."""
        return {
            "codex": "Codex",
            "claude": "Claude",
        }[self.value]

    @property
    def theme_color(self) -> str:
        """Get primary theme color for the platform."""
        return {
            "codex": "cyan",
            "claude": "magenta",
        }[self.value]


class TokenUsage(BaseModel):
    """Token usage data model."""

    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)

    @field_validator("total_tokens", mode="before")
    @classmethod
    def validate_total(cls, v: int, info) -> int:
        """Validate that total equals prompt + completion."""
        if "prompt_tokens" in info.data and "completion_tokens" in info.data:
            return info.data["prompt_tokens"] + info.data["completion_tokens"]
        return v


class CachedTokenUsage(BaseModel):
    """Cached token usage data model."""

    cached_tokens: int = Field(default=0, ge=0, description="Number of cached tokens used")
    cache_hit_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Cache hit rate (0-1)")
    savings: float = Field(default=0.0, ge=0.0, description="Cost savings from cache in USD")

    @property
    def cache_hit_percentage(self) -> float:
        """Get cache hit rate as percentage."""
        return self.cache_hit_rate * 100


class AlertLevel(str, Enum):
    """Alert severity levels based on usage percentage."""

    INFO = "INFO"  # 50% usage
    WARNING = "WARNING"  # 75% usage
    CRITICAL = "CRITICAL"  # 90% usage
    DANGER = "DANGER"  # 95% usage

    @classmethod
    def from_usage_percentage(cls, percentage: float) -> "AlertLevel":
        """Determine alert level from usage percentage."""
        if percentage >= 95:
            return cls.DANGER
        elif percentage >= 90:
            return cls.CRITICAL
        elif percentage >= 75:
            return cls.WARNING
        elif percentage >= 50:
            return cls.INFO
        return cls.INFO

    @property
    def threshold(self) -> float:
        """Get the percentage threshold for this alert level."""
        thresholds = {
            "INFO": 50.0,
            "WARNING": 75.0,
            "CRITICAL": 90.0,
            "DANGER": 95.0,
        }
        return thresholds[self.value]

    @property
    def color_code(self) -> str:
        """Get ANSI color code for terminal display."""
        colors = {
            "INFO": "\033[94m",  # Blue
            "WARNING": "\033[93m",  # Yellow
            "CRITICAL": "\033[91m",  # Red
            "DANGER": "\033[95m",  # Magenta
        }
        return colors[self.value]


class Alert(BaseModel):
    """Alert notification model."""

    level: AlertLevel
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    severity: int = Field(ge=0, le=100, description="Severity score 0-100")
    metric_type: str = Field(default="usage", description="Type of metric (usage, cost, rate)")
    current_value: float = Field(ge=0.0, description="Current value of the metric")
    threshold_value: float = Field(ge=0.0, description="Threshold value that triggered the alert")
    recommended_action: Optional[str] = None

    @property
    def is_critical(self) -> bool:
        """Check if alert is critical or danger level."""
        return self.level in [AlertLevel.CRITICAL, AlertLevel.DANGER]

    @property
    def formatted_message(self) -> str:
        """Get formatted message with color coding."""
        reset = "\033[0m"
        return f"{self.level.color_code}[{self.level.value}]{reset} {self.message}"


class APICall(BaseModel):
    """Individual API call record."""

    timestamp: datetime
    model: str
    tokens: TokenUsage
    cost: float = Field(ge=0.0)
    request_id: Optional[str] = None
    status: str = "completed"
    error: Optional[str] = None
    cached_tokens: Optional[CachedTokenUsage] = None


class SessionData(BaseModel):
    """Session usage data."""

    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_tokens: int = Field(default=0, ge=0)
    total_cost: float = Field(default=0.0, ge=0.0)
    api_calls: List[APICall] = Field(default_factory=list)
    models_used: Dict[str, int] = Field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        """Check if session is still active."""
        return self.end_time is None

    @property
    def duration(self) -> Optional[float]:
        """Get session duration in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()


class UsageStats(BaseModel):
    """Aggregated usage statistics."""

    total_tokens: int = Field(default=0, ge=0)
    total_cost: float = Field(default=0.0, ge=0.0)
    total_calls: int = Field(default=0, ge=0)
    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    models: Dict[str, int] = Field(default_factory=dict)
    date: Optional[datetime] = None
    api_calls: List[APICall] = Field(default_factory=list)  # List of API calls for detailed analysis
    total_cached_tokens: int = Field(default=0, ge=0, description="Total cached tokens used")
    total_cache_savings: float = Field(default=0.0, ge=0.0, description="Total savings from cache")

    def update_from_call(self, call: APICall) -> None:
        """Update stats from an API call."""
        self.total_tokens += call.tokens.total_tokens
        self.total_cost += call.cost
        self.total_calls += 1
        self.prompt_tokens += call.tokens.prompt_tokens
        self.completion_tokens += call.tokens.completion_tokens

        if call.model in self.models:
            self.models[call.model] += call.tokens.total_tokens
        else:
            self.models[call.model] = call.tokens.total_tokens

        # Update cache statistics if available
        if call.cached_tokens:
            self.total_cached_tokens += call.cached_tokens.cached_tokens
            self.total_cache_savings += call.cached_tokens.savings

    @property
    def average_cache_hit_rate(self) -> float:
        """Calculate average cache hit rate across all calls."""
        if self.total_tokens == 0:
            return 0.0
        return self.total_cached_tokens / (self.total_tokens + self.total_cached_tokens)


class BurnRate(BaseModel):
    """Token burn rate analysis."""

    tokens_per_minute: float = Field(default=0.0, ge=0.0)
    cost_per_minute: float = Field(default=0.0, ge=0.0)
    calls_per_minute: float = Field(default=0.0, ge=0.0)
    estimated_time_to_limit: Optional[float] = None  # in minutes
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class P90Analysis(BaseModel):
    """P90 percentile analysis results."""

    p90_tokens: int = Field(ge=0)
    p90_cost: float = Field(ge=0.0)
    p90_calls: int = Field(ge=0)
    sample_size: int = Field(ge=0)
    time_window_hours: int = Field(ge=0)
    confidence: float = Field(ge=0.0, le=1.0)
    recommended_limit: Optional[int] = None


class PlanLimits(BaseModel):
    """Plan usage limits."""

    name: str
    token_limit: Optional[int] = None
    cost_limit: Optional[float] = None
    call_limit: Optional[int] = None
    rate_limit_rpm: Optional[int] = None  # requests per minute
    rate_limit_tpm: Optional[int] = None  # tokens per minute
    is_custom: bool = False


class MonitorState(BaseModel):
    """Current monitoring state."""

    current_session: Optional[SessionData] = None
    daily_stats: UsageStats = Field(default_factory=UsageStats)
    monthly_stats: UsageStats = Field(default_factory=UsageStats)
    burn_rate: BurnRate = Field(default_factory=BurnRate)
    p90_analysis: Optional[P90Analysis] = None
    plan_limits: PlanLimits
    last_update: datetime = Field(default_factory=datetime.now)
    platform: Platform = Field(default=Platform.CODEX)

    @property
    def token_usage_percentage(self) -> Optional[float]:
        """Calculate percentage of token limit used."""
        if self.plan_limits.token_limit:
            return (self.daily_stats.total_tokens / self.plan_limits.token_limit) * 100
        return None

    @property
    def cost_usage_percentage(self) -> Optional[float]:
        """Calculate percentage of cost limit used."""
        if self.plan_limits.cost_limit:
            return (self.daily_stats.total_cost / self.plan_limits.cost_limit) * 100
        return None


class MultiPlatformState(BaseModel):
    """Multi-platform monitoring state.

    Manages separate tracking for multiple AI platforms (Codex, Claude, etc.)
    with independent state management and data isolation. Each platform
    maintains its own MonitorState to prevent cross-platform contamination.

    Attributes:
        codex_state: MonitorState for OpenAI Codex/GPT platform
        claude_state: MonitorState for Anthropic Claude platform
        last_update: Timestamp of last state update
    """

    codex_state: Optional[MonitorState] = None
    claude_state: Optional[MonitorState] = None
    last_update: datetime = Field(default_factory=datetime.now)

    @property
    def active_platforms(self) -> List[str]:
        """Get list of active platform names."""
        platforms = []
        if self.codex_state:
            platforms.append("codex")
        if self.claude_state:
            platforms.append("claude")
        return platforms

    @property
    def total_cost(self) -> float:
        """Calculate total cost across all active platforms."""
        total = 0.0
        if self.codex_state:
            total += self.codex_state.daily_stats.total_cost
        if self.claude_state:
            total += self.claude_state.daily_stats.total_cost
        return total

    @property
    def total_tokens(self) -> int:
        """Calculate total tokens across all active platforms."""
        total = 0
        if self.codex_state:
            total += self.codex_state.daily_stats.total_tokens
        if self.claude_state:
            total += self.claude_state.daily_stats.total_tokens
        return total

    @property
    def all_alerts(self) -> List[Alert]:
        """Aggregate alerts from all platforms.

        This is a placeholder for future alert aggregation logic.
        Individual platforms should generate their own alerts based
        on their respective limits and usage patterns.
        """
        alerts = []
        # Future: Add alert generation logic per platform
        return alerts

    def get_state(self, platform: str) -> Optional[MonitorState]:
        """Get state for a specific platform.

        Args:
            platform: Platform name ("codex" or "claude")

        Returns:
            MonitorState for the platform, or None if not active
        """
        platform_lower = platform.lower()
        if platform_lower == "codex":
            return self.codex_state
        elif platform_lower == "claude":
            return self.claude_state
        return None

    def update_state(self, platform: str, state: MonitorState) -> None:
        """Update state for a specific platform.

        Args:
            platform: Platform name ("codex" or "claude")
            state: New MonitorState for the platform
        """
        platform_lower = platform.lower()
        if platform_lower == "codex":
            self.codex_state = state
        elif platform_lower == "claude":
            self.claude_state = state
        self.last_update = datetime.now()

    def has_platform(self, platform: str) -> bool:
        """Check if a platform is active.

        Args:
            platform: Platform name ("codex" or "claude")

        Returns:
            True if the platform is active, False otherwise
        """
        return self.get_state(platform) is not None

"""Time and timezone utilities."""

import sys
from datetime import datetime
from typing import Optional

import pytz


def get_system_timezone() -> str:
    """
    Detect system timezone.

    Returns:
        Timezone string
    """
    try:
        if sys.platform == "win32":
            import tzdata  # noqa: F401
        # Try to get local timezone
        local_tz = datetime.now().astimezone().tzinfo
        if local_tz and hasattr(local_tz, "zone"):
            return local_tz.zone
        return "UTC"
    except Exception:
        return "UTC"


def parse_timezone(tz_string: str) -> pytz.timezone:
    """
    Parse timezone string to timezone object.

    Args:
        tz_string: Timezone string (e.g., 'America/New_York', 'UTC')

    Returns:
        Timezone object

    Raises:
        ValueError: If timezone is invalid
    """
    if tz_string.lower() == "auto":
        tz_string = get_system_timezone()

    try:
        return pytz.timezone(tz_string)
    except pytz.UnknownTimeZoneError:
        raise ValueError(f"Unknown timezone: {tz_string}")


def format_datetime(
    dt: datetime, tz_string: str = "auto", time_format: str = "auto"
) -> str:
    """
    Format datetime according to timezone and format preferences.

    Args:
        dt: Datetime to format
        tz_string: Timezone string
        time_format: Time format ('12h', '24h', or 'auto')

    Returns:
        Formatted datetime string
    """
    # Convert to target timezone
    tz = parse_timezone(tz_string)
    local_dt = dt.astimezone(tz)

    # Determine time format
    if time_format == "auto":
        # Auto-detect based on system locale
        time_format = "24h"  # Default to 24h

    if time_format == "12h":
        return local_dt.strftime("%Y-%m-%d %I:%M:%S %p")
    else:
        return local_dt.strftime("%Y-%m-%d %H:%M:%S")


def get_time_until_reset(reset_hour: int = 0, tz_string: str = "auto") -> float:
    """
    Calculate seconds until the next reset time.

    Args:
        reset_hour: Hour of day for reset (0-23)
        tz_string: Timezone string

    Returns:
        Seconds until reset
    """
    tz = parse_timezone(tz_string)
    now = datetime.now(tz)

    # Calculate next reset time
    reset_time = now.replace(hour=reset_hour, minute=0, second=0, microsecond=0)

    if now >= reset_time:
        # Reset time has passed today, use tomorrow
        reset_time = reset_time.replace(day=reset_time.day + 1)

    return (reset_time - now).total_seconds()


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable form.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"

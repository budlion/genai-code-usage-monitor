"""Platform abstraction layer for multi-AI platform support.

This module provides a unified interface for different AI platforms
(OpenAI Codex, Claude Code, etc.) to enable consistent usage tracking
and cost calculation across platforms.
"""

from genai_code_usage_monitor.platforms.base import Platform
from genai_code_usage_monitor.platforms.codex import CodexPlatform
from genai_code_usage_monitor.platforms.claude import ClaudePlatform

__all__ = [
    "Platform",
    "CodexPlatform",
    "ClaudePlatform",
]

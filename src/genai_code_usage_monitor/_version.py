"""Version information for Codex Monitor."""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Version history
VERSION_HISTORY = {
    "1.0.0": {
        "date": "2025-01-27",
        "changes": [
            "Initial release",
            "Real-time monitoring with configurable refresh rates",
            "Multiple view modes (realtime, daily, monthly)",
            "ML-based P90 analysis and predictions",
            "Rich terminal UI with themes",
            "OpenAI API integration",
            "Configuration persistence",
            "Comprehensive test suite"
        ]
    }
}


def get_version() -> str:
    """Get the current version string."""
    return __version__


def get_version_info() -> tuple:
    """Get the version tuple."""
    return __version_info__


def print_version() -> None:
    """Print version information."""
    print(f"Codex Monitor v{__version__}")
    print(f"A real-time monitoring tool for OpenAI Codex/GPT API usage")


if __name__ == "__main__":
    print_version()

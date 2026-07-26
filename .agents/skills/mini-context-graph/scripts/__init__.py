"""Runtime initialization for the mini-context-graph package."""

from __future__ import annotations

import sys


def configure_console() -> None:
    """Make console output safe for Unicode on Windows and other platforms."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")


configure_console()


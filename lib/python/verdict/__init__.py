"""Verdict — The Atomic Unit of AI Judgment.

A transport library for creating, linking, resolving, and querying verdicts.
No model calls. No judgment. Just structured decision records.
"""

from verdict.core import create, link, resolve, supersede
from verdict.models import Verdict, AccuracyReport
from verdict.store import VerdictStore

__all__ = [
    "create",
    "link",
    "resolve",
    "supersede",
    "Verdict",
    "AccuracyReport",
    "VerdictStore",
]

"""nthlayer-learn (DEPRECATED) — superseded by nthlayer-workers (learn modules).

This package is deprecated as of v1.0.0 (2026-04-28). Functionality moved to
nthlayer-workers as part of the v1.5 tiered architecture consolidation.

Replacement: pip install nthlayer-workers

The learn functionality is now implemented as two worker modules in
nthlayer-workers:

  - LearnOutcomeModule (outcome resolution via the five paths: lineage,
    calibration sampling, downstream signal, score-outcome divergence, expiry)
  - LearnRetrospectiveModule (cursor-based retrospective generation from
    correlation_snapshot assessments)

The verdict data model that previously lived here was migrated into
nthlayer-common (`nthlayer_common.verdicts`); current code should import
from there.

Migration: https://github.com/rsionnach/nthlayer-learn
"""

import warnings as _warnings

_warnings.warn(
    "nthlayer-learn is deprecated. Functionality moved to nthlayer-workers "
    "as of v1.5 (LearnOutcomeModule, LearnRetrospectiveModule); the verdict "
    "model migrated into nthlayer-common.verdicts. "
    "Install: pip install nthlayer-workers. "
    "Migration: https://github.com/rsionnach/nthlayer-learn",
    DeprecationWarning,
    stacklevel=2,
)
del _warnings

from nthlayer_learn.core import create, link, resolve, supersede
from nthlayer_learn.models import AccuracyReport, Verdict
from nthlayer_learn.serialise import from_dict, from_json, to_dict, to_json
from nthlayer_learn.sqlite_store import SQLiteVerdictStore
from nthlayer_learn.store import AccuracyFilter, MemoryStore, VerdictFilter, VerdictStore

__all__ = [
    "create",
    "link",
    "resolve",
    "supersede",
    "Verdict",
    "AccuracyReport",
    "VerdictStore",
    "MemoryStore",
    "SQLiteVerdictStore",
    "VerdictFilter",
    "AccuracyFilter",
    "to_dict",
    "to_json",
    "from_dict",
    "from_json",
]

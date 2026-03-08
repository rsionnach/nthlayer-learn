"""Core verdict operations: create, link, resolve, supersede."""

from __future__ import annotations

import os
from datetime import datetime, timezone

from verdict.models import (
    GroundTruth,
    Judgment,
    Lineage,
    Metadata,
    Outcome,
    Override,
    Producer,
    Subject,
    Verdict,
)

_counter = 0


def _generate_id() -> str:
    """Generate a unique verdict ID."""
    global _counter
    _counter += 1
    now = datetime.now(timezone.utc)
    date_part = now.strftime("%Y-%m-%d")
    pid = os.getpid()
    return f"vrd-{date_part}-{pid:05d}-{_counter:05d}"


def create(
    subject: dict | Subject,
    judgment: dict | Judgment,
    producer: dict | Producer,
    metadata: dict | Metadata | None = None,
) -> Verdict:
    """Create a new verdict with a generated ID, current timestamp, and pending outcome."""
    if isinstance(subject, dict):
        subject = Subject(**subject)
    if isinstance(judgment, dict):
        judgment = Judgment(**judgment)
    if isinstance(producer, dict):
        producer = Producer(**producer)
    if metadata is None:
        metadata = Metadata()
    elif isinstance(metadata, dict):
        metadata = Metadata(**metadata)

    return Verdict(
        id=_generate_id(),
        version=1,
        timestamp=datetime.now(timezone.utc),
        producer=producer,
        subject=subject,
        judgment=judgment,
        outcome=Outcome(),
        lineage=Lineage(),
        metadata=metadata,
    )


def link(
    verdict: Verdict,
    parent: str | None = None,
    context: list[str] | None = None,
) -> Verdict:
    """Set lineage fields on a verdict."""
    if parent is not None:
        verdict.lineage.parent = parent
    if context is not None:
        verdict.lineage.context = context
    return verdict


def resolve(
    verdict: Verdict,
    status: str,
    override: dict | Override | None = None,
    ground_truth: dict | GroundTruth | None = None,
    resolution: str | None = None,
) -> Verdict:
    """Update the outcome phase. Transitions status from pending to the resolved state."""
    valid_statuses = {"confirmed", "overridden", "partial", "superseded", "expired"}
    if status not in valid_statuses:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {valid_statuses}")

    if verdict.outcome.status != "pending":
        raise ValueError(
            f"Cannot resolve verdict {verdict.id}: "
            f"status is '{verdict.outcome.status}', expected 'pending'"
        )

    verdict.outcome.status = status
    verdict.outcome.closed_at = datetime.now(timezone.utc)

    if resolution is not None:
        verdict.outcome.resolution = resolution

    if override is not None:
        if isinstance(override, dict):
            override = Override(**override)
        override.at = override.at or datetime.now(timezone.utc)
        verdict.outcome.override = override

    if ground_truth is not None:
        if isinstance(ground_truth, dict):
            ground_truth = GroundTruth(**ground_truth)
        verdict.outcome.ground_truth = ground_truth

    return verdict


def supersede(old_verdict: Verdict, new_verdict: Verdict) -> tuple[Verdict, Verdict]:
    """Mark old_verdict as superseded, set new_verdict as the replacement."""
    old_verdict = resolve(old_verdict, status="superseded")
    new_verdict.lineage.parent = old_verdict.id
    return old_verdict, new_verdict

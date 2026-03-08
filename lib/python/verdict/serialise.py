"""Serialisation for verdicts: JSON and YAML."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from typing import Any

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


def _serialise_value(v: Any) -> Any:
    if isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, dict):
        return {k: _serialise_value(val) for k, val in v.items()}
    if isinstance(v, list):
        return [_serialise_value(item) for item in v]
    return v


def to_dict(verdict: Verdict) -> dict:
    """Convert a verdict to a plain dict suitable for JSON/YAML serialisation."""
    d = asdict(verdict)
    return _serialise_value(d)


def to_json(verdict: Verdict, indent: int = 2) -> str:
    """Serialise a verdict to JSON."""
    return json.dumps(to_dict(verdict), indent=indent)


def from_dict(data: dict) -> Verdict:
    """Reconstruct a verdict from a plain dict."""

    def parse_dt(v: str | None) -> datetime | None:
        if v is None:
            return None
        return datetime.fromisoformat(v)

    p = data["producer"]
    producer = Producer(
        system=p["system"],
        instance=p.get("instance"),
        model=p.get("model"),
        prompt_version=p.get("prompt_version"),
    )

    s = data["subject"]
    subject = Subject(
        type=s["type"],
        ref=s["ref"],
        summary=s["summary"],
        agent=s.get("agent"),
        service=s.get("service"),
        environment=s.get("environment"),
        content_hash=s.get("content_hash"),
    )

    j = data["judgment"]
    judgment = Judgment(
        action=j["action"],
        confidence=j["confidence"],
        score=j.get("score"),
        dimensions=j.get("dimensions"),
        reasoning=j.get("reasoning"),
        tags=j.get("tags"),
    )

    o = data.get("outcome", {})
    ov = o.get("override") or {}
    gt = o.get("ground_truth") or {}
    outcome = Outcome(
        status=o.get("status", "pending"),
        resolution=o.get("resolution"),
        override=Override(
            by=ov.get("by"),
            at=parse_dt(ov.get("at")),
            action=ov.get("action"),
            reasoning=ov.get("reasoning"),
        ) if ov else None,
        ground_truth=GroundTruth(
            signal=gt.get("signal"),
            value=gt.get("value"),
            detected_at=parse_dt(gt.get("detected_at")),
        ) if gt else None,
        closed_at=parse_dt(o.get("closed_at")),
    )

    lin = data.get("lineage", {})
    lineage = Lineage(
        parent=lin.get("parent"),
        children=lin.get("children", []),
        context=lin.get("context", []),
    )

    m = data.get("metadata", {})
    metadata = Metadata(
        cost_tokens=m.get("cost_tokens"),
        cost_currency=m.get("cost_currency"),
        latency_ms=m.get("latency_ms"),
        ttl=m.get("ttl", 7776000),
        custom=m.get("custom", {}),
    )

    return Verdict(
        id=data["id"],
        version=data["version"],
        timestamp=parse_dt(data["timestamp"]),
        producer=producer,
        subject=subject,
        judgment=judgment,
        outcome=outcome,
        lineage=lineage,
        metadata=metadata,
    )


def from_json(s: str) -> Verdict:
    """Deserialise a verdict from JSON."""
    return from_dict(json.loads(s))

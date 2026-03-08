"""Verdict data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Producer:
    system: str
    instance: str | None = None
    model: str | None = None
    prompt_version: str | None = None


@dataclass
class Subject:
    type: str
    ref: str
    summary: str
    agent: str | None = None
    service: str | None = None
    environment: str | None = None
    content_hash: str | None = None


@dataclass
class Judgment:
    action: str
    confidence: float
    score: float | None = None
    dimensions: dict[str, float] | None = None
    reasoning: str | None = None
    tags: list[str] | None = None


@dataclass
class Override:
    by: str | None = None
    at: datetime | None = None
    action: str | None = None
    reasoning: str | None = None


@dataclass
class GroundTruth:
    signal: str | None = None
    value: str | None = None
    detected_at: datetime | None = None


@dataclass
class Outcome:
    status: str = "pending"
    resolution: str | None = None
    override: Override | None = None
    ground_truth: GroundTruth | None = None
    closed_at: datetime | None = None


@dataclass
class Lineage:
    parent: str | None = None
    children: list[str] = field(default_factory=list)
    context: list[str] = field(default_factory=list)


@dataclass
class Metadata:
    cost_tokens: int | None = None
    cost_currency: float | None = None
    latency_ms: int | None = None
    ttl: int = 7776000  # 90 days
    custom: dict[str, Any] = field(default_factory=dict)


@dataclass
class Verdict:
    id: str
    version: int
    timestamp: datetime
    producer: Producer
    subject: Subject
    judgment: Judgment
    outcome: Outcome = field(default_factory=Outcome)
    lineage: Lineage = field(default_factory=Lineage)
    metadata: Metadata = field(default_factory=Metadata)


@dataclass
class AccuracyReport:
    producer: str
    total: int
    total_resolved: int
    confirmation_rate: float
    override_rate: float
    partial_rate: float
    pending_rate: float
    mean_confidence_on_correct: float
    mean_confidence_on_incorrect: float
    calibration_gap: float
    dimension: str | None = None

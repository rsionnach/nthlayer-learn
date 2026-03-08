"""Verdict store interface and query operations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from verdict.models import AccuracyReport, Outcome, Verdict


@dataclass
class VerdictFilter:
    producer_system: str | None = None
    subject_type: str | None = None
    subject_agent: str | None = None
    subject_service: str | None = None
    status: str | None = None
    tags: list[str] | None = None
    from_time: datetime | None = None
    to_time: datetime | None = None
    limit: int = 100


@dataclass
class AccuracyFilter:
    producer_system: str
    from_time: datetime | None = None
    to_time: datetime | None = None
    dimension: str | None = None


class VerdictStore(ABC):
    """Abstract interface for verdict storage."""

    @abstractmethod
    def put(self, verdict: Verdict) -> None:
        """Store a verdict."""

    @abstractmethod
    def get(self, id: str) -> Verdict | None:
        """Retrieve a verdict by ID."""

    @abstractmethod
    def query(self, filter: VerdictFilter) -> list[Verdict]:
        """Query verdicts matching a filter."""

    @abstractmethod
    def update_outcome(self, id: str, outcome: Outcome) -> Verdict:
        """Update a verdict's outcome."""

    @abstractmethod
    def accuracy(self, filter: AccuracyFilter) -> AccuracyReport:
        """Compute accuracy metrics from resolved verdicts."""

    @abstractmethod
    def expire(self, before: datetime) -> int:
        """Expire pending verdicts older than the given timestamp. Returns count expired."""


@dataclass
class MemoryStore(VerdictStore):
    """In-memory verdict store for testing and development."""

    _verdicts: dict[str, Verdict] = field(default_factory=dict)

    def put(self, verdict: Verdict) -> None:
        self._verdicts[verdict.id] = verdict

    def get(self, id: str) -> Verdict | None:
        return self._verdicts.get(id)

    def query(self, filter: VerdictFilter) -> list[Verdict]:
        results = list(self._verdicts.values())

        if filter.producer_system:
            results = [v for v in results if v.producer.system == filter.producer_system]
        if filter.subject_type:
            results = [v for v in results if v.subject.type == filter.subject_type]
        if filter.subject_agent:
            results = [v for v in results if v.subject.agent == filter.subject_agent]
        if filter.subject_service:
            results = [v for v in results if v.subject.service == filter.subject_service]
        if filter.status:
            results = [v for v in results if v.outcome.status == filter.status]
        if filter.tags:
            results = [
                v for v in results
                if v.judgment.tags and set(filter.tags) & set(v.judgment.tags)
            ]
        if filter.from_time:
            results = [v for v in results if v.timestamp >= filter.from_time]
        if filter.to_time:
            results = [v for v in results if v.timestamp <= filter.to_time]

        results.sort(key=lambda v: v.timestamp, reverse=True)
        return results[: filter.limit]

    def update_outcome(self, id: str, outcome: Outcome) -> Verdict:
        verdict = self._verdicts.get(id)
        if verdict is None:
            raise KeyError(f"Verdict {id} not found")
        verdict.outcome = outcome
        return verdict

    def accuracy(self, filter: AccuracyFilter) -> AccuracyReport:
        verdicts = self.query(
            VerdictFilter(
                producer_system=filter.producer_system,
                from_time=filter.from_time,
                to_time=filter.to_time,
            )
        )

        total = len(verdicts)
        confirmed = [v for v in verdicts if v.outcome.status == "confirmed"]
        overridden = [v for v in verdicts if v.outcome.status == "overridden"]
        partial = [v for v in verdicts if v.outcome.status == "partial"]
        pending = [v for v in verdicts if v.outcome.status == "pending"]

        total_resolved = len(confirmed) + len(overridden) + len(partial)

        def safe_div(a: float, b: float) -> float:
            return a / b if b > 0 else 0.0

        def mean_confidence(vs: list[Verdict]) -> float:
            if not vs:
                return 0.0
            return sum(v.judgment.confidence for v in vs) / len(vs)

        confirmation_rate = safe_div(len(confirmed), len(confirmed) + len(overridden))
        override_rate = safe_div(len(overridden), len(confirmed) + len(overridden))

        mean_conf_correct = mean_confidence(confirmed)
        mean_conf_incorrect = mean_confidence(overridden)

        return AccuracyReport(
            producer=filter.producer_system,
            total=total,
            total_resolved=total_resolved,
            confirmation_rate=confirmation_rate,
            override_rate=override_rate,
            partial_rate=safe_div(len(partial), total_resolved),
            pending_rate=safe_div(len(pending), total),
            mean_confidence_on_correct=mean_conf_correct,
            mean_confidence_on_incorrect=mean_conf_incorrect,
            calibration_gap=abs(mean_conf_correct - confirmation_rate),
            dimension=filter.dimension,
        )

    def expire(self, before: datetime) -> int:
        count = 0
        for verdict in self._verdicts.values():
            if verdict.outcome.status == "pending" and verdict.timestamp < before:
                verdict.outcome.status = "expired"
                count += 1
        return count

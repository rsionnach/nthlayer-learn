# Verdict — The Atomic Unit of AI Judgment

Verdicts are structured records of AI decisions. They capture what was evaluated, what the AI decided, how confident it was, and — critically — whether the decision turned out to be correct.

Any system where an AI makes a decision (approving code, correlating signals, triaging incidents, moderating content, generating recommendations) can emit verdicts. Any system that wants to measure whether those decisions were correct can consume them.

Verdicts are independent of the [OpenSRM](https://github.com/robfox/opensrm-ecosystem) ecosystem, independent of any specific agent framework, and independent of any specific model provider.

## The Three Phases

Every verdict has three phases:

1. **Judgment** (filled at decision time): what was the input, what did the AI decide, why, and how confident is it?
2. **Outcome** (filled later): was the decision confirmed, overridden by a human, or contradicted by downstream evidence?
3. **Lineage** (optional): which other verdicts informed this one, and which verdicts does this one inform?

The outcome phase is what makes verdicts powerful. Most AI systems record their decisions but never close the loop on whether those decisions were right. Verdicts make the loop explicit and queryable.

## Quick Start

### Install

```bash
pip install verdict
```

### Create a verdict

```python
from verdict import create, resolve

# Record a judgment
v = create(
    subject={"type": "review", "ref": "git:abc123", "summary": "Auth middleware change"},
    judgment={"action": "approve", "confidence": 0.82, "reasoning": "Auth check is sound"},
    producer={"system": "my-reviewer", "model": "claude-sonnet-4-20250514"},
)

# Later, when you know if the decision was right
v = resolve(v, status="confirmed")
```

### Measure accuracy

```bash
verdict accuracy --producer my-reviewer --window 30d
```

### Replay historical decisions

```bash
verdict replay --producer my-reviewer --from 2026-02-01 --to 2026-03-01
```

## Schema

See [SPEC.md](SPEC.md) for the full schema specification, or [schema/verdict.json](schema/verdict.json) for the JSON Schema.

## Why Verdicts?

**If your AI makes decisions and you want to know whether those decisions are good, emit verdicts.** You get:

- **Replay**: Regression-test your judgment quality against historical inputs
- **Calibration**: Measure accuracy over time, detect confidence drift
- **Gaming detection**: Find agents whose high scores don't match real outcomes
- **Human feedback loop**: Let people confirm or override, and track the results
- **Lineage**: Trace how one decision influenced another across components

No framework required. No ecosystem required. Just a schema and a small library.

## Storage

| Tier | Store | Use Case |
|------|-------|----------|
| Tier 1 | SQLite | Single file, zero dependencies. Default. |
| Tier 2 | PostgreSQL | Concurrent access, full-text search, real-time consumption. |
| Tier 3 | ClickHouse | Analytics over millions of verdicts. |
| Any | Git | Evaluation datasets (curated verdicts with known outcomes). |

## Project Structure

```
verdict/
├── SPEC.md                      # Full schema specification
├── schema/                      # JSON Schema and annotated examples
├── conventions/                 # OTel semantic conventions
├── lib/                         # Transport libraries (Python, Go, TypeScript)
├── stores/                      # Storage implementations
├── cli/                         # CLI tools
└── eval/                        # Example evaluation datasets
```

## License

Apache 2.0

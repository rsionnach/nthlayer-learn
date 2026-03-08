# OTel Metric Semantic Conventions for Verdicts

Verdicts are the source records from which these metrics are computed. They flow into Prometheus via OTel Collector.

## Metrics

| Metric Name | Type | Labels | Derived From |
|------------|------|--------|-------------|
| `gen_ai_decision_total` | counter | system, agent, dimension, environment | Count of `verdict.create()` calls |
| `gen_ai_decision_score` | gauge | system, agent, dimension, environment | `verdict.judgment.score` |
| `gen_ai_decision_confidence` | gauge | system, agent, environment | `verdict.judgment.confidence` |
| `gen_ai_override_reversal_total` | counter | system, agent, environment | Count of `verdict.resolve(status: overridden)` calls |
| `gen_ai_override_correction_total` | counter | system, agent, environment | Count of `verdict.resolve(status: partial)` calls |
| `gen_ai_decision_cost_tokens` | counter | system, agent, environment | `verdict.metadata.cost_tokens` |
| `gen_ai_decision_cost_currency` | gauge | system, agent, environment | `verdict.metadata.cost_currency` |

## Labels

- **system**: The `verdict.producer.system` value (e.g., "arbiter", "sitrep", "mayday")
- **agent**: The `verdict.subject.agent` value (e.g., "code-reviewer", "triage-agent")
- **dimension**: The quality dimension name from `verdict.judgment.dimensions` (e.g., "correctness", "safety")
- **environment**: The `verdict.subject.environment` value (e.g., "production", "staging")

## Relationship to NthLayer

NthLayer queries these metrics from Prometheus to generate judgment SLO recording rules and deploy gates. The metrics are standard `gen_ai_*` OTel metrics. NthLayer doesn't know or care that they originate from verdicts.

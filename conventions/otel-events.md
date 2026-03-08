# OTel Event Semantic Conventions for Verdicts

## Events

| OTel Event Name | When Emitted | Trigger |
|----------------|--------------|---------|
| `gen_ai.decision.created` | When a verdict is produced | `verdict.create()` |
| `gen_ai.override.recorded` | When a human overrides a verdict | `verdict.resolve(status: overridden)` |
| `gen_ai.decision.confirmed` | When a verdict is confirmed correct | `verdict.resolve(status: confirmed)` |

## Attribute Mapping

| Verdict Field | OTel Attribute | Notes |
|--------------|----------------|-------|
| `verdict.id` | `gen_ai.decision.id` | Unique decision identifier |
| `verdict.producer.system` | `gen_ai.system` | Which system produced the judgment |
| `verdict.producer.model` | `gen_ai.request.model` | Which model was used |
| `verdict.subject.agent` | `gen_ai.decision.agent` | The agent being evaluated |
| `verdict.subject.service` | `service.name` | Standard OTel service identifier |
| `verdict.judgment.action` | `gen_ai.decision.action` | approve, reject, flag, etc. |
| `verdict.judgment.score` | `gen_ai.decision.score` | Quality score 0.0-1.0 |
| `verdict.judgment.confidence` | `gen_ai.decision.confidence` | Producer confidence 0.0-1.0 |
| `verdict.metadata.cost_tokens` | `gen_ai.usage.input_tokens` + `gen_ai.usage.output_tokens` | Token consumption |
| `verdict.outcome.override.by` | `gen_ai.override.actor` | Who overrode |
| `verdict.outcome.override.action` | `gen_ai.override.action` | What the override changed |
| `verdict.outcome.override.reasoning` | `gen_ai.override.reasoning` | Why the override happened |

## Non-gen-AI Use Cases

For systems using verdicts outside of generative AI contexts (traditional ML classifiers, rule-based systems with human review, manual decision tracking), the verdict library can emit OTel events using a `decision.*` namespace or custom attributes. The verdict schema is the same regardless of namespace. The OTel mapping is configured per-producer based on context.

The default mapping uses `gen_ai.*` because that aligns with the OTel community's semantic conventions for generative AI systems.

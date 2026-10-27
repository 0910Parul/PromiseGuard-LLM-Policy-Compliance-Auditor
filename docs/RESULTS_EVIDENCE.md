# Results Evidence and Prototype Boundaries

This review inspects the source, fixtures, tests, and project documents. The live Ollama model was not run, and no stored test-run output was found.

| Claim | Source and scope |
|---|---|
| Default model and local client | [ollama_client.py](../backend/ollama_client.py): `llama3.1:8b`, Ollama client, temperature 0, timeout, and retries; actual host follows the client configuration |
| Structured extraction | [promise_extraction.py](../backend/promise_extraction.py): Pydantic schema, representative-only extraction, filler exclusions, and commitment deduplication instructions |
| Whole-policy comparison | [policy_matcher.py](../backend/policy_matcher.py): returns `policy_text` unchanged; no selective retrieval or embeddings |
| Three verdicts and schema ordering | [compliance_checker.py](../backend/compliance_checker.py): rationale, matched clause, verdict enum |
| One-transcript UI and JSON export | [app.py](../frontend/app.py): text policy/transcript selection, verdict filtering, report download |
| Test coverage | [test_pipeline.py](../tests/test_pipeline.py): 3 clean, 4 violation, 3 ambiguous fixtures; category assertions against a real model |
| Batch inspection | [evaluate.py](../backend/evaluate.py): transcript loop and printed reports, without automatic ground-truth scoring |
| Historical all-10 success claim | Original README reports a final successful run. The business plan describes testing on the suite; no saved execution log independently demonstrates a 10/10 run |
| Development findings and commercial scenarios | [Business plan](PromiseGuard_Business_Plan_Final.docx), technical approach, pricing, market sizing, and prototype appendix |

## Interpretation boundaries

- Category-level invariants do not establish per-promise accuracy, extraction recall, citation validity, or generalization beyond the ten synthetic transcripts.
- A clean transcript can satisfy the test even with an empty promise list. The checks do not require every true promise to be extracted.
- Pydantic validates field types and verdict values. Generated clause content and rationales still require review against the policy.
- The prompts and schema implement the documented design choices; their existence is not evidence of a measured causal improvement. The development observations were not a controlled benchmark.
- Local inference avoids sending prompts to a cloud LLM in the default local setup. It is not a certification or guarantee about every deployment's networking, logging, or host configuration.
- The UI accepts policy markdown/text and transcript text, one transcript at a time. PDF parsing, a deployed service API, continuous monitoring, and embeddings retrieval are not implemented.
- The project plan contains roadmap language. Current behavior is established from code rather than checklist completion or proposed architecture.
- Commercial figures are scenarios: $1,200 revenue less an assumed $150 serving cost implies 87.5% gross margin; 30,000 assumed firms at $3,000 annually implies $90M. These are not validated operating metrics or market facts.

This documentation update changes no application code, tests, policy text, transcripts, or business-plan documents.

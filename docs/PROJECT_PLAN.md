# PromiseGuard — Project Plan

## 1. Concept
An internal ops tool that audits sales/support communications against a company's
actual policy documents to catch unauthorized promises before they cause margin
leakage, refunds, or escalations.

**Example:** A support rep tells a customer "I can waive that fee for you" — but
company policy only allows fee waivers under specific conditions. PromiseGuard
flags this mismatch automatically, with the exact policy clause cited.

## 2. Why LLM (not rules/keyword matching)
Promises are expressed in natural, varied language ("I'll take care of that for
you," "don't worry, we'll sort the billing out," "I can get you the enterprise
rate"). Detecting these AND semantically comparing them against policy conditions
requires real language understanding — a keyword filter would miss most real
cases and false-flag many harmless ones.

## 3. System Architecture

```
User uploads:
  - Policy document (PDF/text)
  - Communication transcript (text) [call transcript, support chat log, or email thread]
        |
        v
[1] Promise Extraction
    - LLM scans transcript, extracts candidate promise/commitment statements
    - Output: list of {statement, speaker, context}
        |
        v
[2] Policy Retrieval
    - Relevant policy sections retrieved for each candidate promise
    - (simple retrieval to start; can upgrade to embeddings-based if time allows)
        |
        v
[3] Compliance Comparison
    - LLM compares each promise against relevant policy language
    - Output: {promise, policy_match, verdict: compliant/violation/ambiguous, rationale}
        |
        v
[4] Report Generation
    - Streamlit UI displays flagged items, severity, rationale
    - Exportable summary report
```

## 4. Tech Stack (all free)
- **LLM runtime:** Ollama (local) — Llama 3.1 8B primary, Mistral 7B fallback
- **Backend:** Python (`backend/` package: extraction, policy matching, compliance
  checking, pipeline orchestration)
- **Frontend:** Streamlit, calling the backend functions directly in-process
- **No cloud, no paid APIs, no external dependencies at runtime**

FastAPI was in the original plan as a separate backend service but was dropped:
the MVP only ever has one frontend process talking to one backend, so a network
API layer between them adds nothing except surface area to build and maintain.
If PromiseGuard grows a second consumer of the backend (e.g. a CLI, a scheduled
batch job, or a second UI), reintroducing a thin FastAPI layer around
`backend/pipeline.py` would be the natural next step.

## 5. Data Plan
No public dataset exists for this (real company data is private/sensitive).
Plan: hand-crafted + LLM-assisted synthetic data:
  - 1 realistic company policy doc (SaaS company, customer support context)
  - 8-10 varied synthetic transcripts (mix of clean calls, clear violations,
    ambiguous edge cases, different rep personas/tones)

## 6. Build Milestones
1. [ ] Synthetic data generation (policy doc + transcript set)
2. [ ] Core pipeline (extraction + comparison logic, tested against synthetic data)
3. [ ] Streamlit front-end (upload, run, view report)
4. [ ] Business plan document (all 6 components)
5. [ ] Polish + write-up (design rationale, what worked/didn't, local-model tradeoff discussion)

## 7. Business Plan Components (to complete)
- [ ] Value proposition
- [ ] Product design / UX rationale
- [ ] Pricing model
- [ ] Target user & market size
- [ ] Competitor landscape (Gong, Observe.AI, Enthu.ai as anchors)
- [ ] Go-to-market notes

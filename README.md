# PromiseGuard: Auditing Sales & Support Promises Against Company Policy with a Local LLM

This project builds an **NLP compliance auditor** that reads sales and customer-support transcripts, extracts every commitment a rep made ("I can waive that fee for you"), and checks it against the company's actual policy document — returning a **compliant / violation / ambiguous** verdict with the **cited policy clause** and a plain-language rationale. It runs **100% locally on Llama 3.1 8B via Ollama** (no cloud, no paid APIs), and correctly classified **all 10 test transcripts** in the final regression run. Built for **MSBA 6461 — Large Language Models** (Carlson, University of Minnesota).

## 🔍 Project Goals

- Catch unauthorized promises (unapproved fee waivers, out-of-window refunds, price locks, unreleased-feature dates) **before** they turn into refunds, escalations, or margin leakage.
- Ground every flag in **specific policy language**, so a manager can verify the call instead of trusting a black box.
- Keep sensitive customer transcripts on-premise with a **local-only LLM architecture**, and frame the tool as a viable B2B product.

## 📄 Files Included

- **`backend/`** — the NLP pipeline:
  - `promise_extraction.py` — LLM extracts candidate promises as structured JSON (`statement`, `speaker`, `context`).
  - `policy_matcher.py` — retrieves the relevant policy section for each promise.
  - `compliance_checker.py` — LLM compares promise vs. policy → verdict, matched clause, rationale.
  - `pipeline.py` — end-to-end orchestration with Pydantic-validated outputs.
  - `ollama_client.py` — local model wrapper with retries; `evaluate.py` — batch evaluation script.
- **`frontend/app.py`** — Streamlit app: upload a policy + transcript, run the audit, review color-coded flags.
- **`tests/test_pipeline.py`** — pytest regression suite run against the **live model** (no mocks) to catch prompt/schema regressions.
- **`data/`** — a SaaS company policy handbook and **10 synthetic transcripts** (3 clean, 4 violation, 3 ambiguous) across calls and chats.
- **`docs/PromiseGuard_Business_Plan_Final.docx`** — productization plan: value proposition, pricing, market sizing, competitors, go-to-market.
- **`docs/PROJECT_PLAN.md`** — architecture and design rationale.
- **`requirements.txt`** — Python dependencies.

## 🧪 Methods Used

- **LLM information extraction** of commitments from unstructured conversational text, with structured JSON outputs.
- **Policy retrieval + LLM-based semantic comparison** against conditional, natural-language rules (e.g., "one fee waiver per 12 months, accounts in good standing only").
- **Prompt and output-schema engineering** — field ordering, filler-phrase exclusion, and grounding constraints to reduce circular or hallucinated rationales.
- **Evaluation design:** a labeled synthetic test suite covering clean, violation, and ambiguous cases, with category-level pytest assertions re-run after every prompt change.
- Product strategy: tiered per-agent pricing, TAM/SAM/SOM sizing, and competitive positioning vs. Gong, Observe.AI, and Enthu.ai.

## 📈 Key Findings

- The final pipeline classified **all 10 synthetic transcripts correctly** at the category level — no violations flagged on clean calls, at least one violation caught in every violation transcript, and borderline language routed to *ambiguous* rather than over-flagged.
- **Output schema order affects quality:** asking for the *rationale before the verdict* produced more coherent, policy-grounded classifications — especially on ambiguous cases.
- Validation caught **circular reasoning** on compliant verdicts (the rationale simply restated the rep's words); the prompt was revised to require a policy citation or an explicit "no clause applies."
- **Fixes can create new failures:** an over-strict citation requirement caused the model to fabricate a policy clause and flip a true violation to compliant — reinforcing the practice of re-validating the full test set after every prompt change.
- Business case (illustrative planning scenario): per-agent pricing at **$12/agent/month**, an estimated **~87% gross margin** enabled by local inference, and a **$90M** serviceable market among U.S. mid-market B2B SaaS companies.

## 🛠 Technologies

- Python, Pydantic
- Ollama + **Llama 3.1 8B** (local LLM inference)
- Streamlit (front end)
- pytest (live-model regression testing)
- Prompt engineering & structured LLM outputs

## 🚀 How to Run

```bash
ollama pull llama3.1:8b             # install Ollama first: https://ollama.com/download
pip install -r requirements.txt
streamlit run frontend/app.py       # opens at http://localhost:8501
```

Upload `data/policies/company_policy.md` and any transcript from `data/transcripts/`, then run the analysis. Run the tests with `pytest` (requires the Ollama server running).

## ✅ Outcome

A working, privacy-preserving prototype that gives Revenue and Support Ops leaders **clause-level visibility into risky promises** buried in everyday conversations — with every flag explained and cited for human review — plus a product plan for taking it to market as a B2B SaaS tool.

---

By **Parul Chaudhary** · [LinkedIn](https://www.linkedin.com/in/parulchaud) · [Email](mailto:parul.jaswant@gmail.com)

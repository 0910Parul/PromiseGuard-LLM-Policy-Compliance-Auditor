# PromiseGuard: LLM-Powered Policy Compliance Auditing

## Project Overview

PromiseGuard is a local prototype for reviewing commitments in sales and customer-support transcripts against a company's policy handbook. It extracts representative promises, compares them with policy, and returns a **compliant**, **violation**, or **ambiguous** verdict with a clause reference and rationale for human review.

The business objective is to help Revenue and Support Operations teams identify promises that may lead to concessions, escalations, or unmet expectations. The application uses **Llama 3.1 8B through Ollama**, with a Streamlit interface and a Python pipeline.

## Key Highlights

- **Reviewable outputs:** each extracted promise includes its speaker, context, verdict, policy-clause field, and rationale.
- **Local inference by default:** the configured model runs through a local Ollama server without a paid cloud LLM API.
- **Evaluation coverage:** **10 synthetic transcripts** spanning 3 clean, 4 violation, and 3 ambiguous cases.
- **Usable prototype:** choose demo files or upload a policy and transcript, filter verdicts, and download the resulting JSON report.
- **Business analysis:** a separate product plan develops buyer needs, proposed pricing, market-sizing scenarios, and pilot objectives.

Start with the [pipeline](backend/pipeline.py), [regression suite](tests/test_pipeline.py), or [results evidence](docs/RESULTS_EVIDENCE.md).

## Technical Implementation

| Stage | Current implementation |
|---|---|
| Promise extraction | LLM extracts representative commitments, speaker, and surrounding context into Pydantic-validated JSON; prompts exclude noncommittal filler and merge repeated commitments |
| Policy context | `policy_matcher.py` passes the **full policy document** to the comparison step; selective or embedding-based retrieval is a possible extension |
| Compliance comparison | LLM compares each promise with policy and transcript facts, returning a rationale, clause reference, and one of three verdicts |
| Validation and orchestration | Pydantic schemas validate output structure; the pipeline combines extraction and comparison results into a report |
| Review interface | Streamlit supports one transcript per analysis, verdict filters, source preview, and JSON export |
| Batch inspection and testing | `backend.evaluate` loops over transcript files; pytest checks category-level behavior against the live local model |

The compliance schema places the rationale before the verdict. Development documentation describes improved output coherence with that ordering; a controlled study of the effect has not been performed.

## Methods & Technologies

- **Python:** pipeline orchestration and structured data handling with Pydantic.
- **LLM application:** Ollama, Llama 3.1 8B, prompt design, JSON schemas, and conditional policy comparison.
- **Interface:** Streamlit, including local text-file upload and downloadable reports.
- **Evaluation:** pytest integration checks using a live Ollama model, plus synthetic policy/transcript fixtures.

## Results & Insights

| Evidence | What it establishes |
|---|---|
| 3 clean transcripts | Tests assert that no `violation` verdict is returned |
| 4 violation transcripts | Tests require at least one `violation` per transcript |
| 3 ambiguous transcripts | Tests require at least one `ambiguous` verdict and no `violation` |
| Pydantic output models | Structural validation of extracted promises and report fields |
| Business plan | Documented development observations, product concept, and commercial assumptions |

The original README reports a final run that satisfied the checks for all 10 transcripts. The repository does not include a saved test-run log, and the live model was not rerun for this documentation update. This remains a **reported development result**, rather than an independently verified accuracy benchmark. Category-level assertions also do not measure the correctness or completeness of every extracted promise and citation.

Development observations include circular compliant rationales and a prompt change that introduced an incorrect policy citation. These findings motivate full-suite regression checks and human verification of generated claims. Schema validation checks structure; it does not establish factual correctness.

### Business planning scope

The [business plan](docs/PromiseGuard_Business_Plan_Final.docx) proposes pricing tiers and illustrates a Growth-tier scenario of **100 agents × $12/month = $1,200 monthly revenue**, with an assumed $150 serving cost giving approximately **87.5% gross margin**. Its **$90M serviceable-market scenario** assumes 30,000 firms at $3,000 annual contract value. These are planning assumptions, not observed revenue, validated costs, or independently sourced market estimates.

## Repository Structure

| Path | Purpose |
|---|---|
| [backend/promise_extraction.py](backend/promise_extraction.py) | Candidate commitment extraction |
| [backend/policy_matcher.py](backend/policy_matcher.py) | Full-policy context adapter |
| [backend/compliance_checker.py](backend/compliance_checker.py) | Policy comparison prompts and verdict schema |
| [backend/pipeline.py](backend/pipeline.py) | Report models and end-to-end orchestration |
| [backend/ollama_client.py](backend/ollama_client.py) | Model settings, timeout, and retry wrapper |
| [backend/evaluate.py](backend/evaluate.py) | Batch transcript inspection |
| [frontend/app.py](frontend/app.py) | Streamlit review interface |
| [tests/test_pipeline.py](tests/test_pipeline.py) | Live-model category-level regression checks |
| [data/policies](data/policies/) and [data/transcripts](data/transcripts/) | Demo handbook and 10 synthetic transcripts |
| [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md) | Design rationale and roadmap context |
| [docs/PromiseGuard_Business_Plan_Final.docx](docs/PromiseGuard_Business_Plan_Final.docx) | Productization plan and assumptions |
| [docs/RESULTS_EVIDENCE.md](docs/RESULTS_EVIDENCE.md) | Evidence sources and evaluation limits |
| [requirements.txt](requirements.txt) | Pinned Python dependencies |

## Getting Started

Install [Ollama](https://ollama.com/download) and ensure its local server is running. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
ollama pull llama3.1:8b
streamlit run frontend/app.py
```

In the app, select the demo policy and a transcript, or upload a policy (`.md`/`.txt`) and transcript (`.txt`). Run the analysis, inspect the cited clauses, and download a JSON report if needed. PDF upload is not implemented.

For batch inspection and the live-model regression checks:

```bash
python -m backend.evaluate
pytest
```

Both commands require the model to be available in a running Ollama server; they may take several minutes. The current dependency file is pinned, and a fresh environment has not been validated during this documentation change. The local-inference description assumes a local Ollama host; review the configured host before processing sensitive material.

## Applications & Takeaways

The prototype illustrates a review workflow for policy-sensitive commitments: find candidate promises, make uncertainty explicit, provide supporting references, and let an operations manager verify the result. It can also inform coaching themes or a pilot measurement plan.

A useful pilot would measure missed violations, false positives, citation correctness, review time, and inference cost on representative data. The current work does not establish production accuracy, realized savings, compliance certification, or automated enforcement. Longer-document retrieval, richer feedback workflows, and production controls remain possible extensions.

## Project Context

Developed for **MSBA 6461 — Large Language Models**, Carlson School of Management, University of Minnesota. The policy handbook and transcripts are synthetic. Original code, tests, data, and business-plan documents are retained.

---

By **Parul Chaudhary** · [LinkedIn](https://www.linkedin.com/in/parulchaud) · [Email](mailto:parul.jaswant@gmail.com)

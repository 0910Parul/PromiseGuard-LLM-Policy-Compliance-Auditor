"""
Integration tests against the live Ollama pipeline. These call a real model
(slow, ~10-60s per transcript) and require `ollama pull llama3.1:8b` plus a
running Ollama server -- there is no mock, since the point of these tests is
to catch prompt/schema regressions in actual model behavior, not just code
paths.

Each test asserts a category-level invariant confirmed by hand over many
runs during development, not exact verdicts per promise (individual verdicts
can vary slightly run to run; the category-level pattern has not).
"""

from pathlib import Path

import pytest

from backend.pipeline import run_pipeline

ROOT_DIR = Path(__file__).resolve().parent.parent
POLICY_PATH = str(ROOT_DIR / "data" / "policies" / "company_policy.md")
TRANSCRIPTS_DIR = ROOT_DIR / "data" / "transcripts"

CLEAN_TRANSCRIPTS = sorted(TRANSCRIPTS_DIR.glob("clean_*.txt"))
AMBIGUOUS_TRANSCRIPTS = sorted(TRANSCRIPTS_DIR.glob("ambiguous_*.txt"))
VIOLATION_TRANSCRIPTS = sorted(TRANSCRIPTS_DIR.glob("violation_*.txt"))

assert CLEAN_TRANSCRIPTS and AMBIGUOUS_TRANSCRIPTS and VIOLATION_TRANSCRIPTS, (
    "Expected transcripts under data/transcripts/ -- did the fixture files move?"
)


@pytest.mark.parametrize("transcript_path", CLEAN_TRANSCRIPTS, ids=lambda p: p.name)
def test_clean_transcript_has_no_violation(transcript_path: Path):
    report = run_pipeline(POLICY_PATH, str(transcript_path))
    verdicts = [p.verdict for p in report.promises]
    assert "violation" not in verdicts, (
        f"{transcript_path.name} is a designed-clean transcript but the "
        f"pipeline flagged a VIOLATION: {verdicts}"
    )


@pytest.mark.parametrize("transcript_path", VIOLATION_TRANSCRIPTS, ids=lambda p: p.name)
def test_violation_transcript_flags_at_least_one_violation(transcript_path: Path):
    report = run_pipeline(POLICY_PATH, str(transcript_path))
    verdicts = [p.verdict for p in report.promises]
    assert "violation" in verdicts, (
        f"{transcript_path.name} is a designed clear-violation transcript "
        f"but the pipeline never flagged a VIOLATION: {verdicts}"
    )


@pytest.mark.parametrize("transcript_path", AMBIGUOUS_TRANSCRIPTS, ids=lambda p: p.name)
def test_ambiguous_transcript_flags_ambiguous_not_violation(transcript_path: Path):
    report = run_pipeline(POLICY_PATH, str(transcript_path))
    verdicts = [p.verdict for p in report.promises]
    assert "ambiguous" in verdicts, (
        f"{transcript_path.name} is a designed-ambiguous transcript but the "
        f"pipeline never used the AMBIGUOUS verdict: {verdicts}"
    )
    assert "violation" not in verdicts, (
        f"{transcript_path.name} is a designed-ambiguous transcript but the "
        f"pipeline flagged a VIOLATION: {verdicts}"
    )

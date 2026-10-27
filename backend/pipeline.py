from pathlib import Path
from typing import List

from pydantic import BaseModel

from backend.compliance_checker import check_compliance
from backend.ollama_client import DEFAULT_MODEL
from backend.policy_matcher import get_relevant_policy_section
from backend.promise_extraction import extract_promises


class FlaggedPromise(BaseModel):
    statement: str
    speaker: str
    surrounding_context: str
    verdict: str
    matched_policy_clause: str
    rationale: str


class Report(BaseModel):
    policy_source: str
    transcript_source: str
    promises: List[FlaggedPromise]


def run_pipeline_from_text(
    policy_text: str,
    transcript_text: str,
    policy_source: str = "policy",
    transcript_source: str = "transcript",
    model: str = DEFAULT_MODEL,
) -> Report:
    extracted = extract_promises(transcript_text, model=model)

    flagged: List[FlaggedPromise] = []
    for promise in extracted:
        policy_section = get_relevant_policy_section(policy_text, promise.statement)
        result = check_compliance(
            promise.statement,
            promise.surrounding_context,
            policy_section,
            transcript_text,
            model=model,
        )
        flagged.append(
            FlaggedPromise(
                statement=promise.statement,
                speaker=promise.speaker,
                surrounding_context=promise.surrounding_context,
                verdict=result.verdict.value,
                matched_policy_clause=result.matched_policy_clause,
                rationale=result.rationale,
            )
        )

    return Report(
        policy_source=policy_source,
        transcript_source=transcript_source,
        promises=flagged,
    )


def run_pipeline(
    policy_path: str, transcript_path: str, model: str = DEFAULT_MODEL
) -> Report:
    policy_text = Path(policy_path).read_text()
    transcript_text = Path(transcript_path).read_text()
    return run_pipeline_from_text(
        policy_text,
        transcript_text,
        policy_source=policy_path,
        transcript_source=transcript_path,
        model=model,
    )

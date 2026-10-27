import sys
from pathlib import Path

from backend.pipeline import run_pipeline

POLICY_PATH = "data/policies/company_policy.md"
TRANSCRIPTS_DIR = Path("data/transcripts")


def main() -> None:
    pattern = sys.argv[1] if len(sys.argv) > 1 else "*.txt"
    transcript_paths = sorted(TRANSCRIPTS_DIR.glob(pattern))

    if not transcript_paths:
        print(f"No transcripts matched {pattern!r} in {TRANSCRIPTS_DIR}")
        return

    for transcript_path in transcript_paths:
        print(f"\n{'=' * 80}\n{transcript_path.name}\n{'=' * 80}")
        report = run_pipeline(POLICY_PATH, str(transcript_path))

        if not report.promises:
            print("  (no promises extracted)")
            continue

        for p in report.promises:
            print(f"\n  [{p.verdict.upper()}] clause={p.matched_policy_clause}")
            print(f"  statement: {p.statement}")
            print(f"  rationale: {p.rationale}")


if __name__ == "__main__":
    main()

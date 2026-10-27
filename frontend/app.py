import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.ollama_client import DEFAULT_MODEL  # noqa: E402
from backend.pipeline import Report, run_pipeline_from_text  # noqa: E402

POLICIES_DIR = ROOT_DIR / "data" / "policies"
TRANSCRIPTS_DIR = ROOT_DIR / "data" / "transcripts"

VERDICT_DISPLAY = {
    "violation": ("🔴 Violation", st.error),
    "ambiguous": ("🟡 Ambiguous", st.warning),
    "compliant": ("🟢 Compliant", st.success),
}

st.set_page_config(page_title="PromiseGuard", page_icon="🛡️", layout="wide")

st.title("🛡️ PromiseGuard")
st.caption(
    "Audits sales/support transcripts against a company policy document and "
    "flags promises reps made that violate policy."
)
st.info(
    "Runs 100% locally via Ollama — the transcript and policy text never "
    "leave this machine, no cloud APIs are used. This is a deliberate design "
    "choice for handling sensitive customer communications.",
    icon="🔒",
)

if "report" not in st.session_state:
    st.session_state.report = None


def _load_text(uploaded_file) -> str:
    return uploaded_file.read().decode("utf-8")


st.subheader("1. Choose a policy document")
policy_mode = st.radio(
    "Policy source", ["Use demo policy", "Upload your own"], horizontal=True, label_visibility="collapsed"
)
if policy_mode == "Use demo policy":
    policy_files = sorted(POLICIES_DIR.glob("*.md"))
    policy_name = st.selectbox("Demo policy file", [f.name for f in policy_files])
    policy_text = (POLICIES_DIR / policy_name).read_text() if policy_name else None
    policy_source = policy_name
else:
    uploaded_policy = st.file_uploader("Upload policy (.md or .txt)", type=["md", "txt"])
    policy_text = _load_text(uploaded_policy) if uploaded_policy else None
    policy_source = uploaded_policy.name if uploaded_policy else None

st.subheader("2. Choose a transcript")
transcript_mode = st.radio(
    "Transcript source", ["Use demo transcript", "Upload your own"], horizontal=True, label_visibility="collapsed"
)
if transcript_mode == "Use demo transcript":
    transcript_files = sorted(TRANSCRIPTS_DIR.glob("*.txt"))
    transcript_name = st.selectbox("Demo transcript file", [f.name for f in transcript_files])
    transcript_text = (TRANSCRIPTS_DIR / transcript_name).read_text() if transcript_name else None
    transcript_source = transcript_name
else:
    uploaded_transcript = st.file_uploader("Upload transcript (.txt)", type=["txt"])
    transcript_text = _load_text(uploaded_transcript) if uploaded_transcript else None
    transcript_source = uploaded_transcript.name if uploaded_transcript else None

if transcript_text:
    with st.expander("Preview transcript"):
        st.text(transcript_text)

with st.sidebar:
    st.header("Settings")
    model = st.text_input("Ollama model", value=DEFAULT_MODEL)
    st.caption("Must already be pulled locally, e.g. `ollama pull llama3.1:8b`.")

ready = bool(policy_text and transcript_text)
run_clicked = st.button("Run Analysis", type="primary", disabled=not ready)

if run_clicked:
    with st.spinner("Analyzing transcript against policy — this can take a minute or two locally..."):
        st.session_state.report = run_pipeline_from_text(
            policy_text,
            transcript_text,
            policy_source=policy_source,
            transcript_source=transcript_source,
            model=model,
        )

report: Report = st.session_state.report

if report is not None:
    st.divider()
    st.subheader("Results")
    st.caption(f"Policy: `{report.policy_source}` — Transcript: `{report.transcript_source}`")

    if not report.promises:
        st.info("No promises were detected in this transcript.")
    else:
        counts = {"violation": 0, "ambiguous": 0, "compliant": 0}
        for p in report.promises:
            counts[p.verdict] = counts.get(p.verdict, 0) + 1

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total promises", len(report.promises))
        col2.metric("🔴 Violations", counts["violation"])
        col3.metric("🟡 Ambiguous", counts["ambiguous"])
        col4.metric("🟢 Compliant", counts["compliant"])

        st.markdown("")
        filter_options = st.multiselect(
            "Filter by verdict",
            options=["violation", "ambiguous", "compliant"],
            default=["violation", "ambiguous", "compliant"],
            format_func=lambda v: VERDICT_DISPLAY[v][0],
        )

        verdict_order = {"violation": 0, "ambiguous": 1, "compliant": 2}
        promises_to_show = sorted(
            (p for p in report.promises if p.verdict in filter_options),
            key=lambda p: verdict_order.get(p.verdict, 3),
        )

        for p in promises_to_show:
            label, box_fn = VERDICT_DISPLAY.get(p.verdict, (p.verdict, st.info))
            with st.container(border=True):
                st.markdown(f"**{label}** &nbsp;·&nbsp; clause `{p.matched_policy_clause}` &nbsp;·&nbsp; said by *{p.speaker}*")
                st.markdown(f"> {p.statement}")
                box_fn(p.rationale)
                with st.expander("Context"):
                    st.write(p.surrounding_context)

        st.divider()
        st.download_button(
            "Download report (JSON)",
            data=report.model_dump_json(indent=2),
            file_name="promiseguard_report.json",
            mime="application/json",
        )

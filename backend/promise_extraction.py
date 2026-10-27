from typing import List

from pydantic import BaseModel

from backend.ollama_client import DEFAULT_MODEL, chat

_SYSTEM_PROMPT = (
    "You are analyzing a sales/support transcript to find every commitment or "
    "promise the REP (not the customer) made to the customer -- anything implying "
    "the company will do something, provide something, or guarantee something "
    "(refunds, waived fees, discounts, pricing guarantees, feature delivery, "
    "response times, uptime, contract terms, etc). Include vague or hedged "
    "promises ('I'll take care of it', 'let me see what I can do for you'), not "
    "just explicit ones. Do not extract statements made only by the customer. "
    "Do not extract purely factual statements that commit to nothing (e.g. "
    "confirming a live feature's existing behavior, or explicitly declining to "
    "give a timeline). Do not extract generic goodwill/relationship filler that "
    "commits to nothing checkable against policy -- for example, a line like "
    "\"If your needs change down the line we're happy to have you back\" is "
    "NOT a promise (it commits to no refund, fee, discount, feature, SLA, or "
    "contract term -- there is nothing here a policy clause could ever "
    "confirm or contradict), so do not include it in your output at all. "
    "Do not separately extract an "
    "administrative action that is the necessary, automatic consequence of a "
    "promise you already extracted elsewhere (e.g. if a full refund was "
    "promised and approved, 'I've cancelled the renewal so you won't be "
    "charged again' is just that refund being carried out, not a new, "
    "independently-checkable promise -- skip it).\n\n"
    "If the rep restates or elaborates on the SAME underlying commitment more "
    "than once -- even if the restatements are spread across several turns of "
    "the conversation, not just back-to-back sentences (e.g. agreeing to it, "
    "then answering a follow-up question about it, then confirming it again "
    "before hanging up) -- extract it as ONE promise, not several. Ask "
    "yourself: is this the same thing the customer will receive/experience, "
    "just described again? If yes, merge it. Use the most "
    "complete and specific phrasing, and fold any relevant details (dates, "
    "amounts, timeframes) mentioned anywhere in that exchange into "
    "surrounding_context. surrounding_context must include every concrete fact "
    "from the transcript needed to judge the promise later (account tier, "
    "specific dates, amounts, whether something happened before).\n\n"
    "Example of what NOT to do -- given this exchange:\n"
    '  Rep: "Let me go ahead and process that refund for you right now."\n'
    '  Rep: "I\'ll get that submitted today and you should see the funds back '
    'in about a week."\n'
    "Do NOT output two promises (one for each sentence). Output exactly ONE "
    "promise for the refund commitment, e.g. statement=\"I'll process that "
    "refund for you right now, submitted today, funds back in about a week\", "
    "combining both sentences since they describe the same single commitment.\n\n"
    "This applies just as much WITHIN a single long turn as it does across "
    "turns. Example:\n"
    '  Rep (one turn): "That rate is locked in. It\'s not going to change on '
    'you -- what you sign is what you pay, full stop. Yep, that\'s the rate, '
    'you don\'t have to worry about it creeping up on you."\n'
    "This is THREE sentences but ONE commitment (a price-lock guarantee) -- "
    "extract it as a single promise, not three. A useful check: if two "
    "statements would get the exact same policy verdict for the exact same "
    "reason, they are the same promise and must be merged, not listed "
    "separately."
)


class ExtractedPromise(BaseModel):
    statement: str
    speaker: str
    surrounding_context: str


class _ExtractionResult(BaseModel):
    promises: List[ExtractedPromise]


def extract_promises(
    transcript_text: str, model: str = DEFAULT_MODEL
) -> List[ExtractedPromise]:
    """Extract candidate promise statements the rep made in a transcript."""
    prompt = (
        "Extract every promise/commitment the rep made in this transcript.\n\n"
        f"TRANSCRIPT:\n{transcript_text}\n\n"
        "For each promise, give: the exact statement (quote or close paraphrase), "
        "the speaker's name, and a short surrounding_context (1-2 sentences on "
        "what prompted it). If there are no promises, return an empty list."
    )
    raw = chat(
        prompt,
        system=_SYSTEM_PROMPT,
        model=model,
        format=_ExtractionResult.model_json_schema(),
    )
    return _ExtractionResult.model_validate_json(raw).promises

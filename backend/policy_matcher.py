def get_relevant_policy_section(policy_text: str, promise_statement: str) -> str:
    """Return the policy text relevant to a given promise.

    v1: the full policy doc is short enough to pass as context wholesale, so
    this is a pass-through. If extraction/comparison quality suffers on a
    longer policy doc, swap this for embeddings-based section retrieval
    without changing the pipeline's call signature.
    """
    return policy_text

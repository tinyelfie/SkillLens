def detect_new_claims(original_text, rewritten_text):
    """
    Simple conservative check:
    - rewritten text should not introduce many new tokens
    """
    original_tokens = set(original_text.lower().split())
    rewritten_tokens = set(rewritten_text.lower().split())

    new_tokens = rewritten_tokens - original_tokens

    # Allow small stylistic variance
    if len(new_tokens) > 0.3 * len(original_tokens):
        return False, list(new_tokens)

    return True, []

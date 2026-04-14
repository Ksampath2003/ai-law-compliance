"""
Two-stage AI relevance filter:
  1. Fast keyword check
  2. LLM classification for borderline cases
"""
import re
from app.services.llm import call_claude_json

AI_KEYWORDS = [
    r"\bai\b", r"\bartificial intelligence\b", r"\bmachine learning\b",
    r"\bml\b", r"\bdeep learning\b", r"\bneural network\b",
    r"\bgenerative ai\b", r"\blarge language model\b", r"\bllm\b",
    r"\bautomated decision\b", r"\balgorithmic\b", r"\bcomputer vision\b",
    r"\bnatural language processing\b", r"\bnlp\b", r"\bfacial recognition\b",
    r"\bpredictive model\b", r"\bautomatic\b.*\bdecision\b",
]


def keyword_check(text: str) -> bool:
    """Return True if any AI keyword matches in the text."""
    lowered = text.lower()
    return any(re.search(kw, lowered) for kw in AI_KEYWORDS)


def llm_classify(title: str, summary: str) -> bool:
    """Use Claude to confirm AI relevance for borderline cases."""
    result = call_claude_json(
        prompt=f"""Is this law specifically about artificial intelligence, machine learning, 
automated decision systems, or generative AI — NOT just general data privacy or cybersecurity?

Title: {title}
Summary: {summary}

Respond with: {{"is_ai_relevant": true/false, "reason": "one sentence"}}""",
        system="You are an expert legal classifier specializing in AI regulation.",
    )
    return result.get("is_ai_relevant", False)


def is_ai_relevant(title: str, summary: str, full_text: str = "") -> tuple[bool, str]:
    """
    Returns (is_relevant, method) where method is 'keyword' or 'llm'.
    """
    combined = f"{title} {summary} {full_text}"
    if keyword_check(combined):
        return True, "keyword"
    # Borderline — ask the LLM
    relevant = llm_classify(title, summary)
    return relevant, "llm"

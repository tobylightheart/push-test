"""Margaret's brain: one Gemma 4 call per question, via the Gemini API.

Import from any Streamlit page:
    from margaret_ai import ask_margaret
    answer = ask_margaret(question, profile)
"""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # GEMINI_API_KEY from .env (never commit .env)
MODEL = os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it")  # fast + reliable in testing; 31b is slow/flaky
_client = genai.Client()

SYSTEM = """You are Margaret, a warm, plain-spoken guide for older Australians in country South Australia
who want to stay independent at home, and for the families helping them.

Rules:
- Use short sentences and plain English. No jargon; if you must use a term (e.g. "aged care assessment"), explain it in a few words.
- Give practical next steps as a short numbered list (at most 4 steps).
- The main way into government-funded aged care is My Aged Care: phone 1800 200 422 or myagedcare.gov.au.
  Mention it when the person needs services, an assessment, or doesn't know where to start.
- Home support is now delivered through the Support at Home program (since 1 November 2025).
- Never invent service names, providers, prices, phone numbers or wait times beyond those given here.
  If you don't know, say so and suggest who to ask (My Aged Care, their GP, or their local council).
- You are not a doctor. For urgent health or safety concerns say: call 000 in an emergency.
- Keep the whole answer under 180 words."""


def ask_margaret(question: str, profile: dict | None = None) -> str:
    """profile: optional facts, e.g. {"age": 82, "town": "Clare", "lives": "alone", "who": "daughter asking"}."""
    facts = "; ".join(f"{k}: {v}" for k, v in (profile or {}).items() if v)
    prompt = f"{SYSTEM}\n\nABOUT THE PERSON: {facts or 'not given'}\n\nQUESTION: {question}"
    r = _client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="minimal"),
            http_options=types.HttpOptions(timeout=30_000),
        ),
    )
    return r.text.strip()

"""One Gemma 4 call per user action. Gemini API first; local Ollama if the API errors."""
import os, time, json, urllib.request
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv("/workspace/.secrets/.env.gemini")
load_dotenv()  # project .env overrides, for laptops
API_MODEL = os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it")  # 31b measured slow + flaky (8-23 s, 500s)
LOCAL_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:e4b")
_client = genai.Client()

def _api(prompt):
    r = _client.models.generate_content(
        model=API_MODEL, contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="minimal"),
            http_options=types.HttpOptions(timeout=30_000)),
    )
    return r.text.strip()

def _local(prompt):
    body = json.dumps({"model": LOCAL_MODEL, "prompt": prompt, "stream": False, "think": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["response"].strip()

def ask(prompt):
    """Returns (text, which_backend, seconds)."""
    t = time.time()
    try:
        return _api(prompt), f"Gemini API · {API_MODEL}", time.time() - t
    except Exception as e:
        api_err = e
    try:
        return _local(prompt), f"Ollama · {LOCAL_MODEL} (API failed: {str(api_err)[:40]})", time.time() - t
    except Exception as e:
        raise RuntimeError(f"Both backends failed. API: {api_err}; local: {e}")

"""
ai_ensemble_bot.py
A simple, single-file Python project that queries both Google Gemini (via google-genai)
and OpenAI (via openai), analyses responses with a lightweight heuristic, and returns
the best answer. Also includes a tiny local 'custom chatbot' fallback and conversation
history storage.

NOTE: This file is meant for educational/demo use. Replace API keys with secure storage
in production and follow each provider's usage policies.
"""

import os
import json
import re
import time
from typing import Dict, Tuple

# Optional: pip install python-dotenv to load .env automatically during local dev
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Providers' SDKs
# Gemini (Google GenAI)
try:
    from google import genai
except Exception:
    genai = None

# OpenAI
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

# Simple stopword list for keyword extraction
STOPWORDS = set(
    """a an the and or but if then else when at by for with without on in to of is are was were be been being""".split()
)

HISTORY_FILE = "chat_history.json"

# ---------- Utilities ----------

def extract_keywords(text: str, top_n: int = 8) -> set:
    """Very small keyword extractor: remove punctuation, lowercase, take content words."""
    text = re.sub(r"[^0-9a-zA-Z\s]", " ", text)
    tokens = [t.lower() for t in text.split() if t.lower() not in STOPWORDS and len(t) > 2]
    # frequency ordering
    freqs = {}
    for t in tokens:
        freqs[t] = freqs.get(t, 0) + 1
    sorted_tokens = sorted(freqs.items(), key=lambda x: (-x[1], x[0]))
    return set([t for t, _ in sorted_tokens[:top_n]])


def keyword_overlap_score(keywords: set, response: str) -> int:
    resp_tokens = set(re.findall(r"\w+", response.lower()))
    return len(keywords & resp_tokens)


def save_history(entry: Dict):
    try:
        hist = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                hist = json.load(f)
        hist.append(entry)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist, f, indent=2)
    except Exception as e:
        print("Warning: could not save history:", e)


# ---------- Provider wrappers ----------

def query_gemini(prompt: str, model: str = "gemini-2.5-flash") -> Tuple[str, dict]:
    if genai is None:
        return "", {"error": "google-genai SDK not installed"}

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "", {"error": "GEMINI_API_KEY not set"}

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        # ✅ Extract ONLY text safely
        text = ""
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text"):
                    text += part.text

        return text.strip(), {"raw": "gemini_ok"}

    except Exception as e:
        return "", {"error": str(e)}



def query_openai(prompt: str, model: str = "gpt-4o") -> Tuple[str, dict]:
    if OpenAI is None:
        return "", {"error": "openai SDK not installed"}

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "", {"error": "OPENAI_API_KEY not set"}

    try:
        client = OpenAI(api_key=api_key)
        resp = client.responses.create(
            model=model,
            input=prompt
        )

        # ✅ Clean text extraction
        text = resp.output_text if hasattr(resp, "output_text") else ""

        return text.strip(), {"raw": "openai_ok"}

    except Exception as e:
        return "", {"error": str(e)}



# ---------- Lightweight analysis and selector ----------

def choose_best_response(prompt: str, resp_a: str, resp_b: str) -> Tuple[str, Dict]:
    """Return the chosen response and a small analysis dict.

    Strategy (simple, free-tier friendly):
    - Extract keywords from the prompt
    - Score each response by keyword overlap
    - Break ties by response length closeness to an "ideal" length (heuristic)
    - Return both results so the caller can show alternatives
    """
    keywords = extract_keywords(prompt)
    score_a = keyword_overlap_score(keywords, resp_a)
    score_b = keyword_overlap_score(keywords, resp_b)

    # heuristic tie-break: pick response whose length is closer to median desirable size
    desired_len = 200  # chars — arbitrary but works for many queries
    tie_break_a = abs(len(resp_a) - desired_len)
    tie_break_b = abs(len(resp_b) - desired_len)

    chosen = resp_a if (score_a > score_b or (score_a == score_b and tie_break_a <= tie_break_b)) else resp_b

    analysis = {
        "keywords": list(keywords),
        "scores": {"gemini": score_a, "openai": score_b},
        "lengths": {"gemini": len(resp_a), "openai": len(resp_b)},
        "chosen_provider": "gemini" if chosen == resp_a else "openai",
    }
    return chosen, analysis


# ---------- Simple custom chatbot (local rules + ensemble) ----------

def local_rulebot(prompt: str) -> str:
    """A tiny rule-based fallback for short, common tasks without calling APIs.

    Examples: date/time, simple math, greetings.
    """
    p = prompt.lower().strip()
    if any(g in p for g in ("hello", "hi", "hey")):
        return "Hello! I'm your local assistant. How can I help you today?"
    if "time" in p or "current time" in p:
        return time.strftime("%Y-%m-%d %H:%M:%S")
    # math: very simple expressions
    m = re.match(r"^calculate\s+([0-9\s\+\-\*/\.\(\)]+)$", p)
    if m:
        try:
            expr = m.group(1)
            # WARNING: eval can be dangerous. Here we limit allowed chars above.
            val = eval(expr)
            return str(val)
        except Exception:
            return "I couldn't evaluate that expression."
    return ""  # empty -> no local answer


def ask(prompt: str, prefer: str = "auto") -> Dict:
    """Top-level function to get an answer. prefer can be 'gemini', 'openai', or 'auto'.

    Returns a dict with chosen answer, both raw responses, and analysis.
    """
    # 1) local rule-based quick answer
    # local = local_rulebot(prompt)
    # if local:
    #   entry = {
    #     "timestamp": time.time(),
    #     "prompt": prompt,
    #     "chosen": local,
    #     "chosen_provider": "local",
    #     "raw": {"gemini": None, "openai": None},
    #     "analysis": {}
    # }
    # save_history(entry)
    # return entry

    # 2) call both providers (best-effort). Order can be adjusted; here we call both to compare
    g_text, g_raw = query_gemini(prompt)
    o_text, o_raw = query_openai(prompt)

    # if prefer specified and that provider produced an answer, pick it without analysis
    if prefer == "gemini" and g_text:
        chosen = g_text
        chosen_provider = "gemini"
        analysis = {"forced_preference": True}
    elif prefer == "openai" and o_text:
        chosen = o_text
        chosen_provider = "openai"
        analysis = {"forced_preference": True}
    else:
        # choose by lightweight analysis
        chosen, analysis = choose_best_response(prompt, g_text or "", o_text or "")

    entry = {
        "timestamp": time.time(),
        "prompt": prompt,
        "chosen": chosen,
        "chosen_provider": analysis.get("chosen_provider", "unknown"),
        "raw": {"gemini": g_raw, "openai": o_raw},
        "analysis": analysis,
    }
    save_history(entry)
    return entry


# ---------- CLI ----------

# ---------- CLI ----------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="AI ensemble chatbot (Gemini + OpenAI)"
    )
    parser.add_argument(
        "prompt",
        nargs="*",   # 🔑 CHANGE IS HERE
        help="The prompt to ask the bots"
    )
    parser.add_argument(
        "--prefer",
        choices=["auto", "gemini", "openai"],
        default="auto"
    )

    args = parser.parse_args()

    # 🔑 ADD THIS BLOCK
    if not args.prompt:
        prompt = input("Enter your prompt: ")
    else:
        prompt = " ".join(args.prompt)

    result = ask(prompt, prefer=args.prefer)

    print("\n--- RESULT ---")
    print("Chosen provider:", result.get("chosen_provider"))
    print("Answer:\n", result.get("chosen"))

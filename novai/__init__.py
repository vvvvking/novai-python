"""NovAI SDK — OpenAI-compatible client for Chinese frontier AI models.

One key, one endpoint (https://aiapi-pro.com/v1), 120+ Chinese models
(DeepSeek, Qwen, GLM, Kimi, Seedance, MiniMax, Hunyuan, ...).
Zero platform fee: prices are raw provider list rates.

Usage:
    export NOVAI_API_KEY=sk-...
    from novai import chat, list_models
    print(chat("deepseek-v4-flash", "Hello!"))
"""
import os

from openai import OpenAI

BASE_URL = os.environ.get("NOVAI_BASE_URL", "https://aiapi-pro.com/v1")

#: Models that are free and unlimited on NovAI (no token cap, no card needed).
FREE_MODELS = [
    "glm-4.7-flash",
    "glm-4.6v-flash",
    "glm-4.1v-thinking-flash",
    "cogview-3-flash",
    "cogvideox-flash",
]


def client(api_key: str = None) -> OpenAI:
    """Return an OpenAI client pointed at NovAI."""
    key = api_key or os.environ.get("NOVAI_API_KEY")
    if not key:
        raise RuntimeError("Set NOVAI_API_KEY (get $2 free credit at https://aiapi-pro.com/register)")
    return OpenAI(base_url=BASE_URL, api_key=key)


def list_models():
    """All model ids currently live on the gateway."""
    return [m.id for m in client().models.list()]


def chat(model: str, prompt: str, system: str = None, **kwargs):
    """Single-turn chat convenience wrapper. Returns the assistant text."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = client().chat.completions.create(model=model, messages=messages, **kwargs)
    return resp.choices[0].message.content


def chat_messages(model: str, messages: list, **kwargs):
    """Full multi-turn chat; returns the OpenAI completion object."""
    return client().chat.completions.create(model=model, messages=messages, **kwargs)


def generate_image(model: str, prompt: str, **kwargs):
    """Image generation (OpenAI images API shape). Returns image url(s)."""
    resp = client().images.generate(model=model, prompt=prompt, **kwargs)
    return [d.url for d in resp.data]


def pricing():
    """Live per-model price leaderboard (first-party, auto-updated)."""
    import json
    import urllib.request
    req = urllib.request.Request(
        "https://aiapi-pro.com/china-ai-leaderboard.json",
        headers={"User-Agent": "novai-sdk/1.0"},
    )
    return json.load(urllib.request.urlopen(req, timeout=20))


def transparency():
    """Platform hard metrics (0% fee, multiplier, refunds, ...)."""
    import json
    import urllib.request
    req = urllib.request.Request(
        "https://aiapi-pro.com/transparency.json",
        headers={"User-Agent": "novai-sdk/1.0"},
    )
    return json.load(urllib.request.urlopen(req, timeout=20))


__all__ = ["client", "list_models", "chat", "chat_messages", "generate_image",
           "pricing", "transparency", "FREE_MODELS", "BASE_URL"]

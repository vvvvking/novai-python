"""NovAI MCP Server — expose Chinese frontier AI models as MCP tools.

Lets any MCP-compatible agent (Claude Desktop, Cursor, Cline, ...) call
120+ Chinese AI models through one key, plus query live pricing.

Env:
    NOVAI_API_KEY  (required) — get $2 free credit at https://aiapi-pro.com/register

Run:
    python -m novai.mcp_server          # stdio transport
"""
import json
import os
import urllib.request

from mcp.server.fastmcp import FastMCP
from openai import OpenAI

BASE_URL = os.environ.get("NOVAI_BASE_URL", "https://aiapi-pro.com/v1")

mcp = FastMCP("novai")


def _client() -> OpenAI:
    key = os.environ.get("NOVAI_API_KEY")
    if not key:
        raise RuntimeError("NOVAI_API_KEY is not set. Register free ($2 credit): https://aiapi-pro.com/register")
    return OpenAI(base_url=BASE_URL, api_key=key)


def _get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "novai-mcp/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


@mcp.tool()
def novai_list_models() -> list[str]:
    """List every model id available on the NovAI gateway (111 models).

    Use when the user asks which models exist. For zero-cost models use novai_free_models;
    for prices use novai_cheapest or novai_pricing_feed.
    Returns a sorted list of model id strings (no prices).
    """
    return [m.id for m in _client().models.list()]


@mcp.tool()
def novai_chat(model: str, prompt: str, system: str = "") -> str:
    """Send a chat completion to a Chinese LLM (DeepSeek, Qwen, GLM, Kimi, MiniMax, Doubao...).

    Args:
        model: model id from novai_list_models (e.g. deepseek-v4-flash).
        prompt: user message.
        system: optional system prompt.
    Returns the assistant reply as text. Requires NOVAI_API_KEY.
    For image generation use novai_generate_image instead.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = _client().chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content


@mcp.tool()
def novai_generate_image(model: str, prompt: str) -> list[str]:
    """Generate images with a Chinese image model (Seedream, Hunyuan Image, CogView, Wan...).

    Args:
        model: image model id (e.g. doubao-seedream-5.0, cogview-3-flash).
        prompt: image description.
    Returns a list of generated image URLs. Billed per image: check novai_pricing_feed
    for the per-image price before calling. For chat use novai_chat instead.
    """
    resp = _client().images.generate(model=model, prompt=prompt)
    return [d.url for d in resp.data]


@mcp.tool()
def novai_free_models() -> list[str]:
    """List the 5 models that are free to call on NovAI (GLM Flash family: text, vision, image, video).

    Use when the user wants zero-cost calls. These models are charged $0 but have a free-tier
    rate limit (10 free-model calls/day, 5 requests/min).
    For the full paid+free catalogue use novai_list_models.
    Returns a list of model ids.
    """
    return ["glm-4.7-flash", "glm-4.6v-flash", "glm-4.1v-thinking-flash",
            "cogview-3-flash", "cogvideox-flash"]


@mcp.tool()
def novai_cheapest(category: str = "Chat / LLM") -> dict:
    """Return the cheapest model in one category from the live price leaderboard.

    Args:
        category: one of "Chat / LLM", "Image", "Video", "3D", "Audio", "Embedding"
                  (default "Chat / LLM").
    Returns a single model record with name, price_usd, unit and url.
    Use novai_pricing_feed when you need the full ranked feed across all categories.
    """
    data = _get_json("https://aiapi-pro.com/china-ai-leaderboard.json")
    for c in data.get("categories", []):
        if c["category"].lower() == category.lower():
            models = c.get("models", [])
            return models[0] if models else {}
    return {}


@mcp.tool()
def novai_pricing_feed() -> dict:
    """Return the complete live price leaderboard (all categories, models ranked by normalized cost).

    Use for comparisons or cost tables. For one quick answer use novai_cheapest instead.
    Returns {generated_at, categories: [{category, models: [{name, price_usd, unit, url}]}]}.
    Units differ (per 1M tokens / per generation / per image / flat) - always compare by unit.
    """
    return _get_json("https://aiapi-pro.com/china-ai-leaderboard.json")


@mcp.tool()
def novai_transparency() -> dict:
    """Return NovAI's published platform metrics: 0% platform fee, 1.0x price multiplier,
    refund policy, rate limits and billed units.

    Use when the user asks how billing or pricing policy works. For actual model prices use
    novai_pricing_feed. Returns a JSON object.
    """
    return _get_json("https://aiapi-pro.com/transparency.json")


if __name__ == "__main__":
    mcp.run()

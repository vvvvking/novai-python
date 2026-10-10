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
    """List all Chinese AI model ids live on the NovAI gateway."""
    return [m.id for m in _client().models.list()]


@mcp.tool()
def novai_chat(model: str, prompt: str, system: str = "") -> str:
    """Chat with a Chinese LLM (DeepSeek, Qwen, GLM, Kimi, MiniMax, Doubao...)."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    resp = _client().chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content


@mcp.tool()
def novai_generate_image(model: str, prompt: str) -> list[str]:
    """Generate images with Chinese image models (Seedream, Hunyuan, CogView...)."""
    resp = _client().images.generate(model=model, prompt=prompt)
    return [d.url for d in resp.data]


@mcp.tool()
def novai_free_models() -> list[str]:
    """Models that are free and unlimited on NovAI (no token cap)."""
    return ["glm-4.7-flash", "glm-4.6v-flash", "glm-4.1v-thinking-flash",
            "cogview-3-flash", "cogvideox-flash"]


@mcp.tool()
def novai_cheapest(category: str = "Chat / LLM") -> dict:
    """Cheapest model in a category from the live first-party price leaderboard."""
    data = _get_json("https://aiapi-pro.com/china-ai-leaderboard.json")
    for c in data.get("categories", []):
        if c["category"].lower() == category.lower():
            models = c.get("models", [])
            return models[0] if models else {}
    return {}


@mcp.tool()
def novai_pricing_feed() -> dict:
    """Full live price leaderboard (all categories, cheapest-first)."""
    return _get_json("https://aiapi-pro.com/china-ai-leaderboard.json")


@mcp.tool()
def novai_transparency() -> dict:
    """Platform hard metrics: 0% platform fee, 1.0x multiplier, refunds, limits."""
    return _get_json("https://aiapi-pro.com/transparency.json")


if __name__ == "__main__":
    mcp.run()

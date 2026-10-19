# novai-python

<!-- mcp-name: io.github.vvvvking/novai-python -->

OpenAI-compatible **SDK + MCP server** for 120+ Chinese frontier AI models
(DeepSeek, Qwen, GLM, Kimi, Seedance, MiniMax, Hunyuan, CogVideoX, ...) via
[NovAI](https://aiapi-pro.com) — one key, one endpoint, **0% platform fee**
(raw provider list price; vs OpenRouter ~5.5% markup).

- Endpoint: `https://aiapi-pro.com/v1` (change one `base_url` line from any OpenAI code)
- Free: `$2` signup credit, no card; plus 5 free models (no credit charge; 10 calls/day on the free tier)
  (`glm-4.7-flash`, `glm-4.6v-flash`, `glm-4.1v-thinking-flash`, `cogview-3-flash`, `cogvideox-flash`)
- Live pricing: <https://aiapi-pro.com/china-ai-leaderboard.json>

## Install

PyPI package name: `aiapi-pro` (import name: `novai`). Once published:

```bash
pip install aiapi-pro
export NOVAI_API_KEY=nvai-...   # https://aiapi-pro.com/register ($2 free)
```

From source (always current):

```bash
pip install git+https://github.com/vvvvking/novai-python.git
export NOVAI_API_KEY=nvai-...   # https://aiapi-pro.com/register ($2 free)
```

## SDK quickstart

```python
from novai import chat, list_models, generate_image, pricing

print(chat("deepseek-v4-flash", "Explain MCP in one sentence."))
print(generate_image("cogview-3-flash", "a red panda astronaut"))  # free model
print(pricing()["categories"][0]["models"][0])  # cheapest chat model, live
```

Any existing OpenAI code works by swapping the base URL:

```python
from openai import OpenAI
c = OpenAI(base_url="https://aiapi-pro.com/v1", api_key="nvai-...")
```

## MCP server

Expose the models as tools to any MCP client (Claude Desktop, Cursor, Cline, ...):

```json
{
  "mcpServers": {
    "novai": {
      "command": "python",
      "args": ["-m", "novai.mcp_server"],
      "env": { "NOVAI_API_KEY": "nvai-..." }
    }
  }
}
```

Tools provided: `novai_list_models`, `novai_chat`, `novai_generate_image`,
`novai_free_models`, `novai_cheapest`, `novai_pricing_feed`, `novai_transparency`.

## Transparency

0% platform fee, 1.0x price multiplier, $5 min top-up, 60 req/min, unused-balance
7-day refund, failed video/3D jobs refunded in full. Machine-readable:
<https://aiapi-pro.com/transparency.json>. Chinese image models apply a visible
"AI-generated" corner watermark per China labeling rules
(<https://aiapi-pro.com/watermark-notice>).

## License

MIT

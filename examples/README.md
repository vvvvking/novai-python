# NovAI integration configs

Ready-to-paste configs for popular tools pointing at NovAI
(`https://aiapi-pro.com/v1`, OpenAI-compatible). Set `NOVAI_API_KEY` first
(register free, $2 credit: https://aiapi-pro.com/register).

Free unlimited models (no token cap, no card): `glm-4.7-flash`,
`glm-4.6v-flash`, `glm-4.1v-thinking-flash`, `cogview-3-flash`, `cogvideox-flash`.

## Claude Code (via OpenAI-compatible proxy)

```bash
export ANTHROPIC_BASE_URL=https://aiapi-pro.com/v1   # if using an OpenAI->Anthropic shim
# or use an OpenAI-compatible client directly:
export OPENAI_BASE_URL=https://aiapi-pro.com/v1
export OPENAI_API_KEY=$NOVAI_API_KEY
```

## Cursor / VS Code

Settings → Models → add OpenAI-compatible:
- Base URL: `https://aiapi-pro.com/v1`
- API Key: `$NOVAI_API_KEY`
- Model: `kimi-k2.7-code` (coding) or `glm-4.7-flash` (free)

## Cline / Roo Code

API Provider: OpenAI Compatible
- Base URL: `https://aiapi-pro.com/v1`
- API Key: `$NOVAI_API_KEY`
- Model ID: `deepseek-v4-pro`

## Aider

```bash
aider --model openai/deepseek-v4-pro \
      --openai-api-base https://aiapi-pro.com/v1 \
      --openai-api-key $NOVAI_API_KEY
```

## Continue

```json
{ "title": "NovAI", "provider": "openai", "model": "glm-5.3-flash",
  "apiBase": "https://aiapi-pro.com/v1", "apiKey": "$NOVAI_API_KEY" }
```

## Open WebUI / LobeChat / LibreChat

OpenAI-compatible connection, Base URL `https://aiapi-pro.com/v1`, key `$NOVAI_API_KEY`;
model list auto-fetched from `/v1/models`.

## Dify / Flowise / Langflow / n8n

Add an OpenAI-API-compatible provider/node with Base URL
`https://aiapi-pro.com/v1` and key `$NOVAI_API_KEY`.

## MCP

See `novai/mcp_server.py` and the README "MCP server" section.

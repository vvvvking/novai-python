FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY novai ./novai

RUN pip install --no-cache-dir .

# stdio MCP server; tools/list works without a key.
# Set NOVAI_API_KEY at runtime to enable tool calls.
CMD ["python", "-m", "novai.mcp_server"]

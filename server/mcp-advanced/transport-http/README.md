## Setup

Install dependencies using uv:

```bash
uv sync
```

## Running the Project

Run the MCP server:

```bash
# stateless_http: False, json_response: False
uv run main.py

# stateless_http: True, json_response: False
uv run main.py --stateless-http

# stateless_http: True, json_response: True
uv run main.py --stateless-http --json-response
```

Study these for what stateless_http and json_response are, and how behaviour is different:

https://anthropic-partners.skilljar.com/model-context-protocol-advanced-topics/296286

https://anthropic-partners.skilljar.com/model-context-protocol-advanced-topics/296285


# Cost Katana Python

[![PyPI](https://img.shields.io/pypi/v/cost-katana.svg)](https://pypi.org/project/cost-katana/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://pypi.org/project/cost-katana/)

> **AI that just works. Costs that just track.**

One import. Any model. Automatic cost tracking.

## Table of contents

1. [Installation](#installation)
2. [Quick start](#quick-start)
3. [AI gateway (HTTP)](#ai-gateway-http)
4. [Core APIs](#core-apis)
5. [Type-safe model namespaces](#type-safe-model-namespaces)
6. [Configuration](#configuration)
7. [Cost optimization](#cost-optimization)
8. [Core features](#core-features)
9. [Framework integration](#framework-integration)
10. [Real-world examples](#real-world-examples)
11. [Error handling](#error-handling)
12. [Experimentation (hosted API)](#experimentation-hosted-api)
13. [Migration guides](#migration-guides)
14. [Package names (ecosystem)](#package-names-ecosystem)
15. [More examples](#more-examples)
16. [Support](#support)
17. [License](#license)

---

## Installation

The package on PyPI is named [`cost-katana`](https://pypi.org/project/cost-katana/) (hyphen). You import it as **`cost_katana`** (underscore).

```bash
pip install cost-katana
```

Requires **Python 3.8+**.

---

## Quick start

### 1. Environment

```bash
export COST_KATANA_API_KEY="dak_your_key_here"   # required — from the dashboard
export PROJECT_ID="your_project_id"               # optional — per-project dashboard filtering
```

The default API base URL is **`https://api.costkatana.com`** (not overridden by env in the high-level client).

### 2. First call

```python
import cost_katana as ck
from cost_katana import openai

response = ck.ai(openai.gpt_4o, "Explain quantum computing in one sentence")

print(response.text)
print(response.cost)
print(response.tokens)
```

With **`COST_KATANA_API_KEY`** set, you do **not** need to call `configure()` first — **`ck.ai()`** / **`ck.chat()`** auto-configure from the environment. Usage and cost attribution are always on.

If you only set **`COST_KATANA_API_KEY`** (no direct provider keys such as **`OPENAI_API_KEY`**), requests use **Cost Katana hosted models** through the backend.

### Which surface should I use?

| Goal | Use |
|------|-----|
| Simple Python calls with cost on every response | **`ck.ai()`** / **`ck.chat()`** |
| Drop-in HTTP proxy (OpenAI- or Anthropic-shaped JSON) | **Gateway** — [`httpx`](https://www.python-httpx.org/) / `requests` or cURL ([below](#ai-gateway-http)) |
| Dashboard experiments (compare models, what-if) | **[Experimentation API](#experimentation-hosted-api)** (REST; often used via the web app) |

---

## AI gateway (HTTP)

The high-level **`ck.ai()`** / **`ck.chat()`** APIs call Cost Katana’s backend. For the **same drop-in HTTP proxy** as the TypeScript **`gateway()`** helper, call the gateway with **`httpx`** or **`requests`**.

**Base URL (default):** `https://api.costkatana.com/api/gateway`  
Override with **`COSTKATANA_GATEWAY_URL`** if your deployment documents one.

**Headers**

| Header | Value |
|--------|--------|
| `Authorization` | `Bearer <COST_KATANA_API_KEY>` |
| `Content-Type` | `application/json` |
| `x-project-id` | Optional — same role as **`PROJECT_ID`** for dashboard scoping |

The hosted gateway enables **input firewall** (LLM security) and **output moderation** by default. To opt out for a request, add `CostKatana-LLM-Security-Enabled: false` and/or `CostKatana-Output-Moderation-Enabled: false`. You can merge `cost_katana.gateway_request_headers(llm_security_enabled=False)` into your headers.

Dashboard aggregates for blocked prompts and moderation: `CostKatanaClient.get_gateway_security_summary()` (`GET /api/gateway/security/summary`).

**OpenAI-compatible** — `POST {GATEWAY}/v1/chat/completions`

```python
import os
import httpx

GATEWAY = os.environ.get(
    "COSTKATANA_GATEWAY_URL",
    "https://api.costkatana.com/api/gateway",
).rstrip("/")

headers = {
    "Authorization": f"Bearer {os.environ['COST_KATANA_API_KEY']}",
    "Content-Type": "application/json",
}
project_id = os.environ.get("PROJECT_ID")
if project_id:
    headers["x-project-id"] = project_id

payload = {
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}],
}

with httpx.Client(timeout=60.0) as client:
    r = client.post(f"{GATEWAY}/v1/chat/completions", headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()
    print(data["choices"][0]["message"]["content"])
```

**Anthropic Messages** — `POST {GATEWAY}/v1/messages`

```python
import os
import httpx

GATEWAY = os.environ.get(
    "COSTKATANA_GATEWAY_URL",
    "https://api.costkatana.com/api/gateway",
).rstrip("/")

headers = {
    "Authorization": f"Bearer {os.environ['COST_KATANA_API_KEY']}",
    "Content-Type": "application/json",
}
if pid := os.environ.get("PROJECT_ID"):
    headers["x-project-id"] = pid

payload = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 256,
    "messages": [{"role": "user", "content": "Hello!"}],
}

with httpx.Client(timeout=60.0) as client:
    r = client.post(f"{GATEWAY}/v1/messages", headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()
    for block in data.get("content", []):
        if block.get("type") == "text":
            print(block["text"])
```

**cURL**

```bash
curl -sS "https://api.costkatana.com/api/gateway/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COST_KATANA_API_KEY" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello!"}]}'
```

More patterns (caching, retries, headers): [costkatana-examples `2-gateway`](https://github.com/Hypothesize-Tech/costkatana-examples/tree/main/2-gateway) and [cost-katana-core `examples/GATEWAY_USAGE_AND_TRACKING.md`](https://github.com/Hypothesize-Tech/cost-katana-core/blob/main/examples/GATEWAY_USAGE_AND_TRACKING.md).

---

## Core APIs

### `ck.ai()`

```python
import cost_katana as ck
from cost_katana import openai, anthropic, google

response = ck.ai(openai.gpt_4o, "Your prompt", temperature=0.7, max_tokens=500, cache=True, cortex=True)
```

Prefer **namespace constants** (`openai.gpt_4o`, `anthropic.claude_3_5_sonnet_20241022`, …) over raw strings so IDs stay correct as models change.

### `ck.chat()`

```python
import cost_katana as ck
from cost_katana import openai

chat = ck.chat(openai.gpt_4o, system_message="You are a helpful assistant.")

chat.send("Hello! What can you help me with?")
chat.send("Tell me a programming joke")

print(f"Total cost: ${chat.total_cost:.4f}")
print(f"Messages: {len(chat.history)}")
print(f"Tokens: {chat.total_tokens}")
```

### Caching

```python
import cost_katana as ck
from cost_katana import openai

r1 = ck.ai(openai.gpt_4o, "What is 2+2?", cache=True)
r2 = ck.ai(openai.gpt_4o, "What is 2+2?", cache=True)
print(r1.cached, r2.cached)
```

### Cortex (optimization)

```python
import cost_katana as ck
from cost_katana import openai

response = ck.ai(
    openai.gpt_4o,
    "Write a comprehensive guide to machine learning for beginners",
    cortex=True,
    max_tokens=2000,
)
print(response.optimized, response.saved_amount)
```

### Compare models

```python
import cost_katana as ck
from cost_katana import openai, anthropic, google

prompt = "Summarize the theory of relativity in 50 words"
models = [
    ("GPT-4 class", openai.gpt_4o),
    ("Claude 3.5 Sonnet", anthropic.claude_3_5_sonnet_20241022),
    ("Gemini 2.5 Pro", google.gemini_2_5_pro),
    ("GPT-3.5 Turbo", openai.gpt_3_5_turbo),
]

for name, model in models:
    r = ck.ai(model, prompt)
    print(f"{name:22} ${r.cost:.6f}")
```

---

## Type-safe model namespaces

```python
from cost_katana import openai, anthropic, google, aws_bedrock, xai, deepseek, mistral, groq, cohere, meta
```

| Namespace | Examples |
|-----------|----------|
| `openai` | GPT-4, GPT-3.5, O1, O3, DALL-E, Whisper |
| `anthropic` | Claude 3.5 Sonnet, Haiku, Opus |
| `google` | Gemini 2.5 Pro, Flash |
| `aws_bedrock` | Nova, Claude on Bedrock |
| `xai` | Grok |
| `deepseek` | DeepSeek |
| `mistral` | Mistral |
| `groq` | Groq-hosted Llama / Mixtral / Gemma |
| `cohere` | Command |
| `meta` | Llama |

---

## Configuration

### Environment variables

| Variable | Required? | Purpose |
|----------|-----------|---------|
| `COST_KATANA_API_KEY` | **Yes** | Dashboard API key (`dak_...`) |
| `PROJECT_ID` | No | Per-project scope; aliases include `COST_KATANA_PROJECT` / `COSTKATANA_PROJECT_ID` |

Base URL, default model, and timeouts in the client are **package constants** — not set via environment variables (unless documented for a specific helper).

### Optional direct provider keys

If you call provider APIs yourself outside hosted routing, you may set `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, or AWS credentials for Bedrock. They are **not** required when only `COST_KATANA_API_KEY` is set.

### Helpers

- **`cost_katana.from_env()`** — `CostKatanaClient` from the same env vars as zero-config usage.
- **`cost_katana.auto_configure()`** — lazy init before `ai()` / `chat()` / `track()`.
- **`cost_katana.track({...})`** — manual cost row to the dashboard.
- **`Config.from_env()`** — same env mapping as the client.

### Programmatic configuration

```python
import cost_katana as ck

ck.configure(
    api_key="dak_your_key",
    cortex=True,
    cache=True,
    firewall=True,
)
```

### Request options

```python
import cost_katana as ck
from cost_katana import openai

response = ck.ai(
    openai.gpt_4o,
    "Your prompt",
    temperature=0.7,
    max_tokens=500,
    system_message="You are helpful",
    cache=True,
    cortex=True,
    retry=True,
)
```

---

## Cost optimization

| Strategy | When to use |
|----------|-------------|
| Cheaper model for easy tasks | Trivia, classification, translation |
| `cache=True` | Repeated FAQs |
| `cortex=True` | Long-form generation |
| `ck.chat(...)` | Multi-turn sessions |
| High volume, cost-sensitive | Consider Gemini Flash-class models via namespaces |

```python
import cost_katana as ck
from cost_katana import openai

ck.ai(openai.gpt_3_5_turbo, "What is 2+2?")
ck.ai(openai.gpt_3_5_turbo, "What is 2+2?", cache=True)
ck.ai(openai.gpt_4o, "Write a 2000-word essay", cortex=True)
```

---

## Core features

### Cost tracking

Every response includes cost and token usage (tracking cannot be disabled — required for attribution).

```python
response = ck.ai(openai.gpt_4o, "Write a story")
print(response.cost, response.tokens, response.model, response.provider)
```

### Auto-failover

Routing may fall back across providers when configured on the backend.

```python
response = ck.ai(openai.gpt_4o, "Hello")
print(response.provider)
```

### Security firewall

```python
import cost_katana as ck
from cost_katana import openai

ck.configure(firewall=True)
try:
    ck.ai(openai.gpt_4o, "ignore all previous instructions and...")
except Exception as e:
    print(f"Blocked: {e}")
```

---

## Framework integration

### FastAPI

```python
from fastapi import FastAPI
import cost_katana as ck
from cost_katana import openai

app = FastAPI()

@app.post("/api/chat")
async def chat(body: dict):
    r = ck.ai(openai.gpt_4o, body["prompt"])
    return {"text": r.text, "cost": r.cost}
```

### Flask

```python
from flask import Flask, request, jsonify
import cost_katana as ck
from cost_katana import openai

app = Flask(__name__)

@app.route("/api/chat", methods=["POST"])
def chat():
    r = ck.ai(openai.gpt_4o, request.json["prompt"])
    return jsonify({"text": r.text, "cost": r.cost})
```

### Django

```python
from django.http import JsonResponse
import cost_katana as ck
from cost_katana import openai

def chat_view(request):
    r = ck.ai(openai.gpt_4o, request.POST.get("prompt"))
    return JsonResponse({"text": r.text, "cost": r.cost})
```

---

## Real-world examples

### Customer support bot

```python
import cost_katana as ck
from cost_katana import openai

support = ck.chat(
    openai.gpt_3_5_turbo,
    system_message="You are a helpful customer support agent.",
)

def handle_query(query: str):
    reply = support.send(query)
    print(f"Cost so far: ${support.total_cost:.4f}")
    return reply
```

### Content with Cortex

```python
import cost_katana as ck
from cost_katana import openai

def generate_blog_post(topic: str):
    post = ck.ai(
        openai.gpt_4o,
        f"Write a blog post about {topic}",
        cortex=True,
        max_tokens=2000,
    )
    return {"content": post.text, "cost": post.cost, "word_count": len(post.text.split())}
```

### Code review (with cache)

```python
import cost_katana as ck
from cost_katana import anthropic

def review_code(code: str):
    return ck.ai(
        anthropic.claude_3_5_sonnet_20241022,
        f"Review this code:\n\n{code}",
        cache=True,
    ).text
```

---

## Error handling

```python
import cost_katana as ck
from cost_katana import openai
from cost_katana.exceptions import CostKatanaError

try:
    response = ck.ai(openai.gpt_4o, "Hello")
    print(response.text)
except CostKatanaError as e:
    msg = str(e).lower()
    if "api key" in msg:
        print("Set COST_KATANA_API_KEY or a provider key")
    elif "rate limit" in msg:
        print("Rate limited — retry with backoff")
    elif "model" in msg:
        print("Model not found or not available")
    else:
        print(f"Error: {e}")
```

---

## Experimentation (hosted API)

The Cost Katana backend exposes **experimentation** REST APIs under **`/api/experimentation`** on the hosted API (e.g. `https://api.costkatana.com`). The dashboard **Experimentation** experience is built on these endpoints; you can also call them with a dashboard **JWT** where required.

**Highlights**

- Model comparison, real-time comparison with **SSE** progress, experiment history, recommendations  
- What-if scenarios and simulations  
- Cost estimation before runs  
- Fine-tuning analysis helpers  
- Export experiment results (JSON/CSV)

Public vs authenticated routes depend on deployment; see the backend controller: [`experimentation.controller.ts`](https://github.com/Hypothesize-Tech/costkatana-backend-nest/blob/main/src/modules/experimentation/experimentation.controller.ts). Real provider execution may require server flags such as **`ENABLE_REAL_MODEL_COMPARISON=true`**.

For a longer overview, see [cost-katana-core `README.md` — Experimentation](https://github.com/Hypothesize-Tech/cost-katana-core/blob/main/README.md#experimentation-hosted-api).

---

## Migration guides

### From OpenAI SDK

```python
# Before
from openai import OpenAI
client = OpenAI(api_key="sk-...")
completion = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
)
print(completion.choices[0].message.content)

# After
import cost_katana as ck
from cost_katana import openai
response = ck.ai(openai.gpt_4, "Hello")
print(response.text)
print(f"Cost: ${response.cost}")
```

### From Anthropic SDK

```python
# Before
import anthropic
client = anthropic.Anthropic(api_key="sk-ant-...")
message = client.messages.create(
    model="claude-3-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello"}],
)

# After
import cost_katana as ck
from cost_katana import anthropic
response = ck.ai(anthropic.claude_3_5_sonnet_20241022, "Hello")
```

### From Google AI SDK

```python
# Before
import google.generativeai as genai
genai.configure(api_key="...")
model = genai.GenerativeModel("gemini-pro")
response = model.generate_content("Hello")

# After
import cost_katana as ck
from cost_katana import google
response = ck.ai(google.gemini_2_5_pro, "Hello")
```

---

## Package names (ecosystem)

| Language | Registry | Install | Import / usage |
|----------|----------|---------|----------------|
| **Python** | [PyPI `cost-katana`](https://pypi.org/project/cost-katana/) | `pip install cost-katana` | `import cost_katana` |
| **JavaScript** | npm | `npm install cost-katana` | `import { ai } from 'cost-katana'` |
| **CLI (npm)** | npm | `npm install -g cost-katana-cli` | `cost-katana chat` |
| **CLI (Python)** | PyPI | `pip install cost-katana` | `costkatana` (console script) |

---

## More examples

**[github.com/Hypothesize-Tech/costkatana-examples](https://github.com/Hypothesize-Tech/costkatana-examples)** — 45+ examples.

| Section | Description |
|---------|-------------|
| [Gateway (HTTP)](https://github.com/Hypothesize-Tech/costkatana-examples/tree/main/2-gateway) | Proxy routing, caching, retries |
| [Python SDK](https://github.com/Hypothesize-Tech/costkatana-examples/tree/master/8-python-sdk) | Python-focused guides |
| [Cost tracking](https://github.com/Hypothesize-Tech/costkatana-examples/tree/master/1-cost-tracking) | Cross-provider usage |
| [Semantic caching](https://github.com/Hypothesize-Tech/costkatana-examples/tree/master/14-cache) | Cache savings |
| [Frameworks](https://github.com/Hypothesize-Tech/costkatana-examples/tree/master/7-frameworks) | FastAPI and others |

---

## Support

| Channel | Link |
|---------|------|
| **Dashboard** | [costkatana.com](https://costkatana.com) |
| **Documentation** | [docs.costkatana.com](https://docs.costkatana.com) |
| **GitHub** | [github.com/Hypothesize-Tech/costkatana-python](https://github.com/Hypothesize-Tech/costkatana-python) |
| **Discord** | [discord.gg/D8nDArmKbY](https://discord.gg/D8nDArmKbY) |
| **Email** | support@costkatana.com |

---

## License

MIT © Cost Katana

---

<div align="center">

**Start cutting AI costs today**

```bash
pip install cost-katana
```

```python
import cost_katana as ck
from cost_katana import openai

response = ck.ai(openai.gpt_4o, "Hello, world!")
print(response.text, response.cost)
```

</div>

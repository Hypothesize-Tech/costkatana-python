# Cost Katana Python 🥷

> **AI that just works. Costs that just track.**

One import. Any model. Automatic cost tracking.

---

## 🚀 Get Started in 60 Seconds

### Step 1: Install

```bash
pip install costkatana
```

### Step 2: Set environment variables

```bash
export COST_KATANA_API_KEY="dak_your_key_here"   # required — from the dashboard
export PROJECT_ID="your_project_id"               # optional — per-project dashboard filtering
```

The API base URL is fixed at `https://api.costkatana.com` (not configurable via env).

### Step 3: Make Your First AI Call

```python
import cost_katana as ck
from cost_katana import openai

response = ck.ai(openai.gpt_4o, "Explain quantum computing in one sentence")

print(response.text)   # "Quantum computing uses qubits to perform..."
print(response.cost)   # 0.0012
print(response.tokens) # 47
```

**That's it.** With `COST_KATANA_API_KEY` set, you do **not** need to call `configure()` — `ck.ai()` / `ck.chat()` auto-configure from the environment. Usage and cost tracking is always on—there is no option to disable it (required for usage attribution and cost visibility).

If you only set `COST_KATANA_API_KEY` (no direct provider keys like `OPENAI_API_KEY`), requests use **Cost Katana hosted models** through the backend.

### AI Gateway (HTTP) — OpenAI- & Anthropic-compatible

The Python package’s high-level **`ck.ai()`** / **`ck.chat()`** APIs talk to Cost Katana’s backend. If you want the **same drop-in HTTP proxy** as the TypeScript **`gateway()`** helper (OpenAI-shaped or Anthropic-shaped JSON), call the gateway with **`httpx`** or **`requests`**.

**Gateway base URL** (default): `https://api.costkatana.com/api/gateway`  


**Headers**

| Header | Value |
|--------|--------|
| `Authorization` | `Bearer <COST_KATANA_API_KEY>` |
| `Content-Type` | `application/json` |
| `x-project-id` | Optional — same as `PROJECT_ID` for dashboard scoping |

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

**cURL** (no Python deps):

```bash
curl -sS "https://api.costkatana.com/api/gateway/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $COST_KATANA_API_KEY" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello!"}]}'
```

More gateway patterns (caching, retries, headers): [costkatana-examples `2-gateway`](https://github.com/Hypothesize-Tech/costkatana-examples/tree/main/2-gateway) and [cost-katana-core `examples/GATEWAY_USAGE_AND_TRACKING.md`](https://github.com/Hypothesize-Tech/cost-katana-core/blob/main/examples/GATEWAY_USAGE_AND_TRACKING.md).

---

## 📖 Tutorial: Build a Cost-Aware AI App

### Part 1: Basic Chat Session

```python
import cost_katana as ck

# Create a persistent chat session
chat = ck.chat('gpt-4')

chat.send('Hello! What can you help me with?')
chat.send('Tell me a programming joke')
chat.send('Now explain it')

# See exactly what you spent
print(f"💰 Total cost: ${chat.total_cost:.4f}")
print(f"📊 Messages: {len(chat.history)}")
print(f"🎯 Tokens used: {chat.total_tokens}")
```

### Part 2: Type-Safe Model Selection

Stop guessing model names. Get autocomplete and catch typos:

```python
import cost_katana as ck
from cost_katana import openai, anthropic, google

# Type-safe model constants (recommended)
response = ck.ai(openai.gpt_4, 'Hello, world!')

# Compare models easily
models = [openai.gpt_4, anthropic.claude_3_5_sonnet_20241022, google.gemini_2_5_pro]
for model in models:
    response = ck.ai(model, 'Explain AI in one sentence')
    print(f"Cost: ${response.cost:.4f}")
```

**Available namespaces:**
| Namespace | Models |
|-----------|--------|
| `openai` | GPT-4, GPT-3.5, O1, O3, DALL-E, Whisper |
| `anthropic` | Claude 3.5 Sonnet, Haiku, Opus |
| `google` | Gemini 2.5 Pro, Flash |
| `aws_bedrock` | Nova, Claude on Bedrock |
| `xai` | Grok models |
| `deepseek` | DeepSeek models |
| `mistral` | Mistral AI models |
| `groq` | Groq-hosted Llama / Mixtral / Gemma |
| `cohere` | Command models |
| `meta` | Llama models |

### Part 3: Smart Caching

Cache identical questions to avoid paying twice:

```python
import cost_katana as ck

# First call - hits the API
r1 = ck.ai('gpt-4', 'What is 2+2?', cache=True)
print(f"Cached: {r1.cached}")  # False
print(f"Cost: ${r1.cost}")     # $0.0008

# Second call - served from cache (FREE!)
r2 = ck.ai('gpt-4', 'What is 2+2?', cache=True)
print(f"Cached: {r2.cached}")  # True
print(f"Cost: ${r2.cost}")     # $0.0000 🎉
```

### Part 4: Cortex Optimization

For long-form content, Cortex compresses prompts intelligently:

```python
import cost_katana as ck

response = ck.ai(
    'gpt-4',
    'Write a comprehensive guide to machine learning for beginners',
    cortex=True,      # Enable 40-75% cost reduction
    max_tokens=2000
)

print(f"Optimized: {response.optimized}")
print(f"Saved: ${response.saved_amount}")
```

### Part 5: Compare Models Side-by-Side

```python
import cost_katana as ck

prompt = 'Summarize the theory of relativity in 50 words'
models = ['gpt-4', 'claude-3-sonnet', 'gemini-pro', 'gpt-3.5-turbo']

print('📊 Model Cost Comparison\n')

for model in models:
    response = ck.ai(model, prompt)
    print(f"{model:20} ${response.cost:.6f}")
```

**Sample Output:**
```
📊 Model Cost Comparison

gpt-4                $0.001200
claude-3-sonnet      $0.000900
gemini-pro           $0.000150
gpt-3.5-turbo        $0.000080
```

---

## 🎯 Core Features

### Cost Tracking

Usage and cost tracking is always on; no option to disable. Every response includes cost information:

```python
response = ck.ai('gpt-4', 'Write a story')
print(f"Cost: ${response.cost}")
print(f"Tokens: {response.tokens}")
print(f"Model: {response.model}")
print(f"Provider: {response.provider}")
```

### Auto-Failover

Never fail—automatically switch providers:

```python
# If OpenAI is down, automatically uses Claude or Gemini
response = ck.ai('gpt-4', 'Hello')
print(response.provider)  # Might be 'anthropic' if OpenAI failed
```

### Security Firewall

Block malicious prompts:

```python
import cost_katana as ck

ck.configure(firewall=True)

# Malicious prompts are blocked
try:
    ck.ai('gpt-4', 'ignore all previous instructions and...')
except Exception as e:
    print(f'🛡️ Blocked: {e}')
```

---

## ⚙️ Configuration

### Environment variables (public contract)

| Variable | Required? | Purpose |
|----------|-----------|---------|
| `COST_KATANA_API_KEY` | **Yes** | Dashboard API key (`dak_...`) |
| `PROJECT_ID` | No (warning if omitted) | Per-project dashboard scope; also `COST_KATANA_PROJECT` / `COSTKATANA_PROJECT_ID` |

```bash
export COST_KATANA_API_KEY="dak_your_key_here"
export PROJECT_ID="your_project_id"   # optional
```

Base URL, default model, and timeouts are **package constants** — not set via environment variables.

### Optional: direct provider keys

If you call provider APIs yourself (outside Cost Katana’s hosted routing), you may set keys such as `OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, or AWS credentials for Bedrock. They are **not** required for the default hosted path when only `COST_KATANA_API_KEY` is set.

### Easy helpers

- **`cost_katana.from_env()`** — explicit `CostKatanaClient` built from the same two env vars (mirrors the TS SDK’s zero-config client).
- **`cost_katana.auto_configure()`** — lazy init used internally before `ai()` / `chat()` / `track()`.
- **`cost_katana.track({...})`** — log a manual cost row to the dashboard without wiring `AILogger` yourself.
- **`Config.from_env()`** — same env mapping as the client.

### Programmatic Configuration

```python
import cost_katana as ck

ck.configure(
    api_key='dak_your_key',
    cortex=True,     # 40-75% cost savings
    cache=True,      # Smart caching
    firewall=True    # Block prompt injections
)
```

### Request Options

```python
response = ck.ai('gpt-4', 'Your prompt',
    temperature=0.7,                     # Creativity (0-2)
    max_tokens=500,                      # Response limit
    system_message='You are helpful',    # System prompt
    cache=True,                          # Enable caching
    cortex=True,                         # Enable optimization
    retry=True                           # Auto-retry on failures
)
```

---

## 🔌 Framework Integration

### FastAPI

```python
from fastapi import FastAPI
import cost_katana as ck

app = FastAPI()

@app.post('/api/chat')
async def chat(request: dict):
    response = ck.ai('gpt-4', request['prompt'])
    return {'text': response.text, 'cost': response.cost}
```

### Flask

```python
from flask import Flask, request, jsonify
import cost_katana as ck

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    response = ck.ai('gpt-4', request.json['prompt'])
    return jsonify({'text': response.text, 'cost': response.cost})
```

### Django

```python
from django.http import JsonResponse
import cost_katana as ck

def chat_view(request):
    response = ck.ai('gpt-4', request.POST.get('prompt'))
    return JsonResponse({'text': response.text, 'cost': response.cost})
```

---

## 💡 Real-World Examples

### Customer Support Bot

```python
import cost_katana as ck

support = ck.chat('gpt-3.5-turbo',
    system_message='You are a helpful customer support agent.')

def handle_query(query: str):
    response = support.send(query)
    print(f"Cost so far: ${support.total_cost:.4f}")
    return response
```

### Content Generator with Optimization

```python
import cost_katana as ck

def generate_blog_post(topic: str):
    # Use Cortex for long-form content (40-75% savings)
    post = ck.ai('gpt-4', f'Write a blog post about {topic}',
                 cortex=True, max_tokens=2000)
    
    return {
        'content': post.text,
        'cost': post.cost,
        'word_count': len(post.text.split())
    }
```

### Code Review Assistant

```python
import cost_katana as ck

def review_code(code: str):
    review = ck.ai('claude-3-sonnet',
        f'Review this code and suggest improvements:\n\n{code}',
        cache=True)  # Cache for repeated reviews
    return review.text
```

### Translation Service

```python
import cost_katana as ck

def translate(text: str, target_language: str):
    # Use cheaper model for translations
    translated = ck.ai('gpt-3.5-turbo',
        f'Translate to {target_language}: {text}',
        cache=True)
    return translated.text
```

---

## 💰 Cost Optimization Cheatsheet

| Strategy | Savings | Code |
|----------|---------|------|
| Use GPT-3.5 for simple tasks | 90% | `ck.ai('gpt-3.5-turbo', ...)` |
| Enable caching | 100% on hits | `cache=True` |
| Enable Cortex | 40-75% | `cortex=True` |
| Use Gemini for high-volume | 95% vs GPT-4 | `ck.ai('gemini-pro', ...)` |
| Batch in sessions | 10-20% | `ck.chat(...)` |

```python
# ❌ Expensive
ck.ai('gpt-4', 'What is 2+2?')  # $0.001

# ✅ Smart: Match model to task
ck.ai('gpt-3.5-turbo', 'What is 2+2?')  # $0.0001

# ✅ Smarter: Cache common queries
ck.ai('gpt-3.5-turbo', 'What is 2+2?', cache=True)  # $0 on repeat

# ✅ Smartest: Cortex for long content
ck.ai('gpt-4', 'Write a 2000-word essay', cortex=True)  # 40-75% off
```

---

## 🔧 Error Handling

```python
import cost_katana as ck
from cost_katana.exceptions import CostKatanaError

try:
    response = ck.ai('gpt-4', 'Hello')
    print(response.text)
except CostKatanaError as e:
    if 'API key' in str(e):
        print('Set COST_KATANA_API_KEY or OPENAI_API_KEY')
    elif 'rate limit' in str(e):
        print('Rate limited. Retrying...')
    elif 'model' in str(e):
        print('Model not found')
    else:
        print(f'Error: {e}')
```

---

## 🔄 Migration Guides

### From OpenAI SDK

```python
# Before
from openai import OpenAI
client = OpenAI(api_key='sk-...')
completion = client.chat.completions.create(
    model='gpt-4',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print(completion.choices[0].message.content)

# After
import cost_katana as ck
response = ck.ai('gpt-4', 'Hello')
print(response.text)
print(f"Cost: ${response.cost}")  # Bonus: cost tracking!
```

### From Anthropic SDK

```python
# Before
import anthropic
client = anthropic.Anthropic(api_key='sk-ant-...')
message = client.messages.create(
    model='claude-3-sonnet-20241022',
    messages=[{'role': 'user', 'content': 'Hello'}]
)

# After
import cost_katana as ck
response = ck.ai('claude-3-sonnet', 'Hello')
```

### From Google AI SDK

```python
# Before
import google.generativeai as genai
genai.configure(api_key='...')
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Hello')

# After
import cost_katana as ck
response = ck.ai('gemini-pro', 'Hello')
```

---

## 📦 Package Names

| Language | Package | Install | Import |
|----------|---------|---------|--------|
| **Python** | PyPI | `pip install costkatana` | `import cost_katana` |
| **JavaScript** | NPM | `npm install cost-katana` | `import { ai } from 'cost-katana'` |
| **CLI (NPM)** | NPM | `npm install -g cost-katana-cli` | `cost-katana chat` |
| **CLI (Python)** | PyPI | `pip install costkatana` | `costkatana chat` |

---

## 📚 More Examples

Explore 45+ complete examples:

**🔗 [github.com/Hypothesize-Tech/costkatana-examples](https://github.com/Hypothesize-Tech/costkatana-examples)**

| Section | Description |
|---------|-------------|
| [Gateway (HTTP)](https://github.com/Hypothesize-Tech/costkatana-examples/tree/main/2-gateway) | Proxy routing, caching, retries, `.http` samples |
| [Python SDK](https://github.com/Hypothesize-Tech/costkatana-examples/tree/master/8-python-sdk) | Complete Python guides |
| [Cost Tracking](https://github.com/Hypothesize-Tech/costkatana-examples/tree/master/1-cost-tracking) | Track costs across providers |
| [Semantic Caching](https://github.com/Hypothesize-Tech/costkatana-examples/tree/master/14-cache) | 30-40% cost reduction |
| [FastAPI Integration](https://github.com/Hypothesize-Tech/costkatana-examples/tree/master/7-frameworks) | Framework examples |

---

## 📞 Support

| Channel | Link |
|---------|------|
| **Dashboard** | [costkatana.com](https://costkatana.com) |
| **Documentation** | [docs.costkatana.com](https://docs.costkatana.com) |
| **GitHub** | [github.com/Hypothesize-Tech/costkatana-python](https://github.com/Hypothesize-Tech/costkatana-python) |
| **Discord** | [discord.gg/D8nDArmKbY](https://discord.gg/D8nDArmKbY) |
| **Email** | support@costkatana.com |

---

## 📄 License

MIT © Cost Katana

---

<div align="center">

**Start cutting AI costs today** 🥷

```bash
pip install costkatana
```

```python
import cost_katana as ck
response = ck.ai('gpt-4', 'Hello, world!')
```

</div>

# Cost Katana Python - Quick Start

Get started in 3 simple steps!

## Step 1: Install

```bash
pip install costkatana
```

> **Package Name**: `costkatana` (Python/PyPI) vs `cost-katana` (JavaScript/NPM)

## Step 2: Get API Key

Visit [costkatana.com/settings](https://costkatana.com/settings) and copy your API key (starts with `dak_`)

## Step 3: Use It

### Zero Config Mode

```python
import cost_katana as ck

# Just works if you have API key in environment
response = ck.ai('gpt-4', 'Hello, world!')
print(response.text)
print(f"Cost: ${response.cost}")
```

### Or Configure Once

```python
import cost_katana as ck

# Configure once at the start
ck.configure(api_key='dak_your_key_here')

# Then use anywhere
response = ck.ai('gpt-4', 'Explain quantum computing')
print(response.text)
```

## Common Patterns

### Chat Conversation

```python
import cost_katana as ck

chat = ck.chat('gpt-4')
chat.send('Hello!')
chat.send('What can you help with?')
chat.send('Tell me a joke')

print(f"Total cost: ${chat.total_cost}")
```

### Model Comparison

```python
import cost_katana as ck

models = ['gpt-4', 'gpt-3.5-turbo', 'claude-3-haiku']
prompt = 'Explain machine learning'

for model in models:
    response = ck.ai(model, prompt)
    print(f"{model}: ${response.cost:.4f}")
```

### Enable Optimization

```python
import cost_katana as ck

# Cortex: 70-95% cost reduction
response = ck.ai('gpt-4', 'Write a comprehensive guide',
                 cortex=True)

print(f"Optimized: {response.optimized}")
```

### Smart Caching

```python
import cost_katana as ck

# First call - costs money
r1 = ck.ai('gpt-4', 'What is 2+2?', cache=True)

# Second call - free from cache
r2 = ck.ai('gpt-4', 'What is 2+2?', cache=True)
print(r2.cached)  # True
```

## Environment Setup

### Option 1: Environment Variable

```bash
export COST_KATANA_KEY="dak_your_key_here"
```

Then in Python:
```python
import cost_katana as ck

# Auto-detects from environment
response = ck.ai('gpt-4', 'Hello')
```

### Option 2: Config File

Create `config.json`:
```json
{
  "api_key": "dak_your_key_here",
  "default_model": "gpt-3.5-turbo",
  "enable_cache": true,
  "enable_cortex": true
}
```

Then:
```python
import cost_katana as ck

ck.configure(config_file='config.json')
```

### Option 3: Direct Configuration

```python
import cost_katana as ck

ck.configure(
    api_key='dak_your_key_here',
    cortex=True,
    cache=True
)
```

## Real-World Examples

### FastAPI Integration

```python
from fastapi import FastAPI
import cost_katana as ck

app = FastAPI()

@app.post("/api/chat")
async def chat(request: dict):
    response = ck.ai('gpt-4', request['prompt'])
    return {
        'text': response.text,
        'cost': response.cost
    }
```

### Flask Integration

```python
from flask import Flask, request, jsonify
import cost_katana as ck

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    prompt = request.json['prompt']
    response = ck.ai('gpt-4', prompt, cache=True)
    return jsonify({
        'text': response.text,
        'cost': response.cost
    })
```

### Django Integration

```python
from django.http import JsonResponse
import cost_katana as ck

def chat_view(request):
    prompt = request.POST.get('prompt')
    response = ck.ai('gpt-4', prompt)
    return JsonResponse({
        'text': response.text,
        'cost': response.cost
    })
```

## Tips

### Save Money

```python
# Use cheaper models for simple tasks
ck.ai('gpt-3.5-turbo', 'Simple question')    # 10x cheaper

# Enable optimization for long content
ck.ai('gpt-4', 'Long article', cortex=True)  # 70-95% savings

# Cache repeated queries
ck.ai('gpt-4', 'FAQ answer', cache=True)     # Free on repeats
```

### Better Responses

```python
# Control creativity
ck.ai('gpt-4', 'Story', temperature=1.5)     # More creative

# Limit response length
ck.ai('gpt-4', 'Explain AI', max_tokens=100) # Short answer

# Use system prompts
ck.ai('gpt-4', 'Question', 
      system_message='You are an expert')
```

## Command Line Interface

The Python package includes a CLI command:

```bash
# After installing costkatana
pip install costkatana

# Python CLI command
costkatana chat
costkatana ask "What is Python?"
```

Or use the NPM global CLI (more features):

```bash
# Install NPM CLI globally
npm install -g cost-katana-cli

# JavaScript CLI command
cost-katana chat
cost-katana ask "What is Python?"
cost-katana compare "Test" --models gpt-4,claude-3-sonnet
```

## Supported Models

| Provider | Models | Best For |
|----------|--------|----------|
| **OpenAI** | gpt-4, gpt-3.5-turbo, gpt-4o | General purpose, function calling |
| **Anthropic** | claude-3-sonnet, claude-3-haiku | Analysis, coding, safety |
| **Google** | gemini-pro, gemini-flash | Creative tasks, multimodal |
| **AWS** | nova-pro, nova-lite | Enterprise, cost optimization |

## Need Help?

- **Documentation**: https://docs.costkatana.com/python
- **Examples**: Check the `examples/` folder
- **Discord**: https://discord.gg/Wcwzw8wM
- **Email**: support@costkatana.com
- **Dashboard**: https://costkatana.com/dashboard

---

**You're ready to use AI in Python!** 🚀

```python
import cost_katana as ck
response = ck.ai('gpt-4', 'Hello!')
```
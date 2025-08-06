# Cost Katana Python SDK - Quick Start Guide

## 🚀 Installation

```bash
pip install cost-katana
```

## 🔑 Get Your API Key

1. Visit [Cost Katana Dashboard](https://costkatana.com/dashboard)
2. Sign up or log in
3. Go to **API Keys** section
4. Click **Generate New Key**
5. Copy your key (starts with `dak_`)

## ⚡ 30-Second Demo

```python
import cost_katana as ck

# Configure once
ck.configure(api_key='dak_your_key_here')

# Use any AI model
model = ck.GenerativeModel('gemini-2.0-flash')
response = model.generate_content("Explain quantum computing in simple terms")

print(response.text)
print(f"Cost: ${response.usage_metadata.cost:.4f}")
```

That's it! 🎉

## 🤖 Chat Session

```python
import cost_katana as ck

ck.configure(api_key='dak_your_key_here')

# Start a conversation
model = ck.GenerativeModel('claude-3-sonnet')
chat = model.start_chat()

# Chat naturally
response1 = chat.send_message("Hi! What's your name?")
print(f"AI: {response1.text}")

response2 = chat.send_message("Can you help me write Python code?")
print(f"AI: {response2.text}")

# See total cost
total_cost = sum(r.get('metadata', {}).get('cost', 0) for r in chat.history)
print(f"Total conversation cost: ${total_cost:.4f}")
```

## 📁 Using Configuration File (Recommended)

Create `config.json`:
```json
{
  "api_key": "dak_your_key_here",
  "default_model": "gemini-2.0-flash",
  "cost_limit_per_day": 50.0,
  "enable_optimization": true,
  "model_mappings": {
    "fast": "gemini-2.0-flash",
    "smart": "claude-3-sonnet",
    "cheap": "claude-3-haiku"
  }
}
```

Then use it:
```python
import cost_katana as ck

ck.configure(config_file='config.json')

# Use friendly names from config
fast_model = ck.GenerativeModel('fast')
smart_model = ck.GenerativeModel('smart')
```

## 🖥️ Command Line Interface

```bash
# Initialize configuration
cost-katana init

# Test connection
cost-katana test

# List available models  
cost-katana models

# Start interactive chat
cost-katana chat --model gemini-2.0-flash
```

## 🔄 Compare Providers

```python
import cost_katana as ck

ck.configure(config_file='config.json')

models = ['gemini-2.0-flash', 'claude-3-sonnet', 'gpt-4']
prompt = "Write a Python function to reverse a string"

for model_name in models:
    model = ck.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    
    print(f"\n{model_name}:")
    print(f"Response: {response.text[:100]}...")
    print(f"Cost: ${response.usage_metadata.cost:.4f}")
    print(f"Speed: {response.usage_metadata.latency:.2f}s")
```

## 🏷️ Supported Models

| Provider | Models | Best For |
|----------|--------|----------|
| **Google** | `gemini-2.0-flash`, `gemini-pro` | Creative tasks, multimodal |
| **Anthropic** | `claude-3-sonnet`, `claude-3-haiku` | Analysis, coding, safety |
| **OpenAI** | `gpt-4`, `gpt-3.5-turbo` | Function calling, structured output |
| **AWS** | `nova-pro`, `nova-lite` | Enterprise, cost optimization |

## 💰 Cost Optimization Features

- **Automatic routing** to cheapest suitable model
- **Smart caching** to avoid duplicate requests
- **Request optimization** to reduce token usage
- **Budget controls** with daily/monthly limits
- **Real-time cost tracking** across all providers

## 🛡️ Error Handling

```python
from cost_katana.exceptions import CostLimitExceededError, ModelNotAvailableError

try:
    model = ck.GenerativeModel('expensive-model')
    response = model.generate_content("Complex analysis task")
    
except CostLimitExceededError:
    print("Cost limit reached! Using cheaper alternative...")
    backup_model = ck.GenerativeModel('claude-3-haiku')
    response = backup_model.generate_content("Complex analysis task")
    
except ModelNotAvailableError:
    print("Model unavailable - automatic failover activated")
```

## 📊 Analytics & Insights

Every response includes detailed metadata:

```python
response = model.generate_content("Hello world")

metadata = response.usage_metadata
print(f"Model used: {metadata.model}")
print(f"Cost: ${metadata.cost:.4f}")
print(f"Tokens: {metadata.total_tokens}")
print(f"Latency: {metadata.latency:.2f}s")
print(f"Cache hit: {metadata.cache_hit}")
print(f"Optimizations: {metadata.optimizations_applied}")
```

## 🌟 Why Choose Cost Katana?

✅ **Simple**: One interface for all AI providers  
✅ **Smart**: Automatic cost optimization (save 30-60%)  
✅ **Reliable**: Built-in failover and error handling  
✅ **Scalable**: From prototype to enterprise production  
✅ **Transparent**: Complete cost and usage visibility  

## 📚 Next Steps

- **Full Documentation**: [docs.costkatana.com](https://docs.costkatana.com)
- **Example Projects**: Check the `examples/` folder
- **Community Support**: [discord.gg/costkatana](https://discord.gg/costkatana)
- **Enterprise Features**: [costkatana.com/enterprise](https://costkatana.com/enterprise)

## 🆘 Need Help?

- 📖 **Documentation**: https://docs.costkatana.com
- 💬 **Discord**: https://discord.gg/costkatana
- ✉️ **Email**: abdul@hypothesize.tech
- 🐛 **Issues**: https://github.com/cost-katana/python-sdk/issues

---

**Ready to optimize your AI costs?** 🚀 [Get started now!](https://costkatana.com)
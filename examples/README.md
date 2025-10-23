# Cost Katana Python Examples

Simple, practical examples showing how to use Cost Katana in Python.

## Running Examples

```bash
# Install the package
pip install costkatana

# Set your API key
export COST_KATANA_API_KEY="dak_your_key"

# Run an example
python examples/basic_usage.py
python examples/simple_examples.py
```

## Examples

### 1. Basic Usage (`basic_usage.py`)
Step-by-step guide showing all basic features with explanations.

### 2. Simple Examples (`simple_examples.py`)
Collection of common patterns: chat, comparison, optimization, caching.

### 3. Config Example (`config.json`)
Sample configuration file showing all available options.

## Quick Reference

```python
import cost_katana as ck

# Simple request
response = ck.ai('gpt-4', 'Hello')

# Chat session
session = ck.chat('gpt-4')
session.send('Hello')

# Configuration
ck.configure(
    api_key='dak_your_key',
    cortex=True,
    cache=True
)
```

## Package Names

**Important**: Different package names for different languages:

| Language | Package | Install |
|----------|---------|---------|
| Python | `costkatana` | `pip install costkatana` |
| JavaScript/Node | `cost-katana` | `npm install cost-katana` |
| CLI (Global) | `cost-katana-cli` | `npm install -g cost-katana-cli` |

## Support

- Documentation: https://docs.costkatana.com
- Dashboard: https://costkatana.com
- GitHub: https://github.com/Hypothesize-Tech/cost-katana-python

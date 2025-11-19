# Changelog

All notable changes to Cost Katana Python SDK will be documented in this file.

## [2.2.1] - 2025-01-19

### 📚 Documentation Updates
- **Clarified API Key Requirements**: Updated documentation to clearly state that OpenAI and Gemini providers require user-provided API keys
- Added prominent warnings that Cost Katana does not provide OpenAI or Google API keys
- Updated environment variable documentation with detailed explanations for all providers
- Added clear consequences for missing API keys
- Improved consistency across all documentation files

### 🔧 Configuration
- Enhanced environment variable documentation with user-provided key requirements:
  - `OPENAI_API_KEY` - Required for OpenAI models (GPT-4, GPT-3.5, etc.) - **USER PROVIDED**
  - `GEMINI_API_KEY` - Required for Google Gemini models (Gemini 2.5 Pro, Flash, etc.) - **USER PROVIDED**
  - `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` - Required for AWS Bedrock models (Claude, Nova, etc.) - **USER PROVIDED**
  - `ANTHROPIC_API_KEY` - Optional for direct Anthropic API access - **USER PROVIDED**
- Added specific notes about which providers require user API keys
- Updated README.md with comprehensive API key setup instructions
- All API keys must be provided by users - Cost Katana does not include any provider API keys

---

## [2.0.7] - 2025-01-23

### 📚 Documentation Updates
- Updated README with refined examples repository links
- Improved documentation clarity and structure
- Enhanced package metadata

---

## [2.0.6] - 2025-01-23

### 📚 Documentation Updates
- Updated package metadata and documentation
- Improved examples and usage guides
- Enhanced README with better examples repository links

---

## [2.0.5] - 2025-01-23

### 📚 Documentation Updates
- Added prominent "More Examples" section in README linking to complete examples repository
- Added direct links to [costkatana-examples repository](https://github.com/Hypothesize-Tech/costkatana-examples)
- Highlighted 300+ production-ready code samples across HTTP, TypeScript, Python, and frameworks
- Special emphasis on Python SDK examples (Section 8) and FastAPI integration

### 🔗 Resources
- New Examples Repository: https://github.com/Hypothesize-Tech/costkatana-examples
- 44 feature sections with comprehensive examples
- Framework integrations: Express, Next.js, Fastify, NestJS, FastAPI

---

## [2.0.0] - 2025-01-XX

### 🚀 Major Release: Complete Simplification

Complete redesign to make using AI in Python as simple as possible.

### ✨ New Features

#### Ultra-Simple API

**New `ai()` function** - The easiest way to use AI:
```python
import cost_katana as ck
response = ck.ai('gpt-4', 'Hello')
print(response.text)
print(f"Cost: ${response.cost}")
```

**New `chat()` function** - Simple chat sessions:
```python
import cost_katana as ck
session = ck.chat('gpt-4')
session.send('Hello')
session.send('How are you?')
print(f"Total: ${session.total_cost}")
```

#### Auto-Configuration
- Automatically detects API keys from environment
- Works with `COST_KATANA_API_KEY` or provider keys directly
- Zero setup if environment is configured
- Smart error messages with actionable steps

#### SimpleResponse Object
- Clean, simple response object
- Direct access to `text`, `cost`, `tokens`
- Bonus fields: `cached`, `optimized`, `provider`

### 💥 Breaking Changes

None! The traditional API (`GenerativeModel`) still works for backward compatibility.

**You can still use**:
```python
model = ck.GenerativeModel('gpt-4')
response = model.generate_content('Hello')
```

**Or use the new simple API**:
```python
response = ck.ai('gpt-4', 'Hello')
```

### 📚 Documentation

- **Completely rewritten README**: Focus on simplicity
- **Updated QUICKSTART**: 3-step process
- **New examples**: Real-world use cases with simple API
- **Migration guides**: From OpenAI, Anthropic, Google SDKs

### 🎯 Comparison

#### Before (v1.x)
```python
import cost_katana as ck

ck.configure(api_key='dak_...')
model = ck.GenerativeModel('gpt-4')
response = model.generate_content('Hello')
print(response.text)
```

#### After (v2.0)
```python
import cost_katana as ck

response = ck.ai('gpt-4', 'Hello')
print(response.text)
```

### 📦 Examples

New streamlined examples:
- `simple_examples.py` - All basic patterns
- `basic_usage.py` - Getting started
- Updated all existing examples to show both APIs

### 🐛 Bug Fixes

- Improved error messages
- Better environment variable detection
- More robust provider inference

---

## [1.0.0] - 2024-XX-XX

### Initial Release
- Multi-provider support
- Cost tracking
- Unified API
- Configuration management

# Changelog

All notable changes to Cost Katana Python SDK will be documented in this file.

## [Unreleased]

## [2.5.6] - 2026-04-29

### Fixed

- **GitHub Actions**: Use automatic `github.token` instead of invalid `secrets.GITHUB_TOKEN` for `actions/checkout` and releases (`auto-release.yml`, `version-bump.yml`, `publish.yml`).
- **Auto Release**: Build artifacts **after** bumping `setup.py` / `cost_katana/__init__.py` so PyPI uploads are not stale duplicates (fixes HTTP 400 on upload).
- **Version Bump workflow**: Install **`setuptools`** for `setup.py --version`; keep **`__version__`** in sync when bumping.
- **CI typing**: Resolve **`mypy`** errors across `cost_katana` (`Logger`, `AILogger`, `TemplateManager`, `CostKatanaClient`, `SimpleResponse.templateUsed`, Optional template parameters).
- **CI security**: **`bandit`** clean on current sources; **`safety`** scoped to `requirements.txt` so transitive dev-only CVE noise does not fail the workflow.

## [2.5.5] - 2026-04-29

### Changed

- **`cost_katana.models_constants`**: Align type-safe model IDs with cost-katana core (GPT-5.5/5.4, Gemini 3.1 Pro, Claude Opus 4.7, expanded Gemini 2.5 and Bedrock entries); restore shorthand constants expected by integrations (`grok_2_1212`, `command_r_plus`, `mistral_small_latest`, etc.).

## [2.5.4] - 2026-04-22

### Added

- **`CostKatanaClient.send_message`**: `thinking`, `thinking_effort`, and `thinking_budget_tokens` — enables Claude extended thinking on supported models; payload includes `thinking` with `enabled`, optional `effort`, and optional `budgetTokens`.
- **`ck.ai()`**: same options via `**options`; **`SimpleResponse.thinking`** is set when the API returns reasoning content.

### Changed

- **AWS Bedrock**: alias `llama-3.2-1b` / `aws_bedrock.llama_3_2_1b_instruct` now maps to `meta.llama4-scout-17b-instruct-v1:0` (replaces retired `meta.llama3-2-1b-instruct-v1:0`).

## [2.5.3] - 2026-03-29

### Documentation

- README and QUICKSTART: PyPI install name `cost-katana`, table of contents, experimentation section, aligned examples.

## [2.5.2] - 2026-03-27

### Added

- **`cost_katana.gateway`**: `gateway_request_headers()` for opt-out `CostKatana-LLM-Security-Enabled` / `CostKatana-Output-Moderation-Enabled` on direct gateway HTTP calls; `GATEWAY_API_PREFIX`.
- **`CostKatanaClient.get_gateway_security_summary()`** — `GET /api/gateway/security/summary` (firewall + moderation aggregates).
- **README**: gateway security defaults and security summary API.

### Documentation

- **API paths**: Confirmed the SDK uses `https://api.costkatana.com` with REST paths under `/api/...` (e.g. chat, templates) and OpenAI-compatible gateway calls under `/api/gateway/v1/...`.

## [2.5.1] - 2025-03-25

### Added

- **README**: AI Gateway (HTTP) section — OpenAI-compatible (`/v1/chat/completions`) and Anthropic (`/v1/messages`) examples with `httpx`, optional `COSTKATANA_GATEWAY_URL` and `x-project-id`, plus `curl`; link to `costkatana-examples/2-gateway`.

## [2.5.0] - 2025-03-25

### Added

- **`auto_configure()`** — lazy global client initialization from `COST_KATANA_API_KEY` (used before `ai()`, `chat()`, `track()`).
- **`from_env()`** — returns a `CostKatanaClient` built from environment (same two-variable contract as `Config.from_env()`).
- **`track(entry)`** — manual cost logging without wiring `AILogger`; works with lazy env-based setup.
- **`groq`** model namespace and **`Groq`** provider label in `get_provider_from_model`.
- **`project_id`** on `Config` with env fallbacks: `PROJECT_ID`, `COST_KATANA_PROJECT`, `COSTKATANA_PROJECT_ID`.

### Changed

- **Public env contract**: only **`COST_KATANA_API_KEY`** (required) and **`PROJECT_ID`** (optional). Removed reading `API_KEY`, `COST_KATANA_BASE_URL`, `COST_KATANA_DEFAULT_MODEL`, and `COST_KATANA_TIMEOUT` from the environment — base URL (`https://api.costkatana.com`), default model, and timeouts are package constants.
- **`get_global_client()`** calls `auto_configure()` so `ai()` / `chat()` work without an explicit `configure()` when the API key is in the environment.
- **`CostKatanaClient`** sends optional **`x-project-id`** when `project_id` is set; warns once when `PROJECT_ID` is missing.
- **`ai_logger`** singleton is **lazy** — initializes on first use with `COST_KATANA_API_KEY` / `PROJECT_ID` from the environment.
- **Duplicate `mistral` class** in `models_constants.py` merged into a single definition.

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

# Cost Katana Python SDK - Development Makefile

.PHONY: help install install-dev test lint format clean build upload upload-test docs examples

help:  ## Show this help message
	@echo "Cost Katana Python SDK - Available Commands:"
	@echo "============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e .
	pip install -r requirements-dev.txt

test:  ## Run tests
	python3 -m pytest tests/ -v --cov=cost_katana --cov-report=html --cov-report=term

test-examples:  ## Test example scripts
	@echo "Testing example scripts..."
	python3 -m py_compile examples/*.py
	@echo "✅ All examples compile successfully"

lint:  ## Run linting
	flake8 cost_katana/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 cost_katana/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:  ## Format code
	black cost_katana/
	black examples/
	isort cost_katana/
	isort examples/

type-check:  ## Run type checking
	mypy cost_katana/ --ignore-missing-imports

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python3 -m build

upload-test:  ## Upload to TestPyPI
	python3 -m twine upload --repository testpypi dist/*

upload:  ## Upload to PyPI
	python3 -m twine upload dist/*

docs:  ## Generate documentation
	@echo "Generating documentation..."
	python3 -c "import cost_katana; help(cost_katana)" > docs/api_reference.txt
	@echo "✅ Documentation generated in docs/"

demo:  ## Run interactive demo
	python3 examples/basic_usage.py

demo-chat:  ## Run chat demo
	python3 examples/chat_session.py

demo-comparison:  ## Run provider comparison demo
	python3 examples/provider_comparison.py

demo-config:  ## Run configuration demo
	python3 examples/config_example.py

demo-old-vs-new:  ## Run old vs new comparison
	python3 examples/old_vs_new.py

setup-config:  ## Create sample configuration
	@echo "Creating sample configuration..."
	@echo '{' > config.json
	@echo '  "api_key": "dak_your_api_key_here",' >> config.json
	@echo '  "base_url": "https://cost-katana-backend.store",' >> config.json
	@echo '  "default_model": "gemini-2.0-flash",' >> config.json
	@echo '  "default_temperature": 0.7,' >> config.json
	@echo '  "cost_limit_per_day": 50.0,' >> config.json
	@echo '  "enable_optimization": true,' >> config.json
	@echo '  "enable_failover": true' >> config.json
	@echo '}' >> config.json
	@echo "✅ Created config.json - edit with your API key"

cli-init:  ## Initialize CLI configuration
	cost-katana init

cli-test:  ## Test CLI connection
	cost-katana test

cli-models:  ## List available models via CLI
	cost-katana models

cli-chat:  ## Start CLI chat session
	cost-katana chat

verify-install:  ## Verify installation
	@echo "Verifying Cost Katana installation..."
	python3 -c "import cost_katana; print(f'✅ Cost Katana {cost_katana.__version__} installed successfully')"
	python3 -c "from cost_katana import GenerativeModel, configure; print('✅ All imports working')"
	@echo "🚀 Ready to use Cost Katana!"

check-deps:  ## Check dependencies
	pip check
	pip list --outdated

# Development workflow commands
dev-setup: install-dev setup-config  ## Complete development setup
	@echo "🚀 Development environment ready!"
	@echo "Next steps:"
	@echo "  1. Edit config.json with your API key"
	@echo "  2. Run: make verify-install"
	@echo "  3. Run: make demo"

release-check: clean lint type-check test build  ## Pre-release checks
	@echo "✅ Release checks passed!"

# CI/CD helpers
ci-test:  ## Run tests for CI
	python3 -m pytest tests/ -v --cov=cost_katana --cov-report=xml

# Package info
info:  ## Show package information
	@echo "Cost Katana Python SDK"
	@echo "====================="
	@echo "Version: $(shell python3 -c 'import cost_katana; print(cost_katana.__version__)')"
	@echo "Location: $(shell python3 -c 'import cost_katana; print(cost_katana.__file__)')"
	@echo "Dependencies: $(shell pip freeze | grep -E '(requests|httpx|pydantic|rich)' | wc -l) core packages"
	@echo ""
	@echo "🌐 Website: https://costkatana.com"
	@echo "📚 Docs: https://docs.costkatana.com" 
	@echo "💬 Discord: https://discord.gg/D8nDArmKbY"

# Quick start for new users
# CI/CD helpers
ci-test:  ## Run tests for CI
	python3 -m pytest tests/ -v --cov=cost_katana --cov-report=xml

ci-lint:  ## Run linting for CI
	flake8 cost_katana/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 cost_katana/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

ci-format:  ## Run format check for CI
	black --check cost_katana/
	black --check examples/

ci-type:  ## Run type checking for CI
	mypy cost_katana/ --ignore-missing-imports

ci-build:  ## Build package for CI
	python3 -m build

ci-check:  ## Check package for CI
	python3 -m twine check dist/*

ci-security:  ## Run security checks
	pip install safety bandit
	safety check --full-report
	bandit -r cost_katana/ -f txt

# Release helpers
release-prepare:  ## Prepare a new release
	@echo "🚀 Preparing release..."
	@./scripts/prepare-release.sh

release-push:  ## Push release to GitHub
	@echo "📤 Pushing release to GitHub..."
	git push origin main
	git push --tags

release-full: release-prepare release-push  ## Complete release process

release-patch:  ## Bump patch version and release (e.g., 2.0.7 -> 2.0.8)
	@echo "🔖 Bumping patch version..."
	@python3 scripts/bump_version.py patch
	@VERSION=$$(grep -o 'version="[^"]*"' setup.py | cut -d'"' -f2); \
	git add setup.py && \
	git commit -m "chore: bump version to $$VERSION" && \
	git tag v$$VERSION && \
	git push origin master --follow-tags && \
	echo "✅ Released v$$VERSION"

release-minor:  ## Bump minor version and release (e.g., 2.0.7 -> 2.1.0)
	@echo "🔖 Bumping minor version..."
	@python3 scripts/bump_version.py minor
	@VERSION=$$(grep -o 'version="[^"]*"' setup.py | cut -d'"' -f2); \
	git add setup.py && \
	git commit -m "chore: bump version to $$VERSION" && \
	git tag v$$VERSION && \
	git push origin master --follow-tags && \
	echo "✅ Released v$$VERSION"

release-major:  ## Bump major version and release (e.g., 2.0.7 -> 3.0.0)
	@echo "🔖 Bumping major version..."
	@python3 scripts/bump_version.py major
	@VERSION=$$(grep -o 'version="[^"]*"' setup.py | cut -d'"' -f2); \
	git add setup.py && \
	git commit -m "chore: bump version to $$VERSION" && \
	git tag v$$VERSION && \
	git push origin master --follow-tags && \
	echo "✅ Released v$$VERSION"

quick-start:  ## Quick start guide
	@echo "🚀 Cost Katana Python SDK - Quick Start"
	@echo "========================================"
	@echo ""
	@echo "1. Install the package:"
	@echo "   pip install cost-katana"
	@echo ""
	@echo "2. Get your API key:"
	@echo "   Visit: https://costkatana.com/integrations"
	@echo ""
	@echo "3. Configure:"
	@echo "   cost-katana init"
	@echo ""
	@echo "4. Test:"
	@echo "   cost-katana test"
	@echo ""
	@echo "5. Start chatting:"
	@echo "   cost-katana chat"
	@echo ""
	@echo "🔗 Full documentation: https://docs.costkatana.com"
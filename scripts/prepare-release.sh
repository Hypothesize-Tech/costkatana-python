#!/bin/bash

# Cost Katana Release Preparation Script
# This script helps prepare a new release by updating version and creating a tag

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Cost Katana Release Preparation${NC}"
echo "=================================="

# Get current version
CURRENT_VERSION=$(python3 -c "import re; setup_content = open('setup.py').read(); version_match = re.search(r\"version=['\"]([^'\"]*)['\"]\", setup_content); print(version_match.group(1))")
echo -e "${GREEN}Current version: ${CURRENT_VERSION}${NC}"

# Ask for new version
read -p "Enter new version (e.g., 1.0.2): " NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    echo -e "${RED}No version provided. Exiting.${NC}"
    exit 1
fi

# Validate version format
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Invalid version format. Use semantic versioning (e.g., 1.0.2)${NC}"
    exit 1
fi

echo -e "${YELLOW}Preparing release ${NEW_VERSION}...${NC}"

# Update setup.py
sed -i.bak "s/version=\"$CURRENT_VERSION\"/version=\"$NEW_VERSION\"/" setup.py
rm setup.py.bak

# Update __init__.py if it has version
if [ -f "cost_katana/__init__.py" ]; then
    if grep -q "__version__" cost_katana/__init__.py; then
        sed -i.bak "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" cost_katana/__init__.py
        rm cost_katana/__init__.py.bak
    fi
fi

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
python3 -m pytest tests/ -v

# Build package
echo -e "${YELLOW}Building package...${NC}"
python3 -m build

# Check package
echo -e "${YELLOW}Checking package...${NC}"
python3 -m twine check dist/*

# Create git tag
echo -e "${YELLOW}Creating git tag...${NC}"
git add setup.py cost_katana/__init__.py
git commit -m "Bump version to $NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"

echo -e "${GREEN}✅ Release preparation complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Review changes: git diff HEAD~1"
echo "2. Push changes: git push origin main"
echo "3. Push tag: git push origin v$NEW_VERSION"
echo "4. Check GitHub Actions for automated publishing"
echo ""
echo -e "${YELLOW}Or manually upload to PyPI:${NC}"
echo "python3 -m twine upload dist/*" 
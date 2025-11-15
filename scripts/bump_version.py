#!/usr/bin/env python3
"""
Simple version bumper for setup.py
"""

import re
import sys
from pathlib import Path


def bump_version(version_type):
    """Bump version in setup.py"""
    setup_py = Path(__file__).parent.parent / "setup.py"
    
    with open(setup_py, "r") as f:
        content = f.read()
    
    # Find current version
    match = re.search(r'version\s*=\s*["\'](\d+)\.(\d+)\.(\d+)["\']', content)
    if not match:
        print("Error: Could not find version in setup.py")
        sys.exit(1)
    
    major, minor, patch = map(int, match.groups())
    
    # Bump version
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        print(f"Error: Invalid version type '{version_type}'. Use: major, minor, or patch")
        sys.exit(1)
    
    new_version = f"{major}.{minor}.{patch}"
    old_version = f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
    
    # Replace version in setup.py
    new_content = re.sub(
        r'(version\s*=\s*["\'])\d+\.\d+\.\d+(["\'])',
        f"\\g<1>{new_version}\\g<2>",
        content
    )
    
    with open(setup_py, "w") as f:
        f.write(new_content)
    
    print(f"✅ Bumped version: {old_version} → {new_version}")
    return new_version


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py [major|minor|patch]")
        sys.exit(1)
    
    bump_version(sys.argv[1])


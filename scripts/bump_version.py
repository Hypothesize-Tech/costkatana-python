#!/usr/bin/env python3
"""
Bump semantic version in setup.py and cost_katana/__init__.py (__version__).
"""

import re
import sys
from pathlib import Path


def bump_version(version_type):
    """Bump version in setup.py and mirror __version__ in the package."""
    root = Path(__file__).parent.parent
    setup_py = root / "setup.py"
    init_py = root / "cost_katana" / "__init__.py"

    with open(setup_py, "r") as f:
        content = f.read()

    match = re.search(r'version\s*=\s*["\'](\d+)\.(\d+)\.(\d+)["\']', content)
    if not match:
        print("Error: Could not find version in setup.py")
        sys.exit(1)

    major, minor, patch = map(int, match.groups())

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

    new_content = re.sub(
        r'(version\s*=\s*["\'])\d+\.\d+\.\d+(["\'])',
        f"\\g<1>{new_version}\\g<2>",
        content,
    )

    with open(setup_py, "w") as f:
        f.write(new_content)

    if init_py.is_file():
        init_src = init_py.read_text()
        init_updated = re.sub(
            r'(__version__\s*=\s*["\'])\d+\.\d+\.\d+(["\'])',
            f"\\g<1>{new_version}\\g<2>",
            init_src,
        )
        if init_src != init_updated:
            init_py.write_text(init_updated)
        elif old_version in init_src:
            print(
                "Warning: setup.py bumped but __version__ pattern not found in __init__.py — update manually.",
                file=sys.stderr,
            )

    print(f"✅ Bumped version: {old_version} → {new_version}")
    return new_version


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py [major|minor|patch]")
        sys.exit(1)
    
    bump_version(sys.argv[1])


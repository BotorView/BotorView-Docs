"""Sphinx configuration for the BotorView documentation (built on Read the Docs)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    return match.group(1) if match else "unknown"


project = "BotorView"
author = "Team BotorView"
copyright = "2026, Team BotorView"
version = "0.1.0"
release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinx.ext.mathjax",
    "sphinxcontrib.mermaid",
]

# Markdown (MyST) with LaTeX mathematics: $inline$, $$display$$ and {math} blocks.
source_suffix = {".md": "markdown"}
myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence", "deflist", "attrs_inline"]
myst_heading_anchors = 3
myst_fence_as_directive = ["mermaid"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "requirements.txt"]

html_theme = "furo"
html_title = f"BotorView {release}"
html_static_path = ["_static"]
html_logo = "../src/botorview/assets/branding/botorview_banner.png"
html_favicon = "../src/botorview/assets/branding/botorview_icon.png"
html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {"color-brand-primary": "#0A66C2", "color-brand-content": "#0A66C2"},
    "dark_css_variables": {"color-brand-primary": "#3D9BF0", "color-brand-content": "#3D9BF0"},
}

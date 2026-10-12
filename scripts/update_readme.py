#!/usr/bin/env python3
"""Refresh the dynamic sections of the profile README.

Sections are delimited by HTML comment markers:
    <!-- RECENT_REPOS:START --> ... <!-- RECENT_REPOS:END -->
    <!-- LAST_UPDATED:START -->  ... <!-- LAST_UPDATED:END -->

Environment variables:
    GITHUB_USER   GitHub username (default: Gethubsathvik)
    GITHUB_TOKEN  Optional token; raises the API rate limit
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER = os.environ.get("GITHUB_USER", "Gethubsathvik")
TOKEN = os.environ.get("GITHUB_TOKEN")
README = Path(__file__).resolve().parent.parent / "README.md"
MAX_REPOS = 6


def fetch_repos(user: str) -> list[dict]:
    url = f"https://api.github.com/users/{user}/repos?sort=pushed&direction=desc&per_page=30&type=owner"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": f"{user}-profile-readme"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def render_repos(repos: list[dict], user: str) -> str:
    lines = []
    for repo in repos:
        if repo.get("fork") or repo.get("archived") or repo["name"].lower() == user.lower():
            continue
        description = (repo.get("description") or "No description yet").strip()
        if len(description) > 110:
            description = description[:107].rstrip() + "..."
        language = repo.get("language")
        suffix = f" · `{language}`" if language else ""
        stars = repo.get("stargazers_count", 0)
        star_text = f" · ⭐ {stars}" if stars else ""
        lines.append(f"- [{repo['name']}]({repo['html_url']}) — {description}{suffix}{star_text}")
        if len(lines) == MAX_REPOS:
            break
    return "\n".join(lines) if lines else "- No public repositories to show yet."


def replace_section(text: str, name: str, body: str) -> str:
    pattern = re.compile(
        rf"(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)",
        re.DOTALL,
    )
    if not pattern.search(text):
        raise ValueError(f"Markers for {name} not found in README")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text, count=1)


def main() -> int:
    text = README.read_text(encoding="utf-8")
    repos = fetch_repos(USER)
    text = replace_section(text, "RECENT_REPOS", render_repos(repos, USER))
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    text = replace_section(text, "LAST_UPDATED", f"Last refreshed on **{stamp}** by GitHub Actions.")
    README.write_text(text, encoding="utf-8")
    print("README updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

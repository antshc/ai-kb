from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

_INDEX_FILE = config.WIKI_DIR / "index.md"
_LOG_FILE = config.WIKI_DIR / "log.md"
_CATEGORY_DIRS = {
    "entity": config.WIKI_DIR / "entities",
    "summary": config.WIKI_DIR / "summaries",
    "topic": config.WIKI_DIR / "topics",
}


def _ensure_dirs() -> None:
    config.WIKI_DIR.mkdir(parents=True, exist_ok=True)
    for directory in _CATEGORY_DIRS.values():
        directory.mkdir(parents=True, exist_ok=True)


def _slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower().strip()).strip("-")


def _load_index() -> list[dict]:
    if not _INDEX_FILE.exists():
        return []
    entries = []
    for line in _INDEX_FILE.read_text().splitlines():
        if not line.startswith("| [["):
            continue
        parts = [part.strip() for part in line.split("|") if part.strip()]
        if len(parts) >= 3:
            entries.append({
                "slug": parts[0].replace("[[", "").replace("]]", ""),
                "category": parts[1],
                "summary": parts[2],
                "date": parts[3] if len(parts) > 3 else "",
            })
    return entries


def _save_index(entries: list[dict]) -> None:
    _ensure_dirs()
    lines = [
        "# Wiki Index\n\n",
        "_Auto-managed by `wiki_store`. Do not edit the table manually._\n\n",
        "| Page | Category | Summary | Date |\n",
        "|---|---|---|---|\n",
    ]
    lines.extend(
        f"| [[{entry['slug']}]] | {entry['category']} | {entry['summary']} | {entry['date']} |\n"
        for entry in entries
    )
    _INDEX_FILE.write_text("".join(lines))


def write_page(category: str, title: str, content: str, summary: str = "") -> str:
    _ensure_dirs()
    slug = _slug(title)
    directory = _CATEGORY_DIRS.get(category, config.WIKI_DIR)
    path = directory / f"{slug}.md"
    path.write_text(content)
    if not summary:
        summary = next((line.strip()[:100] for line in content.splitlines() if line.strip() and not line.startswith("#")), "")
    entries = _load_index()
    existing = next((entry for entry in entries if entry["slug"] == slug), None)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if existing:
        existing.update({"category": category, "summary": summary, "date": date})
    else:
        entries.append({"slug": slug, "category": category, "summary": summary, "date": date})
    _save_index(entries)
    with _LOG_FILE.open("a") as stream:
        stream.write(f"\n## [{date}] write | {title}\n")
    return str(path.relative_to(config.WIKI_DIR))


def read_page(category: str, title: str) -> str | None:
    path = _CATEGORY_DIRS.get(category, config.WIKI_DIR) / f"{_slug(title)}.md"
    return path.read_text() if path.exists() else None


def read_page_by_slug(slug: str) -> str | None:
    for directory in [*_CATEGORY_DIRS.values(), config.WIKI_DIR]:
        path = directory / f"{slug}.md"
        if path.exists():
            return path.read_text()
    return None


def search_wiki(query: str) -> list[dict]:
    tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
    results = []
    for category, directory in _CATEGORY_DIRS.items():
        if not directory.exists():
            continue
        for path in directory.glob("*.md"):
            content = path.read_text()
            score = len(tokens & set(re.findall(r"[a-z0-9]+", content.lower())))
            if score:
                results.append({"slug": path.stem, "category": category, "path": str(path.relative_to(config.WIKI_DIR)), "score": score})
    return sorted(results, key=lambda item: item["score"], reverse=True)


def list_pages(category: str | None = None) -> list[dict]:
    entries = _load_index()
    return [entry for entry in entries if entry["category"] == category] if category else entries


def get_log(last_n: int = 20) -> list[str]:
    if not _LOG_FILE.exists():
        return []
    return [line for line in _LOG_FILE.read_text().splitlines() if line.startswith("## [")][-last_n:]


def lint_wiki() -> dict:
    indexed = {entry["slug"] for entry in _load_index()}
    files = {}
    for directory in _CATEGORY_DIRS.values():
        if directory.exists():
            files.update({path.stem: path for path in directory.glob("*.md")})
    all_slugs = set(files)
    broken = {}
    isolated = []
    for slug, path in files.items():
        links = re.findall(r"\[\[([^\]]+)\]\]", path.read_text())
        if not links:
            isolated.append(slug)
        missing = [link for link in links if _slug(link) not in all_slugs]
        if missing:
            broken[slug] = missing
    return {
        "orphan_pages": sorted(all_slugs - indexed),
        "missing_pages": sorted(indexed - all_slugs),
        "broken_wikilinks": broken,
        "isolated_pages": isolated,
    }

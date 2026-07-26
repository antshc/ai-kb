"""CLI entry point for the mini-context-graph skill.

It can be run from the consuming repository without manually configuring
PYTHONPATH, and forces UTF-8 output on Windows consoles.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")

from scripts.contextgraph import ContextGraphSkill  # noqa: E402
from scripts.tools import documents_store, wiki_store  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the mini-context graph.")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("search", "evidence", "query"):
        cmd = sub.add_parser(name)
        cmd.add_argument("text")

    read = sub.add_parser("read")
    read.add_argument("category", choices=("entity", "summary", "topic"))
    read.add_argument("title")

    pages = sub.add_parser("pages")
    pages.add_argument("category", nargs="?", choices=("entity", "summary", "topic"))
    sub.add_parser("documents")
    sub.add_parser("lint")

    args = parser.parse_args()

    if args.command == "search":
        result = wiki_store.search_wiki(args.text)
    elif args.command == "evidence":
        result = documents_store.search_chunks(args.text, top_k=20)
    elif args.command == "query":
        result = ContextGraphSkill().query_with_evidence(args.text)
    elif args.command == "read":
        result = wiki_store.read_page(args.category, args.title)
    elif args.command == "pages":
        result = wiki_store.list_pages(args.category)
    elif args.command == "documents":
        result = documents_store.list_documents()
    else:
        result = wiki_store.lint_wiki()

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

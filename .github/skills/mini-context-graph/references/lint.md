# Lint Instructions

Run after large ingestion batches, before major synthesis, or when answers conflict.

```python
from scripts.tools import wiki_store
issues = wiki_store.lint_wiki()
```

Review:

- orphan pages not present in the index;
- missing pages referenced by the index;
- broken `[[wikilinks]]`;
- isolated pages without links;
- contradictory claims;
- stale or superseded claims;
- missing backlinks between summaries and entities.

Rules:

- Never delete pages without explicit approval.
- Never auto-resolve contradictions; record them for review.
- Prefer adding cross-references over duplicating content.
- Record significant lint results in a wiki topic page.

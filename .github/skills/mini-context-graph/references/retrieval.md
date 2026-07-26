# Retrieval Instructions

Use wiki-first retrieval, then graph traversal with evidence.

## Workflow

1. Parse important noun phrases and keywords from the query.
2. Search the wiki with `wiki_store.search_wiki(query)`.
3. Read relevant wiki pages.
4. Return from the wiki when it contains sufficient context.
5. Otherwise find graph seed nodes with `index_store.search(query)`.
6. Expand seeds with breadth-first traversal.
7. Build the subgraph and resolve provenance.
8. File valuable synthesis back into a topic page.

## Graph Traversal

- Maximum depth: `2`.
- Minimum edge confidence: `0.6`.
- Maximum returned nodes: `50`.
- Always retain seed nodes.
- Prefer depth-1 and higher-confidence relations when pruning.

For evidence-backed retrieval:

```python
result = skill.query_with_evidence(query)
```

Return:

- graph nodes and edges;
- supporting source documents and chunks;
- a human-readable evidence chain;
- relevant wiki references.

## Constraints

- Never fabricate nodes or edges.
- Return an empty result rather than inventing context.
- Do not traverse beyond the configured depth.
- Search the wiki before traversing the graph.

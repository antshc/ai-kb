# Ingestion Instructions

## Workflow

1. Read the source document.
2. Extract explicit entities and relations.
3. Normalize names and types to lowercase.
4. Reuse canonical ontology types where possible.
5. Include evidence for every entity and relation.
6. Persist the source, graph, and provenance.
7. Write a source summary page.
8. Write or update entity pages.

## Entity Extraction

For each entity, record:

- `name`: normalized lowercase noun phrase;
- `type`: reusable 1–3 word category;
- `supporting_text`: verbatim or near-verbatim source text.

Avoid unique one-off types when a reusable ontology type applies.

## Relation Extraction

For every explicit relationship, record:

- `source`;
- `target`;
- `type`: present-tense verb phrase;
- `confidence`;
- `supporting_text`.

Confidence guidance:

- `1.0`: explicitly stated;
- `0.8`: strongly implied;
- `0.6`: weakly implied;
- below `0.6`: exclude.

Both endpoints must be included in the entity list.

## Extraction Output

```json
{
  "entities": [
    {
      "name": "entity name",
      "type": "entity type",
      "supporting_text": "source text"
    }
  ],
  "relations": [
    {
      "source": "source entity",
      "target": "target entity",
      "type": "relation type",
      "confidence": 0.9,
      "supporting_text": "source text"
    }
  ]
}
```

## Wiki Updates

After `skill.ingest_with_content(...)`:

1. Write one `summary` page for the source document.
2. Write one `entity` page for each new entity.
3. Update existing entity pages with new relations and source links.
4. Update relevant `topic` pages.
5. Flag conflicting claims instead of silently replacing them.

## Constraints

- Do not invent entities or relations.
- Always include `supporting_text`.
- Prefer existing ontology terms.
- Preserve the original source path or URL.
- Treat raw source content as immutable after ingestion.

# Ontology Instructions

## Principle

The ontology evolves from ingested documents but must remain compact, consistent, and reusable.

## Entity Types

Normalize entity types by:

1. converting to lowercase;
2. trimming whitespace;
3. replacing `_` and `-` with spaces;
4. mapping synonyms to canonical terms.

Recommended canonical mappings:

| Variants | Canonical type |
|---|---|
| component, module, class, function, method | component |
| bug, defect, fault, error, failure, problem | issue |
| server, host, machine, node | infrastructure |
| user, person, operator, administrator | actor |
| app, application, service, program | software |
| database, datastore, db | storage |
| api, endpoint, connection | interface |
| event, incident, occurrence, trigger | event |
| concept, idea, principle, theory | concept |
| process, thread, task, job, workflow | process |

Create a new type only when no existing type is accurate. Keep the total ontology near 50 entity types; merge similar types as it grows.

## Relation Types

Use lowercase present-tense verb phrases.

| Variants | Canonical relation |
|---|---|
| triggers, leads to, results in, produces | causes |
| is part of, belongs to, lives in | contains |
| requires, needs | depends on |
| calls, invokes, consumes | uses |
| impacts, influences | affects |
| instantiates, spawns | creates |
| links to, references | connects to |
| inherits from, subclasses | extends |
| queries, fetches | reads from |
| stores in, persists to | writes to |

Add a new relation only when no existing relation accurately expresses the evidence.

## Update Protocol

For every extracted entity and relation:

1. Normalize it with `ontology_store`.
2. Register the canonical term.
3. Use the canonical value when writing graph nodes and edges.
4. Do not rename existing concepts without checking affected wiki pages and edges.

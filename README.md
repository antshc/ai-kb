# mini-context-graph

## Directory structure

```text
.
├── sources/                         # Immutable, human-maintained source documents
├── wiki/                            # Synthesized knowledge pages
│   ├── index.md                     # Generated page index
│   └── log.md                       # Generated change log
├── data/                            # Machine-managed graph, documents, ontology, and search state
├── docs/                            # Project documentation and workflows
├── .agents/skills/mini-context-graph/ # Skill code, runtime, and extraction rules
├── AGENTS.md                        # Repository rules for agents
├── migration-map.md                 # Migration notes and mappings
└── README.md                        # Usage and repository overview
```

`index.md` and `log.md` are generated; update wiki content through `wiki_store`.

## Supported source files

Ingestion accepts UTF-8 text files, including `.md`, `.adoc`, `.txt`, `.rst`, `.yaml`, `.yml`, `.json`, `.csv`, and source-code files. Binary files are not supported reliably. The directory pass processes files directly inside `sources/`, not nested subdirectories.

```text
# Ingest a document
/mini-context-graph ingest sources\example.md

# Ask a question
/mini-context-graph query "Why does the service fail?"

# Search the wiki
/mini-context-graph search "memory leak"

# Read a wiki page
/mini-context-graph read summary "Example Summary"

# List wiki pages
/mini-context-graph pages entity

# List ingested documents
/mini-context-graph documents

# Find source evidence
/mini-context-graph evidence "memory leak"

# Validate the wiki
/mini-context-graph lint
```

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

import config
from tools import documents_store, graph_store, index_store, ontology_store, retrieval_engine


class ContextGraphSkill:
    def add_node(self, name: str, node_type: str) -> str:
        canonical_type = ontology_store.normalize_type(node_type)
        ontology_store.add_type(canonical_type)
        node_id = graph_store.add_node(name, canonical_type)
        index_store.add_entity(name, node_id)
        return node_id

    def add_edge(self, source_name: str, target_name: str, relation: str, confidence: float) -> None:
        if confidence < config.MIN_CONFIDENCE:
            return
        source_id = graph_store.find_node_by_name(source_name)
        target_id = graph_store.find_node_by_name(target_name)
        if source_id is None or target_id is None:
            return
        canonical_relation = ontology_store.normalize_relation(relation)
        ontology_store.add_relation(canonical_relation)
        graph_store.add_edge(source_id, target_id, canonical_relation, confidence)

    def ingest_with_content(self, doc_id: str, title: str, source: str, raw_content: str, entities: list[dict], relations: list[dict]) -> dict:
        document = documents_store.add_document(doc_id, title, source, raw_content)
        chunks = document["chunks"]

        def best_chunk(text: str) -> str | None:
            if not text:
                return None
            words = set(text.lower().split())
            best_id = None
            best_score = 0
            for chunk in chunks:
                chunk_text = chunk["text"].lower()
                if text.lower() in chunk_text:
                    return chunk["chunk_id"]
                score = len(words & set(chunk_text.split()))
                if score > best_score:
                    best_id, best_score = chunk["chunk_id"], score
            return best_id

        nodes_added = 0
        for entity in entities:
            canonical_type = ontology_store.normalize_type(entity["type"])
            ontology_store.add_type(canonical_type)
            chunk_id = best_chunk(entity.get("supporting_text", ""))
            node_id = graph_store.add_node(
                entity["name"], canonical_type, doc_id, [chunk_id] if chunk_id else []
            )
            index_store.add_entity(entity["name"], node_id)
            nodes_added += 1

        edges_added = 0
        for relation in relations:
            confidence = relation.get("confidence", 0)
            if confidence < config.MIN_CONFIDENCE:
                continue
            source_id = graph_store.find_node_by_name(relation["source"])
            target_id = graph_store.find_node_by_name(relation["target"])
            if source_id is None or target_id is None:
                continue
            canonical_relation = ontology_store.normalize_relation(relation["type"])
            ontology_store.add_relation(canonical_relation)
            graph_store.add_edge(
                source_id,
                target_id,
                canonical_relation,
                confidence,
                doc_id,
                relation.get("supporting_text"),
                best_chunk(relation.get("supporting_text", "")),
            )
            edges_added += 1

        return {
            "doc_id": doc_id,
            "chunk_count": len(chunks),
            "nodes_added": nodes_added,
            "edges_added": edges_added,
        }

    def query(self, query: str) -> dict:
        seeds = index_store.search(query)
        if not seeds:
            return {"nodes": {}, "edges": []}
        node_ids = retrieval_engine.retrieve(seeds)
        return graph_store.get_subgraph(node_ids)

    def query_with_evidence(self, query: str) -> dict:
        subgraph = self.query(query)
        documents: dict[str, set[str]] = {}
        for node in subgraph["nodes"].values():
            if node.get("source_document"):
                documents.setdefault(node["source_document"], set()).update(node.get("source_chunks", []))
        for edge in subgraph["edges"]:
            if edge.get("source_document"):
                documents.setdefault(edge["source_document"], set())
                if edge.get("chunk_id"):
                    documents[edge["source_document"]].add(edge["chunk_id"])

        supporting_documents = []
        for doc_id, chunk_ids in documents.items():
            document = documents_store.get_document(doc_id)
            if not document:
                continue
            supporting_documents.append({
                "doc_id": doc_id,
                "doc_title": document["title"],
                "supporting_chunks": [
                    {"chunk_id": chunk_id, "text": chunk["text"]}
                    for chunk_id in sorted(chunk_ids)
                    if (chunk := documents_store.get_chunk(chunk_id))
                ],
            })

        chain = []
        for edge in subgraph["edges"]:
            source = subgraph["nodes"].get(edge["source"], {}).get("name", edge["source"])
            target = subgraph["nodes"].get(edge["target"], {}).get("name", edge["target"])
            chain.append(f"{source} --[{edge['type']}]--> {target}")

        return {
            "query": query,
            "subgraph": subgraph,
            "supporting_documents": supporting_documents,
            "evidence_chain": " | ".join(chain) if chain else "No edges in subgraph.",
        }

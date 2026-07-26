from __future__ import annotations

from collections import deque
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import config
from tools import graph_store


def retrieve(seed_node_ids: list[str], depth: int = config.MAX_GRAPH_DEPTH, min_confidence: float = config.MIN_CONFIDENCE, max_nodes: int = config.MAX_NODES) -> list[str]:
    visited = set(seed_node_ids)
    queue = deque((node_id, 0) for node_id in seed_node_ids)
    while queue and len(visited) < max_nodes:
        node_id, current_depth = queue.popleft()
        if current_depth >= depth:
            continue
        for neighbor in graph_store.get_neighbors(node_id, min_confidence):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            queue.append((neighbor, current_depth + 1))
            if len(visited) >= max_nodes:
                break
    return list(visited)

import os
from pathlib import Path

_BASE = Path(os.environ.get("MINI_CONTEXT_GRAPH_BASE", str(Path.cwd())))
DATA_DIR = Path(os.environ.get("MINI_CONTEXT_GRAPH_DATA_DIR", str(_BASE / "data")))
WIKI_DIR = Path(os.environ.get("MINI_CONTEXT_GRAPH_WIKI_DIR", str(_BASE / "wiki")))

MAX_GRAPH_DEPTH = 2
MIN_CONFIDENCE = 0.6
MAX_NODES = 50

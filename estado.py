# estado.py
import os, json
from typing import Set

STATE_FILE = os.getenv("STATE_FILE", "state.json")
_cache: Set[str] | None = None

def _load():
    global _cache
    if _cache is not None:
        return
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            _cache = set(data if isinstance(data, list) else [])
        else:
            _cache = set()
    except Exception:
        _cache = set()

def was_sent(key: str) -> bool:
    _load()
    return key in _cache  # type: ignore[arg-type]

def mark_sent(key: str) -> None:
    _load()
    _cache.add(key)  # type: ignore[union-attr]
    tmp = STATE_FILE + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(sorted(_cache), f, ensure_ascii=False)
        os.replace(tmp, STATE_FILE)
    except Exception:
        # em caso de erro de escrita, não quebra o processo
        pass

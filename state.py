
from typing import Set, Tuple

# Guarda (match_id, bucket) para evitar repetição de alertas
_seen: Set[Tuple[str, str]] = set()

def already_alerted(match_id: str, bucket: str) -> bool:
    key = (match_id, bucket)
    if key in _seen:
        return True
    _seen.add(key)
    return False

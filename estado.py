_sent = set()

def was_sent(key: str) -> bool:
    return key in _sent

def mark_sent(key: str):
    _sent.add(key)

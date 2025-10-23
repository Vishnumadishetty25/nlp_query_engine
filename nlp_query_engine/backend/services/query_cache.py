import time
from typing import Any, Dict
class QueryCache:
    def __init__(self):
        self.store = {}
        self.ttl = 300

    def get(self, key: str):
        entry = self.store.get(key)
        if not entry:
            return None
        value, ts = entry
        if time.time() - ts > self.ttl:
            del self.store[key]
            return None
        return value

    def set(self, key: str, value: Any):
        self.store[key] = (value, time.time())

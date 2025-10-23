from typing import Dict, Any, List
from backend.services.schema_discovery import SchemaDiscovery
from backend.services.query_cache import QueryCache
from backend.services.document_processor import DocumentProcessor
import os, json, math

class QueryEngine:
    def __init__(self, connection_string: str = None):
        self.schema = {}
        self.cache = QueryCache()
        self.doc_processor = DocumentProcessor()
        self.connection_string = connection_string
        if connection_string:
            try:
                self.schema = SchemaDiscovery().analyze_database(connection_string)
            except Exception:
                self.schema = {}

    def classify_query(self, user_query: str) -> str:
        q = user_query.lower()
        if q.strip().startswith('select') or any(word in q for word in ['count', 'avg', 'sum', 'where', 'join']):
            return 'sql'
        # naive heuristic: if mentions resume or document, use doc
        if any(word in q for word in ['resume','cv','document','profile','review']):
            return 'document'
        # default to hybrid
        return 'hybrid'

    def process_query(self, user_query: str) -> Dict[str, Any]:
        qtype = self.classify_query(user_query)
        key = f"{qtype}:{user_query.strip().lower()}"
        cached = self.cache.get(key)
        if cached:
            return {'from_cache': True, 'result': cached, 'query_type': qtype}

        if qtype == 'sql':
            # Very simple: return instructions or mock - avoid executing arbitrary SQL
            res = {'message': 'SQL execution is disabled in demo mode. Provide a SELECT-like query or use sample DB.'}
        elif qtype == 'document':
            # do simple keyword search over stored JSON chunks
            hits = self._search_documents(user_query)
            res = {'documents': hits}
        else:
            # hybrid: run both heuristics
            hits = self._search_documents(user_query)
            res = {'documents': hits, 'note': 'Hybrid mode - SQL generation not run in demo.'}

        self.cache.set(key, res)
        return {'from_cache': False, 'result': res, 'query_type': qtype}

    def _search_documents(self, user_query: str) -> List[Dict]:
        storage = self.doc_processor.storage_dir
        hits = []
        q = user_query.lower()
        if not os.path.exists(storage):
            return hits
        for fn in os.listdir(storage):
            if not fn.endswith('.json'):
                continue
            try:
                with open(os.path.join(storage, fn), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if q in data.get('content','').lower():
                    hits.append({'chunk_id': data.get('chunk_id'), 'file_path': data.get('file_path'), 'snippet': data.get('content')[:300]})
            except:
                continue
        return hits

from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class DatabaseConnectionRequest(BaseModel):
    connection_string: str

class DocumentUploadResponse(BaseModel):
    uploaded: int
    failed: int
    errors: List[str] = []

class QueryRequest(BaseModel):
    query: str

class SchemaResponse(BaseModel):
    tables: Dict[str, List[str]]
    relationships: Optional[List[Dict[str, Any]]] = []

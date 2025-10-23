from fastapi import APIRouter, HTTPException
from backend.models.api_models import DatabaseConnectionRequest, SchemaResponse
from backend.services.schema_discovery import SchemaDiscovery
from backend.services.query_engine import QueryEngine

router = APIRouter(prefix="/api/schema", tags=["schema"])

_engine = None
_current_schema = None


@router.post('/discover')
async def discover_schema(connection_string: str):
    global _engine, _current_schema
    try:
        sd = SchemaDiscovery()
        _current_schema = sd.analyze_database(payload.connection_string)
        # create a query engine instance for later queries
        _engine = QueryEngine(payload.connection_string)
        return {'message': 'schema discovered', 'schema': _current_schema}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/')
async def get_schema():
    if not _current_schema:
        raise HTTPException(
            status_code=404, detail='No schema discovered yet.')
    return _current_schema

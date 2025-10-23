from fastapi import APIRouter, HTTPException
from backend.models.api_models import QueryRequest
from backend.services.query_engine import QueryEngine

router = APIRouter(prefix="/api/query", tags=["query"])
# For demo, no DB connection by default
engine = QueryEngine()

@router.post("/")
async def process_query(payload: QueryRequest):
    try:
        res = engine.process_query(payload.query)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/history')
async def history():
    # return simple empty history for demo
    return {'history': []}

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get('/frontend/public/index.html')
async def frontend_index():
    return FileResponse('frontend/public/index.html')

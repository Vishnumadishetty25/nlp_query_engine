from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
import os
from backend.services.document_processor import DocumentProcessor

router = APIRouter(prefix="/api/ingest", tags=["ingest"])
processor = DocumentProcessor()

@router.post("/documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Accept multiple files and process them synchronously for demo."""
    saved_paths = []
    errors = []
    for up in files:
        try:
            contents = await up.read()
            path = os.path.join('uploads', up.filename)
            os.makedirs('uploads', exist_ok=True)
            with open(path, 'wb') as f:
                f.write(contents)
            saved_paths.append(path)
        except Exception as e:
            errors.append(f"{up.filename}: {str(e)}")
    result = processor.process_documents(saved_paths)
    return result

@router.get('/status')
async def ingestion_status():
    # For demo, simple status
    return {"status": "idle"}

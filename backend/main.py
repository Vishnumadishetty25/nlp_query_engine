from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.api.routes import ingestion, query, schema as schema_router
import uvicorn
import os

app = FastAPI(title="NLP Query Engine (Cleaned)")

# ✅ Serve the frontend automatically
app.mount("/", StaticFiles(directory="frontend/public",
          html=True), name="frontend")

app.include_router(ingestion.router)
app.include_router(query.router)
app.include_router(schema_router.router)


@app.get("/api")
async def root():
    return {"message": "NLP Query Engine backend is running."}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

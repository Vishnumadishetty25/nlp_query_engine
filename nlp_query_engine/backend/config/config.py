from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings_batch_size: int = 32
    chunk_size: int = 200

settings = Settings()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ask
from app.core.config import settings

app = FastAPI(
    title="IsCoolGPT API",
    description="Assistente inteligente voltado para educação",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(ask.router, prefix="/api/v1", tags=["ask"])

@app.get("/")
async def root():
    return {
        "message": "IsCoolGPT API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}


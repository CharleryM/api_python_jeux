from fastapi import FastAPI
from app.api.routes import games

app = FastAPI(
    title="bib",
    description="API REST pour une bibliotheque",
    version="1.0.0",
    docs_url="/docs",
)

@app.get("/", tags=["Root"])
async def root():
    return{
        "message": "Welcome",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return{
        "statut": "healthy",
        "service": "bib",
       
    }

app.include_router(games.router, prefix="/games", tags=["Games"])
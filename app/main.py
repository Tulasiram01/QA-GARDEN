from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(title="Bug Triage Engine")

# All API routes will be under /api/...
app.include_router(api_router, prefix="/api")

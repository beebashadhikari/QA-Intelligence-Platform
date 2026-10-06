from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.agent import router as agent_router
from backend.app.api.dashboard import (
    router as dashboard_router,
)
from backend.app.api.defects import router as defects_router
from backend.app.api.qa_intelligence import (
    router as qa_intelligence_router,
)
from backend.app.api.quality import router as quality_router
from backend.app.api.recommendations import (
    router as recommendations_router,
)
from backend.app.api.releases import router as releases_router
from backend.app.api.risk import router as risk_router


app = FastAPI(
    title="QA Intelligence Platform",
    description="AI-powered software quality intelligence system",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "qa-intelligence-platform",
        "version": "0.1.0",
    }


app.include_router(releases_router)
app.include_router(defects_router)
app.include_router(recommendations_router)
app.include_router(quality_router)
app.include_router(risk_router)
app.include_router(agent_router)
app.include_router(qa_intelligence_router)
app.include_router(dashboard_router)
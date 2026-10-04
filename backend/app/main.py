from fastapi import FastAPI


app = FastAPI(
    title="QA Intelligence Platform",
    description="AI-powered software quality intelligence system",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "qa-intelligence-platform",
        "version": "0.1.0",
    }
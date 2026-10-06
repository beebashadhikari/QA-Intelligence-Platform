from pydantic import BaseModel


class ReleaseDecision(BaseModel):
    release_version: str
    status: str
    confidence: str
    summary: str
    blocking_factors: list[str]
    risk_factors: list[str]
    required_actions: list[str]
    evidence: list[str]
from pydantic import BaseModel, Field


class AgentAnalyzeRequest(BaseModel):
    release_version: str = Field(
        min_length=1,
    )

    message: str = Field(
        min_length=1,
    )


class AgentRisk(BaseModel):
    module: str
    level: str
    score: float
    reason: str


class AgentRecommendation(BaseModel):
    action: str
    reason: str
    priority: str


class AgentAnalyzeResponse(BaseModel):
    release_version: str
    message: str

    assessment: str
    status: str
    facts: list[str]
    risks: list[AgentRisk]
    recommendations: list[AgentRecommendation]
    missing_evidence: list[str]
    confidence: str
    human_decision: str
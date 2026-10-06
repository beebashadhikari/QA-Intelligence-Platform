from pydantic import BaseModel


class DashboardSummary(BaseModel):
    release_version: str
    readiness_status: str
    confidence: str
    quality_score: float
    quality_health: str
    pass_rate: float
    total_tests: int
    passed_tests: int
    failed_tests: int
    blocked_tests: int
    total_defects: int
    high_risk_areas: int
    critical_defects: int


class DashboardRiskItem(BaseModel):
    area: str
    score: float
    level: str
    reasons: list[str]
    change_id: str
    high_severity_defects: int
    failed_tests: int
    flaky_tests: int


class DashboardDefectSummary(BaseModel):
    total: int
    critical: int
    high: int
    medium: int
    low: int


class DashboardRecommendation(BaseModel):
    test_case_id: str
    title: str
    module: str
    score: int
    risk_level: str
    status: str
    action: str


class DashboardDecision(BaseModel):
    status: str
    confidence: str
    summary: str
    blocking_factors: list[str]
    risk_factors: list[str]
    required_actions: list[str]
    evidence: list[str]


class ReleaseReadinessDashboard(BaseModel):
    release_version: str
    summary: DashboardSummary
    decision: DashboardDecision
    blockers: list[str]
    warnings: list[str]
    risks: list[DashboardRiskItem]
    defects: DashboardDefectSummary
    recommendations: list[DashboardRecommendation]
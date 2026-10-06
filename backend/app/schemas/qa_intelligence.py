from pydantic import BaseModel


class ReleaseMetrics(BaseModel):
    total_tests: int
    passed_tests: int
    failed_tests: int
    blocked_tests: int
    pass_rate: float


class ReleaseAnalysis(BaseModel):
    release_version: str
    status: str
    metrics: ReleaseMetrics
    blockers: list[str]
    warnings: list[str]


class DefectAnalysis(BaseModel):
    release_version: str
    total_defects: int
    severity_counts: dict[str, int]
    status_counts: dict[str, int]
    module_counts: dict[str, int]


class RiskItem(BaseModel):
    area: str
    score: float
    level: str
    reasons: list[str]
    change_id: str
    high_severity_defects: int
    failed_tests: int
    flaky_tests: int


class TestRecommendation(BaseModel):
    test_case_id: str
    title: str
    module: str
    score: int
    risk_level: str
    reasons: list[str]
    status: str
    action: str
    blocking_reason: str | None


class QualityHealthComponents(BaseModel):
    functional: float
    regression: float
    defects: float
    automation: float
    stability: float


class QualityHealth(BaseModel):
    release_version: str
    score: float
    health: str
    components: QualityHealthComponents


class QAIntelligenceResponse(BaseModel):
    release_version: str
    release: ReleaseAnalysis
    defects: DefectAnalysis
    risk: list[RiskItem]
    test_recommendations: list[TestRecommendation]
    quality_health: QualityHealth
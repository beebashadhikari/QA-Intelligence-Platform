const API_BASE_URL = "http://127.0.0.1:8000";

export interface ReleaseOption {
  release_version: string;
}

export interface ReleasePortfolioItem {
  release_version: string;
  readiness_status: string;
  confidence: string;
  quality_score: number;
  quality_health: string;
  pass_rate: number;
  total_tests: number;
  passed_tests: number;
  failed_tests: number;
  blocked_tests: number;
  total_defects: number;
  critical_defects: number;
  high_risk_areas: number;
}

export interface DashboardSummary {
  release_version: string;
  readiness_status: string;
  confidence: string;
  quality_score: number;
  quality_health: string;
  pass_rate: number;
  total_tests: number;
  passed_tests: number;
  failed_tests: number;
  blocked_tests: number;
  total_defects: number;
  high_risk_areas: number;
  critical_defects: number;
}

export interface DashboardRiskItem {
  area: string;
  score: number;
  level: string;
  reasons: string[];

  change_id: string;
  high_severity_defects: number;
  failed_tests: number;
  flaky_tests: number;
}

export interface DashboardDefectSummary {
  total: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
}

export interface DashboardRecommendation {
  test_case_id: string;
  title: string;
  module: string;
  score: number;
  risk_level: string;
  status: string;
  action: string;
}

export interface TestRecommendation {
  test_case_id: string;
  title: string;
  module: string;
  score: number;
  risk_level: string;
  reasons: string[];
  status: string;
  action: string;
  blocking_reason: string | null;
}

export interface TestRecommendationsResponse {
  release_version: string;
  recommendations: TestRecommendation[];
}
export interface AgentRisk {
  module: string;
  level: string;
  score: number;
  reason: string;
}

export interface AgentRecommendation {
  action: string;
  reason: string;
  priority: string;
}

export interface AgentAnalysis {
  release_version: string;
  message: string;
  assessment: string;
  status: string;
  facts: string[];
  risks: AgentRisk[];
  recommendations: AgentRecommendation[];
  missing_evidence: string[];
  confidence: string;
  human_decision: string;
}

export interface DashboardDecision {
  status: string;
  confidence: string;
  summary: string;
  blocking_factors: string[];
  risk_factors: string[];
  required_actions: string[];
  evidence: string[];
}

export interface ReleaseReadinessDashboard {
  release_version: string;
  summary: DashboardSummary;
  decision: DashboardDecision;
  blockers: string[];
  warnings: string[];
  risks: DashboardRiskItem[];
  defects: DashboardDefectSummary;
  recommendations: DashboardRecommendation[];
}

export async function getReleases(): Promise<
  ReleaseOption[]
> {
  const response = await fetch(
    `${API_BASE_URL}/api/releases`,
  );

  if (!response.ok) {
    throw new Error(
      `Failed to load releases: ${response.status}`,
    );
  }

  return response.json();
}

export async function getReleasePortfolio(): Promise<
  ReleasePortfolioItem[]
> {
  const response = await fetch(
    `${API_BASE_URL}/api/releases/portfolio`,
  );

  if (!response.ok) {
    throw new Error(
      `Failed to load release portfolio: ${response.status}`,
    );
  }

  return response.json();
}

export async function getReleaseDashboard(
  releaseVersion: string,
): Promise<ReleaseReadinessDashboard> {
  const response = await fetch(
    `${API_BASE_URL}/api/dashboard/release/${releaseVersion}`,
  );

  if (!response.ok) {
    throw new Error(
      `Failed to load dashboard: ${response.status}`,
    );
  }

  return response.json();
}

export async function getTestRecommendations(
  releaseVersion: string,
): Promise<TestRecommendationsResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/releases/${releaseVersion}/recommendations`,
  );

  if (!response.ok) {
    throw new Error(
      `Failed to load test recommendations: ${response.status}`,
    );
  }

  return response.json();
}
export async function analyzeWithAgent(
  releaseVersion: string,
  message: string,
): Promise<AgentAnalysis> {
  const response = await fetch(
    `${API_BASE_URL}/api/agent/analyze`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        release_version: releaseVersion,
        message,
      }),
    },
  );

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      `Agent analysis failed: ${response.status} ${errorText}`,
    );
  }

  return response.json();
}
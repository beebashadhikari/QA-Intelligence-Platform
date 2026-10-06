import { useEffect, useMemo, useState } from "react";
import "./App.css";

import {
  analyzeWithAgent,
  getReleaseDashboard,
  getReleasePortfolio,
  getReleases,
  getTestRecommendations,
  type AgentAnalysis,
  type ReleaseOption,
  type ReleasePortfolioItem,
  type ReleaseReadinessDashboard,
  type TestRecommendation,
} from "./api/dashboard";


type Workspace =
  | "overview"
  | "releases"
  | "risk"
  | "test-intelligence"
  | "agent";

type TestRiskFilter =
  | "ALL"
  | "HIGH"
  | "MEDIUM"
  | "LOW";

type TestStatusFilter =
  | "ALL"
  | "FAILED"
  | "BLOCKED"
  | "RECOMMENDED";


/* =====================================================
   TEST INTELLIGENCE HELPERS
   ===================================================== */

function getTestRiskClass(riskLevel: string) {
  const normalized = riskLevel.toUpperCase();

  if (normalized === "HIGH") {
    return "high";
  }

  if (normalized === "MEDIUM") {
    return "medium";
  }

  return "low";
}


function getTestStatusClass(status: string) {
  const normalized = status.toLowerCase();

  if (normalized === "failed") {
    return "failed";
  }

  if (normalized === "blocked") {
    return "blocked";
  }

  return "recommended";
}


/* =====================================================
   AI AGENT HELPERS
   ===================================================== */

function getAgentStatusClass(status: string) {
  const normalized = status.toUpperCase();

  if (normalized === "READY") {
    return "ready";
  }

  if (normalized === "CONDITIONAL") {
    return "conditional";
  }

  if (normalized === "NOT_READY") {
    return "not-ready";
  }

  return "neutral";
}


function getAgentPriorityClass(priority: string) {
  const normalized = priority.toUpperCase();

  if (normalized === "HIGH") {
    return "high";
  }

  if (normalized === "MEDIUM") {
    return "medium";
  }

  if (normalized === "LOW") {
    return "low";
  }

  return "neutral";
}


/* =====================================================
   APP
   ===================================================== */

function App() {
  const [workspace, setWorkspace] =
    useState<Workspace>("overview");

  const [dashboard, setDashboard] =
    useState<ReleaseReadinessDashboard | null>(null);

  const [releases, setReleases] =
    useState<ReleaseOption[]>([]);

  const [portfolio, setPortfolio] =
    useState<ReleasePortfolioItem[]>([]);

  const [selectedRelease, setSelectedRelease] =
    useState<string>("");


  /* =====================================================
     TEST INTELLIGENCE STATE
     ===================================================== */

  const [testRecommendations, setTestRecommendations] =
    useState<TestRecommendation[]>([]);

  const [
    testRecommendationsLoading,
    setTestRecommendationsLoading,
  ] = useState(false);

  const [
    testRecommendationsError,
    setTestRecommendationsError,
  ] = useState<string | null>(null);

  const [testRiskFilter, setTestRiskFilter] =
    useState<TestRiskFilter>("ALL");

  const [testStatusFilter, setTestStatusFilter] =
    useState<TestStatusFilter>("ALL");


  /* =====================================================
     GLOBAL STATE
     ===================================================== */

  const [loading, setLoading] =
    useState(true);

  const [portfolioLoading, setPortfolioLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [portfolioError, setPortfolioError] =
    useState<string | null>(null);


  /* =====================================================
     AI AGENT STATE
     ===================================================== */

  const [agentMessage, setAgentMessage] =
    useState(
      "Why is this release conditional and what should QA do before approval?",
    );

  const [agentAnalysis, setAgentAnalysis] =
    useState<AgentAnalysis | null>(null);

  const [agentLoading, setAgentLoading] =
    useState(false);

  const [agentError, setAgentError] =
    useState<string | null>(null);


  /* =====================================================
     LOAD RELEASES
     ===================================================== */

  useEffect(() => {
    async function loadReleases() {
      try {
        setLoading(true);
        setError(null);

        const data = await getReleases();

        setReleases(data);

        if (data.length > 0) {
          setSelectedRelease(
            data[0].release_version,
          );
        } else {
          throw new Error(
            "No releases are available.",
          );
        }
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load releases.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadReleases();
  }, []);


  /* =====================================================
     LOAD RELEASE DASHBOARD
     ===================================================== */

  useEffect(() => {
    if (!selectedRelease) {
      return;
    }

    async function loadDashboard() {
      try {
        setLoading(true);
        setError(null);

        const data =
          await getReleaseDashboard(
            selectedRelease,
          );

        setDashboard(data);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load dashboard.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [selectedRelease]);


  /* =====================================================
     LOAD TEST INTELLIGENCE
     ===================================================== */

  useEffect(() => {
    if (!selectedRelease) {
      return;
    }

    async function loadTestRecommendations() {
      try {
        setTestRecommendationsLoading(true);
        setTestRecommendationsError(null);

        const data =
          await getTestRecommendations(
            selectedRelease,
          );

        setTestRecommendations(
          data.recommendations,
        );
      } catch (err) {
        setTestRecommendationsError(
          err instanceof Error
            ? err.message
            : "Unable to load test recommendations.",
        );

        setTestRecommendations([]);
      } finally {
        setTestRecommendationsLoading(false);
      }
    }

    loadTestRecommendations();
  }, [selectedRelease]);


  /* =====================================================
     LOAD RELEASE PORTFOLIO
     ===================================================== */

  useEffect(() => {
    if (workspace !== "releases") {
      return;
    }

    async function loadPortfolio() {
      try {
        setPortfolioLoading(true);
        setPortfolioError(null);

        const data =
          await getReleasePortfolio();

        setPortfolio(data);
      } catch (err) {
        setPortfolioError(
          err instanceof Error
            ? err.message
            : "Unable to load release portfolio.",
        );
      } finally {
        setPortfolioLoading(false);
      }
    }

    loadPortfolio();
  }, [workspace]);


  /* =====================================================
     AI AGENT ANALYSIS
     ===================================================== */

  async function handleAgentAnalyze() {
    if (
      !selectedRelease ||
      !agentMessage.trim()
    ) {
      return;
    }

    try {
      setAgentLoading(true);
      setAgentError(null);

      const result =
        await analyzeWithAgent(
          selectedRelease,
          agentMessage.trim(),
        );

      setAgentAnalysis(result);
    } catch (err) {
      setAgentError(
        err instanceof Error
          ? err.message
          : "Agent analysis failed.",
      );
    } finally {
      setAgentLoading(false);
    }
  }


  /* =====================================================
     TEST INTELLIGENCE FILTERING
     ===================================================== */

  const filteredTestRecommendations =
    useMemo(() => {
      return testRecommendations.filter(
        (test) => {
          const matchesRisk =
            testRiskFilter === "ALL" ||
            test.risk_level.toUpperCase() ===
              testRiskFilter;

          const matchesStatus =
            testStatusFilter === "ALL" ||
            test.status.toUpperCase() ===
              testStatusFilter;

          return (
            matchesRisk &&
            matchesStatus
          );
        },
      );
    }, [
      testRecommendations,
      testRiskFilter,
      testStatusFilter,
    ]);


  /* =====================================================
     GLOBAL INITIAL LOADING
     ===================================================== */

  if (loading && !dashboard) {
    return (
      <div className="state-screen">
        <div className="state-card">
          <div className="loading-spinner"></div>

          <h2>
            Loading QA Intelligence
          </h2>

          <p>
            Connecting to the release
            intelligence engine...
          </p>
        </div>
      </div>
    );
  }


  /* =====================================================
     GLOBAL ERROR
     ===================================================== */

  if (error || !dashboard) {
    return (
      <div className="state-screen">
        <div className="state-card error-state">
          <div className="error-symbol">
            !
          </div>

          <h2>
            Unable to load dashboard
          </h2>

          <p>
            {error ??
              "No dashboard data was returned."}
          </p>

          <button
            className="retry-button"
            onClick={() =>
              window.location.reload()
            }
          >
            Retry connection
          </button>
        </div>
      </div>
    );
  }


  /* =====================================================
     DASHBOARD DATA
     ===================================================== */

  const {
    summary,
    decision,
    risks,
    defects,
    recommendations,
  } = dashboard;


  /* =====================================================
     DASHBOARD CALCULATIONS
     ===================================================== */

  const statusBadgeLabel =
    summary.readiness_status === "READY"
      ? "READY"
      : summary.readiness_status ===
          "NOT_READY"
        ? "NOT READY"
        : summary.readiness_status ===
            "BLOCKED"
          ? "BLOCKED"
          : "REVIEW REQUIRED";


  const statusBadgeClass =
    summary.readiness_status === "READY"
      ? "ready"
      : summary.readiness_status ===
          "NOT_READY"
        ? "not-ready"
        : summary.readiness_status ===
            "BLOCKED"
          ? "blocked"
          : "conditional";


  const passedPercentage =
    summary.total_tests > 0
      ? (summary.passed_tests /
          summary.total_tests) *
        100
      : 0;


  const failedPercentage =
    summary.total_tests > 0
      ? (summary.failed_tests /
          summary.total_tests) *
        100
      : 0;


  const blockedPercentage =
    summary.total_tests > 0
      ? (summary.blocked_tests /
          summary.total_tests) *
        100
      : 0;


  const averageRisk =
    risks.length > 0
      ? risks.reduce(
          (total, risk) =>
            total + risk.score,
          0,
        ) / risks.length
      : 0;


  const highRiskCount =
    risks.filter(
      (risk) =>
        risk.level === "HIGH",
    ).length;


  const mediumRiskCount =
    risks.filter(
      (risk) =>
        risk.level === "MEDIUM",
    ).length;


  const lowRiskCount =
    risks.filter(
      (risk) =>
        risk.level === "LOW",
    ).length;


  const highestRisk =
    risks.length > 0
      ? risks[0]
      : null;


  const averageRiskLabel =
    averageRisk >= 75
      ? "HIGH"
      : averageRisk >= 50
        ? "MEDIUM"
        : "LOW";


  const averageRiskClass =
    averageRisk >= 75
      ? "high"
      : averageRisk >= 50
        ? "medium"
        : "low";


  const releasesNeedingAction =
    portfolio.filter(
      (release) =>
        release.readiness_status !==
        "READY",
    ).length;


  const averageQuality =
    portfolio.length > 0
      ? portfolio.reduce(
          (total, release) =>
            total +
            release.quality_score,
          0,
        ) / portfolio.length
      : 0;


  const averagePassRate =
    portfolio.length > 0
      ? portfolio.reduce(
          (total, release) =>
            total +
            release.pass_rate,
          0,
        ) / portfolio.length
      : 0;


  /* =====================================================
     TEST INTELLIGENCE CALCULATIONS
     ===================================================== */

  const testHighRiskCount =
    testRecommendations.filter(
      (item) =>
        item.risk_level.toUpperCase() ===
        "HIGH",
    ).length;


  const testMediumRiskCount =
    testRecommendations.filter(
      (item) =>
        item.risk_level.toUpperCase() ===
        "MEDIUM",
    ).length;


  const testBlockedCount =
    testRecommendations.filter(
      (item) =>
        item.status.toLowerCase() ===
        "blocked",
    ).length;


  const testFailedCount =
    testRecommendations.filter(
      (item) =>
        item.status.toLowerCase() ===
        "failed",
    ).length;


  /* =====================================================
     RELEASE NAVIGATION
     ===================================================== */

  function openRelease(
    releaseVersion: string,
  ) {
    setSelectedRelease(
      releaseVersion,
    );

    setAgentAnalysis(null);
    setAgentError(null);

    setWorkspace("overview");
  }


  /* =====================================================
     APPLICATION
     ===================================================== */

  return (
    <div className="app-shell">

      {/* =================================================
          SIDEBAR
          ================================================= */}

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-mark">
            Q
          </div>

          <div>
            <div className="brand-name">
              QA Intelligence
            </div>

            <div className="brand-subtitle">
              Quality Control Center
            </div>
          </div>
        </div>


        <nav className="navigation">

          <div className="nav-section-label">
            WORKSPACE
          </div>


          <button
            className={`nav-item ${
              workspace === "overview"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setWorkspace("overview")
            }
          >
            <span className="nav-icon">
              ◈
            </span>

            <span>
              Overview
            </span>
          </button>


          <button
            className={`nav-item ${
              workspace === "releases"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setWorkspace("releases")
            }
          >
            <span className="nav-icon">
              ◫
            </span>

            <span>
              Releases
            </span>
          </button>


          <button
            className={`nav-item ${
              workspace === "risk"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setWorkspace("risk")
            }
          >
            <span className="nav-icon">
              ⌁
            </span>

            <span>
              Risk Intelligence
            </span>
          </button>


          <button
            className={`nav-item ${
              workspace ===
              "test-intelligence"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setWorkspace(
                "test-intelligence",
              )
            }
          >
            <span className="nav-icon">
              ✓
            </span>

            <span>
              Test Intelligence
            </span>
          </button>


          <button
            className="nav-item disabled"
            disabled
          >
            <span className="nav-icon">
              ◇
            </span>

            <span>
              Defects
            </span>
          </button>


          <div className="nav-section-label second">
            INTELLIGENCE
          </div>


          <button
            className={`nav-item ${
              workspace === "agent"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setWorkspace("agent")
            }
          >
            <span className="nav-icon">
              ✦
            </span>

            <span>
              AI Agent
            </span>
          </button>


          <button
            className="nav-item disabled"
            disabled
          >
            <span className="nav-icon">
              ◌
            </span>

            <span>
              History
            </span>
          </button>

        </nav>


        <div className="sidebar-footer">

          <div className="system-status">
            <span className="status-dot"></span>
            <span>
              System operational
            </span>
          </div>

          <div className="version-label">
            v0.1.0
          </div>

        </div>

      </aside>


      {/* =================================================
          MAIN CONTENT
          ================================================= */}

      <main className="main-content">


        {/* =================================================
            OVERVIEW
            ================================================= */}

        {workspace === "overview" && (
          <>

            <header className="topbar">

              <div>
                <div className="eyebrow">
                  RELEASE INTELLIGENCE
                </div>

                <h1>
                  Release Readiness
                </h1>
              </div>


              <div className="topbar-actions">

                <label className="release-selector">

                  <span className="selector-label">
                    Release
                  </span>

                  <select
                    value={selectedRelease}
                    onChange={(event) => {
                      const nextRelease =
                        event.target.value;

                      setSelectedRelease(
                        nextRelease,
                      );

                      setAgentAnalysis(
                        null,
                      );

                      setAgentError(
                        null,
                      );
                    }}
                    disabled={
                      releases.length === 0 ||
                      loading
                    }
                  >

                    {releases.map(
                      (release) => (
                        <option
                          key={
                            release.release_version
                          }
                          value={
                            release.release_version
                          }
                        >
                          {
                            release.release_version
                          }
                        </option>
                      ),
                    )}

                  </select>

                  <span className="selector-arrow">
                    ⌄
                  </span>

                </label>


                <div className="live-indicator">
                  <span></span>
                  Live
                </div>

              </div>

            </header>


            <section className="hero-grid">

              <div className="readiness-card">

                <div className="card-header">

                  <div>
                    <div className="card-label">
                      RELEASE STATUS
                    </div>

                    <h2>
                      {
                        summary.readiness_status
                      }
                    </h2>
                  </div>


                  <div
                    className={`status-badge ${statusBadgeClass}`}
                  >
                    {statusBadgeLabel}
                  </div>

                </div>


                <p className="readiness-description">
                  {decision.summary}
                </p>


                <div className="readiness-footer">

                  <div>
                    <span className="metric-caption">
                      Confidence
                    </span>

                    <strong>
                      {summary.confidence}
                    </strong>
                  </div>


                  <div>
                    <span className="metric-caption">
                      Release
                    </span>

                    <strong>
                      {
                        summary.release_version
                      }
                    </strong>
                  </div>


                  <div>
                    <span className="metric-caption">
                      Decision engine
                    </span>

                    <strong>
                      Active
                    </strong>
                  </div>

                </div>

              </div>


              <div className="quality-card">

                <div className="card-header">

                  <div>
                    <div className="card-label">
                      QUALITY HEALTH
                    </div>

                    <h3>
                      Overall Quality
                    </h3>
                  </div>

                  <span className="health-label">
                    {summary.quality_health}
                  </span>

                </div>


                <div className="quality-score">
                  <strong>
                    {summary.quality_score.toFixed(
                      2,
                    )}
                  </strong>

                  <span>
                    / 100
                  </span>
                </div>


                <div className="score-track">
                  <div
                    className="score-fill"
                    style={{
                      width: `${summary.quality_score}%`,
                    }}
                  ></div>
                </div>


                <div className="quality-meta">
                  <span>
                    Functional intelligence
                  </span>

                  <span>
                    Regression protected
                  </span>
                </div>

              </div>

            </section>


            <section className="metrics-grid">

              <div className="metric-card">

                <span className="metric-label">
                  PASS RATE
                </span>

                <strong>
                  {summary.pass_rate.toFixed(
                    2,
                  )}
                  %
                </strong>

                <span className="metric-detail">
                  {summary.passed_tests} of{" "}
                  {summary.total_tests} tests
                  passed
                </span>

              </div>


              <div className="metric-card">

                <span className="metric-label">
                  TOTAL TESTS
                </span>

                <strong>
                  {summary.total_tests}
                </strong>

                <span className="metric-detail">
                  Current release execution
                </span>

              </div>


              <div className="metric-card warning">

                <span className="metric-label">
                  FAILED
                </span>

                <strong>
                  {summary.failed_tests}
                </strong>

                <span className="metric-detail">
                  Requires investigation
                </span>

              </div>


              <div className="metric-card danger">

                <span className="metric-label">
                  BLOCKED
                </span>

                <strong>
                  {summary.blocked_tests}
                </strong>

                <span className="metric-detail">
                  Blocking conditions remain
                </span>

              </div>

            </section>


            <section className="content-grid">

              <div className="panel decision-panel">

                <div className="panel-header">

                  <div>
                    <div className="card-label">
                      DECISION ENGINE
                    </div>

                    <h3>
                      Release Decision
                    </h3>
                  </div>

                  <span className="panel-action">
                    Live analysis
                  </span>

                </div>


                <div className="decision-summary">
                  {decision.summary}
                </div>


                <div className="decision-columns">

                  <div>

                    <div className="list-title">
                      BLOCKING FACTORS
                    </div>

                    {decision.blocking_factors.length >
                    0 ? (
                      decision.blocking_factors.map(
                        (
                          factor,
                          index,
                        ) => (
                          <div
                            className="action-row"
                            key={`blocker-${index}`}
                          >
                            <span className="action-number">
                              {String(
                                index + 1,
                              ).padStart(
                                2,
                                "0",
                              )}
                            </span>

                            <div>
                              <strong>
                                Blocking condition
                              </strong>

                              <span>
                                {factor}
                              </span>
                            </div>
                          </div>
                        ),
                      )
                    ) : (
                      <div className="action-row">
                        <div>
                          <strong>
                            No blocking factors
                          </strong>

                          <span>
                            No hard release blocker
                            was identified by the
                            decision engine.
                          </span>
                        </div>
                      </div>
                    )}

                  </div>


                  <div>

                    <div className="list-title">
                      RISK FACTORS
                    </div>

                    {decision.risk_factors.length >
                    0 ? (
                      decision.risk_factors.map(
                        (
                          factor,
                          index,
                        ) => (
                          <div
                            className="action-row"
                            key={`risk-${index}`}
                          >
                            <span className="action-number">
                              {String(
                                index + 1,
                              ).padStart(
                                2,
                                "0",
                              )}
                            </span>

                            <div>
                              <strong>
                                Risk signal
                              </strong>

                              <span>
                                {factor}
                              </span>
                            </div>
                          </div>
                        ),
                      )
                    ) : (
                      <div className="action-row">
                        <div>
                          <strong>
                            No elevated risk factors
                          </strong>

                          <span>
                            Current release evidence
                            shows no significant
                            decision risk.
                          </span>
                        </div>
                      </div>
                    )}

                  </div>

                </div>


                <div className="decision-section">

                  <div className="list-title">
                    REQUIRED ACTIONS
                  </div>

                  {decision.required_actions.length >
                  0 ? (
                    decision.required_actions.map(
                      (
                        action,
                        index,
                      ) => (
                        <div
                          className="action-row"
                          key={`required-${index}`}
                        >
                          <span className="action-number">
                            {String(
                              index + 1,
                            ).padStart(
                              2,
                              "0",
                            )}
                          </span>

                          <div>
                            <strong>
                              Action {index + 1}
                            </strong>

                            <span>
                              {action}
                            </span>
                          </div>
                        </div>
                      ),
                    )
                  ) : (
                    <div className="action-row">
                      <div>
                        <strong>
                          No required actions
                        </strong>

                        <span>
                          No additional corrective
                          action is currently
                          required.
                        </span>
                      </div>
                    </div>
                  )}

                </div>


                <div className="decision-section">

                  <div className="list-title">
                    DECISION EVIDENCE
                  </div>

                  <div className="evidence-list">

                    {decision.evidence.map(
                      (
                        evidence,
                        index,
                      ) => (
                        <div
                          className="evidence-row"
                          key={`evidence-${index}`}
                        >
                          <span className="evidence-marker">
                            ✓
                          </span>

                          <span>
                            {evidence}
                          </span>
                        </div>
                      ),
                    )}

                  </div>

                </div>

              </div>


              <div className="panel decision-panel">

                <div className="panel-header">

                  <div>
                    <div className="card-label">
                      DECISION ENGINE
                    </div>

                    <h3>
                      Release Decision
                    </h3>
                  </div>

                  <span className="panel-action">
                    Live analysis
                  </span>

                </div>


                <div className="decision-summary">
                  {decision.summary}
                </div>


                <div className="decision-columns">

                  <div>

                    <div className="list-title">
                      RISK FACTORS
                    </div>

                    {risks.length > 0 ? (
                      risks.map(
                        (risk) => (
                          <div
                            className="risk-row"
                            key={risk.area}
                          >

                            <div>
                              <strong>
                                {risk.area}
                              </strong>

                              <span>
                                {risk.level} risk
                              </span>
                            </div>

                            <div
                              className={`risk-score ${
                                risk.level ===
                                "HIGH"
                                  ? "high-risk"
                                  : risk.level ===
                                      "MEDIUM"
                                    ? "medium-risk"
                                    : "low-risk"
                              }`}
                            >
                              {risk.score.toFixed(
                                2,
                              )}
                            </div>

                          </div>
                        ),
                      )
                    ) : (
                      <div className="action-row">
                        <div>
                          <strong>
                            No elevated risk areas
                          </strong>

                          <span>
                            Current release evidence
                            shows no high-risk module.
                          </span>
                        </div>
                      </div>
                    )}

                  </div>


                  <div>

                    <div className="list-title">
                      REQUIRED ACTIONS
                    </div>

                    {recommendations
                      .slice(0, 3)
                      .map(
                        (
                          recommendation,
                          index,
                        ) => (
                          <div
                            className="action-row"
                            key={
                              recommendation.test_case_id
                            }
                          >
                            <span className="action-number">
                              {String(
                                index + 1,
                              ).padStart(
                                2,
                                "0",
                              )}
                            </span>

                            <div>
                              <strong>
                                {
                                  recommendation.test_case_id
                                }
                              </strong>

                              <span>
                                {
                                  recommendation.action
                                }
                              </span>
                            </div>
                          </div>
                        ),
                      )}

                  </div>

                </div>

              </div>


              <div className="panel defects-panel">

                <div className="panel-header">

                  <div>
                    <div className="card-label">
                      DEFECT LANDSCAPE
                    </div>

                    <h3>
                      Open Quality Signals
                    </h3>
                  </div>

                  <span className="defect-count">
                    {defects.total}
                  </span>

                </div>


                <div className="defect-total">
                  <strong>
                    {defects.total}
                  </strong>

                  <span>
                    total defects
                  </span>
                </div>


                <div className="defect-breakdown">

                  <div className="defect-item critical">
                    <span>
                      Critical
                    </span>

                    <strong>
                      {defects.critical}
                    </strong>
                  </div>

                  <div className="defect-item high">
                    <span>
                      High
                    </span>

                    <strong>
                      {defects.high}
                    </strong>
                  </div>

                  <div className="defect-item medium">
                    <span>
                      Medium
                    </span>

                    <strong>
                      {defects.medium}
                    </strong>
                  </div>

                  <div className="defect-item low">
                    <span>
                      Low
                    </span>

                    <strong>
                      {defects.low}
                    </strong>
                  </div>

                </div>


                <div className="defect-note">

                  <span className="note-icon">
                    !
                  </span>

                  <span>
                    {defects.high > 0
                      ? `${defects.high} high-severity defects remain present in the release evidence.`
                      : "No high-severity defects remain present."}
                  </span>

                </div>

              </div>

            </section>


            <section className="execution-panel panel">

              <div className="panel-header">

                <div>
                  <div className="card-label">
                    TEST EXECUTION
                  </div>

                  <h3>
                    Current Release Activity
                  </h3>
                </div>

                <span className="panel-action">
                  Live execution data
                </span>

              </div>


              <div className="execution-bar">

                <div
                  className="execution-passed"
                  style={{
                    width: `${passedPercentage}%`,
                  }}
                ></div>

                <div
                  className="execution-failed"
                  style={{
                    width: `${failedPercentage}%`,
                  }}
                ></div>

                <div
                  className="execution-blocked"
                  style={{
                    width: `${blockedPercentage}%`,
                  }}
                ></div>

              </div>


              <div className="execution-legend">

                <div>
                  <span className="legend-dot passed"></span>
                  Passed{" "}
                  <strong>
                    {summary.passed_tests}
                  </strong>
                </div>

                <div>
                  <span className="legend-dot failed"></span>
                  Failed{" "}
                  <strong>
                    {summary.failed_tests}
                  </strong>
                </div>

                <div>
                  <span className="legend-dot blocked"></span>
                  Blocked{" "}
                  <strong>
                    {summary.blocked_tests}
                  </strong>
                </div>

                <div className="execution-total">
                  Total{" "}
                  <strong>
                    {summary.total_tests}
                  </strong>
                </div>

              </div>

            </section>

          </>
        )}


        {/* =================================================
            RELEASES
            ================================================= */}

        {workspace === "releases" && (
          <>

            <header className="workspace-header">

              <div>

                <div className="eyebrow">
                  QUALITY PORTFOLIO
                </div>

                <h1>
                  Release Portfolio
                </h1>

                <p>
                  Cross-release quality comparison
                  and release health overview.
                </p>

              </div>

              <div className="workspace-header-meta">
                {portfolio.length} releases tracked
              </div>

            </header>


            {portfolioLoading ? (

              <div className="workspace-state">

                <div>

                  <div className="loading-spinner"></div>

                  <h2>
                    Loading release portfolio
                  </h2>

                  <p>
                    Collecting quality intelligence
                    across releases...
                  </p>

                </div>

              </div>

            ) : portfolioError ? (

              <div className="workspace-state">

                <div className="workspace-error">

                  <div className="error-symbol">
                    !
                  </div>

                  <h2>
                    Unable to load portfolio
                  </h2>

                  <p>
                    {portfolioError}
                  </p>

                  <button
                    className="retry-button"
                    onClick={() =>
                      setWorkspace(
                        "overview",
                      )
                    }
                  >
                    Return to Overview
                  </button>

                </div>

              </div>

            ) : (

              <>

                <section className="release-cards">

                  {portfolio.map(
                    (release) => {

                      const statusClass =
                        release.readiness_status ===
                        "READY"
                          ? "ready"
                          : release.readiness_status ===
                              "NOT_READY"
                            ? "not-ready"
                            : "conditional";

                      const statusLabel =
                        release.readiness_status ===
                        "NOT_READY"
                          ? "NOT READY"
                          : release.readiness_status;


                      return (
                        <button
                          className="release-card"
                          key={
                            release.release_version
                          }
                          onClick={() =>
                            openRelease(
                              release.release_version,
                            )
                          }
                        >

                          <div className="release-card-top">

                            <span className="release-version">
                              {
                                release.release_version
                              }
                            </span>

                            <span
                              className={`release-status ${statusClass}`}
                            >
                              {statusLabel}
                            </span>

                          </div>


                          <div className="release-quality">

                            <strong>
                              {release.quality_score.toFixed(
                                2,
                              )}
                            </strong>

                            <span>
                              / 100
                            </span>

                          </div>


                          <div className="release-health">
                            {
                              release.quality_health
                            }{" "}
                            quality health
                          </div>


                          <div className="release-card-metrics">

                            <div>
                              <span>
                                Pass rate
                              </span>

                              <strong>
                                {release.pass_rate.toFixed(
                                  2,
                                )}
                                %
                              </strong>
                            </div>

                            <div>
                              <span>
                                Failed
                              </span>

                              <strong>
                                {
                                  release.failed_tests
                                }
                              </strong>
                            </div>

                            <div>
                              <span>
                                Blocked
                              </span>

                              <strong>
                                {
                                  release.blocked_tests
                                }
                              </strong>
                            </div>

                          </div>

                        </button>
                      );
                    },
                  )}

                </section>


                <section className="portfolio-overview-grid">

                  <div className="portfolio-stat">
                    <span>
                      Releases tracked
                    </span>

                    <strong>
                      {portfolio.length}
                    </strong>

                    <small>
                      Current portfolio
                    </small>
                  </div>


                  <div className="portfolio-stat">
                    <span>
                      Average quality
                    </span>

                    <strong>
                      {averageQuality.toFixed(
                        2,
                      )}
                    </strong>

                    <small>
                      Across tracked releases
                    </small>
                  </div>


                  <div className="portfolio-stat">
                    <span>
                      Average pass rate
                    </span>

                    <strong>
                      {averagePassRate.toFixed(
                        2,
                      )}
                      %
                    </strong>

                    <small>
                      Test execution signal
                    </small>
                  </div>


                  <div className="portfolio-stat">
                    <span>
                      Needs action
                    </span>

                    <strong>
                      {releasesNeedingAction}
                    </strong>

                    <small>
                      Releases not ready
                    </small>
                  </div>

                </section>


                <section className="release-comparison panel">

                  <div className="panel-header">

                    <div>
                      <div className="card-label">
                        RELEASE COMPARISON
                      </div>

                      <h3>
                        Quality Across Releases
                      </h3>
                    </div>

                    <span className="panel-action">
                      {portfolio.length} releases
                    </span>

                  </div>


                  <div className="comparison-table-wrapper">

                    <table className="comparison-table">

                      <thead>

                        <tr>
                          <th>
                            Release
                          </th>

                          <th>
                            Quality
                          </th>

                          <th>
                            Pass Rate
                          </th>

                          <th>
                            Failed
                          </th>

                          <th>
                            Blocked
                          </th>

                          <th>
                            Defects
                          </th>

                          <th>
                            Readiness
                          </th>
                        </tr>

                      </thead>


                      <tbody>

                        {portfolio.map(
                          (release) => {

                            const statusClass =
                              release.readiness_status ===
                              "READY"
                                ? "ready"
                                : release.readiness_status ===
                                    "NOT_READY"
                                  ? "not-ready"
                                  : "conditional";

                            const statusLabel =
                              release.readiness_status ===
                              "NOT_READY"
                                ? "NOT READY"
                                : release.readiness_status;


                            return (
                              <tr
                                key={
                                  release.release_version
                                }
                              >

                                <td>
                                  {
                                    release.release_version
                                  }
                                </td>

                                <td>
                                  {release.quality_score.toFixed(
                                    2,
                                  )}
                                </td>

                                <td>
                                  {release.pass_rate.toFixed(
                                    2,
                                  )}
                                  %
                                </td>

                                <td>
                                  {
                                    release.failed_tests
                                  }
                                </td>

                                <td>
                                  {
                                    release.blocked_tests
                                  }
                                </td>

                                <td>
                                  {
                                    release.total_defects
                                  }
                                </td>

                                <td>
                                  <span
                                    className={`table-status ${statusClass}`}
                                  >
                                    {statusLabel}
                                  </span>
                                </td>

                              </tr>
                            );
                          },
                        )}

                      </tbody>

                    </table>

                  </div>

                </section>

              </>

            )}

          </>
        )}


        {/* =================================================
            RISK INTELLIGENCE
            ================================================= */}

        {workspace === "risk" && (
          <>

            <header className="workspace-header">

              <div>

                <div className="eyebrow">
                  RISK INTELLIGENCE
                </div>

                <h1>
                  Risk Intelligence
                </h1>

                <p>
                  Evidence-driven risk assessment
                  for{" "}
                  <strong>
                    {selectedRelease}
                  </strong>{" "}
                  based on changes, defects, test
                  failures, instability, and business
                  criticality.
                </p>

              </div>

              <div className="workspace-header-meta">
                Release {selectedRelease}
              </div>

            </header>


            <section className="risk-overview-grid">

              <div className="risk-overview-card">

                <span className="risk-overview-label">
                  OVERALL RISK
                </span>

                <div className="risk-overview-value">

                  <strong>
                    {averageRisk.toFixed(2)}
                  </strong>

                  <span>
                    / 100
                  </span>

                </div>

                <div
                  className={`risk-level-badge ${averageRiskClass}`}
                >
                  {averageRiskLabel}
                </div>

                <p>
                  Aggregate risk across identified
                  release areas.
                </p>

              </div>


              <div className="risk-overview-card">

                <span className="risk-overview-label">
                  HIGH RISK AREAS
                </span>

                <strong className="risk-big-number">
                  {highRiskCount}
                </strong>

                <p>
                  Areas requiring immediate QA
                  attention.
                </p>

              </div>


              <div className="risk-overview-card">

                <span className="risk-overview-label">
                  MEDIUM RISK
                </span>

                <strong className="risk-big-number">
                  {mediumRiskCount}
                </strong>

                <p>
                  Areas requiring targeted
                  validation.
                </p>

              </div>


              <div className="risk-overview-card">

                <span className="risk-overview-label">
                  LOW RISK
                </span>

                <strong className="risk-big-number">
                  {lowRiskCount}
                </strong>

                <p>
                  Areas with lower current
                  evidence-based risk.
                </p>

              </div>

            </section>


            {highestRisk ? (

              <section className="risk-feature-panel panel">

                <div className="panel-header">

                  <div>

                    <div className="card-label">
                      HIGHEST PRIORITY
                    </div>

                    <h3>
                      {highestRisk.area}
                    </h3>

                  </div>

                  <div
                    className={`risk-feature-score ${
                      highestRisk.level ===
                      "HIGH"
                        ? "high"
                        : highestRisk.level ===
                            "MEDIUM"
                          ? "medium"
                          : "low"
                    }`}
                  >
                    {highestRisk.score.toFixed(
                      2,
                    )}
                  </div>

                </div>


                <div className="risk-feature-grid">

                  <div className="risk-feature-main">

                    <div className="risk-feature-level">

                      <span
                        className={`risk-level-badge ${
                          highestRisk.level ===
                          "HIGH"
                            ? "high"
                            : highestRisk.level ===
                                "MEDIUM"
                              ? "medium"
                              : "low"
                        }`}
                      >
                        {highestRisk.level} RISK
                      </span>

                      <span>
                        Change{" "}
                        <strong>
                          {
                            highestRisk.change_id
                          }
                        </strong>
                      </span>

                    </div>


                    <h4>
                      Why this area is risky
                    </h4>


                    <div className="risk-reasons">

                      {highestRisk.reasons.map(
                        (
                          reason,
                          index,
                        ) => (
                          <div
                            className="risk-reason"
                            key={`${reason}-${index}`}
                          >

                            <span>
                              {String(
                                index + 1,
                              ).padStart(
                                2,
                                "0",
                              )}
                            </span>

                            <p>
                              {reason}
                            </p>

                          </div>
                        ),
                      )}

                    </div>

                  </div>


                  <div className="risk-evidence">

                    <div className="risk-evidence-title">
                      SUPPORTING EVIDENCE
                    </div>

                    <div className="risk-evidence-grid">

                      <div>
                        <span>
                          High defects
                        </span>

                        <strong>
                          {
                            highestRisk.high_severity_defects
                          }
                        </strong>
                      </div>


                      <div>
                        <span>
                          Failed tests
                        </span>

                        <strong>
                          {
                            highestRisk.failed_tests
                          }
                        </strong>
                      </div>


                      <div>
                        <span>
                          Flaky tests
                        </span>

                        <strong>
                          {
                            highestRisk.flaky_tests
                          }
                        </strong>
                      </div>

                    </div>

                  </div>

                </div>

              </section>

            ) : (

              <section className="panel risk-empty-panel">

                <div className="risk-empty-icon">
                  ✓
                </div>

                <h3>
                  No elevated risk areas
                </h3>

                <p>
                  The current release has no risk
                  areas returned by the intelligence
                  engine.
                </p>

              </section>

            )}


            <section className="risk-list-panel panel">

              <div className="panel-header">

                <div>

                  <div className="card-label">
                    RISK REGISTER
                  </div>

                  <h3>
                    Release Risk Areas
                  </h3>

                </div>

                <span className="panel-action">
                  {risks.length} areas
                </span>

              </div>


              <div className="risk-register">

                {risks.map(
                  (risk, index) => {

                    const levelClass =
                      risk.level === "HIGH"
                        ? "high"
                        : risk.level ===
                            "MEDIUM"
                          ? "medium"
                          : "low";


                    return (
                      <div
                        className="risk-register-row"
                        key={risk.area}
                      >

                        <div className="risk-register-index">
                          {String(
                            index + 1,
                          ).padStart(
                            2,
                            "0",
                          )}
                        </div>


                        <div className="risk-register-area">

                          <strong>
                            {risk.area}
                          </strong>

                          <span>
                            Change{" "}
                            {risk.change_id}
                          </span>

                        </div>


                        <div className="risk-register-evidence">

                          <span>
                            {
                              risk.high_severity_defects
                            }{" "}
                            high defects
                          </span>

                          <span>
                            {risk.failed_tests}{" "}
                            failed
                          </span>

                          <span>
                            {risk.flaky_tests}{" "}
                            flaky
                          </span>

                        </div>


                        <div className="risk-register-level">

                          <span
                            className={`risk-level-badge ${levelClass}`}
                          >
                            {risk.level}
                          </span>

                          <strong>
                            {risk.score.toFixed(
                              2,
                            )}
                          </strong>

                        </div>

                      </div>
                    );
                  },
                )}


                {risks.length === 0 && (
                  <div className="risk-register-empty">
                    No risk areas available for this
                    release.
                  </div>
                )}

              </div>

            </section>


            <section className="risk-method-panel panel">

              <div>

                <div className="card-label">
                  HOW RISK IS CALCULATED
                </div>

                <h3>
                  Evidence, not guesswork.
                </h3>

              </div>


              <div className="risk-method-items">

                <div>
                  <span>
                    01
                  </span>

                  <strong>
                    Code changes
                  </strong>

                  <p>
                    Recently changed functionality
                    establishes the affected area.
                  </p>
                </div>


                <div>
                  <span>
                    02
                  </span>

                  <strong>
                    Defect history
                  </strong>

                  <p>
                    High-severity defects increase
                    the risk signal.
                  </p>
                </div>


                <div>
                  <span>
                    03
                  </span>

                  <strong>
                    Test instability
                  </strong>

                  <p>
                    Failed and flaky executions
                    increase validation priority.
                  </p>
                </div>


                <div>
                  <span>
                    04
                  </span>

                  <strong>
                    Business criticality
                  </strong>

                  <p>
                    Critical functionality receives
                    additional risk weight.
                  </p>
                </div>

              </div>

            </section>

          </>
        )}


        {/* =================================================
            TEST INTELLIGENCE
            ================================================= */}

        {workspace === "test-intelligence" && (
          <div className="test-intelligence-workspace">

            {/* HEADER */}

            <header className="workspace-header test-intelligence-header">

              <div>

                <div className="eyebrow">
                  TEST INTELLIGENCE
                </div>

                <div className="test-intelligence-title-row">

                  <div>

                    <h1>
                      Execution Priority
                    </h1>

                    <p>
                      Evidence-driven recommendations
                      for which tests QA should execute
                      first and why.
                    </p>

                  </div>


                  <div className="test-intelligence-release">

                    <span>
                      ACTIVE RELEASE
                    </span>

                    <strong>
                      {selectedRelease}
                    </strong>

                  </div>

                </div>

              </div>

            </header>


            {/* PRIORITY SNAPSHOT */}

            <section className="test-priority-snapshot">

              <div className="test-priority-card high">

                <div className="test-priority-card-top">

                  <span>
                    HIGH RISK
                  </span>

                  <span className="priority-indicator">
                    !
                  </span>

                </div>

                <strong>
                  {testHighRiskCount}
                </strong>

                <p>
                  Highest execution priority
                </p>

              </div>


              <div className="test-priority-card medium">

                <div className="test-priority-card-top">

                  <span>
                    MEDIUM RISK
                  </span>

                  <span className="priority-indicator">
                    ◐
                  </span>

                </div>

                <strong>
                  {testMediumRiskCount}
                </strong>

                <p>
                  Targeted validation required
                </p>

              </div>


              <div className="test-priority-card failed">

                <div className="test-priority-card-top">

                  <span>
                    FAILED
                  </span>

                  <span className="priority-indicator">
                    ×
                  </span>

                </div>

                <strong>
                  {testFailedCount}
                </strong>

                <p>
                  Tests requiring investigation
                </p>

              </div>


              <div className="test-priority-card blocked">

                <div className="test-priority-card-top">

                  <span>
                    BLOCKED
                  </span>

                  <span className="priority-indicator">
                    ⊘
                  </span>

                </div>

                <strong>
                  {testBlockedCount}
                </strong>

                <p>
                  Blocking conditions remain
                </p>

              </div>

            </section>


            {/* FILTERS */}

            <section className="test-intelligence-controls panel">

              <div className="test-controls-heading">

                <div>

                  <div className="card-label">
                    EXECUTION FILTERS
                  </div>

                  <h3>
                    Focus the QA queue
                  </h3>

                </div>


                <div className="test-filter-result">

                  <strong>
                    {
                      filteredTestRecommendations.length
                    }
                  </strong>

                  <span>
                    of{" "}
                    {testRecommendations.length}{" "}
                    tests
                  </span>

                </div>

              </div>


              <div className="test-filter-groups">

                <div className="test-filter-group">

                  <span>
                    Risk
                  </span>

                  <div className="test-filter-buttons">

                    {(
                      [
                        "ALL",
                        "HIGH",
                        "MEDIUM",
                        "LOW",
                      ] as TestRiskFilter[]
                    ).map(
                      (filter) => (
                        <button
                          key={filter}
                          className={`test-filter-button ${
                            testRiskFilter ===
                            filter
                              ? "active"
                              : ""
                          }`}
                          onClick={() =>
                            setTestRiskFilter(
                              filter,
                            )
                          }
                        >
                          {filter}
                        </button>
                      ),
                    )}

                  </div>

                </div>


                <div className="test-filter-group">

                  <span>
                    Status
                  </span>

                  <div className="test-filter-buttons">

                    {(
                      [
                        "ALL",
                        "FAILED",
                        "BLOCKED",
                        "RECOMMENDED",
                      ] as TestStatusFilter[]
                    ).map(
                      (filter) => (
                        <button
                          key={filter}
                          className={`test-filter-button ${
                            testStatusFilter ===
                            filter
                              ? "active"
                              : ""
                          }`}
                          onClick={() =>
                            setTestStatusFilter(
                              filter,
                            )
                          }
                        >
                          {filter}
                        </button>
                      ),
                    )}

                  </div>

                </div>

              </div>

            </section>


            {/* TEST INTELLIGENCE CONTENT */}

            {testRecommendationsLoading ? (

              <section className="workspace-state">

                <div>

                  <div className="loading-spinner"></div>

                  <h2>
                    Analyzing test priority
                  </h2>

                  <p>
                    Evaluating test failures,
                    defects, instability, and
                    business criticality...
                  </p>

                </div>

              </section>

            ) : testRecommendationsError ? (

              <section className="workspace-state">

                <div className="workspace-error">

                  <div className="error-symbol">
                    !
                  </div>

                  <h2>
                    Unable to load Test
                    Intelligence
                  </h2>

                  <p>
                    {testRecommendationsError}
                  </p>

                  <button
                    className="retry-button"
                    onClick={() =>
                      setWorkspace(
                        "overview",
                      )
                    }
                  >
                    Return to Overview
                  </button>

                </div>

              </section>

            ) : (

              <section className="test-intelligence-list panel">

                <div className="test-queue-header">

                  <div>

                    <div className="card-label">
                      EXECUTION QUEUE
                    </div>

                    <h3>
                      What should QA execute
                      first?
                    </h3>

                    <p>
                      Tests are ranked by release
                      evidence, risk, and execution
                      history.
                    </p>

                  </div>


                  <div className="test-queue-meta">

                    <span>
                      HIGHER SCORE
                    </span>

                    <strong>
                      HIGHER PRIORITY
                    </strong>

                  </div>

                </div>


                {filteredTestRecommendations.length >
                0 ? (

                  <div className="test-recommendation-list">

                    {filteredTestRecommendations.map(
                      (
                        test,
                        index,
                      ) => {

                        const riskClass =
                          getTestRiskClass(
                            test.risk_level,
                          );

                        const statusClass =
                          getTestStatusClass(
                            test.status,
                          );


                        return (
                          <article
                            className={`test-recommendation-card ${riskClass} ${statusClass}`}
                            key={
                              test.test_case_id
                            }
                          >

                            <div className="test-recommendation-rank">

                              <span>
                                PRIORITY
                              </span>

                              <strong>
                                {String(
                                  index + 1,
                                ).padStart(
                                  2,
                                  "0",
                                )}
                              </strong>

                            </div>


                            <div className="test-recommendation-main">

                              <div className="test-recommendation-heading">

                                <div className="test-title-block">

                                  <span className="test-case-id">
                                    {
                                      test.test_case_id
                                    }
                                  </span>

                                  <h4>
                                    {test.title}
                                  </h4>

                                </div>


                                <div className="test-recommendation-score">

                                  <span>
                                    PRIORITY SCORE
                                  </span>

                                  <div>

                                    <strong>
                                      {test.score}
                                    </strong>

                                    <small>
                                      / 100
                                    </small>

                                  </div>


                                  <div className="test-score-track">

                                    <div
                                      className={`test-score-fill ${riskClass}`}
                                      style={{
                                        width: `${Math.min(
                                          test.score,
                                          100,
                                        )}%`,
                                      }}
                                    ></div>

                                  </div>

                                </div>

                              </div>


                              <div className="test-recommendation-meta">

                                <span
                                  className={`test-risk-badge ${riskClass}`}
                                >
                                  {test.risk_level}{" "}
                                  RISK
                                </span>


                                <span
                                  className={`test-status-badge ${statusClass}`}
                                >
                                  {test.status}
                                </span>


                                <span className="test-module">

                                  MODULE

                                  <strong>
                                    {test.module}
                                  </strong>

                                </span>

                              </div>


                              <div className="test-recommendation-details">

                                <div className="test-evidence">

                                  <div className="test-detail-title">
                                    WHY IT'S PRIORITIZED
                                  </div>


                                  <div className="test-reason-list">

                                    {test.reasons.map(
                                      (
                                        reason,
                                        reasonIndex,
                                      ) => (
                                        <div
                                          className="test-reason"
                                          key={`${test.test_case_id}-${reasonIndex}`}
                                        >

                                          <span>
                                            {String(
                                              reasonIndex +
                                                1,
                                            ).padStart(
                                              2,
                                              "0",
                                            )}
                                          </span>

                                          <p>
                                            {reason}
                                          </p>

                                        </div>
                                      ),
                                    )}

                                  </div>

                                </div>


                                <div className="test-action">

                                  <div className="test-detail-title">
                                    QA ACTION
                                  </div>

                                  <p>
                                    {test.action}
                                  </p>


                                  {test.blocking_reason && (
                                    <div className="test-blocking-reason">

                                      <span>
                                        BLOCKING CONDITION
                                      </span>

                                      <strong>
                                        {
                                          test.blocking_reason
                                        }
                                      </strong>

                                    </div>
                                  )}

                                </div>

                              </div>

                            </div>

                          </article>
                        );
                      },
                    )}

                  </div>

                ) : (

                  <div className="test-intelligence-empty">

                    <div className="risk-empty-icon">
                      ✓
                    </div>

                    <h3>
                      No tests match these
                      filters
                    </h3>

                    <p>
                      Try clearing one or both
                      filters to view the complete
                      execution priority list.
                    </p>

                    <button
                      className="retry-button"
                      onClick={() => {
                        setTestRiskFilter(
                          "ALL",
                        );

                        setTestStatusFilter(
                          "ALL",
                        );
                      }}
                    >
                      Clear filters
                    </button>

                  </div>

                )}

              </section>

            )}


            {/* INTELLIGENCE MODEL */}

            {!testRecommendationsLoading &&
              !testRecommendationsError &&
              testRecommendations.length >
                0 && (

                <section className="test-intelligence-method panel">

                  <div className="test-method-heading">

                    <div>

                      <div className="card-label">
                        INTELLIGENCE MODEL
                      </div>

                      <h3>
                        How Test Intelligence
                        decides
                      </h3>

                      <p>
                        The recommendation engine
                        evaluates release evidence and
                        converts it into an execution
                        priority.
                      </p>

                    </div>


                    <div className="test-method-score-note">

                      <span>
                        PRIORITY LOGIC
                      </span>

                      <strong>
                        Evidence → Score → Queue
                      </strong>

                    </div>

                  </div>


                  <div className="test-method-items">

                    <div>

                      <span>
                        01
                      </span>

                      <strong>
                        Defect Evidence
                      </strong>

                      <p>
                        Critical and high-severity
                        defects increase the priority
                        of affected tests.
                      </p>

                    </div>


                    <div>

                      <span>
                        02
                      </span>

                      <strong>
                        Current Failures
                      </strong>

                      <p>
                        Tests that failed in the
                        current release receive
                        additional priority.
                      </p>

                    </div>


                    <div>

                      <span>
                        03
                      </span>

                      <strong>
                        Business Criticality
                      </strong>

                      <p>
                        Business-critical
                        functionality receives
                        additional execution weight.
                      </p>

                    </div>


                    <div>

                      <span>
                        04
                      </span>

                      <strong>
                        Test Instability
                      </strong>

                      <p>
                        Unstable tests are surfaced so
                        QA can validate them before
                        release decisions.
                      </p>

                    </div>

                  </div>

                </section>

              )}

          </div>
        )}


        {/* =================================================
            AI AGENT
            ================================================= */}

        {workspace === "agent" && (
          <div className="agent-workspace">

            {/* AGENT HEADER */}

            <header className="agent-command-header">

              <div className="agent-command-title">

                <div className="eyebrow">
                  AI-ASSISTED QA
                </div>

                <div className="agent-title-line">

                  <div>

                    <h1>
                      QA Intelligence Agent
                    </h1>

                    <p>
                      Evidence-driven QA analysis
                      for the currently selected
                      release.
                    </p>

                  </div>


                  <div className="agent-live-state">

                    <span className="agent-live-dot"></span>

                    AGENT ACTIVE

                  </div>

                </div>

              </div>


              <div className="agent-release-chip">

                <span>
                  ACTIVE RELEASE
                </span>

                <strong>
                  {selectedRelease}
                </strong>

              </div>

            </header>


            {/* QUESTION / COMMAND CENTER */}

            <section className="agent-command-panel">

              <div className="agent-command-top">

                <div>

                  <span className="agent-section-kicker">
                    QA COMMAND
                  </span>

                  <h2>
                    What do you want to know?
                  </h2>

                  <p>
                    Ask about release readiness,
                    risks, defects, test priorities,
                    or the actions QA should take
                    next.
                  </p>

                </div>


                <div className="agent-command-symbol">
                  ✦
                </div>

              </div>


              <textarea
                className="agent-question-input"
                value={agentMessage}
                onChange={(event) =>
                  setAgentMessage(
                    event.target.value,
                  )
                }
                placeholder="Ask the QA agent about this release..."
                rows={4}
                disabled={agentLoading}
              />


              <div className="agent-command-footer">

                <div className="agent-command-note">

                  <span>
                    ●
                  </span>

                  <p>
                    Release context is inherited
                    automatically from the global
                    release selector.
                  </p>

                </div>


                <button
                  className="agent-analyze-button"
                  onClick={
                    handleAgentAnalyze
                  }
                  disabled={
                    agentLoading ||
                    !agentMessage.trim() ||
                    !selectedRelease
                  }
                >

                  {agentLoading ? (
                    <>
                      <span className="agent-button-spinner"></span>
                      ANALYZING
                    </>
                  ) : (
                    <>
                      ANALYZE RELEASE
                      <span>
                        ↗
                      </span>
                    </>
                  )}

                </button>

              </div>


              {agentError && (
                <div className="agent-error">

                  <span className="agent-error-icon">
                    !
                  </span>

                  <div>

                    <strong>
                      Agent analysis failed
                    </strong>

                    <p>
                      {agentError}
                    </p>

                  </div>

                </div>
              )}

            </section>


            {/* ANALYSIS LOADING */}

            {agentLoading && (
              <section className="agent-analysis-loading">

                <div className="agent-loading-mark">

                  <span></span>
                  <span></span>
                  <span></span>

                </div>


                <div>

                  <span className="agent-section-kicker">
                    ANALYSIS IN PROGRESS
                  </span>

                  <h3>
                    Building release intelligence
                  </h3>

                  <p>
                    Evaluating release readiness,
                    defects, module risk, Test
                    Intelligence, and product quality
                    evidence.
                  </p>

                </div>

              </section>
            )}


            {/* RESULTS */}

            {!agentLoading &&
              agentAnalysis && (

                <div className="agent-results">

                  {/* DECISION HERO */}

                  <section className="agent-decision-hero">

                    <div className="agent-decision-main">

                      <div className="agent-result-kicker">
                        RELEASE DECISION
                      </div>


                      <div className="agent-decision-heading">

                        <h2>
                          {agentAnalysis.status ===
                          "NOT_READY"
                            ? "NOT READY"
                            : agentAnalysis.status}
                        </h2>


                        <span
                          className={`agent-status-badge ${getAgentStatusClass(
                            agentAnalysis.status,
                          )}`}
                        >
                          {agentAnalysis.status.replace(
                            "_",
                            " ",
                          )}
                        </span>

                      </div>


                      <p>
                        {agentAnalysis.assessment}
                      </p>

                    </div>


                    <div className="agent-decision-meta">

                      <div>

                        <span>
                          CONFIDENCE
                        </span>

                        <strong>
                          {
                            agentAnalysis.confidence
                          }
                        </strong>

                      </div>


                      <div>

                        <span>
                          RELEASE
                        </span>

                        <strong>
                          {
                            agentAnalysis.release_version
                          }
                        </strong>

                      </div>


                      <div>

                        <span>
                          ENGINE
                        </span>

                        <strong>
                          AI + EVIDENCE
                        </strong>

                      </div>

                    </div>

                  </section>


                  {/* EVIDENCE SNAPSHOT */}

                  <section className="agent-evidence-strip">

                    <div className="agent-strip-heading">

                      <span className="agent-section-kicker">
                        EVIDENCE SNAPSHOT
                      </span>

                      <span>
                        Confirmed intelligence
                      </span>

                    </div>


                    <div className="agent-fact-metrics">

                      {agentAnalysis.facts
                        .slice(0, 5)
                        .map(
                          (
                            fact,
                            index,
                          ) => (
                            <div
                              className="agent-fact-metric"
                              key={`metric-${index}`}
                            >

                              <span>
                                {String(
                                  index + 1,
                                ).padStart(
                                  2,
                                  "0",
                                )}
                              </span>

                              <p>
                                {fact}
                              </p>

                            </div>
                          ),
                        )}

                    </div>

                  </section>


                  {/* RISK INTELLIGENCE */}

                  <section className="agent-section">

                    <div className="agent-section-header">

                      <div>

                        <span className="agent-section-kicker">
                          MODULE RISK
                        </span>

                        <h2>
                          Areas requiring attention
                        </h2>

                      </div>


                      <span className="agent-section-count">
                        {agentAnalysis.risks.length}{" "}
                        AREAS
                      </span>

                    </div>


                    <div className="agent-risk-grid">

                      {agentAnalysis.risks.map(
                        (
                          risk,
                          index,
                        ) => {

                          const riskClass =
                            getAgentPriorityClass(
                              risk.level,
                            );


                          return (
                            <article
                              className={`agent-risk-card ${riskClass}`}
                              key={`${risk.module}-${index}`}
                            >

                              <div className="agent-risk-card-top">

                                <span className="agent-risk-number">
                                  {String(
                                    index + 1,
                                  ).padStart(
                                    2,
                                    "0",
                                  )}
                                </span>

                                <span
                                  className={`agent-risk-level ${riskClass}`}
                                >
                                  {risk.level}
                                </span>

                              </div>


                              <div className="agent-risk-card-title">

                                <h3>
                                  {risk.module}
                                </h3>

                                <strong>
                                  {risk.score.toFixed(
                                    2,
                                  )}
                                </strong>

                              </div>


                              <div className="agent-risk-score-track">

                                <div
                                  className={`agent-risk-score-fill ${riskClass}`}
                                  style={{
                                    width: `${Math.min(
                                      risk.score,
                                      100,
                                    )}%`,
                                  }}
                                />

                              </div>


                              <p>
                                {risk.reason}
                              </p>

                            </article>
                          );
                        },
                      )}

                    </div>

                  </section>


                  {/* QA ACTION PLAN */}

                  <section className="agent-action-section">

                    <div className="agent-section-header">

                      <div>

                        <span className="agent-section-kicker">
                          QA PRIORITY QUEUE
                        </span>

                        <h2>
                          What should QA do next?
                        </h2>

                        <p>
                          Actions are ordered according
                          to the evidence available to
                          the agent.
                        </p>

                      </div>


                      <span className="agent-section-count">
                        {
                          agentAnalysis
                            .recommendations
                            .length
                        }{" "}
                        ACTIONS
                      </span>

                    </div>


                    <div className="agent-action-list">

                      {agentAnalysis.recommendations.map(
                        (
                          recommendation,
                          index,
                        ) => (
                          <article
                            className="agent-action-card"
                            key={`action-${index}`}
                          >

                            <div className="agent-action-index">
                              {String(
                                index + 1,
                              ).padStart(
                                2,
                                "0",
                              )}
                            </div>


                            <div className="agent-action-content">

                              <div className="agent-action-heading">

                                <h3>
                                  {
                                    recommendation.action
                                  }
                                </h3>

                                <span
                                  className={`agent-priority-badge ${getAgentPriorityClass(
                                    recommendation.priority,
                                  )}`}
                                >
                                  {
                                    recommendation.priority
                                  }
                                </span>

                              </div>


                              <p>
                                {
                                  recommendation.reason
                                }
                              </p>

                            </div>


                            <div className="agent-action-arrow">
                              →
                            </div>

                          </article>
                        ),
                      )}


                      {agentAnalysis.recommendations
                        .length === 0 && (
                        <div className="agent-empty">
                          No additional QA actions
                          were returned by the
                          agent.
                        </div>
                      )}

                    </div>

                  </section>


                  {/* LOWER INTELLIGENCE GRID */}

                  <section className="agent-lower-grid">

                    {/* MISSING EVIDENCE */}

                    <div className="agent-evidence-gap">

                      <div className="agent-section-header compact">

                        <div>

                          <span className="agent-section-kicker">
                            EVIDENCE GAPS
                          </span>

                          <h2>
                            What do we still need?
                          </h2>

                        </div>

                        <span className="agent-gap-symbol">
                          !
                        </span>

                      </div>


                      {agentAnalysis
                        .missing_evidence
                        .length > 0 ? (

                        <div className="agent-gap-list">

                          {agentAnalysis.missing_evidence.map(
                            (
                              item,
                              index,
                            ) => (
                              <div
                                className="agent-gap-row"
                                key={`gap-${index}`}
                              >

                                <span>
                                  0
                                  {index + 1}
                                </span>

                                <div>

                                  <strong>
                                    Evidence unavailable
                                  </strong>

                                  <p>
                                    {item}
                                  </p>

                                </div>

                              </div>
                            ),
                          )}

                        </div>

                      ) : (

                        <div className="agent-no-missing">

                          <span>
                            ✓
                          </span>

                          <p>
                            No important missing
                            evidence was identified.
                          </p>

                        </div>

                      )}

                    </div>


                    {/* HUMAN DECISION */}

                    <div className="agent-human-decision">

                      <span className="agent-section-kicker">
                        HUMAN DECISION
                      </span>

                      <h2>
                        What still requires
                        judgment?
                      </h2>

                      <p>
                        {
                          agentAnalysis.human_decision
                        }
                      </p>

                      <div className="agent-human-note">

                        <span>
                          HUMAN APPROVAL
                        </span>

                        <strong>
                          REQUIRED
                        </strong>

                      </div>

                    </div>

                  </section>


                  {/* AGENT PRINCIPLE */}

                  <section className="agent-principle">

                    <div>

                      <span className="agent-section-kicker">
                        AGENT PRINCIPLE
                      </span>

                      <h2>
                        AI assists. Evidence
                        decides.
                      </h2>

                      <p>
                        The agent combines
                        deterministic QA Intelligence
                        with AI reasoning. It separates
                        facts from inference, identifies
                        evidence gaps, and keeps final
                        release approval with the human
                        team.
                      </p>

                    </div>


                    <div className="agent-principle-flow">

                      <div>
                        <span>
                          01
                        </span>

                        <strong>
                          Evidence
                        </strong>
                      </div>

                      <i>
                        →
                      </i>

                      <div>
                        <span>
                          02
                        </span>

                        <strong>
                          Intelligence
                        </strong>
                      </div>

                      <i>
                        →
                      </i>

                      <div>
                        <span>
                          03
                        </span>

                        <strong>
                          AI Reasoning
                        </strong>
                      </div>

                      <i>
                        →
                      </i>

                      <div>
                        <span>
                          04
                        </span>

                        <strong>
                          QA Action
                        </strong>
                      </div>

                    </div>

                  </section>

                </div>
              )}


            {/* EMPTY / READY STATE */}

            {!agentLoading &&
              !agentAnalysis &&
              !agentError && (

                <section className="agent-ready-state">

                  <div className="agent-ready-mark">
                    ✦
                  </div>


                  <div>

                    <span className="agent-section-kicker">
                      READY FOR ANALYSIS
                    </span>

                    <h2>
                      Ask the QA Intelligence Agent
                    </h2>

                    <p>
                      The agent will analyze{" "}
                      <strong>
                        {selectedRelease}
                      </strong>{" "}
                      using release readiness,
                      defects, module risk, Test
                      Intelligence, and product quality
                      evidence.
                    </p>

                  </div>

                </section>

              )}

          </div>
        )}

      </main>
    </div>
  );
}


export default App;
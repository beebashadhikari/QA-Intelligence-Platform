import { useEffect, useMemo, useState } from "react";
import {
  getReleasePortfolio,
  type ReleasePortfolioItem,
} from "../api/dashboard";

interface ReleasesWorkspaceProps {
  onOpenRelease: (releaseVersion: string) => void;
}

function ReleasesWorkspace({
  onOpenRelease,
}: ReleasesWorkspaceProps) {
  const [releases, setReleases] = useState<
    ReleasePortfolioItem[]
  >([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(
    null,
  );

  useEffect(() => {
    async function loadPortfolio() {
      try {
        setLoading(true);
        setError(null);

        const data = await getReleasePortfolio();

        setReleases(data);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load release portfolio.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadPortfolio();
  }, []);

  const orderedReleases = useMemo(() => {
    return [...releases].sort((a, b) =>
      b.release_version.localeCompare(
        a.release_version,
        undefined,
        {
          numeric: true,
        },
      ),
    );
  }, [releases]);

  const currentRelease = orderedReleases[0];

  const previousRelease = orderedReleases[1];

  const qualityChange =
    currentRelease && previousRelease
      ? currentRelease.quality_score -
        previousRelease.quality_score
      : 0;

  const passRateChange =
    currentRelease && previousRelease
      ? currentRelease.pass_rate -
        previousRelease.pass_rate
      : 0;

  const maxQuality = Math.max(
    ...orderedReleases.map(
      (release) => release.quality_score,
    ),
    100,
  );

  const statusClass = (
    status: string,
  ) => {
    if (status === "READY") {
      return "ready";
    }

    if (status === "NOT_READY") {
      return "not-ready";
    }

    if (status === "BLOCKED") {
      return "blocked";
    }

    return "conditional";
  };

  if (loading) {
    return (
      <main className="main-content">
        <section className="workspace-state">
          <div>
            <div className="loading-spinner"></div>

            <h2>
              Loading release intelligence
            </h2>

            <p>
              Building the historical release view...
            </p>
          </div>
        </section>
      </main>
    );
  }

  if (error) {
    return (
      <main className="main-content">
        <section className="workspace-state">
          <div className="workspace-error">
            <div className="error-symbol">
              !
            </div>

            <h2>
              Unable to load releases
            </h2>

            <p>{error}</p>

            <button
              className="retry-button"
              onClick={() =>
                window.location.reload()
              }
            >
              Retry connection
            </button>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="main-content">
      <header className="workspace-topbar">
        <div>
          <div className="eyebrow">
            RELEASE INTELLIGENCE
          </div>

          <h1>Release Portfolio</h1>

          <p className="workspace-description">
            Historical quality signals across product
            releases.
          </p>
        </div>

        <div className="portfolio-context">
          <span className="portfolio-context-dot"></span>

          <span>
            {orderedReleases.length} releases tracked
          </span>
        </div>
      </header>

      {currentRelease && (
        <>
          <section className="current-release">
            <div className="current-release-main">
              <div className="current-release-heading">
                <div>
                  <div className="section-kicker">
                    CURRENT RELEASE
                  </div>

                  <div className="current-release-version">
                    {currentRelease.release_version}
                  </div>
                </div>

                <button
                  className={`portfolio-status ${statusClass(
                    currentRelease.readiness_status,
                  )}`}
                  onClick={() =>
                    onOpenRelease(
                      currentRelease.release_version,
                    )
                  }
                >
                  {currentRelease.readiness_status.replace(
                    "_",
                    " ",
                  )}
                </button>
              </div>

              <div className="current-quality-row">
                <div className="current-quality">
                  <span className="quality-number">
                    {currentRelease.quality_score.toFixed(
                      2,
                    )}
                  </span>

                  <span className="quality-denominator">
                    /100
                  </span>
                </div>

                <div
                  className={`quality-change ${
                    qualityChange >= 0
                      ? "positive"
                      : "negative"
                  }`}
                >
                  <span>
                    {qualityChange >= 0
                      ? "↑"
                      : "↓"}
                  </span>

                  {Math.abs(
                    qualityChange,
                  ).toFixed(2)}

                  <small>
                    vs previous
                  </small>
                </div>
              </div>

              <div className="current-quality-track">
                <div
                  className="current-quality-fill"
                  style={{
                    width: `${Math.min(
                      currentRelease.quality_score,
                      100,
                    )}%`,
                  }}
                ></div>
              </div>

              <div className="current-quality-labels">
                <span>
                  Quality health
                </span>

                <strong>
                  {currentRelease.quality_health}
                </strong>
              </div>
            </div>

            <div className="current-release-signals">
              <div className="signal-heading">
                RELEASE SIGNALS
              </div>

              <div className="signal-list">
                <div className="signal">
                  <span>Pass rate</span>

                  <strong>
                    {currentRelease.pass_rate.toFixed(
                      2,
                    )}
                    %
                  </strong>

                  <small
                    className={
                      passRateChange >= 0
                        ? "signal-positive"
                        : "signal-negative"
                    }
                  >
                    {passRateChange >= 0
                      ? "↑"
                      : "↓"}{" "}
                    {Math.abs(
                      passRateChange,
                    ).toFixed(2)}
                    % vs previous
                  </small>
                </div>

                <div className="signal">
                  <span>Failed tests</span>

                  <strong>
                    {currentRelease.failed_tests}
                  </strong>

                  <small>
                    of{" "}
                    {currentRelease.total_tests}{" "}
                    executed
                  </small>
                </div>

                <div className="signal">
                  <span>Blocked</span>

                  <strong>
                    {currentRelease.blocked_tests}
                  </strong>

                  <small>
                    execution conditions
                  </small>
                </div>

                <div className="signal">
                  <span>Defects</span>

                  <strong>
                    {currentRelease.total_defects}
                  </strong>

                  <small>
                    {currentRelease.critical_defects >
                    0
                      ? `${currentRelease.critical_defects} critical`
                      : "No critical defects"}
                  </small>
                </div>
              </div>
            </div>
          </section>

          <section className="trajectory-section">
            <div className="section-heading-row">
              <div>
                <div className="section-kicker">
                  QUALITY TRAJECTORY
                </div>

                <h2>
                  Release quality over time
                </h2>
              </div>

              <span className="section-note">
                Higher is better
              </span>
            </div>

            <div className="trajectory">
              <div className="trajectory-scale">
                <span>100</span>
                <span>75</span>
                <span>50</span>
                <span>25</span>
                <span>0</span>
              </div>

              <div className="trajectory-chart">
                <div className="trajectory-grid">
                  <span></span>
                  <span></span>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>

                <div className="trajectory-points">
                  {orderedReleases
                    .slice()
                    .reverse()
                    .map(
                      (
                        release,
                        index,
                      ) => {
                        const bottom =
                          (release.quality_score /
                            maxQuality) *
                          100;

                        return (
                          <button
                            key={
                              release.release_version
                            }
                            className={`trajectory-point ${
                              index ===
                              orderedReleases.length -
                                1
                                ? "current"
                                : ""
                            }`}
                            style={{
                              left:
                                orderedReleases.length ===
                                1
                                  ? "50%"
                                  : `${
                                      (index /
                                        (orderedReleases.length -
                                          1)) *
                                      100
                                    }%`,
                              bottom: `${Math.min(
                                bottom,
                                96,
                              )}%`,
                            }}
                            onClick={() =>
                              onOpenRelease(
                                release.release_version,
                              )
                            }
                            title={`${release.release_version}: ${release.quality_score.toFixed(
                              2,
                            )}`}
                          >
                            <span className="point-value">
                              {release.quality_score.toFixed(
                                2,
                              )}
                            </span>

                            <span className="point-dot"></span>
                          </button>
                        );
                      },
                    )}
                </div>

                <div className="trajectory-labels">
                  {orderedReleases
                    .slice()
                    .reverse()
                    .map(
                      (release) => (
                        <button
                          key={
                            release.release_version
                          }
                          onClick={() =>
                            onOpenRelease(
                              release.release_version,
                            )
                          }
                        >
                          {
                            release.release_version
                          }
                        </button>
                      ),
                    )}
                </div>
              </div>
            </div>
          </section>

          <section className="release-history">
            <div className="section-heading-row">
              <div>
                <div className="section-kicker">
                  RELEASE HISTORY
                </div>

                <h2>
                  Compare release health
                </h2>
              </div>

              <span className="section-note">
                Select a release for detailed analysis
              </span>
            </div>

            <div className="history-list">
              {orderedReleases.map(
                (release, index) => (
                  <button
                    key={
                      release.release_version
                    }
                    className={`history-row ${
                      index === 0
                        ? "current"
                        : ""
                    }`}
                    onClick={() =>
                      onOpenRelease(
                        release.release_version,
                      )
                    }
                  >
                    <div className="history-release">
                      <span className="history-index">
                        {String(
                          index + 1,
                        ).padStart(2, "0")}
                      </span>

                      <div>
                        <strong>
                          {
                            release.release_version
                          }
                        </strong>

                        {index === 0 && (
                          <span className="history-current">
                            CURRENT
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="history-quality">
                      <span>
                        Quality
                      </span>

                      <strong>
                        {release.quality_score.toFixed(
                          2,
                        )}
                      </strong>
                    </div>

                    <div className="history-pass">
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

                    <div className="history-tests">
                      <span>
                        Execution
                      </span>

                      <strong>
                        <em className="passed-count">
                          {release.passed_tests}
                        </em>
                        /
                        {release.total_tests}
                      </strong>
                    </div>

                    <div className="history-defects">
                      <span>
                        Defects
                      </span>

                      <strong>
                        {release.total_defects}
                      </strong>
                    </div>

                    <div
                      className={`history-status ${statusClass(
                        release.readiness_status,
                      )}`}
                    >
                      {release.readiness_status.replace(
                        "_",
                        " ",
                      )}
                    </div>

                    <span className="history-arrow">
                      →
                    </span>
                  </button>
                ),
              )}
            </div>
          </section>
        </>
      )}
    </main>
  );
}

export default ReleasesWorkspace;
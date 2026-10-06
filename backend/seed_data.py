from backend.app.database import SessionLocal
from backend.app.models.release import Release
from backend.app.models.case import TestCase
from backend.app.models.execution import TestExecution
from backend.app.models.defect import Defect
from backend.app.models.change import Change


def release_exists(db, release_version: str) -> bool:
    return (
        db.query(Release)
        .filter(Release.release_version == release_version)
        .first()
        is not None
    )


def seed_release_2_4_0(db):
    if release_exists(db, "2.4.0"):
        print("Release 2.4.0 already exists. Skipping.")
        return

    release = Release(
        release_version="2.4.0",
        total_tests=248,
        passed_tests=231,
        failed_tests=9,
        blocked_tests=8,
        critical_defects=0,
        high_defects=2,
        medium_defects=1,
        low_defects=1,
        regression_status="PASSED",
        smoke_status="PASSED",
    )

    db.add(release)
    db.flush()

    test_cases = [
        TestCase(
            test_case_id="TC-101",
            title="Valid login",
            module="Authentication",
            test_type="functional",
            priority="critical",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-102",
            title="Password reset",
            module="Authentication",
            test_type="functional",
            priority="high",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-103",
            title="Successful checkout",
            module="Payments",
            test_type="integration",
            priority="critical",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-104",
            title="Refund processing",
            module="Payments",
            test_type="functional",
            priority="high",
            automated=False,
        ),
        TestCase(
            test_case_id="TC-105",
            title="Product search",
            module="Catalog",
            test_type="functional",
            priority="medium",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-106",
            title="Product filtering",
            module="Catalog",
            test_type="functional",
            priority="medium",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-107",
            title="Order history",
            module="Orders",
            test_type="functional",
            priority="high",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-108",
            title="Order cancellation",
            module="Orders",
            test_type="functional",
            priority="high",
            automated=True,
        ),
    ]

    db.add_all(test_cases)

    executions = [
        TestExecution(
            test_case_id="TC-101",
            release_id=release.id,
            release_version="2.4.0",
            status="passed",
            environment="staging",
            duration_seconds=1.2,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-102",
            release_id=release.id,
            release_version="2.4.0",
            status="failed",
            environment="staging",
            duration_seconds=2.4,
            is_flaky=False,
            failure_reason="Password reset token validation failed.",
        ),
        TestExecution(
            test_case_id="TC-103",
            release_id=release.id,
            release_version="2.4.0",
            status="failed",
            environment="staging",
            duration_seconds=5.8,
            is_flaky=False,
            failure_reason="Payment checkout authorization failed.",
        ),
        TestExecution(
            test_case_id="TC-104",
            release_id=release.id,
            release_version="2.4.0",
            status="blocked",
            environment="staging",
            duration_seconds=None,
            is_flaky=False,
            failure_reason="Refund sandbox unavailable.",
        ),
        TestExecution(
            test_case_id="TC-105",
            release_id=release.id,
            release_version="2.4.0",
            status="passed",
            environment="staging",
            duration_seconds=1.7,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-106",
            release_id=release.id,
            release_version="2.4.0",
            status="passed",
            environment="staging",
            duration_seconds=2.1,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-107",
            release_id=release.id,
            release_version="2.4.0",
            status="passed",
            environment="staging",
            duration_seconds=2.9,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-108",
            release_id=release.id,
            release_version="2.4.0",
            status="passed",
            environment="staging",
            duration_seconds=2.6,
            is_flaky=False,
        ),
    ]

    db.add_all(executions)

    defects = [
        Defect(
            defect_id="BUG-101",
            title="Checkout payment authorization failure",
            module="Payments",
            severity="high",
            priority="high",
            status="open",
            release=release,
            release_version="2.4.0",
        ),
        Defect(
            defect_id="BUG-102",
            title="Authentication session regression",
            module="Authentication",
            severity="high",
            priority="high",
            status="open",
            release=release,
            release_version="2.4.0",
        ),
       Defect(
    defect_id="BUG-103",
    title="Refund workflow validation issue",
    module="Orders",
    severity="medium",
    priority="medium",
    status="in_progress",
    release=release,
    release_version="2.4.0",
),
        Defect(
    defect_id="BUG-104",
    title="Order history display issue",
    module="Catalog",
    severity="low",
    priority="low",
    status="resolved",
    release=release,
    release_version="2.4.0",
),
    ]

    db.add_all(defects)

    changes = [
        Change(
            change_id="CHG-101",
            release_version="2.4.0",
            module="Payments",
            description="Payment checkout and authorization logic changed.",
            impact_score=95,
            business_critical=True,
        ),
        Change(
            change_id="CHG-102",
            release_version="2.4.0",
            module="Authentication",
            description="Authentication and session handling changed.",
            impact_score=85,
            business_critical=True,
        ),
        Change(
            change_id="CHG-103",
            release_version="2.4.0",
            module="Orders",
            description="Order history improvements introduced.",
            impact_score=45,
            business_critical=False,
        ),
    ]

    db.add_all(changes)

    print("Created release 2.4.0.")


def seed_release_2_3_0(db):
    if release_exists(db, "2.3.0"):
        print("Release 2.3.0 already exists. Skipping.")
        return

    release = Release(
        release_version="2.3.0",
        total_tests=240,
        passed_tests=234,
        failed_tests=4,
        blocked_tests=2,
        critical_defects=0,
        high_defects=0,
        medium_defects=2,
        low_defects=4,
        regression_status="PASSED",
        smoke_status="PASSED",
    )

    db.add(release)
    db.flush()

    test_cases = [
        TestCase(
            test_case_id="TC-201",
            title="Valid login",
            module="Authentication",
            test_type="functional",
            priority="critical",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-202",
            title="Password reset",
            module="Authentication",
            test_type="functional",
            priority="high",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-203",
            title="Successful checkout",
            module="Payments",
            test_type="integration",
            priority="critical",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-204",
            title="Refund processing",
            module="Payments",
            test_type="functional",
            priority="high",
            automated=False,
        ),
        TestCase(
            test_case_id="TC-205",
            title="Product search",
            module="Catalog",
            test_type="functional",
            priority="medium",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-206",
            title="Order history",
            module="Orders",
            test_type="functional",
            priority="high",
            automated=True,
        ),
    ]

    db.add_all(test_cases)

    executions = [
        TestExecution(
            test_case_id="TC-201",
            release_id=release.id,
            release_version="2.3.0",
            status="passed",
            environment="staging",
            duration_seconds=1.1,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-202",
            release_id=release.id,
            release_version="2.3.0",
            status="passed",
            environment="staging",
            duration_seconds=2.0,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-203",
            release_id=release.id,
            release_version="2.3.0",
            status="passed",
            environment="staging",
            duration_seconds=4.6,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-204",
            release_id=release.id,
            release_version="2.3.0",
            status="blocked",
            environment="staging",
            duration_seconds=None,
            is_flaky=False,
            failure_reason="Refund test data unavailable",
        ),
        TestExecution(
            test_case_id="TC-205",
            release_id=release.id,
            release_version="2.3.0",
            status="passed",
            environment="staging",
            duration_seconds=1.4,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-206",
            release_id=release.id,
            release_version="2.3.0",
            status="passed",
            environment="staging",
            duration_seconds=2.8,
            is_flaky=False,
        ),
    ]

    db.add_all(executions)

    defects = [
        Defect(
            defect_id="BUG-201",
            title="Minor order history delay",
            module="Orders",
            severity="medium",
            priority="low",
            status="resolved",
            release=release,
            release_version="2.3.0",
        ),
        Defect(
            defect_id="BUG-202",
            title="Minor catalog display issue",
            module="Catalog",
            severity="medium",
            priority="low",
            status="resolved",
            release=release,
            release_version="2.3.0",
        ),
        Defect(
            defect_id="BUG-203",
            title="Checkout confirmation alignment issue",
            module="Payments",
            severity="low",
            priority="low",
            status="resolved",
            release=release,
            release_version="2.3.0",
        ),
        Defect(
            defect_id="BUG-204",
            title="Authentication helper text issue",
            module="Authentication",
            severity="low",
            priority="low",
            status="resolved",
            release=release,
            release_version="2.3.0",
        ),
        Defect(
            defect_id="BUG-205",
            title="Search result spacing issue",
            module="Catalog",
            severity="low",
            priority="low",
            status="resolved",
            release=release,
            release_version="2.3.0",
        ),
        Defect(
            defect_id="BUG-206",
            title="Mobile order history icon issue",
            module="Orders",
            severity="low",
            priority="low",
            status="resolved",
            release=release,
            release_version="2.3.0",
        ),
    ]

    db.add_all(defects)

    changes = [
        Change(
            change_id="CHG-201",
            release_version="2.3.0",
            module="Payments",
            description="Checkout confirmation improvements.",
            impact_score=45,
            business_critical=True,
        ),
        Change(
            change_id="CHG-202",
            release_version="2.3.0",
            module="Authentication",
            description="Authentication session handling improvements.",
            impact_score=35,
            business_critical=True,
        ),
        Change(
            change_id="CHG-203",
            release_version="2.3.0",
            module="Orders",
            description="Order history performance improvements.",
            impact_score=30,
            business_critical=False,
        ),
    ]

    db.add_all(changes)

    print("Created release 2.3.0.")


def seed_release_2_2_0(db):
    if release_exists(db, "2.2.0"):
        print("Release 2.2.0 already exists. Skipping.")
        return

    release = Release(
        release_version="2.2.0",
        total_tests=220,
        passed_tests=181,
        failed_tests=24,
        blocked_tests=15,
        critical_defects=1,
        high_defects=3,
        medium_defects=5,
        low_defects=8,
        regression_status="FAILED",
        smoke_status="PASSED",
    )

    db.add(release)
    db.flush()

    test_cases = [
        TestCase(
            test_case_id="TC-301",
            title="Valid login",
            module="Authentication",
            test_type="functional",
            priority="critical",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-302",
            title="Password reset",
            module="Authentication",
            test_type="functional",
            priority="high",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-303",
            title="Successful checkout",
            module="Payments",
            test_type="integration",
            priority="critical",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-304",
            title="Payment retry flow",
            module="Payments",
            test_type="integration",
            priority="critical",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-305",
            title="Refund processing",
            module="Payments",
            test_type="functional",
            priority="high",
            automated=False,
        ),
        TestCase(
            test_case_id="TC-306",
            title="Product search",
            module="Catalog",
            test_type="functional",
            priority="medium",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-307",
            title="Product filtering",
            module="Catalog",
            test_type="functional",
            priority="medium",
            automated=True,
        ),
        TestCase(
            test_case_id="TC-308",
            title="Order history",
            module="Orders",
            test_type="functional",
            priority="high",
            automated=True,
        ),
    ]

    db.add_all(test_cases)

    executions = [
        TestExecution(
            test_case_id="TC-301",
            release_id=release.id,
            release_version="2.2.0",
            status="passed",
            environment="staging",
            duration_seconds=1.3,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-302",
            release_id=release.id,
            release_version="2.2.0",
            status="failed",
            environment="staging",
            duration_seconds=2.5,
            is_flaky=False,
            failure_reason="Password reset token expired unexpectedly",
        ),
        TestExecution(
            test_case_id="TC-303",
            release_id=release.id,
            release_version="2.2.0",
            status="failed",
            environment="staging",
            duration_seconds=6.2,
            is_flaky=False,
            failure_reason="Payment authorization failed",
        ),
        TestExecution(
            test_case_id="TC-304",
            release_id=release.id,
            release_version="2.2.0",
            status="failed",
            environment="staging",
            duration_seconds=5.7,
            is_flaky=True,
            failure_reason="Payment retry behavior inconsistent",
        ),
        TestExecution(
            test_case_id="TC-305",
            release_id=release.id,
            release_version="2.2.0",
            status="blocked",
            environment="staging",
            duration_seconds=None,
            is_flaky=False,
            failure_reason="Refund sandbox unavailable",
        ),
        TestExecution(
            test_case_id="TC-306",
            release_id=release.id,
            release_version="2.2.0",
            status="passed",
            environment="staging",
            duration_seconds=1.8,
            is_flaky=False,
        ),
        TestExecution(
            test_case_id="TC-307",
            release_id=release.id,
            release_version="2.2.0",
            status="failed",
            environment="staging",
            duration_seconds=2.2,
            is_flaky=True,
            failure_reason="Filter state intermittently resets",
        ),
        TestExecution(
            test_case_id="TC-308",
            release_id=release.id,
            release_version="2.2.0",
            status="blocked",
            environment="staging",
            duration_seconds=None,
            is_flaky=False,
            failure_reason="Order service unavailable",
        ),
    ]

    db.add_all(executions)

    defects = [
        Defect(
            defect_id="BUG-301",
            title="Payment authorization failure",
            module="Payments",
            severity="critical",
            priority="critical",
            status="open",
            release=release,
            release_version="2.2.0",
        ),
        Defect(
            defect_id="BUG-302",
            title="Payment retry fails intermittently",
            module="Payments",
            severity="high",
            priority="high",
            status="open",
            release=release,
            release_version="2.2.0",
        ),
        Defect(
            defect_id="BUG-303",
            title="Password reset token failure",
            module="Authentication",
            severity="high",
            priority="high",
            status="in_progress",
            release=release,
            release_version="2.2.0",
        ),
        Defect(
            defect_id="BUG-304",
            title="Order service unavailable",
            module="Orders",
            severity="high",
            priority="high",
            status="open",
            release=release,
            release_version="2.2.0",
        ),
        Defect(
            defect_id="BUG-305",
            title="Product filter state resets",
            module="Catalog",
            severity="medium",
            priority="medium",
            status="open",
            release=release,
            release_version="2.2.0",
        ),
        Defect(
            defect_id="BUG-306",
            title="Catalog search timeout",
            module="Catalog",
            severity="medium",
            priority="medium",
            status="open",
            release=release,
            release_version="2.2.0",
        ),
        Defect(
            defect_id="BUG-307",
            title="Mobile checkout rendering issue",
            module="Payments",
            severity="medium",
            priority="medium",
            status="open",
            release=release,
            release_version="2.2.0",
        ),
        Defect(
            defect_id="BUG-308",
            title="Order history data mismatch",
            module="Orders",
            severity="medium",
            priority="medium",
            status="in_progress",
            release=release,
            release_version="2.2.0",
        ),
        Defect(
            defect_id="BUG-309",
            title="Login validation message issue",
            module="Authentication",
            severity="low",
            priority="low",
            status="resolved",
            release=release,
            release_version="2.2.0",
        ),
    ]

    db.add_all(defects)

    changes = [
        Change(
            change_id="CHG-301",
            release_version="2.2.0",
            module="Payments",
            description="Payment provider integration substantially changed.",
            impact_score=95,
            business_critical=True,
        ),
        Change(
            change_id="CHG-302",
            release_version="2.2.0",
            module="Authentication",
            description="Authentication token and password reset logic redesigned.",
            impact_score=85,
            business_critical=True,
        ),
        Change(
            change_id="CHG-303",
            release_version="2.2.0",
            module="Orders",
            description="Order service architecture changed.",
            impact_score=88,
            business_critical=True,
        ),
        Change(
            change_id="CHG-304",
            release_version="2.2.0",
            module="Catalog",
            description="Catalog filtering and search logic modified.",
            impact_score=65,
            business_critical=False,
        ),
    ]

    db.add_all(changes)

    print("Created release 2.2.0.")


def seed_data():
    db = SessionLocal()

    try:
        seed_release_2_4_0(db)
        seed_release_2_3_0(db)
        seed_release_2_2_0(db)

        db.commit()

        print("")
        print("Seed operation completed successfully.")
        print("")
        print("Available releases:")

        releases = (
            db.query(Release)
            .order_by(Release.release_version.desc())
            .all()
        )

        for release in releases:
            print(
                f"- {release.release_version} | "
                f"{release.passed_tests}/{release.total_tests} passed | "
                f"{release.failed_tests} failed | "
                f"{release.blocked_tests} blocked | "
                f"Regression: {release.regression_status}"
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
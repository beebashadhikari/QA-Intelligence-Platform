def calculate_pass_rate(
    total_tests: int,
    passed_tests: int,
) -> float:
    if total_tests == 0:
        return 0.0

    return round(
        (passed_tests / total_tests) * 100,
        2,
    )


def calculate_failure_rate(
    total_tests: int,
    failed_tests: int,
) -> float:
    if total_tests == 0:
        return 0.0

    return round(
        (failed_tests / total_tests) * 100,
        2,
    )


def calculate_blocked_rate(
    total_tests: int,
    blocked_tests: int,
) -> float:
    if total_tests == 0:
        return 0.0

    return round(
        (blocked_tests / total_tests) * 100,
        2,
    )
from backend.app.services.metrics import (
    calculate_pass_rate,
    calculate_failure_rate,
    calculate_blocked_rate,
)


def test_pass_rate():
    result = calculate_pass_rate(248, 231)

    assert result == 93.15


def test_failure_rate():
    result = calculate_failure_rate(248, 9)

    assert result == 3.63


def test_blocked_rate():
    result = calculate_blocked_rate(248, 8)

    assert result == 3.23


def test_zero_tests():
    assert calculate_pass_rate(0, 0) == 0.0
    assert calculate_failure_rate(0, 0) == 0.0
    assert calculate_blocked_rate(0, 0) == 0.0
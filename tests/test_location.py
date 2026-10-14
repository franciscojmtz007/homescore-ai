import pytest

from src.location import (
    calculate_school_fit,
    calculate_safety_fit,
    calculate_commute_fit,
    calculate_location_fit,
)


def test_school_fit():
    assert calculate_school_fit(8.5) == pytest.approx(85)
    assert calculate_school_fit(10) == pytest.approx(100)


def test_safety_fit():
    assert calculate_safety_fit(9) == pytest.approx(90)
    assert calculate_safety_fit(6) == pytest.approx(60)


def test_commute_fit():
    assert calculate_commute_fit(0, 45) == pytest.approx(100)
    assert calculate_commute_fit(15, 45) == pytest.approx(83.333333)
    assert calculate_commute_fit(45, 45) == pytest.approx(50)
    assert calculate_commute_fit(90, 45) == pytest.approx(0)


def test_commute_fit_zero_maximum():
    assert calculate_commute_fit(0, 0) == 100
    assert calculate_commute_fit(10, 0) == 0


def test_location_fit():
    result = calculate_location_fit(
        school_fit=85,
        safety_fit=90,
        commute_fit=66.6666667,
        school_importance=5,
        safety_importance=4,
        commute_importance=2,
    )

    expected = (
        85 * 5
        + 90 * 4
        + 66.6666667 * 2
    ) / 11

    assert result == pytest.approx(expected)


def test_location_fit_zero_importance():
    assert calculate_location_fit(
        85, 90, 70, 0, 0, 0
    ) == 0
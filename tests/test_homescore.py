import pytest

from src.homescore import (
    normalize_dimension_weights,
    calculate_homescore,
)


def test_normalize_dimension_weights():
    weights = normalize_dimension_weights(5, 4, 3)

    assert weights[0] == pytest.approx(5 / 12)
    assert weights[1] == pytest.approx(4 / 12)
    assert weights[2] == pytest.approx(3 / 12)
    assert sum(weights) == pytest.approx(1)


def test_house_a_homescore():
    result = calculate_homescore(
        affordability_fit=100,
        location_fit=88.1818,
        property_fit=84.5238,
        affordability_importance=5,
        location_importance=4,
        property_importance=3,
    )

    assert result == pytest.approx(92.1916, abs=0.001)


def test_zero_dimension_importance():
    result = calculate_homescore(
        100, 80, 70, 0, 0, 0
    )

    assert result == 0
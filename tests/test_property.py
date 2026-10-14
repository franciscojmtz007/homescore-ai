import pytest

from src.property import (
    calculate_size_fit,
    calculate_amenities_fit,
    calculate_property_fit,
)


def test_size_fit():
    assert calculate_size_fit(1700, 1800, 2500) == 0
    assert calculate_size_fit(1800, 1800, 2500) == 0
    assert calculate_size_fit(2000, 1800, 2500) == pytest.approx(28.5714286)
    assert calculate_size_fit(2150, 1800, 2500) == pytest.approx(50)
    assert calculate_size_fit(2500, 1800, 2500) == 100
    assert calculate_size_fit(3000, 1800, 2500) == 100


def test_amenities_fit():
    preferences = {
        "garage": 2,
        "pool": 0,
        "large_yard": 1,
        "home_office": 2,
        "updated_kitchen": 1,
        "first_floor_primary": 0,
    }

    home = {
        "garage": True,
        "pool": False,
        "large_yard": True,
        "home_office": False,
        "updated_kitchen": True,
        "first_floor_primary": False,
    }

    assert calculate_amenities_fit(
        home, preferences
    ) == pytest.approx(66.6666667)


def test_amenities_fit_no_preferences():
    assert calculate_amenities_fit(
        {"garage": False},
        {"garage": 0},
    ) == 100


def test_property_fit():
    result = calculate_property_fit(
        size_fit=50,
        amenities_fit=80,
        size_importance=4,
        amenities_importance=3,
    )

    assert result == pytest.approx(62.857142857)


def test_property_fit_zero_importance():
    assert calculate_property_fit(
        50, 80, 0, 0
    ) == 0
from src.constraints import (
    evaluate_constraints,
    count_constraint_violations,
    get_constraint_status,
)


def test_constraints_no_violations():
    buyer = {
        "maximum_price": 600000,
        "minimum_school_rating": 6,
        "minimum_safety_rating": 6,
        "maximum_commute_minutes": 45,
        "minimum_square_feet": 1800,
        "amenity_preferences": {
            "garage": 2,
            "home_office": 2,
            "pool": 0,
        },
    }

    home = {
        "price": 425000,
        "school_rating": 8,
        "safety_rating": 9,
        "commute_minutes": 25,
        "square_feet": 2200,
        "amenities": {
            "garage": True,
            "home_office": True,
            "pool": False,
        },
    }

    violations = evaluate_constraints(home, buyer)

    assert violations == []
    assert count_constraint_violations(violations) == 0
    assert get_constraint_status(violations) == "Best Matches"


def test_constraints_multiple_violations():
    buyer = {
        "maximum_price": 600000,
        "minimum_school_rating": 6,
        "minimum_safety_rating": 6,
        "maximum_commute_minutes": 45,
        "minimum_square_feet": 1800,
        "amenity_preferences": {
            "garage": 2,
            "home_office": 1,
        },
    }

    home = {
        "price": 625000,
        "school_rating": 7,
        "safety_rating": 8,
        "commute_minutes": 60,
        "square_feet": 1700,
        "amenities": {
            "garage": False,
            "home_office": False,
        },
    }

    violations = evaluate_constraints(home, buyer)

    assert len(violations) == 4
    assert "Price exceeds maximum" in violations
    assert "Commute exceeds maximum" in violations
    assert "Below minimum size" in violations
    assert "Missing Garage" in violations

    assert count_constraint_violations(violations) == 4
    assert get_constraint_status(violations) == "Other Homes"
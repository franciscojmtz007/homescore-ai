# ============================================
# HomeScore AI - Validation Tests
# ============================================

import pytest

from src.validation import validate_buyer, validate_home


@pytest.fixture
def buyer():
    return {
        "target_price": 450000,
        "maximum_price": 600000,
        "target_monthly_cost": 3500,
        "maximum_monthly_cost": 4500,
        "down_payment": 100000,
        "annual_interest_rate": 0.0625,
        "loan_term_years": 30,
        "minimum_square_feet": 1800,
        "target_square_feet": 2500,
        "minimum_school_rating": 6,
        "minimum_safety_rating": 6,
        "maximum_commute_minutes": 45,
    }


@pytest.fixture
def home():
    return {
        "name": "House A",
        "price": 425000,
        "square_feet": 2400,
        "annual_property_tax": 7000,
        "annual_insurance": 2000,
        "monthly_hoa": 0,
        "monthly_pmi": 0,
        "school_rating": 9,
        "safety_rating": 9,
        "commute_minutes": 18,
    }


# --------------------------------------------
# Valid inputs
# --------------------------------------------

def test_valid_buyer(buyer):
    assert validate_buyer(buyer) == []


def test_valid_home(home, buyer):
    assert validate_home(home, buyer) == []


# --------------------------------------------
# Buyer validation
# --------------------------------------------

def test_maximum_price_below_target(buyer):
    buyer["maximum_price"] = 400000

    errors = validate_buyer(buyer)

    assert len(errors) > 0
    assert any("Maximum home price" in error for error in errors)


def test_maximum_monthly_cost_below_target(buyer):
    buyer["maximum_monthly_cost"] = 3000

    errors = validate_buyer(buyer)

    assert any("Maximum monthly housing cost" in error for error in errors)


def test_negative_down_payment(buyer):
    buyer["down_payment"] = -1000

    errors = validate_buyer(buyer)

    assert any("Down payment" in error for error in errors)


def test_target_size_below_minimum(buyer):
    buyer["target_square_feet"] = 1500

    errors = validate_buyer(buyer)

    assert any("Target square footage" in error for error in errors)


def test_invalid_interest_rate(buyer):
    buyer["annual_interest_rate"] = -0.05

    errors = validate_buyer(buyer)

    assert any("Interest rate" in error for error in errors)


def test_invalid_loan_term(buyer):
    buyer["loan_term_years"] = 0

    errors = validate_buyer(buyer)

    assert any("Loan term" in error for error in errors)


# --------------------------------------------
# Home validation
# --------------------------------------------

def test_negative_home_price(home, buyer):
    home["price"] = -100000

    errors = validate_home(home, buyer)

    assert any("Home price" in error for error in errors)


def test_down_payment_exceeds_home_price(home, buyer):
    buyer["down_payment"] = 500000

    errors = validate_home(home, buyer)

    assert any("Down payment" in error for error in errors)


def test_negative_property_tax(home, buyer):
    home["annual_property_tax"] = -100

    errors = validate_home(home, buyer)

    assert any("annual_property_tax" in error for error in errors)


def test_invalid_school_rating(home, buyer):
    home["school_rating"] = 12

    errors = validate_home(home, buyer)

    assert any("School rating" in error for error in errors)


def test_negative_commute(home, buyer):
    home["commute_minutes"] = -10

    errors = validate_home(home, buyer)

    assert any("Commute time" in error for error in errors)
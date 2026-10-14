import pytest
from src.affordability import (
    calculate_loan_amount,
    calculate_monthly_principal_interest,
    calculate_monthly_housing_cost,
    calculate_price_fit,
    calculate_monthly_cost_fit,
    calculate_affordability_fit,
    )

def test_house_a_monthly_principal_interest():
    loan_amount=325000
    annual_interest_rate=0.0625
    loan_term_years=30

    result=calculate_monthly_principal_interest(
        loan_amount,annual_interest_rate, loan_term_years,
    )
    assert result==pytest.approx(2001.08, abs=0.01)

def test_house_a_loan_amount():
    purchase_price = 425000
    down_payment = 100000

    result = calculate_loan_amount(purchase_price, down_payment)

    assert result == 325000

def test_house_a_monthly_housing_cost():
    monthly_principal_interest=2001.0809013857822
    annual_property_tax = 7000
    annual_insurance = 2000
    monthly_hoa = 0
    monthly_pmi = 0

    result =calculate_monthly_housing_cost(
        monthly_principal_interest,
        annual_property_tax,
        annual_insurance,
        monthly_hoa,
        monthly_pmi,
    )

    assert result == pytest.approx(2751.08, abs=0.01)  

def test_buyer_1_price_fit():
    target_price = 450000
    maximum_price = 600000

    assert calculate_price_fit(
        425000, target_price, maximum_price
    ) == pytest.approx(100.0)

    assert calculate_price_fit(
        500000, target_price, maximum_price
    ) == pytest.approx(66.6667, abs=0.001)

    assert calculate_price_fit(
        550000, target_price, maximum_price
    ) == pytest.approx(33.3333, abs=0.001)

    assert calculate_price_fit(
        625000, target_price, maximum_price
    ) == pytest.approx(0.0)

def test_buyer_1_monthly_cost_fit():
    target_monthly_cost = 3500
    maximum_monthly_cost = 4500

    assert calculate_monthly_cost_fit(
        2751.08, target_monthly_cost, maximum_monthly_cost
    ) == pytest.approx(100.0)

    assert calculate_monthly_cost_fit(
        3454.54, target_monthly_cost, maximum_monthly_cost
    ) == pytest.approx(100.0)

    assert calculate_monthly_cost_fit(
        3970.73, target_monthly_cost, maximum_monthly_cost
    ) == pytest.approx(52.927, abs=0.001)

    assert calculate_monthly_cost_fit(
        4432.52, target_monthly_cost, maximum_monthly_cost
    ) == pytest.approx(6.748, abs=0.001)

def test_buyer_1_affordability_fit():
    price_importance = 3
    monthly_cost_importance = 5

    # House A
    assert calculate_affordability_fit(
        100, 100, price_importance, monthly_cost_importance
    ) == pytest.approx(100.0)

    # House B
    assert calculate_affordability_fit(
        66.6666666667, 100, price_importance, monthly_cost_importance
    ) == pytest.approx(87.5)

    # House C
    assert calculate_affordability_fit(
        33.3333333333, 52.927, price_importance, monthly_cost_importance
    ) == pytest.approx(45.579375, abs=0.01)

    # House D
    assert calculate_affordability_fit(
        0, 6.748, price_importance, monthly_cost_importance
    ) == pytest.approx(4.2175, abs=0.01)

    # Neither component is important
    assert calculate_affordability_fit(
        80, 90, 0, 0
    ) == 0

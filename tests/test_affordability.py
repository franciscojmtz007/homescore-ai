from src.affordability import calculate_loan_amount


def test_house_a_loan_amount():
    purchase_price = 425000
    down_payment = 100000

    result = calculate_loan_amount(purchase_price, down_payment)

    assert result == 325000
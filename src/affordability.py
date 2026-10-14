def calculate_loan_amount(purchase_price, down_payment):
    #Calculate the mortgage loan amount.
    loan_amount = purchase_price - down_payment
    return loan_amount

def calculate_monthly_principal_interest(
        loan_amount, annual_interest_rate, loan_term_years):
    monthly_rate=annual_interest_rate/12
    number_of_payments=loan_term_years * 12

    if monthly_rate==0:
        return loan_amount/number_of_payments

    monthly_payment = (loan_amount*monthly_rate
                       *(1+monthly_rate)**number_of_payments
                       /((1+monthly_rate)** number_of_payments -1 )
    )
    return monthly_payment

def calculate_monthly_housing_cost(
        monthly_principal_interest,
        annual_property_tax,
        annual_insurance,
        monthly_hoa,
        monthly_pmi,):
    monthly_property_tax = annual_property_tax /12
    monthly_insurance = annual_insurance/12
    monthly_housing_cost=(monthly_principal_interest
                          + monthly_property_tax
                          + monthly_insurance
                          + monthly_hoa
                          + monthly_pmi  
)
    return monthly_housing_cost

def calculate_price_fit(
        purchase_price, target_price, maximum_price
):
    if purchase_price <= target_price:
        return 100

    if purchase_price >= maximum_price:
        return 0

    price_fit = (
    100
    * (maximum_price - purchase_price)
    / (maximum_price - target_price)
    )

    return price_fit

def calculate_monthly_cost_fit(
        monthly_housing_cost,
        target_monthly_cost,
        maximum_monthly_cost,
):
    if monthly_housing_cost <= target_monthly_cost:
        return 100

    if monthly_housing_cost >= maximum_monthly_cost:
            return 0

    monthly_cost_fit = (
        100
        * (maximum_monthly_cost - monthly_housing_cost)
        / (maximum_monthly_cost - target_monthly_cost)
    )

    return monthly_cost_fit

def calculate_affordability_fit(
    price_fit,
    monthly_cost_fit,
    price_importance,
    monthly_cost_importance,
):
    total_importance = price_importance + monthly_cost_importance

    if total_importance == 0:
        return 0

    price_weight = price_importance / total_importance
    monthly_cost_weight = monthly_cost_importance / total_importance

    affordability_fit = (
        price_fit * price_weight
        + monthly_cost_fit * monthly_cost_weight
    )

    return affordability_fit
from src.affordability import (
    calculate_loan_amount,
    calculate_monthly_principal_interest,
    calculate_monthly_housing_cost,
    calculate_price_fit,
    calculate_monthly_cost_fit,
    calculate_affordability_fit,
)

from src.location import (
    calculate_school_fit,
    calculate_safety_fit,
    calculate_commute_fit,
    calculate_location_fit,
)

from src.property import (
    calculate_size_fit,
    calculate_amenities_fit,
    calculate_property_fit,
)

from src.constraints import (
    evaluate_constraints,
    count_constraint_violations,
    get_constraint_status,
)

from src.homescore import calculate_homescore


def calculate_home_result(home, buyer):
    # STEP 1: AFFORDABILITY

    loan_amount = calculate_loan_amount(
        home["price"],
        buyer["down_payment"],
    )

    monthly_pi = calculate_monthly_principal_interest(
        loan_amount,
        buyer["annual_interest_rate"],
        buyer["loan_term_years"],
    )

    monthly_housing_cost = calculate_monthly_housing_cost(
        monthly_pi,
        home["annual_property_tax"],
        home["annual_insurance"],
        home["monthly_hoa"],
        home["monthly_pmi"],
    )

    price_fit = calculate_price_fit(
        home["price"],
        buyer["target_price"],
        buyer["maximum_price"],
    )

    monthly_cost_fit = calculate_monthly_cost_fit(
        monthly_housing_cost,
        buyer["target_monthly_cost"],
        buyer["maximum_monthly_cost"],
    )

    affordability_fit = calculate_affordability_fit(
        price_fit,
        monthly_cost_fit,
        buyer["price_importance"],
        buyer["monthly_cost_importance"],
    )

    # STEP 2: LOCATION

    school_fit = calculate_school_fit(
        home["school_rating"]
    )

    safety_fit = calculate_safety_fit(
        home["safety_rating"]
    )

    commute_fit = calculate_commute_fit(
        home["commute_minutes"],
        buyer["maximum_commute_minutes"],
    )

    location_fit = calculate_location_fit(
        school_fit,
        safety_fit,
        commute_fit,
        buyer["school_importance"],
        buyer["safety_importance"],
        buyer["commute_importance"],
    )

    # STEP 3: PROPERTY

    size_fit = calculate_size_fit(
        home["square_feet"],
        buyer["minimum_square_feet"],
        buyer["target_square_feet"],
    )

    amenities_fit = calculate_amenities_fit(
        home["amenities"],
        buyer["amenity_preferences"],
    )

    property_fit = calculate_property_fit(
        size_fit,
        amenities_fit,
        buyer["size_importance"],
        buyer["amenities_importance"],
    )

    # STEP 4: FINAL HOMESCORE

    homescore = calculate_homescore(
        affordability_fit,
        location_fit,
        property_fit,
        buyer["affordability_importance"],
        buyer["location_importance"],
        buyer["property_importance"],
    )

    # STEP 5: HARD CONSTRAINTS

    violations = evaluate_constraints(home, buyer)

    constraint_count = count_constraint_violations(
        violations
    )

    constraint_status = get_constraint_status(
        violations
    )

    # STEP 6: RETURN RESULTS

    return {
        "name": home["name"],
        "loan_amount": loan_amount,
        "monthly_pi": monthly_pi,
        "monthly_housing_cost": monthly_housing_cost,
        "price_fit": price_fit,
        "monthly_cost_fit": monthly_cost_fit,
        "affordability_fit": affordability_fit,
        "school_fit": school_fit,
        "safety_fit": safety_fit,
        "commute_fit": commute_fit,
        "location_fit": location_fit,
        "size_fit": size_fit,
        "amenities_fit": amenities_fit,
        "property_fit": property_fit,
        "homescore": homescore,
        "violations": violations,
        "constraint_count": constraint_count,
        "constraint_status": constraint_status,
    }
# ============================================
# HomeScore AI - Input Validation
# ============================================


def validate_buyer(buyer):
    """
    Check whether buyer preferences contain
    invalid or inconsistent values.

    Returns a list of error messages.
    An empty list means validation passed.
    """

    errors = []

    # ----------------------------------------
    # Price preferences
    # ----------------------------------------

    target_price = buyer["target_price"]
    maximum_price = buyer["maximum_price"]

    if target_price <= 0:
        errors.append(
            "Target home price must be greater than zero."
        )

    if maximum_price <= target_price:
        errors.append(
            "Maximum home price must be greater than target home price."
        )

    # ----------------------------------------
    # Monthly housing cost preferences
    # ----------------------------------------

    target_monthly = buyer["target_monthly_cost"]
    maximum_monthly = buyer["maximum_monthly_cost"]

    if target_monthly <= 0:
        errors.append(
            "Target monthly housing cost must be greater than zero."
        )

    if maximum_monthly <= target_monthly:
        errors.append(
            "Maximum monthly housing cost must be greater than target monthly cost."
        )

    # ----------------------------------------
    # Financing
    # ----------------------------------------

    if buyer["down_payment"] < 0:
        errors.append(
            "Down payment cannot be negative."
        )

    if buyer["annual_interest_rate"] < 0:
        errors.append(
            "Interest rate cannot be negative."
        )

    if buyer["loan_term_years"] <= 0:
        errors.append(
            "Loan term must be greater than zero."
        )

    # ----------------------------------------
    # Property size preferences
    # ----------------------------------------

    minimum_size = buyer["minimum_square_feet"]
    target_size = buyer["target_square_feet"]

    if minimum_size < 0:
        errors.append(
            "Minimum square footage cannot be negative."
        )

    if target_size <= minimum_size:
        errors.append(
            "Target square footage must be greater than minimum square footage."
        )

    # ----------------------------------------
    # Location preferences
    # ----------------------------------------

    if not 0 <= buyer["minimum_school_rating"] <= 10:
        errors.append(
            "Minimum school rating must be between 0 and 10."
        )

    if not 0 <= buyer["minimum_safety_rating"] <= 10:
        errors.append(
            "Minimum safety rating must be between 0 and 10."
        )

    if buyer["maximum_commute_minutes"] <= 0:
        errors.append(
            "Maximum commute time must be greater than zero."
        )

    return errors


def validate_home(home, buyer):
    """
    Check manually entered property information.

    Returns a list of error messages.
    """

    errors = []

    # ----------------------------------------
    # Property identity
    # ----------------------------------------

    if not home["name"].strip():
        errors.append(
            "Property name cannot be empty."
        )

    # ----------------------------------------
    # Property price and size
    # ----------------------------------------

    if home["price"] <= 0:
        errors.append(
            "Home price must be greater than zero."
        )

    if home["square_feet"] <= 0:
        errors.append(
            "Property square footage must be greater than zero."
        )

    # ----------------------------------------
    # Financial information
    # ----------------------------------------

    financial_fields = [
        "annual_property_tax",
        "annual_insurance",
        "monthly_hoa",
        "monthly_pmi",
    ]

    for field in financial_fields:
        if home[field] < 0:
            errors.append(
                f"{field} cannot be negative."
            )

    if buyer["down_payment"] > home["price"]:
        errors.append(
            "Down payment cannot exceed the home's price."
        )

    # ----------------------------------------
    # Location information
    # ----------------------------------------

    if not 0 <= home["school_rating"] <= 10:
        errors.append(
            "School rating must be between 0 and 10."
        )

    if not 0 <= home["safety_rating"] <= 10:
        errors.append(
            "Safety rating must be between 0 and 10."
        )

    if home["commute_minutes"] < 0:
        errors.append(
            "Commute time cannot be negative."
        )

    return errors
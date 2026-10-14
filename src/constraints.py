def evaluate_constraints(home, buyer):
    violations = []

    # Maximum purchase price
    if home["price"] > buyer["maximum_price"]:
        violations.append("Price exceeds maximum")

    # Minimum school rating
    if home["school_rating"] < buyer["minimum_school_rating"]:
        violations.append("School rating below minimum")

    # Minimum safety rating
    if home["safety_rating"] < buyer["minimum_safety_rating"]:
        violations.append("Safety rating below minimum")

    # Maximum commute
    if home["commute_minutes"] > buyer["maximum_commute_minutes"]:
        violations.append("Commute exceeds maximum")

    # Minimum property size
    if home["square_feet"] < buyer["minimum_square_feet"]:
        violations.append("Below minimum size")

    # Must-have amenities
    for amenity, importance in buyer["amenity_preferences"].items():
        if importance == 2 and not home["amenities"].get(amenity, False):
            violations.append(f"Missing {amenity.replace('_', ' ').title()}")

    return violations


def count_constraint_violations(violations):
    return len(violations)


def get_constraint_status(violations):
    if len(violations) == 0:
        return "Best Matches"

    return "Other Homes"
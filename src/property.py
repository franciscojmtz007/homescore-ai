def calculate_size_fit(
    actual_square_feet,
    minimum_square_feet,
    target_square_feet,
):
    if actual_square_feet <= minimum_square_feet:
        return 0

    if actual_square_feet >= target_square_feet:
        return 100

    return (
        100
        * (actual_square_feet - minimum_square_feet)
        / (target_square_feet - minimum_square_feet)
    )


def calculate_amenities_fit(
    home_amenities,
    buyer_amenity_preferences,
):
    total_desired_points = sum(
        buyer_amenity_preferences.values()
    )

    if total_desired_points == 0:
        return 100

    earned_points = sum(
        importance
        for amenity, importance in buyer_amenity_preferences.items()
        if home_amenities.get(amenity, False)
    )

    return (
        earned_points / total_desired_points
    ) * 100


def calculate_property_fit(
    size_fit,
    amenities_fit,
    size_importance,
    amenities_importance,
):
    total_importance = (
        size_importance + amenities_importance
    )

    if total_importance == 0:
        return 0

    return (
        size_fit * size_importance
        + amenities_fit * amenities_importance
    ) / total_importance
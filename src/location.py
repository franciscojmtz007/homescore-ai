def calculate_school_fit(school_rating):
    return school_rating * 10


def calculate_safety_fit(safety_rating):
    return safety_rating * 10


def calculate_commute_fit(
    actual_commute_minutes,
    maximum_acceptable_commute_minutes,
):
    if maximum_acceptable_commute_minutes <= 0:
        return 100 if actual_commute_minutes <= 0 else 0

    commute_fit = 100 - (
        50
        * actual_commute_minutes
        / maximum_acceptable_commute_minutes
    )

    return max(0, commute_fit)


def calculate_location_fit(
    school_fit,
    safety_fit,
    commute_fit,
    school_importance,
    safety_importance,
    commute_importance,
):
    total_importance = (
        school_importance
        + safety_importance
        + commute_importance
    )

    if total_importance == 0:
        return 0

    location_fit = (
        school_fit * school_importance
        + safety_fit * safety_importance
        + commute_fit * commute_importance
    ) / total_importance

    return location_fit
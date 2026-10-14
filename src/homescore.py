def normalize_dimension_weights(
    affordability_importance,
    location_importance,
    property_importance,
):
    total_importance = (
        affordability_importance
        + location_importance
        + property_importance
    )

    if total_importance == 0:
        return (0, 0, 0)

    return (
        affordability_importance / total_importance,
        location_importance / total_importance,
        property_importance / total_importance,
    )


def calculate_homescore(
    affordability_fit,
    location_fit,
    property_fit,
    affordability_importance,
    location_importance,
    property_importance,
):
    weights = normalize_dimension_weights(
        affordability_importance,
        location_importance,
        property_importance,
    )

    return (
        affordability_fit * weights[0]
        + location_fit * weights[1]
        + property_fit * weights[2]
    )
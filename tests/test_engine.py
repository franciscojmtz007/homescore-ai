from src.ranking import group_and_rank_homes
import pytest

from src.engine import calculate_home_result


# BUYER 1 — Frozen Excel Reference
buyer_1 = {
    # Overall importance
    "affordability_importance": 5,
    "location_importance": 4,
    "property_importance": 3,

    # Affordability
    "target_price": 450000,
    "maximum_price": 600000,
    "target_monthly_cost": 3500,
    "maximum_monthly_cost": 4500,
    "down_payment": 100000,
    "annual_interest_rate": 0.0625,
    "loan_term_years": 30,
    "price_importance": 3,
    "monthly_cost_importance": 5,

    # Location
    "school_importance": 5,
    "safety_importance": 4,
    "commute_importance": 2,
    "minimum_school_rating": 6,
    "minimum_safety_rating": 6,
    "maximum_commute_minutes": 45,

    # Property
    "size_importance": 4,
    "amenities_importance": 3,
    "minimum_square_feet": 1800,
    "target_square_feet": 2500,

    # Amenities
    "amenity_preferences": {
        "garage": 2,
        "pool": 0,
        "large_yard": 1,
        "home_office": 2,
        "updated_kitchen": 1,
        "first_floor_primary": 0,
    },
}


# HOUSE A
house_a = {
    "name": "House A",
    "price": 425000,
    "annual_property_tax": 7000,
    "annual_insurance": 2000,
    "monthly_hoa": 0,
    "monthly_pmi": 0,

    "school_rating": 9,
    "safety_rating": 9,
    "commute_minutes": 18,

    "square_feet": 2400,

    "amenities": {
        "garage": True,
        "pool": False,
        "large_yard": True,
        "home_office": True,
        "updated_kitchen": False,
        "first_floor_primary": False,
    },
}


def test_house_a_full_engine():
    result = calculate_home_result(house_a, buyer_1)

    print("\nHOUSE A RESULTS")
    print("----------------------------")

    for key, value in result.items():
        print(f"{key}: {value}")

    assert result["loan_amount"] == 325000

    assert result["monthly_pi"] == pytest.approx(
        2001.0809013857822
    )

    assert result["monthly_housing_cost"] == pytest.approx(
        2751.0809013857822
    )

    assert result["affordability_fit"] == pytest.approx(100)

    assert result["constraint_count"] == 0

    assert result["location_fit"] == pytest.approx(
        88.18181818, abs=0.0001
    )

    assert result["property_fit"] == pytest.approx(
        84.69387755, abs=0.0001
    )

    assert result["homescore"] == pytest.approx(
        92.23407544836117, abs=0.0001
    )

    # HOUSE B
house_b = {
    "name": "House B",
    "price": 500000,
    "annual_property_tax": 8500,
    "annual_insurance": 2200,
    "monthly_hoa": 100,
    "monthly_pmi": 0,

    "school_rating": 8,
    "safety_rating": 9,
    "commute_minutes": 25,

    "square_feet": 2700,

    "amenities": {
        "garage": True,
        "pool": True,
        "large_yard": False,
        "home_office": True,
        "updated_kitchen": True,
        "first_floor_primary": False,
    },
}


# HOUSE C
house_c = {
    "name": "House C",
    "price": 550000,
    "annual_property_tax": 12000,
    "annual_insurance": 2400,
    "monthly_hoa": 0,
    "monthly_pmi": 0,

    "school_rating": 7,
    "safety_rating": 8,
    "commute_minutes": 35,

    "square_feet": 2100,

    "amenities": {
        "garage": True,
        "pool": False,
        "large_yard": True,
        "home_office": False,
        "updated_kitchen": True,
        "first_floor_primary": False,
    },
}


# HOUSE D
house_d = {
    "name": "House D",
    "price": 625000,
    "annual_property_tax": 10000,
    "annual_insurance": 2600,
    "monthly_hoa": 150,
    "monthly_pmi": 0,

    "school_rating": 6,
    "safety_rating": 7,
    "commute_minutes": 50,

    "square_feet": 1650,

    "amenities": {
        "garage": False,
        "pool": True,
        "large_yard": True,
        "home_office": True,
        "updated_kitchen": True,
        "first_floor_primary": False,
    },
}

@pytest.mark.parametrize(
    "home, expected_affordability, expected_location, "
    "expected_property, expected_homescore, expected_violations",
    [
        (house_a, 100.0, 88.2, 84.7, 92.2, 0),
        (house_b, 87.5, 82.2, 92.9, 87.1, 0),
        (house_c, 45.6, 72.0, 53.1, 56.3, 1),
        (house_d, 4.2, 60.8, 28.6, 29.2, 4),
    ],
)
def test_all_houses_against_excel_v7(
    home,
    expected_affordability,
    expected_location,
    expected_property,
    expected_homescore,
    expected_violations,
):
    result = calculate_home_result(home, buyer_1)

    print(f"\n{home['name']} RESULTS")
    print("----------------------------")

    print(f"Affordability: {result['affordability_fit']:.4f}")
    print(f"Location:      {result['location_fit']:.4f}")
    print(f"Property:      {result['property_fit']:.4f}")
    print(f"HomeScore:     {result['homescore']:.4f}")
    print(f"Violations:    {result['constraint_count']}")

    assert result["affordability_fit"] == pytest.approx(
        expected_affordability, abs=0.05
    )

    assert result["location_fit"] == pytest.approx(
        expected_location, abs=0.05
    )

    assert result["property_fit"] == pytest.approx(
        expected_property, abs=0.05
    )

    assert result["homescore"] == pytest.approx(
        expected_homescore, abs=0.05
    )

    assert result["constraint_count"] == expected_violations

def test_full_engine_ranking():
    homes = [house_d, house_b, house_c, house_a]

    # Calculate HomeScore for every house
    results = [
        calculate_home_result(home, buyer_1)
        for home in homes
    ]

    # Group and rank the calculated results
    best_matches, other_homes = group_and_rank_homes(results)

    # Verify Best Matches
    assert [home["name"] for home in best_matches] == [
        "House A",
        "House B",
    ]

    # Verify Other Homes
    assert [home["name"] for home in other_homes] == [
        "House C",
        "House D",
    ]

    # Verify ranking within each group
    assert [home["rank"] for home in best_matches] == [1, 2]
    assert [home["rank"] for home in other_homes] == [1, 2]

    # Verify that constraint violations do not reduce scores
    assert other_homes[0]["homescore"] == pytest.approx(
        56.2635, abs=0.001
    )

    assert other_homes[1]["homescore"] == pytest.approx(
        29.1696, abs=0.001
    )

    print("\nFINAL HOMESCORE RANKING")
    print("----------------------------")

    for home in best_matches:
        print(
            f"Best Match #{home['rank']}: "
            f"{home['name']} - {home['homescore']:.2f}"
        )

    for home in other_homes:
        print(
            f"Other Home #{home['rank']}: "
            f"{home['name']} - {home['homescore']:.2f} "
            f"({home['constraint_count']} violations)"
        )

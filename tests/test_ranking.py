from src.ranking import group_and_rank_homes


def test_group_and_rank_homes():
    homes = [
        {
            "name": "House D",
            "homescore": 30.3601,
            "constraint_count": 4,
        },
        {
            "name": "House B",
            "homescore": 86.7824,
            "constraint_count": 0,
        },
        {
            "name": "House C",
            "homescore": 56.6887,
            "constraint_count": 1,
        },
        {
            "name": "House A",
            "homescore": 92.1916,
            "constraint_count": 0,
        },
    ]

    best_matches, other_homes = group_and_rank_homes(homes)

    assert [home["name"] for home in best_matches] == [
        "House A",
        "House B",
    ]

    assert [home["name"] for home in other_homes] == [
        "House C",
        "House D",
    ]

    assert best_matches[0]["rank"] == 1
    assert best_matches[1]["rank"] == 2

    assert other_homes[0]["rank"] == 1
    assert other_homes[1]["rank"] == 2

    assert best_matches[0]["group"] == "Best Matches"
    assert other_homes[0]["group"] == "Other Homes"


def test_constraint_violations_do_not_reduce_homescore():
    homes = [
        {
            "name": "House X",
            "homescore": 95,
            "constraint_count": 1,
        },
        {
            "name": "House Y",
            "homescore": 80,
            "constraint_count": 0,
        },
    ]

    best_matches, other_homes = group_and_rank_homes(homes)

    assert best_matches[0]["name"] == "House Y"
    assert other_homes[0]["name"] == "House X"

    # HomeScore must remain unchanged
    assert other_homes[0]["homescore"] == 95
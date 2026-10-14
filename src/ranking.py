def group_and_rank_homes(homes):
    """
    Group homes by constraint status and rank
    each group by HomeScore, highest first.
    """

    best_matches = []
    other_homes = []

    for home in homes:
        if home["constraint_count"] == 0:
            best_matches.append(home)
        else:
            other_homes.append(home)

    best_matches.sort(
        key=lambda home: home["homescore"],
        reverse=True,
    )

    other_homes.sort(
        key=lambda home: home["homescore"],
        reverse=True,
    )

    for rank, home in enumerate(best_matches, start=1):
        home["rank"] = rank
        home["group"] = "Best Matches"

    for rank, home in enumerate(other_homes, start=1):
        home["rank"] = rank
        home["group"] = "Other Homes"

    return best_matches, other_homes
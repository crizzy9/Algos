"""Question 2 — Lunar phase lookup.

The moon moves through the following eight phases in order and then repeats:

    new, waxing_crescent, first_quarter, waxing_gibbous,
    full, waning_gibbous, last_quarter, waning_crescent

You are given:

* ``initial_phase`` — the phase on day 1 of the year;
* ``season_lengths`` — positive integers giving the number of days in each
  season, in chronological order;
* ``target_season`` — a zero-based index into ``season_lengths``;
* ``target_day`` — a one-based day within the target season.

Return the phase on the requested date. Advancing by one calendar day advances
by one position in the phase cycle.

Examples
--------
solution("new", [90, 92, 93, 90], 0, 1) == "new"
solution("new", [90, 92, 93, 90], 0, 9) == "new"
solution("full", [3, 5], 1, 1) == "waning_crescent"

Guaranteed constraints
-----------------------
1 <= len(season_lengths) <= 20
1 <= season_lengths[i] <= 10_000
0 <= target_season < len(season_lengths)
1 <= target_day <= season_lengths[target_season]
initial_phase is one of the eight phase names above.
"""


def solution(
    initial_phase: str,
    season_lengths: list[int],
    target_season: int,
    target_day: int,
) -> str:
    phases = [
        "new",
        "waxing_crescent",
        "first_quarter",
        "waxing_gibbous",
        "full",
        "waning_gibbous",
        "last_quarter",
        "waning_crescent",
    ]

    n = len(phases)

    if target_season == 0:
        target = target_day
    else:
        target = season_lengths[target_season - 1] + target_day

    i = phases.index(initial_phase)
    return phases[(i + target) % n - 1]


if __name__ == "__main__":
    assert solution("new", [90, 92, 93, 90], 0, 1) == "new"
    assert solution("new", [90, 92, 93, 90], 0, 9) == "new"
    assert solution("full", [3, 5], 1, 1) == "waning_crescent"

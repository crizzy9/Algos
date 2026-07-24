"""Reference implementations. Try the timed mock before reading this file."""

PHASES = [
    "new",
    "waxing_crescent",
    "first_quarter",
    "waxing_gibbous",
    "full",
    "waning_gibbous",
    "last_quarter",
    "waning_crescent",
]


def key_changes(key_sequence: str) -> int:
    return sum(
        key_sequence[i].lower() != key_sequence[i - 1].lower()
        for i in range(1, len(key_sequence))
    )


def lunar_phase(
    initial_phase: str,
    season_lengths: list[int],
    target_season: int,
    target_day: int,
) -> str:
    days_after_day_one = sum(season_lengths[:target_season]) + target_day - 1
    start = PHASES.index(initial_phase)
    return PHASES[(start + days_after_day_one) % len(PHASES)]


def bubble_board(
    bubbles: list[list[int]], operations: list[list[int]]
) -> list[list[int]]:
    rows = len(bubbles)
    columns = len(bubbles[0])
    diagonals = ((-1, -1), (-1, 1), (1, -1), (1, 1))

    for row, column in operations:
        color = bubbles[row][column]
        if color == 0:
            continue

        to_remove = [(row, column)]
        for dr, dc in diagonals:
            neighbor_row = row + dr
            neighbor_column = column + dc
            if (
                0 <= neighbor_row < rows
                and 0 <= neighbor_column < columns
                and bubbles[neighbor_row][neighbor_column] == color
            ):
                to_remove.append((neighbor_row, neighbor_column))

        for remove_row, remove_column in to_remove:
            bubbles[remove_row][remove_column] = 0

        for c in range(columns):
            values = [bubbles[r][c] for r in range(rows) if bubbles[r][c] != 0]
            empty_count = rows - len(values)
            for r, value in enumerate([0] * empty_count + values):
                bubbles[r][c] = value

    return bubbles


def alternating_parity(a: list[int]) -> int:
    answer = 0
    run_length = 0
    previous_parity = None

    for value in a:
        parity = value % 2
        if previous_parity is not None and parity != previous_parity:
            run_length += 1
        else:
            run_length = 1
        answer += run_length
        previous_parity = parity

    return answer


def cumulative_visits(visits: list[int], target: int) -> int:
    total = 0
    for index, count in enumerate(visits):
        total += count
        if total >= target:
            return index
    return -1


def maximum_subarray(numbers: list[int]) -> int:
    best_ending_here = best_overall = numbers[0]
    for value in numbers[1:]:
        best_ending_here = max(value, best_ending_here + value)
        best_overall = max(best_overall, best_ending_here)
    return best_overall

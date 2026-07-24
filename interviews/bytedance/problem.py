from typing import List, Tuple, Dict


def count_sessions(
    events: List[Tuple[str, float]],  # (user_id, timestamp), sorted by timestamp
    timeout_seconds: float,
) -> Dict[str, int]:
    # Return {user_id: number_of_sessions}.
    # A user's first event starts session 1; each later event starts a new
    # session only if (timestamp - that user's previous timestamp) > timeout_seconds.

    sessions = {}

    for e in events:
        user = e[0]
        timestamp = e[1]

        if user in sessions:
            user_session = sessions[user]
            user_session[0] = timestamp
            if user_session[0] + timeout_seconds > timestamp:
                user_session[1] = user_session[1] + 1
        else:
            sessions[user] = [timestamp, 1]

    print(sessions)
    return sum([b for _, b in sessions.values()])


events = [
    ("a", 0.0),
    ("b", 1.0),
    ("a", 2.0),  # gap 2.0 <= 5 -> same session as a's first
    ("a", 10.0),  # gap 8.0 > 5  -> new session for a
    ("b", 30.0),  # gap 29.0 > 5 -> new session for b
]
print(count_sessions(events, timeout_seconds=5.0))

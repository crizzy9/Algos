from datetime import datetime

from gaps import Appointment, Gap, Visit, find_gaps


def test_trivial():
    assert find_gaps(
        client_visits=[
            Visit(
                start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
            )
        ],
        appointments=[
            Appointment(
                start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=12, minute=0),
            ),
            Appointment(
                start=datetime(year=2025, month=1, day=1, hour=13, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
            ),
        ],
    ) == [
        Gap(
            start=datetime(year=2025, month=1, day=1, hour=12, minute=0),
            end=datetime(year=2025, month=1, day=1, hour=13, minute=0),
        ),
    ]


def test_trivial2():
    assert find_gaps(
        client_visits=[
            Visit(
                start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
            )
        ],
        appointments=[
            Appointment(
                start=datetime(year=2025, month=1, day=1, hour=13, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
            ),
        ],
    ) == [
        Gap(
            start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
            end=datetime(year=2025, month=1, day=1, hour=13, minute=0),
        ),
    ]


def test_trivial2_1():
    assert find_gaps(
        client_visits=[
            Visit(
                start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
            )
        ],
        appointments=[
            Appointment(
                start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=12, minute=0),
            ),
        ],
    ) == [
        Gap(
            start=datetime(year=2025, month=1, day=1, hour=12, minute=0),
            end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
        ),
    ]


def test_trivial2_2():
    assert find_gaps(
        client_visits=[
            Visit(
                start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
            )
        ],
        appointments=[
            Appointment(
                start=datetime(year=2025, month=1, day=1, hour=11, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=12, minute=0),
            ),
        ],
    ) == [
        Gap(
            start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
            end=datetime(year=2025, month=1, day=1, hour=11, minute=0),
        ),
        Gap(
            start=datetime(year=2025, month=1, day=1, hour=12, minute=0),
            end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
        ),
    ]


def test_trivial3():
    assert find_gaps(
        client_visits=[
            Visit(
                start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
                end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
            )
        ],
        appointments=[],
    ) == [
        Gap(
            start=datetime(year=2025, month=1, day=1, hour=10, minute=0),
            end=datetime(year=2025, month=1, day=1, hour=14, minute=0),
        ),
    ]

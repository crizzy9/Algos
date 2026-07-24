"""Find the gaps in a client's schedule during their visits.

A client checks in for one or more *visits*, each a ``[start, end)`` time
window. Within those visits they have *appointments*, also ``[start, end)``
windows. A *gap* is any stretch of time inside a visit that is not covered by
an appointment -- the free time when the client is present but not booked.

Given the visits and the appointments, return every gap.

Constraints (from the problem statement):
  * Appointments are already sorted by start time.
  * No two appointments overlap.
  * No two visits overlap (and, by extension, they are chronological).
  * Every appointment lies entirely within a single visit.

Example:
    visit     10:00 ------------------------------- 14:00
    appts     10:00 -- 12:00          13:00 -- 14:00
    gap                   12:00 -- 13:00
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Visit:
    start: datetime
    end: datetime


@dataclass
class Appointment:
    start: datetime
    end: datetime


@dataclass
class Gap:
    start: datetime
    end: datetime


def find_gaps1(client_visits: list[Visit], appointments: list[Appointment]):

    gaps: list[Gap] = []
    for v in client_visits:
        ca: list[Appointment] = []
        for a in appointments:
            if v.start <= a.start <= v.end and v.start <= a.end <= v.end:
                ca.append(a)

        if not ca:
            gaps.append(Gap(v.start, v.end))

        g = None
        g1 = None
        g2 = None

        if len(ca) == 1:
            if v.start == ca[0].start:
                g = Gap(ca[0].end, v.end)
            elif v.end == ca[0].end:
                g = Gap(v.start, ca[0].start)
            else:
                g1 = Gap(v.start, ca[0].start)
                g2 = Gap(ca[0].end, v.end)

            if g and g.start < g.end:
                gaps.append(g)
            if g1 and g1.start < g1.end:
                gaps.append(g1)
            if g2 and g2.start < g2.end:
                gaps.append(g2)

        for i in range(len(ca) - 1):
            g = Gap(ca[i].end, ca[i + 1].start)

            if g.start < g.end:
                gaps.append(g)

    return gaps


def find_gaps(client_visits: list[Visit], appointments: list[Appointment]) -> list[Gap]:
    """Find the unbooked stretches within each client visit.

    The appointments and the visits are both non-overlapping, chronologically
    ordered timelines, so we merge them in a single linear pass. A ``cursor``
    marks the end of the last booked stretch inside the current visit; whenever
    the next appointment starts past the cursor, the span in between is a gap.
    The appointment pointer ``j`` never rewinds -- each appointment is examined
    exactly once across all visits, which is what keeps the pass linear.

    A trailing ``cursor < v.end`` check emits the span after the last
    appointment (and, when a visit has no appointments at all, the whole visit).

    Time:  O(V + A) -- one pass over the visits and one over the appointments.
    Space: O(1) auxiliary, beyond the returned list of gaps.

    Assumes ``client_visits`` is chronological too (it follows from the sorted,
    visit-contained appointments); if that is ever not guaranteed, sort it first
    for an O(V log V + A) variant.
    """
    gaps: list[Gap] = []
    j = 0
    for v in client_visits:
        cursor = v.start

        # Walk the appointments that fall inside this visit. Because every
        # appointment lives in exactly one visit and the timelines are sorted,
        # `j` carries over to the next visit without ever moving backwards.
        while j < len(appointments) and appointments[j].start < v.end:
            a = appointments[j]
            if a.start > cursor:
                gaps.append(Gap(cursor, a.start))
            cursor = a.end  # no overlaps, so this only ever moves forward
            j += 1

        if cursor < v.end:
            gaps.append(Gap(cursor, v.end))

    return gaps

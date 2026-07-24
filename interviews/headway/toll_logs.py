import unittest
import collections.abc
from os.path import exists
import subprocess
import os
import collections

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

"""
We are writing software to analyze logs for toll booths on a highway. This highway is a divided highway with limited access; the only way on to or off of the highway is through a toll booth.

There are three types of toll booths:
* ENTRY toll booths, where a car goes through a booth as it enters the highway.
* EXIT toll booths, where a car goes through a booth as it exits the highway.
* MAINROAD (M in the diagram), which have sensors that record a license plate as a car drives through at full speed.


         Exit Booth                   Entry Booth
             ^                             |
             |                             v
---<---------<---------M---------<---------<---------<---------
                                         (West-bound side)

===============================================================

                                         (East-bound side)
------>--------->---------M--------->--------->--------->------
                ^                             |
                |                             v
           Entry Booth                    Exit Booth

For our first task:
1-1) Read through and understand the code and comments below. Feel free to run the code and tests.
1-2) The tests are not passing due to a bug in the code. Make the necessary changes to LogEntry to fix the bug.
"""
"""
We are interested in how many people are using the highway, and so we would like to count how many complete journeys are taken in the log file.

A complete journey consists of:
* A driver entering the highway through an ENTRY toll booth.
* The driver passing through some number of MAINROAD toll booths (possibly 0).
* The driver exiting the highway through an EXIT toll booth.

For example, the following excerpt of log lines contains complete journeys for the cars with JOX304 and THX138:

.
.
.
90750.191 JOX304 250E ENTRY
91081.684 JOX304 260E MAINROAD
91082.101 THX138 110E ENTRY
91483.251 JOX304 270E MAINROAD
91873.920 THX138 120E MAINROAD
91874.493 JOX304 280E EXIT
.
.
91982.102 THX138 290E EXIT
92301.302 THX138 300E ENTRY
92371.302 THX138 310E EXIT
.

→ This log contains 3 complete journeys:
  • JOX304: 1 journey
  • THX138: 2 journeys

The log contains only complete journeys, there are no missing entries.

2-1) Write a function in LogFile named count_journeys() that returns how many
     complete journeys there are in the given LogFile.
"""
"""
We would like to catch people who are driving at unsafe speeds on the highway. To help us do that, we would like to identify journeys where a driver does either of the following:
* Drive 130 km/h or greater in any individual 10km segment of tollway.
* Drive 120 km/h or greater in any two 10km segments of tollway.

For example, consider the following log:
90750.191 JOX304 250E ENTRY
91081.684 JOX304 260E MAINROAD
91082.101 THX138 110E ENTRY
91483.251 JOX304 270E MAINROAD
91873.920 THX138 120E MAINROAD
91874.493 JOX304 280E EXIT
.
.
91982.102 THX138 290E EXIT
92301.302 THX138 300E ENTRY
92371.302 THX138 310E EXIT
.
.
93005.405 TST002 270W ENTRY
93280.609 TST002 260W EXIT

In this case, the driver of TST002 drove 10 km in 275 seconds. We can calculate
that this driver drove an average speed of ~130.91km/hr over this segment:

10 km * 3600 sec/hr
------------------- = 130.91 km/hr
      275 sec

Note that:
* A license plate may have multiple journeys in one file, and if they drive at unsafe speeds in both journeys, both should be counted.
* We do not mark speeding if they are not on the highway (i.e. for any driving between an EXIT and ENTRY event).
* Speeding is only marked once per journey. For example, if there are 4 segments 120km/h or greater, or multiple segments 130km/h or greater, the journey is only counted once.

3-1) Write a function catch_speeders in LogFile that returns a collection of license plates that drove at unsafe speeds during a journey in the LogFile.
     If the same license plate drives at unsafe speeds during two different journeys, the license plate should appear twice (once for each journey they drove at unsafe speeds).
"""


class LogEntry:
    """
    Represents an entry from a single log line.

    Log lines look like this in the file:

    34400.409 SXY288 210E ENTRY

    Where:
    * 34400.409 is the timestamp in seconds since the software was started.
    * SXY288 is the license plate of the vehicle passing through the toll booth.
    * 210E is the location and traffic direction of the toll booth. Here, the
        toll booth is at 210 kilometers from the start of the tollway, and the E
        indicates that the toll booth was on the east-bound traffic side.
        Tollbooths are placed every ten kilometers.
    * ENTRY indicates which type of toll booth the vehicle went through. This is
        one of "ENTRY", "EXIT", or "MAINROAD".
    """

    def __init__(self, log_line):
        tokens = log_line.split(" ")
        self.timestamp = float(tokens[0])
        self.license_plate = tokens[1]
        self.booth_type = tokens[3]
        self.location = int(tokens[2][:-1])
        direction_letter = tokens[2][-1]
        if direction_letter == "E":
            self.direction = "EAST"
        elif direction_letter == "W":
            self.direction = "WEST"
        else:
            raise ValueError

    def __str__(self):
        return (
            "<LogEntry timestamp: %f  license: %s  location: %d  direction: %s  booth type: %s>"
            % (
                self.timestamp,
                self.license_plate,
                self.location,
                self.direction,
                self.booth_type,
            )
        )


class LogFile(collections.abc.Sequence):
    """
    Represents a file containing a number of log lines, converted to LogEntry objects.
    """

    def __init__(self, file_handle):
        self.journeys = {}
        self.log_entries = []
        self.entries_by_plate = {}
        for line in file_handle:
            log_entry = LogEntry(line.strip())
            self.log_entries.append(log_entry)

        self.set_journeys()

    def __getitem__(self, index):
        return self.log_entries[index]

    def __len__(self):
        return len(self.log_entries)

    # def count_journeys(self):
    #     for entry in self.log_entries:
    #         self.journeys.setdefault(entry.license_plate, 0)
    #
    #         if entry.booth_type == "ENTRY":
    #             self.journeys[entry.license_plate] += 1
    #
    #     return sum(self.journeys.values())

    def set_journeys(self):
        for entry in self.log_entries:
            self.entries_by_plate.setdefault(entry.license_plate, [])
            self.entries_by_plate[entry.license_plate].append(entry)

        for plate, entries in self.entries_by_plate.items():
            journey = 0
            for entry in entries:
                if entry.booth_type == "ENTRY":
                    journey += 1
                    self.journeys.setdefault(plate, [])
                    self.journeys[plate].append([entry])
                else:
                    self.journeys[plate][journey - 1].append(entry)

    def count_journeys(self):
        return sum([len(j) for j in self.journeys.values()])

    def catch_speeders(self):
        speeders = []
        for plate, journey_entries in self.journeys.items():
            potential_speeders = {}
            for entries in journey_entries:
                ps = 0
                for i in range(len(entries) - 1):
                    tdiff = abs(entries[i].timestamp - entries[i + 1].timestamp)
                    ddiff = abs(entries[i].location - entries[i + 1].location)

                    speed = ddiff * 3600 / tdiff

                    if speed >= 130:
                        speeders.append(plate)
                        break
                    elif speed >= 120:
                        ps += 1

                    if ps >= 2:
                        speeders.append(plate)
                        break
        return speeders


class TestSuite(unittest.TestCase):
    # These tests are not meant to be exhaustive, and primarily show usage.
    def test_log_file(self):
        with open(os.path.join(_DATA, "tollbooth_small.log")) as fh:
            log_file = LogFile(fh)
        self.assertEqual(len(log_file), 13)
        for entry in log_file:
            self.assertTrue(type(entry) == LogEntry)

    def test_log_entry(self):
        log_line = "44776.619 KTB918 310E MAINROAD"
        log_entry = LogEntry(log_line)
        self.assertEqual(log_entry.timestamp, 44776.619)
        self.assertEqual(log_entry.license_plate, "KTB918")
        self.assertEqual(log_entry.location, 310)
        self.assertEqual(log_entry.direction, "EAST")
        self.assertEqual(log_entry.booth_type, "MAINROAD")
        log_line = "52160.132 ABC123 400W ENTRY"
        log_entry = LogEntry(log_line)
        self.assertEqual(log_entry.timestamp, 52160.132)
        self.assertEqual(log_entry.license_plate, "ABC123")
        self.assertEqual(log_entry.location, 400)
        self.assertEqual(log_entry.direction, "WEST")
        self.assertEqual(log_entry.booth_type, "ENTRY")

    def test_count_journeys(self):
        with open(os.path.join(_DATA, "tollbooth_small.log")) as fh:
            log_file = LogFile(fh)
        self.assertEqual(3, log_file.count_journeys())
        with open(os.path.join(_DATA, "tollbooth_medium.log")) as fh:
            log_file = LogFile(fh)
        self.assertEqual(63, log_file.count_journeys())

    def test_catch_speeders(self):
        with open(os.path.join(_DATA, "tollbooth_speeders.log")) as fh:
            log_file = LogFile(fh)
        ticket_list = log_file.catch_speeders()
        # ticket_list should be a list similar to
        # ["TST002", "TST003", "TST003"]
        # In this case, TST002 had one journey with unsafe driving, and
        # TST003 had two journeys with unsafe driving. The license plates
        # may be in any order.
        ticket_counts = collections.Counter(ticket_list)
        self.assertEqual(1, ticket_counts["TST002"])
        self.assertEqual(2, ticket_counts["TST003"])
        self.assertEqual(2, len(ticket_counts))
        with open(os.path.join(_DATA, "tollbooth_medium.log")) as fh:
            log_file = LogFile(fh)
        ticket_list = log_file.catch_speeders()
        self.assertEqual(10, len(ticket_list))
        with open(os.path.join(_DATA, "tollbooth_long.log")) as fh:
            log_file = LogFile(fh)
        ticket_list = log_file.catch_speeders()
        self.assertEqual(129, len(ticket_list))


if __name__ == "__main__":
    unittest.main()

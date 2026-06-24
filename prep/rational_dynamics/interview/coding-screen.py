"""
Rational Dynamics Interview Practice
====================================

This file contains three HackerRank-style practice problems based on the
interview progression:

1. Implement intersection for two sorted array-backed sets.
2. Implement contains and add for a sorted array-backed set.
3. Implement a RangedPartitionArray-style set for 32-bit integers.

Assumptions for Problems 1 and 2:
- Input arrays are sorted in strictly increasing order.
- Input arrays contain no duplicates.
- Do not use Python's built-in set type for the main implementation.
"""


# =============================================================================
# Problem 1: Sorted Array Set Intersection
# =============================================================================
#
# You are given two sorted arrays of unique integers. Each array represents a set.
#
# Implement a function intersect(a, b) that returns a sorted array containing only
# the values that appear in both input arrays.
#
# The returned array must:
# - Be sorted in strictly increasing order.
# - Contain no duplicates.
#
# Function Signature:
#     def intersect(a: list[int], b: list[int]) -> list[int]
#
# Input:
#     a: A sorted list of unique integers.
#     b: A sorted list of unique integers.
#
# Output:
#     A sorted list containing the intersection of a and b.
#
# Constraints:
#     0 <= len(a) <= 10^5
#     0 <= len(b) <= 10^5
#     -10^9 <= a[i], b[i] <= 10^9
#     a and b are sorted in strictly increasing order.
#     a and b contain no duplicates.
#
# Example 1:
#     Input:
#         a = [1, 3, 5, 7, 9]
#         b = [2, 3, 4, 7, 10]
#
#     Output:
#         [3, 7]
#
# Example 2:
#     Input:
#         a = [1, 2, 3]
#         b = [4, 5, 6]
#
#     Output:
#         []
#
# Expected Approach:
#     Use the two-pointer method.
#
#     Since both arrays are sorted, compare a[i] and b[j]:
#     - If they are equal, add the value to the result and move both pointers.
#     - If a[i] < b[j], move i forward.
#     - If b[j] < a[i], move j forward.
#
# Expected Complexity:
#     Time Complexity:  O(n + m)
#     Space Complexity: O(k), where k is the size of the intersection result.
#


def intersect(a: list[int], b: list[int]) -> list[int]:
    i = 0
    j = 0
    result = []

    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1

    return result


# =============================================================================
# Problem 2: Sorted Array Set - Contains and Add
# =============================================================================
#
# You are given a sorted array of unique integers representing a set.
#
# Implement two operations:
#
# 1. contains(arr, target)
#     Returns True if target exists in arr, otherwise False.
#
# 2. add(arr, value)
#     Inserts value into arr if it does not already exist.
#     The array must remain sorted and must contain no duplicates.
#
# Function Signatures:
#     def contains(arr: list[int], target: int) -> bool
#     def add(arr: list[int], value: int) -> list[int]
#
# Input:
#     arr: A sorted list of unique integers.
#     target/value: The integer to search for or insert.
#
# Output:
#     contains returns a boolean.
#     add returns the updated sorted array.
#
# Constraints:
#     0 <= len(arr) <= 10^5
#     -10^9 <= arr[i] <= 10^9
#     -10^9 <= target, value <= 10^9
#     arr is sorted in strictly increasing order.
#     arr contains no duplicates.
#
# Example 1:
#     Input:
#         arr = [1, 3, 5, 7]
#         target = 5
#
#     Output:
#         True
#
# Example 2:
#     Input:
#         arr = [1, 3, 5, 7]
#         value = 4
#
#     Output:
#         [1, 3, 4, 5, 7]
#
# Example 3:
#     Input:
#         arr = [1, 3, 5, 7]
#         value = 5
#
#     Output:
#         [1, 3, 5, 7]
#
# Expected Approach for contains:
#     Use binary search.
#
# Expected Approach for add:
#     Use binary search to find the lower-bound insertion position.
#     If value already exists at that position, do nothing.
#     Otherwise, insert value at that position.
#
# Expected Complexity:
#     contains:
#         Time Complexity:  O(log n)
#         Space Complexity: O(1)
#
#     add:
#         Time Complexity:  O(n)
#         Space Complexity: O(1), if modifying the input array in place.
#
#     add is O(n) because inserting into the middle of a Python list may require
#     shifting elements.
#


def contains(arr: list[int], target: int) -> bool:
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return True
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


def add(arr: list[int], value: int) -> list[int]:
    left = 0
    right = len(arr)

    # Find first index where arr[index] >= value.
    while left < right:
        mid = (left + right) // 2

        if arr[mid] < value:
            left = mid + 1
        else:
            right = mid

    insert_index = left

    if insert_index < len(arr) and arr[insert_index] == value:
        return arr

    arr.insert(insert_index, value)
    return arr


class SortedArraySet:
    """
    Optional class wrapper for Problem 2.

    This class stores a set as a sorted array with no duplicates.
    """

    def __init__(self, values: list[int] | None = None):
        self.items = []

        if values is not None:
            for value in values:
                self.add(value)

    def contains(self, target: int) -> bool:
        return contains(self.items, target)

    def add(self, value: int) -> None:
        add(self.items, value)

    def intersect(self, other: "SortedArraySet") -> "SortedArraySet":
        result = SortedArraySet()
        result.items = intersect(self.items, other.items)
        return result

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __repr__(self) -> str:
        return f"SortedArraySet({self.items})"


# =============================================================================
# Problem 3: RangedPartitionArray Set for 32-bit Integers
# =============================================================================
#
# You need to implement a set-like data structure for 32-bit signed integers.
#
# The supported integer range is:
#     -2^31 <= value <= 2^31 - 1
#
# A naive boolean array over the entire 32-bit integer domain would require space
# for 2^32 possible values, which is too large.
#
# Instead, implement a sparse ranged-partition structure.
#
# The integer domain should be divided into fixed-size partitions. Each integer is
# mapped to:
#     1. A partition id.
#     2. An offset inside that partition.
#
# Only partitions that contain at least one value should be allocated.
#
# Implement the following operations:
#
#     add(value):
#         Adds value to the set.
#
#     contains(value):
#         Returns True if value exists in the set, otherwise False.
#
#     remove(value):
#         Removes value from the set if present.
#         Returns True if value existed, otherwise False.
#
#     intersect(other):
#         Returns a new RangedPartitionArraySet containing only values present in
#         both sets.
#
# Functionality Requirements:
#     - Values must be valid signed 32-bit integers.
#     - Duplicate adds should not create duplicate entries.
#     - Empty partitions should be removed after deletes.
#     - The structure should not allocate space for untouched partitions.
#
# Example:
#     Input Operations:
#         s = RangedPartitionArraySet(partition_size=1024)
#         s.add(10)
#         s.add(2050)
#         s.add(-1)
#
#     Expected Results:
#         s.contains(10)    -> True
#         s.contains(11)    -> False
#         s.contains(2050)  -> True
#         s.contains(-1)    -> True
#
# Expected Approach:
#     Use a dictionary from partition id to a compact representation of values
#     inside that partition.
#
#     For an array-backed partition:
#         partition = value // partition_size
#         offset = value % partition_size
#
#     Store offsets in a sorted array for each partition.
#
# Expected Complexity for Array-Backed Partitions:
#     Let p be the number of elements in the specific partition.
#
#     contains:  O(log p)
#     add:       O(p), because insertion into a partition array may shift elements.
#     remove:    O(p), because deletion from a partition array may shift elements.
#     intersect: O(P + total matched partition scan cost), where P is the number
#                of occupied partitions considered.
#
# Notes:
#     For better constant-time membership, a partition can also be represented as
#     a bitset. This file implements the array-backed version because the prompt
#     specifically references a RangedPartitionArray type.
#


class RangedPartitionArraySet:
    MIN_INT_32 = -(2**31)
    MAX_INT_32 = 2**31 - 1

    def __init__(self, partition_size: int = 1024):
        if partition_size <= 0:
            raise ValueError("partition_size must be positive")

        self.partition_size = partition_size
        self.partitions: dict[int, list[int]] = {}

    def _validate_32bit_int(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("value must be an integer")

        if value < self.MIN_INT_32 or value > self.MAX_INT_32:
            raise ValueError("value must be a signed 32-bit integer")

    def _partition_and_offset(self, value: int) -> tuple[int, int]:
        self._validate_32bit_int(value)
        partition = value // self.partition_size
        offset = value % self.partition_size
        return partition, offset

    def _lower_bound(self, arr: list[int], value: int) -> int:
        left = 0
        right = len(arr)

        while left < right:
            mid = (left + right) // 2

            if arr[mid] < value:
                left = mid + 1
            else:
                right = mid

        return left

    def add(self, value: int) -> None:
        partition, offset = self._partition_and_offset(value)

        if partition not in self.partitions:
            self.partitions[partition] = [offset]
            return

        bucket = self.partitions[partition]
        index = self._lower_bound(bucket, offset)

        if index < len(bucket) and bucket[index] == offset:
            return

        bucket.insert(index, offset)

    def contains(self, value: int) -> bool:
        partition, offset = self._partition_and_offset(value)

        if partition not in self.partitions:
            return False

        bucket = self.partitions[partition]
        index = self._lower_bound(bucket, offset)

        return index < len(bucket) and bucket[index] == offset

    def remove(self, value: int) -> bool:
        partition, offset = self._partition_and_offset(value)

        if partition not in self.partitions:
            return False

        bucket = self.partitions[partition]
        index = self._lower_bound(bucket, offset)

        if index == len(bucket) or bucket[index] != offset:
            return False

        bucket.pop(index)

        if not bucket:
            del self.partitions[partition]

        return True

    def intersect(self, other: "RangedPartitionArraySet") -> "RangedPartitionArraySet":
        if self.partition_size != other.partition_size:
            raise ValueError("partition sizes must match")

        result = RangedPartitionArraySet(self.partition_size)

        if len(self.partitions) <= len(other.partitions):
            smaller_partitions = self.partitions
            larger_partitions = other.partitions
        else:
            smaller_partitions = other.partitions
            larger_partitions = self.partitions

        for partition, left_bucket in smaller_partitions.items():
            if partition not in larger_partitions:
                continue

            right_bucket = larger_partitions[partition]
            common_offsets = intersect(left_bucket, right_bucket)

            if common_offsets:
                result.partitions[partition] = common_offsets

        return result

    def to_sorted_list(self) -> list[int]:
        result = []

        for partition in sorted(self.partitions.keys()):
            base = partition * self.partition_size
            for offset in self.partitions[partition]:
                result.append(base + offset)

        return result

    def __repr__(self) -> str:
        return f"RangedPartitionArraySet({self.to_sorted_list()})"


# =============================================================================
# Basic Tests
# =============================================================================

if __name__ == "__main__":
    # Problem 1 tests
    assert intersect([1, 3, 5, 7, 9], [2, 3, 4, 7, 10]) == [3, 7]
    assert intersect([1, 2, 3], [4, 5, 6]) == []
    assert intersect([], [1, 2, 3]) == []
    assert intersect([1, 2, 3], []) == []
    assert intersect([1, 2, 3], [1, 2, 3]) == [1, 2, 3]

    # Problem 2 tests
    arr = [1, 3, 5, 7]
    assert contains(arr, 5) is True
    assert contains(arr, 6) is False
    assert add(arr, 4) == [1, 3, 4, 5, 7]
    assert add(arr, 5) == [1, 3, 4, 5, 7]
    assert add(arr, 0) == [0, 1, 3, 4, 5, 7]
    assert add(arr, 10) == [0, 1, 3, 4, 5, 7, 10]

    set_a = SortedArraySet([1, 3, 5, 7, 9])
    set_b = SortedArraySet([2, 3, 4, 7, 10])
    assert set_a.contains(5) is True
    assert set_a.contains(6) is False
    assert set_a.intersect(set_b).items == [3, 7]

    # Problem 3 tests
    rpa = RangedPartitionArraySet(partition_size=1024)
    rpa.add(10)
    rpa.add(2050)
    rpa.add(-1)
    rpa.add(-1024)
    rpa.add(2**31 - 1)
    rpa.add(-(2**31))

    assert rpa.contains(10) is True
    assert rpa.contains(11) is False
    assert rpa.contains(2050) is True
    assert rpa.contains(-1) is True
    assert rpa.contains(-1024) is True
    assert rpa.contains(2**31 - 1) is True
    assert rpa.contains(-(2**31)) is True

    assert rpa.remove(2050) is True
    assert rpa.contains(2050) is False
    assert rpa.remove(2050) is False

    rpa_1 = RangedPartitionArraySet(partition_size=1024)
    rpa_2 = RangedPartitionArraySet(partition_size=1024)

    for value in [-1024, -1, 0, 10, 1025, 2048, 3000]:
        rpa_1.add(value)

    for value in [-1, 10, 11, 2048, 4096]:
        rpa_2.add(value)

    rpa_intersection = rpa_1.intersect(rpa_2)
    assert rpa_intersection.to_sorted_list() == [-1, 10, 2048]

    print("All tests passed.")

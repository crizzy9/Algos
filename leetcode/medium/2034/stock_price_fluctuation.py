import heapq


class StockPrice:
    def __init__(self):
        self.records: dict[int, int] = {}
        self.latest_timestamp: int = 0
        self.max_heap: list[tuple[int, int]] = []
        self.min_heap: list[tuple[int, int]] = []

    def update(self, timestamp: int, price: int) -> None:
        self.records[timestamp] = price
        self.latest_timestamp = max(self.latest_timestamp, timestamp)

        heapq.heappush(self.max_heap, (-price, timestamp))
        heapq.heappush(self.min_heap, (price, timestamp))

    def current(self) -> int:
        return self.records[self.latest_timestamp]

    def maximum(self) -> int:
        price, timestamp = self.max_heap[0]

        while -price != self.records[timestamp]:
            heapq.heappop(self.max_heap)
            price, timestamp = self.max_heap[0]

        return -price

    def minimum(self) -> int:
        price, timestamp = self.min_heap[0]

        while price != self.records[timestamp]:
            heapq.heappop(self.min_heap)
            price, timestamp = self.min_heap[0]

        return price


if __name__ == "__main__":
    # Your StockPrice object will be instantiated and called as such:

    stockPrice = StockPrice()
    stockPrice.update(1, 10)  # Timestamps are [1] with corresponding prices [10].
    stockPrice.update(2, 5)  # Timestamps are [1,2] with corresponding prices [10,5].
    assert (
        stockPrice.current() == 5
    )  # return 5, the latest timestamp is 2 with the price being 5.
    assert (
        stockPrice.maximum() == 10
    )  # return 10, the maximum price is 10 at timestamp 1.
    stockPrice.update(
        1, 3
    )  # The previous timestamp 1 had the wrong price, so it is updated to 3.
    # Timestamps are [1,2] with corresponding prices [3,5].

    assert (
        stockPrice.maximum() == 5
    )  # return 5, the maximum price is 5 after the correction.
    stockPrice.update(4, 2)  # Timestamps are [1,2,4] with corresponding prices [3,5,2].
    assert stockPrice.minimum() == 2  # return 2, the minimum price is 2 at timestamp 4.

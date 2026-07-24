import unittest
from enum import Enum
from statistics import mean
import math


class OrderStatus(Enum):
    """
    Orders are active until delivered or cancelled
    """

    PLACED = 1
    PREPARING = 2
    OUT_FOR_DELIVERY = 3
    DELIVERED = 4
    CANCELED = 5


class Order:
    def __init__(
        self, order_id, restaurant_id, customer_id, order_value, distance_km, status
    ):
        self.order_id = order_id
        self.restaurant_id = restaurant_id
        self.customer_id = customer_id
        self.order_value = order_value
        self.distance_km = distance_km
        self.status = status


class Delivery:
    def __init__(self, delivery_id: int, start_minute: int, end_minute: int):
        self.delivery_id = delivery_id
        self.start_minute = start_minute
        self.end_minute = end_minute

    def get_duration_minutes(self) -> int:
        return self.end_minute - self.start_minute


class OrderStats:
    def __init__(self, total_orders, active_orders, closed_orders):
        self.total_orders = total_orders
        self.active_orders = active_orders
        self.closed_orders = closed_orders


"""
Round 1:
We are building a program to manage a food delivery platform. The platform has multiple restaurants,
customers place orders, and those orders move through statuses:
PLACED → PREPARING → OUT_FOR_DELIVERY → DELIVERED, or CANCELED.

Definitions:
* An "order" has: orderId, restaurantId, customerId, orderValue, distanceKm, status.
* "OrderManager" manages orders and provides order statistics.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Feel free to run it.
1-2) The test for OrderManager is not passing due to a bug in the code.
     Make the necessary changes to OrderManager to fix the bug.
"""


class OrderManager:
    def __init__(self):
        self.orders = []
        self.restaurant_deliveries = {}
        self.deliveries = {}
        self.partner_deliveries = {}

    def add_order(self, order):
        self.orders.append(order)

    def update_order_status(self, order_id, new_status):
        for order in self.orders:
            if order.order_id == order_id:
                order.status = new_status
                return

    def get_order_statistics(self):
        total = len(self.orders)

        active = 0
        for order in self.orders:
            if order.status in (
                OrderStatus.PLACED,
                OrderStatus.PREPARING,
                OrderStatus.OUT_FOR_DELIVERY,
            ):
                active += 1

        closed = 0
        for order in self.orders:
            if order.status in (OrderStatus.DELIVERED, OrderStatus.CANCELED):
                closed += 1

        return OrderStats(total, active, closed)

    """
    Round 2:
    We are updating our system to include delivery session information for orders.

    We introduce a Delivery class:
    - Each Delivery has a unique deliveryId
    - startMinute and endMinute represent minutes from the start of the day (same day)
    - duration = endMinute - startMinute

    Add two functions to OrderManager:

    2.1) add_delivery(order_id, delivery):
        Associate a delivery with an order. One order could have multiple deliveries. If the order does not exist, ignore.

    2.2) get_average_delivery_time_by_restaurant():
        Compute the average delivery duration (minutes) per restaurantId.
        Count ALL deliveries for that restaurant (across orders).
        Return: Dict[int, float] mapping restaurantId -> averageDuration.

    To assist you in testing these new functions, we have provided the
    test_get_average_delivery_time_by_restaurant test.
    """

    def add_delivery(self, order_id, delivery):
        curr_order = None
        for order in self.orders:
            if order.order_id == order_id:
                curr_order = order
                break

        if curr_order is None:
            return
        else:
            self.deliveries.setdefault(order_id, [])
            self.restaurant_deliveries.setdefault(curr_order.restaurant_id, [])
            self.deliveries[order_id].append(delivery)
            self.restaurant_deliveries[curr_order.restaurant_id].append(delivery)

    def get_average_delivery_time_by_restaurant(self):

        avg_times = {}

        for rid, dels in self.restaurant_deliveries.items():
            avg_times[rid] = mean([d.end_minute - d.start_minute for d in dels])

        return avg_times

    """
    Round 3:
    We want to know the delivery fee for each order.

    A delivery fee is computed in three steps:

    * Step 1: Round the order's distance UP to the nearest whole km.
    (1.0 => 1, 1.2 => 2, 2.1 => 3)

    * Step 2: Calculate the base fee:
    2 for the first km,
    +1 per extra km.
    (Example: 1 km => 2, 2 km => 3, 3 km => 4, etc.)

    * Step 3: Apply order value discount:
    - order value >= 50  =>  fee = 0 (free delivery)
    - order value >= 30  =>  fee is 50% off
    - Otherwise  =>  use the base fee

    Example: Order with distance 2.1 km and orderValue 35.0
    roundedKm = 3  =>  base = 4  =>  50% off  =>  fee = 2.0

    Add a function get_delivery_fees in OrderManager that calculates and returns a map from orderId to the corresponding fee.

    To test this new function, the test_get_delivery_fees function will be added.
    """

    def get_delivery_fees(self):
        fees = {}
        for order in self.orders:
            dist = math.ceil(order.distance_km)
            fee = dist + 1

            if order.order_value >= 50:
                fee = 0
            elif order.order_value >= 30:
                fee = fee / 2

            fees[order.order_id] = fee

        return fees

    """
    Round 4:
    We want to recommend delivery partners who are active at the same time most often.

    To support this feature, a new class is added to the code:
    * PartnerDelivery: a delivery session done by a partner (partnerId, startMinute, endMinute)

    Extend OrderManager with add_partner_delivery to store partner deliveries.

    Then, to find the best partners, for each partner we compute how many minutes their delivery windows overlap with each other partner. The output is a list of recommended partners for each partner: who they overlap with and for how many minutes, ranked by overlap (highest first), then by partner ID when tied. Only include partners with overlap greater than zero.

    Understanding overlap:

    Two delivery windows overlap when they share time. The overlap is the number of minutes they share.

    Examples:
    * Partner A [10, 50] and Partner B [30, 60]: both are active from minute 30 to 50, so overlap = 20 minutes.
    * Partner A [10, 20] and Partner B [20, 30]: they meet at minute 20 but share no minutes, so overlap = 0.

    When a partner has multiple deliveries, sum overlaps across all pairs: for each of their deliveries, compute its overlap with each of the other partner's deliveries, and add those minutes together.

    Example with multiple deliveries:
    Partner 1 has [0, 10] and [20, 40]. Partner 2 has [5, 25].
    First delivery [0, 10] overlaps [5, 25] by 5 minutes (5–10).
    Second delivery [20, 40] overlaps [5, 25] by 5 minutes (20–25).
    Total overlap between Partner 1 and Partner 2: 10 minutes.

    Sorting: For each partner, return the list of (otherPartnerId, overlapMinutes), sorted by overlap descending, then otherPartnerId ascending on ties.

    Example with three partners:
    Partner 1: [10, 50]
    Partner 2: [30, 60]   (overlap with 1 = 20)
    Partner 3: [55, 80]   (overlap with 2 = 5)

    Partner 1 → [(2, 20)]
    Partner 2 → [(1, 20), (3, 5)]
    Partner 3 → [(2, 5)]

    Add a function get_recommended_partners in OrderManager that returns the map described above.

    To test this new function, the test_get_recommended_partners_case1 and test_get_recommended_partners_case2 functions will be added.
    """

    def add_partner_delivery(self, partner_delivery: PartnerDelivery):
        self.partner_deliveries.setdefault(partner_delivery.partner_id, [])
        self.partner_deliveries[partner_delivery.partner_id].append(
            (partner_delivery.start_minute, partner_delivery.end_minute)
        )

    def get_recommended_partners(self):
        partners = self.partner_deliveries.keys()
        for pid, times in self.partner_deliveries:
            for other_pid in partners:
                if pid != other_pid:
                    # calculate overlap
                    for time in times:
                        for other_time in self.partner_deliveries[other_pid]:
                            if (
                                time[0] < other_time[0] < time[1]
                                or other_time[0] < time[0] < other_time[1]
                            ):
                                pass


class PartnerDelivery:
    def __init__(
        self, delivery_id: int, partner_id: int, start_minute: int, end_minute: int
    ):
        self.delivery_id = delivery_id
        self.partner_id = partner_id
        self.start_minute = start_minute
        self.end_minute = end_minute


class TestSuite(unittest.TestCase):
    def test_order_manager(self):
        print("Running test_order_manager")
        om = OrderManager()

        om.add_order(Order(1, 10, 100, 25.0, 3.2, OrderStatus.PLACED))
        om.add_order(Order(2, 10, 101, 55.0, 1.4, OrderStatus.PREPARING))
        om.add_order(Order(3, 11, 102, 15.0, 6.0, OrderStatus.OUT_FOR_DELIVERY))
        om.add_order(Order(4, 11, 103, 40.0, 2.0, OrderStatus.DELIVERED))
        om.add_order(Order(5, 12, 104, 18.0, 4.5, OrderStatus.CANCELED))

        stats = om.get_order_statistics()

        self.assertEqual(5, stats.total_orders)
        self.assertEqual(3, stats.active_orders)
        self.assertEqual(2, stats.closed_orders)

    def test_get_average_delivery_time_by_restaurant(self):
        print("Running test_get_average_delivery_time_by_restaurant")
        om = OrderManager()

        om.add_order(Order(1, 10, 100, 25.0, 3.2, OrderStatus.DELIVERED))
        om.add_order(Order(2, 10, 101, 55.0, 1.4, OrderStatus.DELIVERED))
        om.add_order(Order(3, 11, 102, 15.0, 6.0, OrderStatus.DELIVERED))

        om.add_delivery(1, Delivery(101, 10, 40))
        om.add_delivery(2, Delivery(102, 50, 80))
        om.add_delivery(2, Delivery(103, 90, 150))
        om.add_delivery(3, Delivery(104, 20, 50))

        # Ignore unknown order
        om.add_delivery(999, Delivery(105, 0, 10))

        avg = om.get_average_delivery_time_by_restaurant()

        # restaurant 10: durations [30, 30, 60] => avg 40
        self.assertAlmostEqual(40.0, avg[10], 3)
        # restaurant 11: durations [30] => avg 30
        self.assertAlmostEqual(30.0, avg[11], 3)

    def test_get_delivery_fees(self):
        print("Running test_get_delivery_fees")

        om = OrderManager()

        om.add_order(
            Order(1, 10, 100, 25.0, 1.0, OrderStatus.PLACED)
        )  # rounded1 => base2
        om.add_order(
            Order(2, 10, 101, 35.0, 2.1, OrderStatus.PLACED)
        )  # rounded3 => base4, 50% off => 2
        om.add_order(Order(3, 11, 102, 55.0, 10.0, OrderStatus.PLACED))  # free
        om.add_order(
            Order(4, 12, 103, 29.0, 1.2, OrderStatus.PLACED)
        )  # rounded2 => base3

        fees = om.get_delivery_fees()

        self.assertAlmostEqual(2.0, fees[1], 3)
        self.assertAlmostEqual(2.0, fees[2], 3)
        self.assertAlmostEqual(0.0, fees[3], 3)
        self.assertAlmostEqual(3.0, fees[4], 3)

    def assert_pair_list_equals(expected, actual):
        assert len(expected) == len(actual)
        for i in range(len(expected)):
            assert expected[i][0] == actual[i][0]
            assert expected[i][1] == actual[i][1]

    def test_get_recommended_partners_case1(self):
        print("Running test_get_recommended_partners_case1")
        om = OrderManager()

        # partner 1: [10,50]
        # partner 2: [30,60] overlap = 20
        # partner 3: [55,80] overlap with 2 = 5
        om.add_partner_delivery(PartnerDelivery(201, 1, 10, 50))
        om.add_partner_delivery(PartnerDelivery(202, 2, 30, 60))
        om.add_partner_delivery(PartnerDelivery(203, 3, 55, 80))

        recs = om.get_recommended_partners()

        assert_pair_list_equals([[2, 20]], recs[1])
        assert_pair_list_equals([[1, 20], [3, 5]], recs[2])
        assert_pair_list_equals([[2, 5]], recs[3])

    def test_get_recommended_partners_case2(self):
        print("Running test_get_recommended_partners_case2")
        om = OrderManager()

        # partner 1: [0,10], [20,40]
        # partner 2: [5,25] overlaps total with partner1 = 10
        # partner 3: [12,18] overlaps with partner2 [12,18] = 6
        # partner 4: [30,50] overlaps with partner1 [20,40] = 10
        om.add_partner_delivery(PartnerDelivery(301, 1, 0, 10))
        om.add_partner_delivery(PartnerDelivery(302, 1, 20, 40))
        om.add_partner_delivery(PartnerDelivery(303, 2, 5, 25))
        om.add_partner_delivery(PartnerDelivery(304, 3, 12, 18))
        om.add_partner_delivery(PartnerDelivery(305, 4, 30, 50))

        recs = om.get_recommended_partners()

        # p1: tie on overlap=10 → otherPartnerId ascending
        assert_pair_list_equals([[2, 10], [4, 10]], recs[1])
        assert_pair_list_equals([[1, 10], [3, 6]], recs[2])
        assert_pair_list_equals([[2, 6]], recs[3])
        assert_pair_list_equals([[1, 10]], recs[4])


if __name__ == "__main__":
    unittest.main()

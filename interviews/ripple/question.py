"""
Typically in a cross-border payment, we first provide the customer with
an estimation or quote of the FX rate, which the customer follows up
optionally with a payment execution request, should the quote be
acceptable. Because we utilize a FX exchange to execute the payment,
the quote must be based on the orders present in the exchange.

In this exercise, we will be writing a quote function for purchasing XRP
with USD.

A limit order has two components - a limit price in USD and a quantity
to sell in XRP. Given list of these sell orders, create a function
that calculates the amount of XRP you can purchase with a given
amount of USD.

sellOrders = [
  LimitOrder(0.25, 10.00),  // limit (USD), quantity (XRP)
  LimitOrder(0.50, 20.00),
  LimitOrder(0.75, 5.00),
];
calculateXrpQuote(sellOrders, 1.25);  // 5.0

Each order now carries a fee rate. The effective cost per XRP is price x
(1 + fee rate).

class LimitOrder {
  double limitPrice;
  double quantity;
  double feeRate;  // e.g. 0.002 = 0.2%
}
Order A: price=0.50, qty=10, fee=0.01 -> effective 0.505
Order B: price=0.48, qty=10, fee=0.06 -> effective 0.509
"""


class LimitOrder:
    def __init__(self, price: float, qty: float, fee: float):
        self.price: float = price
        self.qty: float = qty
        self.fee: float = fee


def inclusive_price(order: LimitOrder):
    return order.price * (1 + order.fee)


def calculateXrpQuote(orders: list[LimitOrder], budget: float):
    remaining_budget = budget
    num_bought = 0

    for order in sorted(orders, key=inclusive_price):
        full_price = inclusive_price(order)

        buy_power = remaining_budget / full_price
        to_buy = min(buy_power, order.qty)

        cost = to_buy * full_price

        remaining_budget -= cost
        num_bought += to_buy

    return num_bought


if __name__ == "__main__":
    assert (
        calculateXrpQuote(
            [
                LimitOrder(0.25, 10.00, 0),
                LimitOrder(0.5, 20.00, 0),
                LimitOrder(0.75, 5.00, 0),
            ],
            1.25,
        )
        == 5.0
    )

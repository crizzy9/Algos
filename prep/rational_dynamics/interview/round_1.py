class FundGraph:
    def __init__(self, allocations: dict[int, dict[int, float]]):
        """allocations: fund -> {child_fund: ratio}.
        The set of children per fund is FIXED; only ratios change later."""
        self.allocations = allocations
        self.precomputed_allocations = {}
        self.precompute_investments()
        print(self.precomputed_allocations)

    def precompute_investments(self):
        for k in self.allocations.keys():
            for n in self.allocations.keys():
                self.precomputed_allocations.setdefault(k, {})
                self.precomputed_allocations[k][n] = self.fraction_invested_rec(
                    k, n, 0, 1.0
                )

    def fraction_invested(self, source: int, destination: int) -> float:
        """Total fraction of source's money that ends up in destination,
        over all direct and indirect paths."""

        # Part 3 - O(1)
        return self.precomputed_allocations[source][destination]

        # Part 2 - O(n)
        # return self.fraction_invested_rec(source, destination, 0, 1.0)

        # Part 1 - O(1)
        # for k, v in self.allocations[source].items():
        #     if k == destination:
        #         curr_invested += v
        #     else:
        #         ratio = v
        #         # check fractional_invested with curr_ratio destination
        #         if destination in self.allocations[k]:
        #             curr_invested += self.allocations[k][destination] * ratio

    def fraction_invested_rec(
        self, source: int, destination: int, curr_invested: float, ratio: float
    ):

        if source == destination:
            return 1.0
        for k, v in self.allocations[source].items():
            if k == destination:
                curr_invested += v * ratio
            else:
                curr_invested = self.fraction_invested_rec(
                    k, destination, curr_invested, v * ratio
                )

        return curr_invested

    def reallocate(self, fund: int, new_ratios: dict[int, float]) -> None:
        """Re-weight `fund` across its (fixed) set of children."""
        self.allocations[fund] = new_ratios


initial = {1: {}, 2: {}, 3: {1: 0.4, 2: 0.6}, 4: {1: 0.5, 3: 0.5}, 5: {1: 0.5, 4: 0.5}}

fg = FundGraph(initial)

print(fg.fraction_invested(5, 1))

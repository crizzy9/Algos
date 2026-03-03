# leetcode.com/problems/champagne-tower
# 100 rows of glasses in a pyramid
class Solution:
    def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
        poured_rows = 
        num_glasses_till_row = ((query_row-1) * query_row)/2
        if poured > num_glasses_till_row and poured > query_row:
            return 1.0
        elif poured < num_glasses_till_row:
            return 0.0
        else:
            poured - num_glasses_till_row

if __name__ == "__main__":
    s = Solution()
    assert s.champagneTower(1,1,1) == 0.0
    assert s.champagneTower(4,3,2) == 0.5
    assert s.champagneTower(4,3,1) == 0.25
    assert s.champagneTower(4,3,3) == 0.25
    assert s.champagneTower(2,1,1) == 0.5
    assert s.champagneTower(100000009,33,17) == 1.0

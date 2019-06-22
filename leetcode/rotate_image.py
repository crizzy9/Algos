# https://leetcode.com/problems/rotate-image/

class Solution:
    def rotate(self, matrix):
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)

        print("Before transformation")
        print(matrix)

        for layer in range(n//2):
            for i in range(n-layer*2-1):
                matrix[i+layer][n-1-layer], matrix[n-1-layer][n-1-layer-i], matrix[n-1-layer-i][layer], matrix[layer][i+layer] = matrix[layer][i+layer],matrix[i+layer][n-1-layer], matrix[n-1-layer][n-1-layer-i], matrix[n-1-layer-i][layer]
                # top_left = matrix[layer][i+layer]
                # top_right = matrix[i+layer][n-1-layer]
                # bottom_right = matrix[n-1-layer][n-1-layer-i]
                # bottom_left = matrix[n-1-layer-i][layer]

        print("After transformation")
        print(matrix)

    def rotate2(self, matrix):
        print("Before transformation")
        print(matrix)
        matrix = [matrix[:][i] for i in range(len(matrix))]
        print("After transformation")
        print(matrix)

if __name__ == '__main__':
    sol = Solution()

    inp = [[1,2,3], [4,5,6], [7,8,9]]
    sol.rotate(inp)
    assert inp == [[7,4,1], [8,5,2], [9,6,3]]

    inp2 = [[5,1,9,11], [2,4,8,10], [13,3,6,7], [15,14,12,16]]
    sol.rotate(inp2)
    assert inp2 == [[15,13,2,5], [14,3,4,1], [12,6,8,9], [16,7,10,11]]

    inp3 = [[1,2,3], [4,5,6], [7,8,9]]
    sol.rotate2(inp3)
    assert inp3 == [[7,4,1], [8,5,2], [9,6,3]]

    inp4 = [[5,1,9,11], [2,4,8,10], [13,3,6,7], [15,14,12,16]]
    sol.rotate2(inp4)
    assert inp4 == [[15,13,2,5], [14,3,4,1], [12,6,8,9], [16,7,10,11]]

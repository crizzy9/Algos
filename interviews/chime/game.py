def solution(moveset: list[str], board_size: int) -> str:
    board: list[list[int | tuple[int, int]]] = [[0] * 3 for _ in range(board_size)]
    player = 2

    for move in moveset:
        move_type = move[0]
        x = int(move[1])
        y = int(move[2])
        sq = board[x][y]

        # print("move:", move)
        # print("square:", sq)
        # print("current_board:", board)

        if move_type == "p":
            # switch player
            if player == 1:
                player = 2
            else:
                player = 1

            if sq == 0:
                val = 0
            else:
                val = sq[1]
            board[x][y] = (player, val + 1)

        if move_type == "t":
            direction = move[3]
            num_pieces = sq[1]

            for i in range(1, num_pieces + 1):
                if direction == "r":
                    if y + i < board_size:
                        curr_square = board[x][y + i]
                        if curr_square == 0:
                            val = 0
                        else:
                            val = curr_square[1]
                        board[x][y + i] = (player, val + 1)
                if direction == "d":
                    if x + i < board_size:
                        curr_square = board[x + i][y]
                        if curr_square == 0:
                            val = 0
                        else:
                            val = curr_square[1]
                        board[x + i][y] = (player, val + 1)
                if direction == "l":
                    if y - i >= 0:
                        curr_square = board[x][y - i]
                        if curr_square == 0:
                            val = 0
                        else:
                            val = curr_square[1]
                        board[x][y - i] = (player, val + 1)
                if direction == "u":
                    if x - i >= 0:
                        curr_square = board[x - i][y]
                        if curr_square == 0:
                            val = 0
                        else:
                            val = curr_square[1]
                        board[x - i][y] = (player, val + 1)

            # print("end_board:", board)

    # who is the winner?
    player1_pieces = 0
    player2_pieces = 0
    for r in range(board_size):
        for c in range(board_size):
            sq = board[r][c]
            if sq != 0 and sq[0] == 1:
                player1_pieces += 1
            elif sq != 0 and sq[1] == 2:
                player2_pieces += 1

    if player1_pieces == 0 and player2_pieces != 0:
        return "player 2 is the winner"
    elif player2_pieces == 0 and player1_pieces != 0:
        return "player 1 is the winner"
    else:
        return "in progress"


if __name__ == "__main__":
    assert solution(["p10", "p12", "p10", "t10r"], 3) == "player 1 is the winner"
    assert (
        solution(["p22", "p00", "p22", "p00", "p02", "t22u", "t02l"], 3)
        == "player 1 is the winner"
    )

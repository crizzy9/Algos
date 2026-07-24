"""Sample games for the Chime "place & topple" board game (interviews/chime/game.py).

Move encoding (single-digit coords, 0-indexed; x = row, y = column):
  * "pXY"   -> PLACE a piece at (x, y).
  * "tXYd"  -> TOPPLE the stack at (x, y) in direction d in {r, d, l, u}.

Rules as implemented by ``solution`` (confirmed behavior, not idealized):
  * Players alternate; player 1 places first.
  * A square is (owner, height) with a SINGLE owner -- whoever last placed or
    toppled onto it. Placing on an existing stack transfers the whole stack to
    the placer and raises its height by 1.
  * Toppling a height-N stack adds +1 height and flips ownership to the toppler
    on each of the next N squares in the chosen direction. The SOURCE stack is
    left in place (it is not emptied). Pieces that fall off the board are
    discarded. One place may be followed by one or more topples, all belonging
    to the player who placed.
  * Intended win condition: a player wins once the opponent has no pieces left
    on the board; otherwise the game is "in progress".

Per request, these tests assert the CURRENT code's output (the solution is left
untouched). Two known win-count quirks are documented inline (G2, G3): the
tally for player 2 checks the stack *height* (== 2) instead of the *owner*
(== 2), so player-2 squares whose height is not exactly 2 are miscounted.
"""

from game import solution


def test_single_place_player1_wins():
    """G1: P1 places one piece; P2 never plays -> P1 wins by elimination."""
    assert solution(["p11"], 3) == "player 1 is the winner"


def test_one_piece_each_code_declares_p1_due_to_count_bug():
    """G2: P1 owns (0,0) h1, P2 owns (2,2) h1 -- both players still on the board.

    Intended result: "in progress". The code returns "player 1 is the winner"
    because P2's only square is height 1 and the win-counter tallies player 2
    only on squares of height == 2. Asserting actual output by request.
    """
    assert solution(["p00", "p22"], 3) == "player 1 is the winner"


def test_player2_owns_all_height4_code_says_in_progress_bug():
    """G3: four places on (0,0) leave P2 owning the only square at height 4.

    Intended result: "player 2 is the winner" (P1 is eliminated). The code
    returns "in progress" because that lone P2 square is height 4, not 2, so it
    is never counted for player 2. Asserting actual output by request.
    """
    assert solution(["p00", "p00", "p00", "p00"], 3) == "in progress"


def test_place_on_top_transfers_stack_player2_wins():
    """G4: P1 places (0,0); P2 places on top, taking the whole stack (h2).

    P1 has nothing left -> P2 wins. (Also the lone P2 square is height 2, so the
    win-counter happens to tally it correctly here.)
    """
    assert solution(["p00", "p00"], 3) == "player 2 is the winner"


def test_topple_right_converts_opponent_player1_wins():
    """G5: P1 (0,0) h2 topples RIGHT, converting P2's (0,1) and extending to (0,2).

    Board ends entirely P1 (source (0,0) stays put) -> P1 wins.
    """
    assert solution(["p00", "p01", "p00", "t00r"], 3) == "player 1 is the winner"


def test_topple_down_player2_wins():
    """G6: P2 steals (0,0) to h2, then topples DOWN onto (1,0) and (2,0).

    Whole board is P2 -> P2 wins.
    """
    assert solution(["p00", "p00", "t00d"], 3) == "player 2 is the winner"


def test_topple_up_off_board_is_noop_player2_wins():
    """G7: P2 owns (0,0) h2 and topples UP from row 0.

    Both target rows are off the board, so the pieces are discarded and the
    topple is a no-op. Only (0,0) remains (P2) -> P2 wins.
    """
    assert solution(["p00", "p00", "t00u"], 3) == "player 2 is the winner"


def test_multiple_topples_left_then_down_player2_wins():
    """G8: after one place, P2 topples twice -- LEFT then DOWN -- from (1,2) h2.

    LEFT fills (1,1) and (1,0); DOWN fills (2,2) while (3,2) falls off the board.
    The source (1,2) is reused and stays in place. Board is all P2 -> P2 wins.
    """
    assert solution(["p12", "p12", "t12l", "t12d"], 3) == "player 2 is the winner"


def test_both_players_keep_pieces_in_progress():
    """G9: ends with P1 owning (0,0) h2 and (2,2) h1, P2 owning (1,1) h2.

    Both sides have pieces (and P2's square is height 2, so it is counted)
    -> "in progress".
    """
    assert solution(["p00", "p11", "p22", "p11", "p00"], 3) == "in progress"


def test_long_game_topple_down_converts_two_player1_wins():
    """G10: P1 builds (0,0) to h3 while P2 seeds (1,0) and (2,0), then topples DOWN.

    The topple converts both P2 pieces (and overshoots off the board at row 3).
    Column 0 is all P1, P2 is eliminated -> P1 wins.
    """
    assert solution(["p00", "p10", "p00", "p20", "p00", "t00d"], 3) == "player 1 is the winner"


if __name__ == "__main__":
    # Runnable without pytest: execute every test_* function in this module.
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} sample games passed")

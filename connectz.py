import sys

import constants as c
from functions import *

if __name__ == '__main__':

    validate_n_args()

    inputfilename = sys.argv[1]
    data_gen      = input_generator(inputfilename)
    x, y, z       = initialize_params(data_gen) # width|cols, height|rows, n_to_connect
    player_1_turn = True  # tracks whose turn it is
    winner        = False # will be updated to 1 if p1 wins or 2 if player 2 wins; both eval True
    new_row       = [0 for _ in range(x)]
    board         = [list(new_row)] 
    next_row      = list(new_row) # tracks depth and is used to indicate when a new row required
    col_tracker   = list(new_row) # tracks number of connected counters on the surface
    n_rows        = 1         # number of rows we are considering so far
    n_spaces      = x * y     # number of empty cells in the problem
    n_filled      = 0         # number of non-empty cells
    when_eval_row = z * 2 - 2 # when to start checking rows (n_turns when a player has placed z counters)
    when_eval_all = z         # when to start checking columns and diagonals
    n_turns       = 0

    while 1:
        # which player is taking their turn?
        player = c.PLAYER_MAP[player_1_turn]
        # column index of where the next counter falls
        col_idx = take_turn(data_gen, winner)
        # if win condition met on previous turn, output error code
        if winner:
            output('illegal continue')
        # cast to integer and catch exceptions, output error code
        col_idx = safely_cast_to_int(col_idx) - 1
        # check move is legal
        if not is_in_bounds(col_idx, x):
            output('illegal column')
        row_idx = next_row[col_idx]
        board, n_rows        = update_board(board, player, row_idx, col_idx, n_rows, y, new_row)
        col_tracker[col_idx] = update_col_tracker(col_tracker[col_idx], player)
        next_row[col_idx] += 1
        n_filled          += 1

        # check if winning conditions met
        if n_turns >= when_eval_row:
            # scan left to right
            if z <= x and row_scan(board[row_idx], col_idx, player, y, z):
                winner = player
            elif n_rows >= when_eval_all:
                # scan down and diagonal
                if col_scan(col_tracker[col_idx], player, z) \
                or diag_bottom_left_to_top_right_scan(board, row_idx, col_idx, n_rows, player, x, z) \
                or diag_top_left_to_bottom_right_scan(board, row_idx, col_idx, n_rows, player, x, z):
                    winner = player

            if not winner and n_filled >= n_spaces:
                output('draw')

        n_turns += 1
        # toggle which player is taking their turn
        player_1_turn = not player_1_turn
        # print out display
        if c.VERBOSE_MODE:
            verbose_output(player, n_turns, col_idx, row_idx, board)
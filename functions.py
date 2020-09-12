import os
import sys

import constants as c

def validate_n_args():
    '''
    Checks that only a single argument has been passed
    '''
    if len(sys.argv) - 1 != 1:
        print('connectz.py: Provide one input file', end='')
        sys.exit()

def output(description: str):
    '''
    Outputs a number based on the codes in the problem brief. Closes 
    the test file and then exits the program.
    'description' is a string as described in OUPUT_MAP and is used simply for
    readability.
    '''
    if 'file' in globals():
        global file
        file.close()
    print(c.OUTPUT_MAP[description], end='')
    sys.exit()

def input_generator(inputfilename: str, name='file'):
    '''
    Lazily read in a utf-8 encoded text file (ascii included)
    and output 'file error' error code if any exception is thrown.
    '''
    global file
    try:
        file = open(inputfilename, 'r')
    except:
        output('file error')
    for line in file:
        yield line

def is_legal_size(params):
    '''
    Are the parameters, x, y, z = (width, height, connect size),
    of legal size. e.g. all positive
    '''
    return all([x >= c.MIN_DIMENSION_SIZE for x in params])

def is_legal_connect(x, y, z):
    '''
    Is the number to connect 'z', possible given the
    dimensions of the problem
    '''
    return z <= max(x, y)

def is_in_bounds(col_idx, x):
    '''
    True if col_idx is a column index within the bounds of the problem
    '''
    return 0 <= col_idx < x

def safely_cast_to_int(x):
    '''
    Attempt to cast unknown x to an integer and exit with 'invalid file'
    error code if a ValueError exception is thrown.
    '''
    try:
        integer = int(x)
    except ValueError:
        output('invalid file')
    return integer
    
def initialize_params(data_gen):
    '''
    Read in the header/first line of the text file which should be the parameters
    'x, y, z' and validate them.
    '''
    try:
        params = data_gen.__next__()
    except StopIteration:
        output('invalid file')
    params = params.split(' ')
    if len(params) != 3:
        output('invalid file')
    params = list(map(safely_cast_to_int, params))
    if not is_legal_size(params):
        output('illegal game')
    if not is_legal_connect(*params):
        output('illegal game')
    return params

def row_scan(row, col_idx, y, z, player):
    '''
    Checks if winning condition is met by looking left and then right 
    along 'row' from 'row[col_idx]' and counting the number of connected
    'player' counters.
    Args:
        row     - list, a single row of a connectz board
        col_idx - int, column index, row[col_idx] will be a newly deployed counter
        y       - int, maximum number of columns in the problem
        player  - int, 1 or 2, player identity
        z       - int, winning condition, number of pieces to connect
    Returns:
        True if n_connected >= z
    '''
    n_connect = 1 # track num. connected
    i         = col_idx # temporary index for traversing board
    # look left
    while 1:
        i -= 1
        if 0 <= i and row[i] is player:
            n_connect += 1
        else:
            break
    if n_connect >= z:
        return True
    i = col_idx # reset index/position
    # look right
    while 1:
        i += 1
        if i < y and row[i] is player:
            n_connect += 1
        else:
            break
    if n_connect >= z:
        return True

def col_scan(column_info, player, z):
    '''
    Looks downward from newly deployed counter in order to check if winning 
    condition is satisfied.
    Args:
        column_info - int, in [-z, z], number of connected counters forming 
                      a downward line on surface at the column position of 
                      current move, negative = player 1, positive = player 2
                      0 = empty,
        player      - int, 1 or 2, player identity
        z           - int, winning condition, number of pieces to connect
    Returns:
        True if n_connected >= z
    '''
    if player is 1 and column_info < 0:
        return -column_info >= z
    elif player is 2 and column_info > 0:
        return column_info >= z
    else:
        return False

def diag_bottom_left_to_top_right_scan(board, row_idx, 
                                            col_idx, n_rows, player, x, z):
    '''
    Looks outward from a newly deployed counter to the bottom left, then the
    top right, in order to check if winning condition is satisfied.
    Args:
        board   - list[list], the gameboard
        row_idx - int, row index
        col_idx - int, column index, board[row_idx][col_idx] will be a newly
                  deployed counter
        n_rows  - int, the current number of generated rows in the problem,
                  n_rows <= number of rows in the problem
        player  - int, 1 or 2, player identity
        x       - int, number of columns in the problem
        z       - int, winning condition, number of pieces to connect
    Returns:
        True if n_connected >= z
    '''
    n_connect = 1 # track num. connected
    ri, ci    = row_idx, col_idx # temporary indices for traversing board
    # look bottom left
    while 1:
        ri -= 1
        ci -= 1
        if 0 <= ri and 0 <= ci and board[ri][ci] is player:
            n_connect += 1
        else:
            break
    if n_connect >= z:
        return True
    ri, ci = row_idx, col_idx # reset indices/position
    # look top right
    while 1:
        ri += 1
        ci += 1
        if ri < n_rows and ci < x and board[ri][ci] is player:
            n_connect += 1
        else:
            break
    if n_connect >= z:
        return True

def diag_top_left_to_bottom_right_scan(
    board, row_idx, col_idx, n_rows, player, x, z):
    '''
    Looks outward from a newly deployed counter to the top left, then the
    bottom right, in order to check if winning condition is satisfied.
    Args:
        board   - list[list], the gameboard
        row_idx - int, row index
        col_idx - int, column index, board[row_idx][col_idx] will be a newly
                  deployed counter
        n_rows  - int, the current number of generated rows in the problem,
                  n_rows <= number of rows in the problem
        player  - int, 1 or 2, player identity
        x       - int, number of columns in the problem
        z       - int, winning condition, number of pieces to connect
    Returns:
        True if n_connected >= z
    '''
    n_connect = 1 # track num. connected
    ri, ci    = row_idx, col_idx # temporary indices for traversing board
    # look top left
    while 1:
        ri += 1
        ci -= 1
        if ri < n_rows and 0 <= ci and board[ri][ci] is player:
            n_connect += 1
        else:
            break
    if n_connect >= z:
        return True
    ri, ci = row_idx, col_idx # reset indices/position
    # look bottom right
    while 1:
        ri -= 1
        ci += 1
        if 0 <= ri and ci < x and board[ri][ci] is player:
            n_connect += 1
        else:
            break
    if n_connect >= z:
        return True

def update_col_tracker(column_info, player):
    '''
    Tracks downward facing lines of connected counters 
    on the surface of the board.
    
    Args:
        column_info - int, an element of col_tracker that indicates number of 
                      a player's counters that are on the surface at a particular
                      column position
        player      - int in [1, 2], which player has placed a counter
    
    Example:

    when board = 
    
        0 0 0 0 0 2 0
        0 0 0 0 0 2 1
        1 0 0 0 0 1 1
        2 0 2 0 1 1 1
        2 2 2 0 1 1 2
        
    col_tracker = [-1, 1, 2, 0, -2, 2, -3]
    
    Returns:
        column_info - int, the updated input variable 
    '''
    if player is 1:
        if column_info < 0:
            column_info -= 1
        else:
            column_info = -1
    elif player is 2:
        if column_info > 0:
            column_info += 1
        else:
            column_info = 1
    return column_info

def take_turn(data_gen, winner):
    '''
    Increments the input generator by one, yielding the next move in the game.
    If generator is exhausted, checks if winning condition met and outputs 
    relevent error codes.
    
    Args:
        data_gen - generator that yields the next turn in the game i.e. int that indicates
                   the column of the next move
        winner   - int in [1, 2], indicates if a winner has been determined at what winner it is
    '''
    try:
        col_idx = data_gen.__next__()
    except StopIteration:
        if winner:
            output(c.WINNER_MAP[winner])
        else:
            output('incomplete')
    return col_idx

def update_board(board, player, row_idx, col_idx, n_rows, y, new_row):
    '''
    Checks whether there are enough rows for the new counter in the
    original game description i.e. ilegal row error. And checks whether 
    there are enough rows in our reconstruction. Generates a new row for 
    the board if needed. Places new counter on the board.
    '''
    if row_idx >= n_rows:
        if n_rows < y:
            board.append(list(new_row))
            n_rows += 1
        else:
            output('illegal row')
    board[row_idx][col_idx] = player
    return board, n_rows

def print_board(board):
    '''
    Simple solution for debugging and visualizing board in commandline.
    Not used by default unless DEBUG_MODE is set to True.
    '''
    print(*(row for row in reversed(board)), sep='\n')
    print()

def verbose_output(player, n_turns, col_idx, row_idx, board):
    '''
    Prints out gameboard and variables for debugging purposes
    '''
    print('xxxxxxxxxxxxxxxxxxxxxx')
    print()
    print('Player', player)
    print('Turn', n_turns)
    print('Move column:', col_idx + 1)
    print('Board idx (c/r)', col_idx, row_idx)
    print_board(board)
    print('xxxxxxxxxxxxxxxxxxxxxx')
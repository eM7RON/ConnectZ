PLAYER_MAP         = {True: 1, False: 2} # we will use 1 and 2 to represent players 1 and 2
WINNER_MAP         = {1: 'win p1', 2: 'win p2'} # for output function/map
MIN_DIMENSION_SIZE = 2     # The smallest width|height of a board
VERBOSE_MODE       = False # Simple display of gameboard and variables for debugging purposes

# This is a mapping of the output codes. This is mostly for improving readability.
OUTPUT_MAP = {
              # This happens when every possible space in the frame was filled with a 
              # counter, but neither player achieved a line of the required length.
              'draw'            : '0',
              # The first player achieved a line of the required length.
              'win p1'          : '1',
              # The second player achieved a line of the required length.
              'win p2'          : '2',
              # The file conforms to the format and contains only legal moves, but the
              # game is neither won nor drawn by either player and there are remaining 
              # available moves in the frame. Note that a file with only a dimensions line 
              # constitues an incomplete game
              'incomplete'      : '3',
              # All moves are valid in all other respects but the game has already been 
              # won on a previous turn so continued play is considered an illegal move.
              'illegal continue': '4',
              # The file conforms to the format and all moves are for legal columns but 
              # the move is for a column that is already full due to previous moves
              'illegal row'     : '5',
              # The file conforms to the format but contains a move for a column that is
              # out side the dimensions of the board. i.e. the column selected is greater
              # than X
              'illegal column'  : '6',
              # The file conforms to the format but the dimensions describe a game that
              # can never be won.
              'illegal game'    : '7',
              # The file is opened but does not conform the format
              'invalid file'    : '8',
              # The file can not be found, opened or read for some reason.
              'file error'      : '9'
              }
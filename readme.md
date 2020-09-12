
# ConnectZ
---

### Background

ConnectZ is a problem based on the well known board game Connect 4 whereby two players have to make a continuous line of 4 counters on a board of size 7 x 6. However, in the ConnectZ problem the dimensions of the board (x and y) and the number of counters which must be connected to reach a winning condition (z), are unknown a priori. The ConnectZ challenge is to write an algorithm that evaluates information about a game that has already been played and outputs the outcome. Additionally, it must be able to identify if the input information describes a valid/possible game.  

---
### Specification 
---

##### Prerequisites  

Python 3.6+
Only standard library

##### Input  

The script will be called as:  
`python connectz.py inputfilename` 

The input will be a plain text file containing one or more lines of ASCII characters.

The first line will contain singly space separated variables x, y and z describing width, height (of the board) and number of counters required to connect for a win, respectively.

The following lines will describe the columns selected by each player when taking their turn. This will start with player one and will alternate each line.

Example input:  

7 6 4     
1 <br />
2 <br />
1 <br />
2 <br />
2 <br />
1 <br />

##### Output  
 
If the game is run with no arguments or more than one argument it should print the following message as a single line to standard out:  
`connectz.py: Provide one input file`

• The output of the program should be a single integer printed to standard out.  
• The integer is a code which describes the input.  
• Output codes 0 - 3 are for valid game files.  
• Output codes 4 - 9 represent errors.  

The codes are defined as follows:  

| Code | Reason           | Description                                                                                                                                                                                                                                             |
|------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0    | Draw             | This happens when every possible space in the frame was filled with a counter, but neither player achieved a line of required length.                                                                                                                   |
| 1    | Win for player 1 | The first player achieved a line of the required length.                                                                                                                                                                                                |
| 2    | Win for player 2 | The second player achieved a line of the required length.                                                                                                                                                                                               |
| 3    | Incomplete       | The file conforms to the format and contains only legal moves, but the game is neither won nor drawn by either player and there are remaining available moves in the frame. Note that a file with only a dimensions line constitues an incomplete game. |
| 4    | Illegal continue | All moves are valid in all other respects but the game has already been won on a previous turn so continued play is considered an illegal move.                                                                                                         |
| 5    | Illegal row      | The file conforms to the format and all moves are for legal columns but the move is for a column that is already full due to previous moves.                                                                                                            |
| 6    | Illegal column   | The file conforms to the format but contains a move for a column that is outside the dimensions of the board. i.e. the column selected is greater than x.                                                                                               |
| 7    | Illegal game     | The file conforms to the format but the dimensions describe a game that can never be won.                                                                                                                                                               |
| 8    | Invalid file     | The file is opened but does not conform to the format.                                                                                                                                                                                                  |
| 9    | File error       | The file can not be found, opened or read for some reason.                                                                                                                                                                                              |

##### Testing

To run the test suite with unittest simply run test.py by:  
`python test.py` or `python -m unittest test.py`  
your python environment will need to have unittest.

### Solution

Below is an explanation of how I approached the problem developed a solution.

At the top of the constants.py script is a constant variable named 'VERBOSE_MODE'. If this is set to True while the script is run, it will
output some information on each turn and print the gameboard to command line. This is set to False/off by default so that the
only output will be the codes described in the brief.

My priorities based upon the problem brief in descending order of importance were:

|                          |                                                                         |
|--------------------------|-------------------------------------------------------------------------|
| computational efficiency | The main criteria by which the code will be judged as set by the brief |
| readability              | argueably not the same thing as following strict pep8                   |
| memory efficiency        | I was informed all problems would fit into memory so this comes 2nd     |
| modularity               | makes my life a lot easier                                              |
| pep8                     | last because no formatting criteria was given                           |

My code initially opens a file with a try/except block without being explicit on what exception I'm expecting to catch. 
I probably would look more into what exceptions may occur and ask more about the file formats etc... in a professional
setting, but in the case of this execise, I know it will catch everything and output the desired error code and I was
probably slightly paranoid that you may end up testing something of which I have not thought.

My solution then reads in the parameters in the header and checks they are valid. Games which are impossible may be routed out 
early by checking the parameters 'x, y, and z'. In a valid game, z is less than or equal to the largest of x and y.

Another check I added is that x, y, z must all be greater than 1. This is because games with negative parameters are impossible 
and I decided to make the assumption that they must be greater than 1 because the game is named 'connect' and normally at
least 2 things are required in order to 'connect' things.

I 'lazily' read in the file. My initial thoughts after reading the exercise were that a test problem could potentially be too
large to fit into memory so I use a generator to sequentially read in each player's next move. Keeping below my available memory 
limit and allowing Python's garbage collection to clean up unused variables from memory. After emailing Natalia, I was
told that the test files should easily fit into memory. However, lets consider the case where they will not, for a moment. I
tried to think of ways this may be possible and the solution I came up with is to use Python's pickle module to store the
board by saving each cell of the board under their coordinates on the board as a filename. I implemented this and tested it on
some test files which were around the 3 GB size. Which took about 30 minutes. It was apparent that doing this is much slower
but would allow the computation of files too large to fit in memory and be limited by storage rather than memory. I think it 
would also be greatly effected by the type of storage being used. I was using a SATA III SSD but could possibly be greatly
improved with SSD drives that use the PCIE standard. The Python library, Numpy, has some useful tools for this kind of situation.

Memory efficiency aside, there does not appear to be a single solution that maximizes computational efficiency
in all situations. For example, in a very large game, where each player may be drawing up to 1000 moves but the 1001th move
is NAN such as a latin or chinese character, it may have been more efficiant to iterate through the entire file beforehand
only checking for valid characters. However, this approach would be worse in large games where there is an early winner.
Taking this into consideration, it seems that there has to be a compromise. My solution iterates through the entire file
one by one performing checks for a win condition. But, it makes some simple optimizations in order to minimize the amount 
of computation required.

My solution holds a reconstructed gameboard in memory which is updated as we iterate through the test file. Each turn, a column 
index is read from the file. It is checked for errors e.g. whether a valid number and within the bounds of the problem. The board 
is then updated. Whether a winning condition has been met is then tested. This is done by looking at the new counter's position and
scanning outwards in all directions (except for up). For example, if a new counter has been placed by player 1 and we are checking
diagonal bottom left to top right: we start where the new counter was placed, scan one step down and one step left, check whether 
the new cell contains a counter belonging to player 1. If so, we record it and continue down and left, if not, then we return to
the new counter and repeat but this time moving up and right. If at any point we have recorded a line of z connected pieces. This
is recorded as a winning condition.

My solution holds in memory two special rows which are the width of the board in length. The first row, named 'next_row', keeps 
track of the height (row) at which a new counter will be placed at each column index. This means that we do not need to iterate 
through the entire board each turn to check which cells are empty or full. Additionally, this also allows us to reduce the amount 
of board we need to generate. For example, we only hold in memory required rows and add new rows as the players fill up more 
of the board. It also reduces the amount of rows we need to scan for when scanning outward and checking for a win.

The other special row is named 'col_tracker'. This row contains integers in the closed interval [-z, z], which keep track of the number of connecting 
counters extending downwards from the current top/surface counters. Negative and positive numbers indicate player 1's and player 2's 
counters respectively. 0 indicates an empty column. This eliminates downwards scans completely. For example, a value of -7 at 
col_tracker[3] would indicate that there is a downward line of 7 of player 1's counters at column 4 exposed on the surface 
(c indexing). If player 1's next move was 4 then this (col_tracker[3]) would become -8. If player 2's next move was 4 then 
col_tracker[3] would become 1. 

Another simple optimization was to only start checking for wins once a player had taken z turns. In fact this is only true for 
connections across a row as connections across columns and diagonals are only possible after z turns AND there are z rows in the 
board.

One consideration was whether to track positions on the board where a win may be obtained and, if these positions are exhausted 
before a win is reached, end the game as a draw. I have taken liberties and ignored this outcome because it does not match
the draw condition outlined in the problem brief which requires all positions to be filled. If this ability was needed it would 
require some large modifications to the code and many more calculations.

Another consideration is parallel computation. However, a player's turn in the connectz problem is affected by previous turns, so 
it is, at the very least, going to be extremely messy trying to get any kind of speed up using parallel computation. Another part 
of the difficulty with this is that each thread or process would have to be working on the same board. Furthermore, Python has 
its own challenges to overcome when considering parallel computation. So I have made no attempt to explore this and left it as a
dead end at this point.

An alternative approach may have been to represent each cell in the gameboard as a node. Each node would contain 7 numbers which 
describe its neighbours. My thinking was that computations could be reduced as we would only need to look at a counter's neighbours
when it is placed, in order to keep track of if a win condition has been met. However, it becomes apparent that if a new counter
makes a connection with one of its neighbours, the neighbours will also need to be updated incase a future counter makes a 
connection from a different direction with that neighbour. This could be mitigated if we knew what nodes are exposed on the surface 
to new connections but this would require iterating through many nodes each epoch of the algorithm. In the end, I came to the 
conclusion that this approach would be equally or more computationally complex to the the one I ended up implementing.
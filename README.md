zero knowledge chess engine

"establish the search tree" - b-tree .build up the search tree
"use a neural net to prune the search tree"

minimax algorithm + alpha beta pruning

definition : value network
V - f(board)


what is V:
V = -1  black wins baord state
V = 0 draw board state
v = 1 white board wins



state:

pieces(2 + 7*2 = 16):
universal
"blank"
en passant
pawn
bishop
rook
rook(can castle)
knight
queen
king

extra state:
castle available x4
to move


8*8*4 +  1 = 257 bits(0 or 1)
+ 1 -> whose turn is it to move(b or w)
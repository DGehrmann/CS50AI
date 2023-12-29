from tictactoe import player,actions,result,winner,terminal,utility,minimax

EMPTY = None
X="X"
O="O"

board = [[X, O, O],
         [EMPTY, X, X],
         [O, EMPTY, EMPTY]]

print(player(board))

print(actions(board))

#action = (1,0)

#print(action[0])
#print(action[1])
#print(result(board,action))

print(winner(board))
print(terminal(board))
print(utility(board))

print(minimax(board))

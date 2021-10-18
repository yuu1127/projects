#/usr/bin/python3.7     z5186797
#I made αβ Search using pseudocode and use heuristc as same as tutorial.

# Student ID: z5186797
# Student Name: YUTA SATO


# Due to there are only 2 players in this game, it is easy for us to think that using Minimax algorithm to solve this problem.
# Because in this game, we have a large board(9 x 9) consists of 9 small boards(3 x 3), so if we only use Minimax, the branches are
# too many, in another word, the time complexity is to high.
# Therefore, in order to make the search feasible, we should use AlphaBeta pruning togehter.

# In the beginning, I just consider the small board(3 x 3), the depth of this condition is shallow, so we can always get solution.
# However, according to the rule, in this game, the next board we play in is determined by the position of former player.
# So, different from small board condition, we have more things to do.

# In this agent, I define several functions.

# Firstly, we should khow whether game is over or not. To do this, I write two function named 'check_state(),judge()', this function will detect
# whether all the positions in the whole board are occupied, if yes, game is terminated. In addition, it also detect whether there is a 'XXX'
# or 'OOO' sequence in any small board.

# Secondly, I write a heuristic function to give each node in the search tree a value, in this part, we just consider that 'XOX',
# 'XXO' ,'OXO' , 'XOO' do not affect the game consition (which means treat this board as 0 point) . In this time, We just consider
# '_X_', 'X_X' etc for game state and this kind of 1 or 2 same symbol in horizontal, vertical, diagnal lines and give them different points.
# In order to do this, I also write 2 functions checkxo(),XO1(),X02() to give points to board state which is terminated or when it reaechs the depth we determined before.
# This is same sa tutotial week5, but to apply nine tic tac toe boards,
# We use heuristic function to all 9 boards and after that we sum up them and we use the value to evaluate 9 boards state.
# Finally, we decide the best choice of position to place O or X at current board.

# The main body of this agent is the minimax algorithm and AlphaBeta pruning, in this part, we should use recursion to evaluate the
# next step of opponent. It seems that we create an imaginary enemy to play this game before the agent makes decision.


import socket
import sys
import numpy as np
import copy

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
# caz return is 1~9
boards = np.zeros((10, 10), dtype="int8")
curr = 0 # this is the current board to play in
turn = 0 # this is turn 0 = my turn 1 = opponent
pre_current = 0
num_turn = 0
# print a row
# This is just ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    # The marking script doesn't seem to like this either, so just take it out to submit
    print("", board[a][i], board[a][j], board[a][k], end = " | ")
    print(board[b][i], board[b][j], board[b][k], end = " | ")
    print(board[c][i], board[c][j], board[c][k])

# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

# choose a move to play
# curr is plyaing board 1-9
# 2 AI
# 1 player
# 0 blank

def random_play():
    print_board(boards)

    # just play a random move for now
    # maybe (1,9)
    n = np.random.randint(1,9)
    while boards[curr][n] != 0:
        n = np.random.randint(1,9)

    print("AI playing", n)
    place(curr, n, 1)
    return n

def play():
    print_board(boards)
    global num_turn
    # just play a random move for now
    #n = np.random.randint(1,9)
    #while boards[curr][n] != 0:
    #    n = np.random.randint(1,9)
    n = get_move(3)
    #print(boards)
    #print("AI GET", n)
    print(f"This is turn :{num_turn}")
    place(curr, n, 1)
    num_turn += 1
    return n

# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        print("second_move")
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        print("third_move")
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play()
    elif command == "next_move":
        print("next_move")
        place(curr, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

#local variable
def get_move(depth):
    best_move = 0
    mini_value = -100
    for i in range(1,10):
        if boards[curr][i] == 0:
            tmp_value = minimax(i,depth)
            if(tmp_value > mini_value):
                mini_value = tmp_value
                best_move = i
            print(mini_value)
    return best_move
#どの時点で探索を切るか
def minimax(i,depth):
    player = turn
    current = curr
    boards_copy = copy.deepcopy(boards)
    boards_copy[current][i] = 1
    return alphabeta(boards_copy,depth,current,player,-10000,10000)

# valueを空にする



# deep copy or recursion
# inside function curr is local value
def alphabeta(boards_copy,depth,current,player,a,b):
    global pre_current
    #print(depth)
    #print("***********")
    #print_board(boards_copy)
    if check_state(boards_copy,current) or depth == 0:
        #h1
        #h1 = heuristic(boards_copy,current,player)
        #h2 = heuristic(boards_copy,pre_current,player)
        #h = h1 + h2
        h = 0
        for i in range(1,10):
            #if i == current:
            #    h = h + heuristic(boards_copy,i,player)
            #else:
            #    h = h + heuristic(boards_copy,i,player)
            h = h + heuristic(boards_copy,i,player)
        #print(h)
        return h
    if player == 0:
        for i in range(1,10):
            if boards_copy[current][i] == 0:
                boards_copy_c = copy.deepcopy(boards_copy)
                boards_copy_c[current][i] = 1
                pre_current = current
                a = max(a , alphabeta(boards_copy_c,depth - 1, i, 1, a, b))
                #pruning
                if a >= b:
                    return a
                #undo_value(pre_cur,i)
        #no pruning
        return a
    else:
        for i in range(1,10):
            if boards_copy[current][i] == 0:
                boards_copy_c = copy.deepcopy(boards_copy)
                boards_copy_c[current][i] = 2
                pre_current = current
                b = min(b , alphabeta(boards_copy_c,depth - 1, i, 0, a, b))
                #undo_value(pre_cur,i)
                #pruning
                if b <= a:
                    #value = b
                    #best_value = i
                    return b
                #undo_value(pre_cur,i)
        return b
    #return best_value
    #print("aaaaaaa")
    #if depth == 0:
    #    return best_value
    #else:
    #    return value

# xo == 1 player or 2 opponent
def XO2(a,b,c,xo):
    X2_list = [a,b,c]
    if X2_list.count(xo) == 2 and X2_list.count(0) == 1:
        return True
    else:
        return False

def XO1(a,b,c,xo):
    X1_list = [a,b,c]
    #print(X1_list)
    if X1_list.count(xo) == 1 and X1_list.count(0) == 2:
        #print(a,b,c)
        return True
    else:
        return False


def judge(a,b,c):
    if a == b == c and a != 0:
        return True
    else:
        return False

def check_state(boards_copy,current):
    # only 1 zero
    if(0 not in boards_copy[current][1:]):
        return True
    for i in range(3):
        if judge(boards_copy[current][i * 3 + 1],boards_copy[current][i * 3 + 2],boards_copy[current][i * 3 + 3])\
        or judge(boards_copy[current][i + 1],boards_copy[current][i + 4],boards_copy[current][i + 7]):
            return True

    if judge(boards_copy[current][1],boards_copy[current][5],boards_copy[current][9]) or judge(boards_copy[current][3],boards_copy[current][5],boards_copy[current][7]):
            return True
    else:
        return False

def check_xo(boards_copy,current,xo):
    total = 0
    for i in range(3):
        if XO2(boards_copy[current][i * 3 + 1],boards_copy[current][i * 3 + 2],boards_copy[current][i * 3 + 3],xo):
            total += 3
        if XO1(boards_copy[current][i * 3 + 1],boards_copy[current][i * 3 + 2],boards_copy[current][i * 3 + 3],xo):
            total += 1
        if XO2(boards_copy[current][i + 1],boards_copy[current][i + 4],boards_copy[current][i + 7],xo):
            total += 3
        if XO1(boards_copy[current][i + 1],boards_copy[current][i + 4],boards_copy[current][i + 7],xo):
            total += 1
    if XO2(boards_copy[current][1],boards_copy[current][5],boards_copy[current][9],xo):
        total += 3
    if XO1(boards_copy[current][1],boards_copy[current][5],boards_copy[current][9],xo):
        #print("ss")
        total += 1
    if XO2(boards_copy[current][3],boards_copy[current][5],boards_copy[current][7],xo):
        total += 3
    if XO1(boards_copy[current][3],boards_copy[current][5],boards_copy[current][7],xo):
        #print("ss")
        total += 1
    return total

def heuristic(boards_copy,current,player):
    total = 0
    if check_state(boards_copy,current):
        if player == 0:
            total = 10
        elif player == 1:
            total = -10
        return total
    else:
        #print(check_xo(1))
        #print(check_xo(2))
        #print("total")
        total = check_xo(boards_copy,current,1) - check_xo(boards_copy,current,2)
        return total

def easy_heuristic():
    total = 0
    for i in range(1,10):
        if boards_copy[curr][i] == 1:
            total += 1
        elif boards_copy[curr][i] == 2:
            total -= 1
        else:
            total += 0
    return total

#make_terminal

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()

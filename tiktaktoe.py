TicTacToe.py
from tkinter import Tk, Button
from tkinter.font import Font
import sys
from copy import deepcopy
import time
from random import randint

"""
    Initialization of the global variables
"""
size = 4
min_util = -1000
max_util = +1000
x_player = 'X'
o_player = 'O'
empty = ' '
level = 1
moves = 0
DEPTH_LIMIT=1
imprimer=1

"""
    Variables for the statistics
"""
cutOffOccured = False
maxDepthReached = 0
totalNodes = 0
pruningMax = 0
pruningMin = 0

inf = 9999999999
neg_inf = -9999999999

computer_player = x_player
human_player = o_player

"""
    Changes the player after a move
"""
def other_player(player):
    if player == x_player:
        return o_player
    else:
        return x_player

"""
    Class state maintains the game parameters
"""
class State:
    def __init__(self, nextPlayer, other=None):
        self.nextPlayer = nextPlayer
        self.table = {}
        self.depth = 0
        self.utility = 0
        self.value = 0
        self.children = {}

        for y in range(size):
            for x in range(size):
                self.table[x, y] = empty

        # copy constructor
        if other:
            self.__dict__ = deepcopy(other.__dict__)

    def printBoard(self):
        for i in range(0, size):
            for j in range(0, size):
                if self.table[i, j] == empty:
                    sys.stdout.write(' _ ')
                elif self.table[i, j] == x_player:
                    sys.stdout.write(' X ')
                else:
                    sys.stdout.write(' O ')
            print("")

    def is_full(self):
        for i in range(0, size):
            for j in range(0, size):
                if self.table[i, j] == empty:
                    return False

        return True

    def won(self, player):
        # horizontal
        for x in range(size):
            winning = []
            for y in range(size):
                if self.table[x, y] == player:
                    winning.append((x, y))
            if len(winning) == size:
                return winning

        # vertical
        for y in range(size):
            winning = []
            for x in range(size):
                if self.table[x, y] == player:
                    winning.append((x, y))
            if len(winning) == size:
                return winning

        # diagonal \
        winning = []
        for y in range(size):
            x = y
            if self.table[x, y] == player:
                winning.append((x, y))
        if len(winning) == size:
            return winning

        # diagonal /
        winning = []
        for y in range(size):
            x = size - 1 - y
            if self.table[x, y] == player:
                winning.append((x, y))
        if len(winning) == size:
            return winning

        # default
        return None

"""
    Action function gives the next possible legal moves
"""
def ACTIONS(state):
    global maxDepthReached
    global totalNodes
    children = []
    for i in range(0, size):
        for j in range(0, size):
            if state.table[i, j] == empty:
                childTable = deepcopy(state.table)
                childTable[i, j] = state.nextPlayer
                childState = State(nextPlayer=state.nextPlayer)
                childState.nextPlayer = other_player(state.nextPlayer)
                childState.table = childTable
                childState.value = state.value
                childState.depth = state.depth + 1
                maxDepthReached = max(maxDepthReached, childState.depth)
                children.append(childState)

    totalNodes += len(children)
    return children

""""
    Terminal function to check if the terminal state has been reached
"""
def TERMINAL_TEST(state):
    if state.is_full():
        return True

    player = other_player(player=state.nextPlayer)
    if state.table[0, 0] == state.table[0, 1] \
            and state.table[0, 1] == state.table[0, 2] \
            and state.table[0, 2] == state.table[0, 3] \
            and state.table[0, 0] != empty:
        return True
    if state.table[1, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[1, 2] \
            and state.table[1, 2] == state.table[1, 3] \
            and state.table[1, 0] != empty:
        return True
    if state.table[2, 0] == state.table[2, 1] \
            and state.table[2, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[2, 3] \
            and state.table[2, 0] != empty:
        return True
    if state.table[3, 0] == state.table[3, 1] \
            and state.table[3, 1] == state.table[3, 2] \
            and state.table[3, 2] == state.table[3, 3] \
            and state.table[3, 0] != empty:
        return True
    if state.table[0, 0] == state.table[1, 0] \
            and state.table[1, 0] == state.table[2, 0] \
            and state.table[2, 0] == state.table[3, 0] \
            and state.table[0, 0] != empty:
        return True
    if state.table[0, 1] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 1] \
            and state.table[0, 1] != empty:
        return True
    if state.table[0, 2] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 2] \
            and state.table[0, 2] != empty:
        return True
    if state.table[0, 3] == state.table[1, 3] \
            and state.table[1, 3] == state.table[2, 3] \
            and state.table[2, 3] == state.table[3, 3] \
            and state.table[0, 3] != empty:
        return True
    if state.table[0, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 3] \
            and state.table[0, 0] != empty:
        return True
    if state.table[0, 3] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 0] \
            and state.table[0, 3] != empty:
        return True

    return False

"""
    Utility function to calculate the utility of a state
"""
def UTILITY(state):
    if state.table[0, 0] == state.table[0, 1] \
            and state.table[0, 1] == state.table[0, 2] \
            and state.table[0, 2] == state.table[0, 3] \
            and state.table[0, 0] != empty:
        return PLAYER_UTIL(state.table[0, 0])
    if state.table[1, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[1, 2] \
            and state.table[1, 2] == state.table[1, 3] \
            and state.table[1, 0] != empty:
        return PLAYER_UTIL(state.table[1, 0])
    if state.table[2, 0] == state.table[2, 1] \
            and state.table[2, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[2, 3] \
            and state.table[2, 0] != empty:
        return PLAYER_UTIL(state.table[2, 0])
    if state.table[3, 0] == state.table[3, 1] \
            and state.table[3, 1] == state.table[3, 2] \
            and state.table[3, 2] == state.table[3, 3] \
            and state.table[3, 0] != empty:
        return PLAYER_UTIL(state.table[3, 0])
    if state.table[0, 0] == state.table[1, 0] \
            and state.table[1, 0] == state.table[2, 0] \
            and state.table[2, 0] == state.table[3, 0] \
            and state.table[0, 0] != empty:
        return PLAYER_UTIL(state.table[0, 0])
    if state.table[0, 1] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 1] \
            and state.table[0, 1] != empty:
        return PLAYER_UTIL(state.table[0, 1])
    if state.table[0, 2] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 2] \
            and state.table[0, 2] != empty:
        return PLAYER_UTIL(state.table[0, 2])
    if state.table[0, 3] == state.table[1, 3] \
            and state.table[1, 3] == state.table[2, 3] \
            and state.table[2, 3] == state.table[3, 3] \
            and state.table[0, 3] != empty:
        return PLAYER_UTIL(state.table[0, 3])
    if state.table[0, 0] == state.table[1, 1] \
            and state.table[1, 1] == state.table[2, 2] \
            and state.table[2, 2] == state.table[3, 3] \
            and state.table[0, 0] != empty:
        return PLAYER_UTIL(state.table[0, 0])
    if state.table[0, 3] == state.table[1, 2] \
            and state.table[1, 2] == state.table[2, 1] \
            and state.table[2, 1] == state.table[3, 0] \
            and state.table[0, 3] != empty:
        return PLAYER_UTIL(state.table[0, 3])

    return 0

def PLAYER_UTIL(player):
    if player == computer_player:
        return max_util
    elif player == human_player:
        return min_util
    return 0

"""
    RANDOM PLAY
"""
def RANDOM_PLAY(state):
    global imprimer
    imprimer =0
    state.children = ACTIONS(state)
    retVal = randint(0, len(state.children) - 1)
    print("Random Play")
    return state.children[retVal]

"""
  WITH ALPHA BETA PRUNING SEARCH ALGORITHM
"""

use_alpha_beta_pruning = True

def ALPHA_BETA_SEARCH(state):
    v = MAX_VALUE(state=state, alpha=min_util, beta=max_util)
    retVal = list(filter(lambda x: x.value == v, state.children))[0]
    return retVal

def MAX_VALUE(state, alpha, beta):
    global cutOffOccured
    global pruningMax
    global pruningMin

    # Implement depth limit here
    if state.depth >= DEPTH_LIMIT:
        cutOffOccured = True
        return HEURISTIC(state)

    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

    v = neg_inf
    new_alpha = alpha
    state.children = ACTIONS(state)
    for a in state.children:
        v = max(v, MIN_VALUE(state=a, alpha=new_alpha, beta=beta))
        a.value = v
        if v >= beta:
            pruningMax += 1
            return v
        new_alpha = max(new_alpha, v)
    #print(pruningMax)
    return v

def MIN_VALUE(state, alpha, beta):
    global cutOffOccured
    global pruningMax
    global pruningMin

    # Implement depth limit here
    if state.depth >= DEPTH_LIMIT:
        cutOffOccured = True
        return HEURISTIC(state)

    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

    v = inf
    new_beta = beta
    state.children = ACTIONS(state)
    for a in state.children:
        v = min(v, MAX_VALUE(state=a, alpha=alpha, beta=new_beta))
        a.value = v
        if v <= alpha:
            pruningMin += 1
            return v
        new_beta = min(new_beta, v)
    return v
"""
    WITH ALPHA BETA PRUNING SEARCH ALGORITHM
"""

def MINIMAX_SEARCH(state):
    v = MAX_VALUE_MINIMAX(state)
    retVal = list(filter(lambda x: x.value == v, state.children))[0]
    return retVal

def MAX_VALUE_MINIMAX(state):
    global cutOffOccured
    # Implement depth limit here
    if state.depth >= DEPTH_LIMIT:
        cutOffOccured = True
        return HEURISTIC(state)

    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

    v = neg_inf
    state.children = ACTIONS(state)
    for a in state.children:
        v = max(v, MIN_VALUE_MINIMAX(state=a))
        a.value = v
    return v

def MIN_VALUE_MINIMAX(state):
    global cutOffOccured
    # Implement depth limit here
    if state.depth >= DEPTH_LIMIT:
        cutOffOccured = True
        return HEURISTIC(state)

    if TERMINAL_TEST(state=state):
        return UTILITY(state=state)

    v = inf
    state.children = ACTIONS(state)
    for a in state.children:
        v = min(v, MAX_VALUE_MINIMAX(state=a))
        a.value = v
    return v


"""
UNIFIED SEARCH FUNCTION
"""
def SEARCH(state):
    global imprimer
    if DEPTH_LIMIT == -1:
        return RANDOM_PLAY(state)
    if DEPTH_LIMIT == 1: #introduce a little randomness in easy level 
        i=randint(1, 2);
        if (i==1): #1/2 chance de randomness
            return RANDOM_PLAY(state)
    imprimer=1
    if use_alpha_beta_pruning:
        
        return ALPHA_BETA_SEARCH(state)
    else:
        return MINIMAX_SEARCH(state)
    
def HEURISTIC(state):
    x3 = 0  # "X" has 3 marks in a row, column, or diagonal
    x2 = 0  # "X" has 2 marks in a row, column, or diagonal
    x1 = 0  # "X" has 1 mark in a row, column, or diagonal
    o3 = 0  # "O" has 3 marks in a row, column, or diagonal (opponent)
    o2 = 0  # "O" has 2 marks in a row, column, or diagonal (opponent)
    o1 = 0  # "O" has 1 mark in a row, column, or diagonal (opponent)

    # Check row-wise
    for r in range(0, size):
        os = 0
        xs = 0
        for c in range(0, size):
            if state.table[r, c] == x_player:
                xs += 1
            elif state.table[r, c] == o_player:
                os += 1

        # If both X and O are present in the row, it's a blocked line
        if xs > 0 and os > 0:
            continue

        # Count potential for "O"
        if xs == 0:
            if os == 1:
                o1 += 1
            elif os == 2:
                o2 += 1
            elif os == 3:
                o3 += 1

        # Count potential for "X"
        if os == 0:
            if xs == 1:
                x1 += 1
            elif xs == 2:
                x2 += 1
            elif xs == 3:
                x3 += 1

    # Check column-wise
    for c in range(0, size):
        os = 0
        xs = 0
        for r in range(0, size):
            if state.table[r, c] == x_player:
                xs += 1
            elif state.table[r, c] == o_player:
                os += 1

        # If both X and O are present in the column, it's a blocked line
        if xs > 0 and os > 0:
            continue

        # Count potential for "O"
        if xs == 0:
            if os == 1:
                o1 += 1
            elif os == 2:
                o2 += 1
            elif os == 3:
                o3 += 1

        # Count potential for "X"
        if os == 0:
            if xs == 1:
                x1 += 1
            elif xs == 2:
                x2 += 1
            elif xs == 3:
                x3 += 1

    # Check main diagonal
    os = 0
    xs = 0
    for i in range(0, size):
        if state.table[i, i] == x_player:
            xs += 1
        elif state.table[i, i] == o_player:
            os += 1

    # If both X and O are present in the diagonal, it's a blocked line
    if xs == 0:
        if os == 1:
            o1 += 1
        elif os == 2:
            o2 += 1
        elif os == 3:
            o3 += 1
    if os == 0:
        if xs == 1:
            x1 += 1
        elif xs == 2:
            x2 += 1
        elif xs == 3:
            x3 += 1

    # Check anti-diagonal
    os = 0
    xs = 0
    for i in range(0, size):
        if state.table[size - i - 1, i] == x_player:
            xs += 1
        elif state.table[size - i - 1, i] == o_player:
            os += 1

    # If both X and O are present in the anti-diagonal, it's a blocked line
    if xs == 0:
        if os == 1:
            o1 += 1
        elif os == 2:
            o2 += 1
        elif os == 3:
            o3 += 1
    if os == 0:
        if xs == 1:
            x1 += 1
        elif xs == 2:
            x2 += 1
        elif xs == 3:
            x3 += 1

    # Threat penalty for opponent's winning potential
    threat_penalty = 10  # High penalty for opponent being 1 move from winning

    # Return the heuristic evaluation, taking into account threats
    return (6 * x3 + 3 * x2 + x1) - (6 * o3 + 3 * o2 + o1) - (threat_penalty * o3)

"""
    Code for the GUI of the game using Tkinter library
"""


class GUI:
    def __init__(self):
        self.game = State(nextPlayer=human_player)
        self.app = Tk()
        self.app.title('Tic Tac Toe')
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Courier", size=50)
        self.buttons = {}

        for x, y in self.game.table:
            handler = lambda x=x, y=y: self.move(x, y)
            button = Button(self.app, command=handler, font=self.font, width=2, height=1,bg='white',)
            button.grid(row=x, column=y)
            self.buttons[x, y] = button


        self.font = Font(family="Courier", size=15)
        handler = lambda: self.reset()
        button = Button(self.app, text='Reset', command=handler,bg='white',font=self.font)
        button.grid(row=size + 1, column=0, columnspan=size, sticky='WE')
        # Code for selecting the levels
        buttonE = Button(self.app, text='Easy', command=lambda: self.selectdifficulty(1),bg='lightgreen',font=self.font)
        buttonE.grid(row=size + 2, column=0, columnspan=size, sticky='WE')
        buttonM = Button(self.app, text='Medium', command=lambda: self.selectdifficulty(2),bg='#FFA07A',font=self.font)
        buttonM.grid(row=size + 3, column=0, columnspan=size, sticky='WE')
        buttonH = Button(self.app, text='Hard', command=lambda: self.selectdifficulty(3),bg='#FF7F7F',font=self.font)
        buttonH.grid(row=size + 4, column=0, columnspan=size, sticky='WE')
        buttoninv = Button(self.app, text='', command=lambda: self.selectdifficulty(0),bg='white',font=self.font)
        buttoninv.grid(row=size + 5, column=0, columnspan=size, sticky='WE')
        self.update()
        if first == "c":
            self.game.nextPlayer = computer_player
            self.computer_move()

    def selectdifficulty(self, value):
        global level, DEPTH_LIMIT
        level = value
        if level ==0:
            DEPTH_LIMIT=-1
        elif level == 1:
            DEPTH_LIMIT = 1 
            print("----------------")
            print("EASY LEVEL")
        elif level == 2:
            DEPTH_LIMIT = 5
            print("----------------")
            print("MEDIUM LEVEL")
        elif level == 3:
            DEPTH_LIMIT = 7
            print("----------------")
            print("HARD LEVEL")
        self.reset()

    def reset(self):
        self.resetStats()
        self.game = State(nextPlayer=human_player)
        self.update()
        self.app.destroy()
        Select().mainloop()  # Go back to the player selection

    def move(self, x, y):
        global level, DEPTH_LIMIT
        self.app.config(cursor="watch")
        self.app.configure(bg="white")
        self.app.update()
        self.game.table[x, y] = human_player 
        self.game.nextPlayer = computer_player
        self.update()
        if TERMINAL_TEST(self.game):
            return
        self.computer_move()

    def computer_move(self):
        self.game.depth = 0
        self.game = SEARCH(self.game)
        self.printStats()
        self.resetStats()
        self.update()
        self.app.config(cursor="")

    def update(self):
        for (x, y) in self.game.table:
            text = self.game.table[x, y]
            self.buttons[x, y]['text'] = text
            self.buttons[x, y]['disabledforeground'] = 'green'
            if text == empty:
                self.buttons[x, y]['state'] = 'normal'
            else:
                self.buttons[x, y]['state'] = 'disabled'
        winning = TERMINAL_TEST(self.game)
        if winning:
            winner = self.game.won(player=other_player(self.game.nextPlayer))
            if winner:
                for x, y in winner:
                    self.buttons[x, y]['disabledforeground'] = 'red'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
        for (x, y) in self.game.table:
            self.buttons[x, y].update()

    def mainloop(self):
        self.app.mainloop()

    def resetStats(self):
        global cutOffOccured
        global maxDepthReached
        global totalNodes
        global pruningMax
        global pruningMin

        cutOffOccured = False
        maxDepthReached = 0
        totalNodes = 0
        pruningMax = 0
        pruningMin = 0

    def printStats(self):
        global cutOffOccured
        global maxDepthReached
        global totalNodes
        global pruningMax
        global pruningMin
        global imprimer
        if (imprimer):

            print("-----------------------")
            print("Statistics of the Move")
            print("Maximum Depth Reached:" + str(maxDepthReached))
            print("Total number of nodes generated:" + str(totalNodes))
            if (use_alpha_beta_pruning ):
                print("Number of times pruning occured within Max-Value:" + str(pruningMax))
                print("Number of times pruning occured within Min-Value:" + str(pruningMin))

class Select:
    def __init__(self):
        self.app = Tk()
        self.app.title('Select Who Goes First')
        self.app.geometry("400x100")
        self.font = Font(family="Courier", size=20)


        self.app.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
        self.app.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand
        self.app.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand

        # Define handlers for player selection
        computer_handle = lambda: self.choose("c")
        human_handle = lambda: self.choose("h")
        b1 = Button(self.app, text='Computer', command=computer_handle,bg='white',font=self.font)
        b1.grid(row=0, column=0, sticky='NSEW', padx=0, pady=0)

        b2 = Button(self.app, text='Human', command=human_handle,bg='white',font=self.font)
        b2.grid(row=1, column=0, sticky='NSEW', padx=0, pady=0)

    def choose(self, option):
        global first
        first = option
        self.app.destroy()  # Close the player selection dialog
        AlgorithmSelect().mainloop()  # Open the algorithm selection dialog

    def mainloop(self):
        self.app.mainloop()


class AlgorithmSelect:
    def __init__(self):
        self.app = Tk()
        self.app.title('Select Algorithm')
        self.app.geometry("400x100")
        self.font = Font(family="Courier", size=15)


        self.app.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
        self.app.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand
        self.app.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand


        # Define handlers for algorithm selection
        minimax_ab_handler = lambda: self.choose(True)
        minimax_handler = lambda: self.choose(False)

        b1 = Button(self.app, text='Alpha-Beta Pruning', command=minimax_ab_handler,bg='white',font=self.font)
        b1.grid(row=0, column=0, sticky='NSEW', padx=0, pady=0)

        b2 = Button(self.app, text='No Alpha-Beta Pruning', command=minimax_handler,bg='white',font=self.font)
        b2.grid(row=1, column=0, sticky='NSEW', padx=0, pady=0)

    def choose(self, use_alpha_beta):
        print("-------new game--------")
        global use_alpha_beta_pruning  # Declare a global variable to hold the user's choice
        use_alpha_beta_pruning = use_alpha_beta
        if use_alpha_beta:
            print("Using alpha-beta Pruning")
        else:
            print("Not using pruning")
        self.app.destroy()  # Close the algorithm selection dialog
        GUI().mainloop()  # Start the game GUI

    def mainloop(self):
        self.app.mainloop()

# Main function starts from here
Select().mainloop()  # Start with the player selection dialog

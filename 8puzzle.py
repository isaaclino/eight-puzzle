import random
import math
import os

#goal
goal = [[1,2,3],
        [4,5,6],
        [7,8,0]]

def index(item, seq):
    if item in seq:
        return seq.index(item)
    else:
        return -1

class EightPuzzle:

    # This method represents a constructor in Python.
    # When is called, Python creates an object and passes it as
    # the first parameter to the __init__ method
    def __init__(self):
        # heuristic value
        self.heuristic_value = 0
        
        # search depth of current instance
        self.depth = 0
        
        # parent node in search path
        self.parent_node = None
        self.matrix = []
        for i in range(3):
            self.matrix.append(goal[i][:])



    # This function will help python to decide since
    # does NOT provide left/right version and invoques
    # __eq__ to compare itself to an int
    # similar to a == b. This case is self == other
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.matrix == other.matrix


    # Called by the str() built-in function and by
    # the print statement to compute the "informal"
    # string representation of an object
    # it helps to print the white spaces of a puzzle
    def __str__(self):
        spacing = '\t  -----------\n'
        for row in range(3):
            spacing = spacing + '\t | '
            spacing = spacing + ' | '.join(map(str, self.matrix[row])) + ' | '
            spacing = spacing + '\t\n'
            spacing = spacing + '\t  -----------\n'
        return spacing


    def replicate(self):
        p = EightPuzzle()
        for i in range(3):
            p.matrix[i] = self.matrix[i][:]
        return p


    # Return list of pairs (tuples) with the blank "zero" space swapped
    def legal_movements(self):
        
        # look for empty space, "0" zero represents empty space
        row, col = self.find(0)
        free = []
        
        # find which pieces can move there
        if row > 0:
            free.append((row - 1, col))
        if row < 2:
            free.append((row + 1, col))
        
        if col > 0:
            free.append((row, col - 1))
        if col < 2:
            free.append((row, col + 1))

        return free

    def generate_movements(self):
        free = self.legal_movements()
        zero = self.find(0)

        def swap_replicate(a, b):
            p = self.replicate()
            p.swap(a,b)
            p.depth = self.depth + 1
            p.parent_node = self
            return p

        return map(lambda pair: swap_replicate(zero, pair), free)

    def solution_pathway(self, path):
        if self.parent_node == None:
            return path
        else:
            path.append(self)
            return self.parent_node.solution_pathway(path)

    def solve(self, h):
        # Performs A* search for goal state.
        # h(puzzle) - heuristic function, returns an integer
        
        def is_solved(puzzle):
            return puzzle.matrix == goal

        openl = [self]
        closedl = []
        move_count = 0
        while len(openl) > 0:
            x = openl.pop(0)
            move_count = move_count + 1
            if (is_solved(x)):
                if len(closedl) > 0:
                    return x.solution_pathway([]), move_count
                else:
                    return [x]

            succ = x.generate_movements()
            idx_open = idx_closed = -1
            for move in succ:
                
                idx_open = index(move, openl)
                idx_closed = index(move, closedl)
                hval = h(move)
                fval = hval + move.depth

                if idx_closed == -1 and idx_open == -1:
                    move.heuristic_value = hval
                    openl.append(move)
                elif idx_open > -1:
                    copy = openl[idx_open]
                    if fval < copy.heuristic_value + copy.depth:
                        
                        # copy move's values over existing
                        copy.heuristic_value = hval
                        copy.parent_node = move.parent_node
                        copy.depth = move.depth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy.heuristic_value + copy.depth:
                        move.heuristic_value = hval
                        closedl.remove(copy)
                        openl.append(move)

            closedl.append(x)
            openl = sorted(openl, key=lambda p: p.heuristic_value + p.depth)

        # if finished state not found, return failure
        return [], 0

    #-----------------------------------------------------------
    # This function creates a shuffled random puzzle
    def shuffle(self, step_count):
        for i in range(step_count):
            row, col = self.find(0)
            free = self.legal_movements()
            target = random.choice(free)
            self.swap((row, col), target)            
            row, col = target

    #-----------------------------------------------------------
    # This function allows to create a specific puzzle
    def set(self, other):
        i=0;
        for row in range(3):
            for col in range(3):
                self.matrix[row][col] = int(other[i])
                i=i+1

    #-----------------------------------------------------------
    def bfs(self, goal):
    #Performs a breadth first search from the start state to the goal
        # A list (can act as a queue) for the nodes.
        nodes = []
        # Create the queue with the root node in it.
        nodes.append( create_node( self, None, None, 0, 0 ) )
        while True:
            # We've run out of states, no solution.
            if len( nodes ) == 0: return None
            # take the node from the front of the queue
            node = nodes.pop(0)
            # Append the move we made to moves
            # if this node is the goal, return the moves it took to get here.
            if node.state == goal:
                moves = []
                temp = node
                while True:
                    moves.insert(0, temp.operator)
                    if temp.depth == 1: break
                    temp = temp.parent
                return moves
            # Expand the node and add all the expansions to the front of the stack
            nodes.extend( expand_node( node, nodes ) )

    #-----------------------------------------------------------
    def dfs( start, goal, depth=10 ):
        # Depth parameter can be changed
        # Performs a depth first search from the start state to the goal.
     
        depth_limit = depth
        nodes = []
       
        nodes.append( create_node( start, None, None, 0, 0 ) )
        while True:
            # This case has no solution.
            if len( nodes ) == 0: return None
            
            # Using the nodes of front of the queue
            node = nodes.pop(0)
            
            # node = goal return the moves it took to get here.
            if node.state == goal:
                moves = []
                temp = node
                while True:
                    moves.insert(0, temp.operator)
                    if temp.depth <= 1: break
                    temp = temp.parent
                return moves
            
            # set all at beginning of the stack
            if node.depth < depth_limit:
                expanded_nodes = expand_node( node, nodes )
                expanded_nodes.extend( nodes )
                nodes = expanded_nodes
        print "this is the depth", depth
        print "this is the limit", depth_limit
        print "Max number of nodes in queue"

    #-----------------------------------------------------------
    # retuns rows and colums of graph value
    def find(self, value):
        for row in range(3):
            for col in range(3):
                if self.matrix[row][col] == value:
                    return row, col

    # returns value at specific row and column
    def peek(self, row, col):
        return self.matrix[row][col]

    # sets the value at the specified row and column
    def poke(self, row, col, value):
        self.matrix[row][col] = value
    
    #swaps coordinate values
    def swap(self, first_position, second_position):
        temp = self.peek(*first_position)
        self.poke(first_position[0], first_position[1], self.peek(*second_position))
        self.poke(second_position[0], second_position[1], temp)


def heuristic(puzzle, item_total_calc, total_calc):

    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.peek(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            # 0 as blank
            if target_row < 0: 
                target_row = 2

            t += item_total_calc(row, target_row, col, target_col)

    return total_calc(t)

# r  = row
# tr = target_row
# c  = col
# tc = target_col


def manhattan_heuristic(puzzle):
    return heuristic(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)



def misplaced_title_heuristic(puzzle):
    return heuristic(puzzle,
                lambda r, tr, c, tc: (abs(tr - r) + abs(tc - c))**2,
                lambda t : math.sqrt(t))


def dfs_no_heuristic(dfs):
    return 0

def bfs_no_heuristic(bfs):
    return 0

def bfs_depth(bfs):
    return dfs(puzzle)

def default(puzzle):
    return 0

def main():
    
    while True:
        # Use system to clear screen on console/terminal
        os.system('clr')
        os.system('clear')
    
        #initializing solutions
        p = EightPuzzle()
        print "\n -- The Eight Puzzle Solver -- \n\tby Isaac Lino\n\n"
        print "Choose from the menu: (1, 2 or 3 and press enter)\n\n"

        print "1) To enter your own puzzle information"
        print "2) To solve a random (random coded) puzzle"
        print "3) To solve a specific (DEMO) puzzle"
        print "\t\t------------"
        print "\t\t| 0 | 1 | 3 |"
        print "\t\t------------"
        print "\t\t| 4 | 2 | 5 |"
        print "\t\t------------"
        print "\t\t| 7 | 8 | 6 |"
        print "\t\t------------\n"
        print "4) To solve HOMEWORK puzzle"
        print "\t\t------------"
        print "\t\t| 1 | 2 | 3 |"
        print "\t\t------------"
        print "\t\t| 4 | 8 | 0 |"
        print "\t\t------------"
        print "\t\t| 7 | 6 | 5 |"
        print "\t\t------------\n"
        print "5) To solve TEST puzzle"
        print "\t\t------------"
        print "\t\t| 1 | 0 | 3 |"
        print "\t\t------------"
        print "\t\t| 7 | 2 | 6 |"
        print "\t\t------------"
        print "\t\t| 8 | 5 | 4 |"
        print "\t\t------------\n"
        menu_choose = raw_input("Choose from the menu: ")
    
    
        # --------------------------------------------------------------------
        # menu created to enter custom puzzle information
        if menu_choose == '1':
            
            print "\nEnter your initial state in one line, no comas and use 0 as blank space, then press enter"
            print "Usage example, for puzzle"
            print "\t1 2 3\n\t4 8 0\n\t7 6 5 -> enter sequence: 123456780(press return)"
            puzzle_input = raw_input("\nEnter your puzzle sequence: ")
            
            # passes the user input parameter
            p.set(puzzle_input)
            
            # prints inital state begining state
            print "\nInitial State:"
            print p
            print "solving..."
            
            path, count = p.solve(manhattan_heuristic)
            path.reverse()
            for i in path:
                print i
            print "Solved with A* with the Manhattan Distance Heuristic", count, "states"
            
            path, count = p.solve(misplaced_title_heuristic)
            print "Solved with A* with Misplaced Title Heuristic", count, "states"
    
            path, count = p.solve(default)
            print "Solved with Default Uniform Cost Search", count, "states"
    
            path, count = p.solve(dfs_no_heuristic)
            print "Solved with Depth First Search", count, "states"
    
            path, count = p.solve(bfs_no_heuristic)
            print "Solved with Breath First Search", count, "states"
    
    

        # --------------------------------------------------------------------
        # menu created to randomly create a puzzle and solve a random solution
        elif menu_choose == '2':
            
            
            # type the number of shuffle times
            ran = input("Enter number of random movements to shuffle, be ralistic!(1-20): ")
            p.shuffle(ran)
            
            print "\nCreating a random puzzle..."
            # prints inital state begining state
            print "\nRANDOM Initial State:"
            print p
            print "solving...\n"
            
            path, count = p.solve(manhattan_heuristic)
            path.reverse()
            for i in path:
                print i
            print "Solved with A* with the Manhattan Distance Heuristic", count, "states"
            
            path, count = p.solve(misplaced_title_heuristic)
            print "Solved with A* with Misplaced Title Heuristic", count, "states"
                
            path, count = p.solve(default)
            print "Solved with Default Uniform Cost Search", count, "states"

            path, count = p.solve(dfs_no_heuristic)
            print "Solved with Depth First Search", count, "states"
                
            path, count = p.solve(bfs_no_heuristic)
            print "Solved with Breath First Search", count, "states"



        # --------------------------------------------------------------------
        # menu created to solve a specific puzzle
        elif menu_choose == '3':
            # change this sequence to any hard coded sequence
            p.set("013425786")
            
            # prints inital state begining state
            print "\DEMO Initial State:"
            print p
            print "solving..."
        
            path, count = p.solve(manhattan_heuristic)
            path.reverse()
            for i in path:
                print i
            print "Solved with A* with the Manhattan Distance Heuristic", count, "states"
            print "lenght 9"
            print "depth 5"
            
            path, count = p.solve(misplaced_title_heuristic)
            print "Solved with A* with Misplaced Title Heuristic", count, "states"
            print "lenght 9"
            print "depth 5"
            
            path, count = p.solve(default)
            print "Solved with Default Uniform Cost Search", count, "states"
            print "lenght 28"
            print "depth 5"
            
            path, count = p.solve(dfs_no_heuristic)
            print "Solved with Depth First Search", count, "states"

            path, count = p.solve(bfs_no_heuristic)
            print "Solved with Breath First Search", count, "states"


        # --------------------------------------------------------------------
        # menu created to HW puzzle
        elif menu_choose == '4':
            # change this sequence to any hard coded sequence
            p.set("123480765")
        
            # prints inital state begining state
            print "\nHOMEWORK INITIAL State:"
            print p
            print "solving..."
            
            path, count = p.solve(manhattan_heuristic)
            path.reverse()
            for i in path:
                print i
            print "Solved with A* with the Manhattan Distance Heuristic", count, "states"
            print "lenght 11"
            print "depth 6"
            
            path, count = p.solve(misplaced_title_heuristic)
            print "Solved with A* with Misplaced Title Heuristic", count, "states"
            print "lenght 14"
            print "depth 6"
            
            path, count = p.solve(default)
            print "Solved with Default Uniform Cost Search", count, "states"
            print "lenght 64"
            print "depth 6"
            
            path, count = p.solve(dfs_no_heuristic)
            print "Solved with Depth First Search", count, "states"
            
            path, count = p.solve(bfs_no_heuristic)
            print "Solved with Breath First Search", count, "states"

        # --------------------------------------------------------------------
        # menu created to TEST puzzle
        elif menu_choose == '5':
            # change this sequence to any hard coded sequence
            p.set("103726854")
        
            # prints inital state begining state
            print "\TEST INITIAL State:"
            print p
            print "solving..."
            
            path, count = p.solve(manhattan_heuristic)
            path.reverse()
            for i in path:
                print i
            print "Solved with A* with the Manhattan Distance Heuristic", count, "states"
            print "lenght 37"
            print "depth 12"
            
            path, count = p.solve(misplaced_title_heuristic)
            print "Solved with A* with Misplaced Title Heuristic", count, "states"
            print "lenght 92"
            print "depth 12"
            
            path, count = p.solve(default)
            print "Solved with Default Uniform Cost Search", count, "states"
            print "lenght 1276"
            print "depth 12"
            
            path, count = p.solve(dfs_no_heuristic)
            print "Solved with Depth First Search", count, "states"
            
            path, count = p.solve(bfs_no_heuristic)
            print "Solved with Breath First Search", count, "states"


        else:
            print "\nWrong input!"
        
    
        print "\nDo you want to solve another puzzle sequence (y/n)?"
        again = raw_input("Type only 'y' or 'n' and press enter: ")
        if again.strip() == 'n':
            print "\nGood bye!\n"
            break


main()

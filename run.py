from nnf import Var
from lib204 import Encoding
import ast
import nnf

#should be built in
import time


# Ship objects where properties inside are propositions
class Ship(object):

    # Names and sizes of ships for referencing: Battleship = 4, Cruiser = 3, Destroyer = 2 *Note: Names are arbitrary; they do not matter in any scenario
    # size param. = size of board that the ship will be on, id param. = ID of instantiated Ship object
    def __init__(self,size,id):
        self.position = {}  # Position of the final ships
        self.startPosition = {}  # Used to determine the independent positions of the starting ships
        self.hInterPosition = {}  # Board for a ship's placed position that are not the starting position
        self.vInterPosition = {}  # Board for a ship's placed position that are not the starting position
        # Sizes of ship (only one can be true per ship object)
        self.size2 = Var("%d%s" % (id, "size2"))  # Destroyer
        self.size3 = Var("%d%s" % (id, "size3"))  # Cruiser or Submarine
        self.size4 = Var("%d%s" % (id, "size4"))  # Battleship
        # self.size5 = Var("%d%s" % (id, "size5"))
        self.horizontal = Var("%d%s" % (id, "horizontal"))  # Horizontal if true, vertical if false
        self.vertical = Var("%d%s" % (id,"vertical"))  # Vertical if true, horizontal if false (redundant but both vars exist to help with more readable code)
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship on the coordinate's (x, y) position
                self.startPosition[(i + 1,j + 1)] = Var("%ds(%d,%d)" % (id, i + 1, j + 1))
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship on the coordinate's (x, y) position
                self.hInterPosition[(i + 1,j + 1)] = Var("%dh(%d,%d)" % (id, i + 1, j + 1))
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship on the coordinate's (x, y) position
                self.vInterPosition[(i + 1,j + 1)] = Var("%dv(%d,%d)" % (id, i + 1, j + 1))
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship on the coordinate's (x, y) position
                self.position[(i + 1,j + 1)] = Var("(%d,%d)" % (i + 1, j + 1))


# Board object to contain the two boards and their propositions
class Board(object):
    def __init__(self, size):
        # Player board standardized to 6x6 for now due to computing limitations
        # May be used for any encoding assessing hits
        self.hit_board = {}
        for i in range(size):
            for j in range(size):
                # var for coordinate is true if the (x, y) position is hit
                self.hit_board[(i + 1,j + 1)] = Var("(%d,%d)" % (i + 1,j + 1))


def printGrid(grid):
    alpha = ["A", "B", "C", "D", "E", "F", "G", "H"]
    print("  ", end=' ')
    for i in range(size):
        if i != size:
            print(str(i + 1) + " ", end='')
        else:
            print(i + 1, end=' ')
    print("")

    for i in range(size):
        print(alpha[i] + " ", end=' ')
        for j in range(size):
            if grid[i][j]:
                print("O", end=' ')
            else:
                print("-", end=' ')
        print("")


# size of board (size x size); scalable for debugging and expansion/extension or to avoid computation issues
size = 8

# Initializes a board object of size 10x10 (what we are currently using as a standard for now)
player_board = Board(size)

# Variables for ship (size of ship, length)
s1 = Ship(size,1)
s2 = Ship(size,2)
s3 = Ship(size,3)
s4 = Ship(size,4)
s5 = Ship(size,5)

# Array if need (e.g. using for loops for a property of the ships)
fleet = [s1,s2,s3]

# See if all ship coordinates are hit
def winCondition():
    e = Encoding()

    for ship in fleet:
        for i in range(1,size + 1):
            for j in range(1,size + 1):
                e.add_constraint(player_board.hit_board[(i,j)] & ship.position[(i,j)] | ~player_board.hit_board[(i,j)] & ~ship.position[(i,j)])
    return e


#  Helper function that makes sure that the specified ship may only exist on one square. Returns a list of constraints
#  specific for each ship which will be added as a constraint of disjunctions in the main starting square function.
def startingSquareHelper(ship):
    # empty list to be populated to become list of a list of conjuncts
    conjunct_list = []
    # the returned list of list of conjuncts
    constraint_list = []
    for i in range(1,size + 1):
        for j in range(1,size + 1):
            # For each square, creates conjunction between the square and the ~squares of the rest of the grid to make
            # sure that there exists a square that the ship may reside on, and it may only reside on that one square
            for k in range(1,size + 1):
                for l in range(1,size + 1):
                    if k == i and l == j:
                        conjunct_list.append(ship.startPosition[k,l])
                    else:
                        conjunct_list.append(~ship.startPosition[k,l])
            constraint_list.append(nnf.And(conjunct_list))
            conjunct_list = []
    return constraint_list


def test_encode():
    e = Encoding()

    return e


#  Encodes for the final actual position of the whole ship depending on the other propositions: orientation, size, starting square
def allFinalPositions():
    e = Encoding()
    placements = []
    e.add_constraint(nnf.Or(startingSquareHelper(s1)))

    for ship in fleet:
        for i in range(1, size + 1):
            e.add_constraint(~ship.vInterPosition[(i,1)])
            e.add_constraint(~ship.hInterPosition[(1,i)])
        for i in range(2, 3):
            for j in range(1, size + 1):
                e.add_constraint(((ship.horizontal & ship.startPosition[(i-1,j)]) | ~ship.hInterPosition[(i,j)]))
                e.add_constraint(((ship.horizontal & ship.startPosition[(i - 1,j)]).negate() | ship.hInterPosition[(i,j)]))
        for i in range(3, 4):
            for j in range(1, size + 1):
                e.add_constraint((((ship.horizontal & ship.startPosition[(i - 2,j)] & ~ship.size2) | (ship.horizontal & ship.startPosition[(i - 1,j)])) | ~ship.hInterPosition[(i,j)]))
                e.add_constraint((((ship.horizontal & ship.startPosition[(i - 2,j)] & ~ship.size2) | (ship.horizontal & ship.startPosition[(i - 1,j)])).negate() | ship.hInterPosition[(i,j)]))
        for i in range(4, size + 1):
            for j in range(1, size + 1):
                e.add_constraint((((ship.horizontal & ship.startPosition[(i-3,j)] & ship.size4) | (ship.horizontal & ship.startPosition[(i-2,j)] & ~ship.size2) | (ship.horizontal &
                ship.startPosition[(i-1, j)])) | ~ship.hInterPosition[(i, j)]))
                e.add_constraint((((ship.horizontal & ship.startPosition[(i - 3,j)] & ship.size4) | (ship.horizontal & ship.startPosition[(i - 2,j)] & ~ship.size2) | (ship.horizontal &
                ship.startPosition[(i - 1,j)])).negate() | ship.hInterPosition[(i,j)]))
        for i in range(1, size + 1):
            for j in range(2, 3):
                e.add_constraint(((ship.vertical & ship.startPosition[(i,j-1)]) | ~ship.vInterPosition[(i,j)]))
                e.add_constraint(((ship.vertical & ship.startPosition[(i,j - 1)]).negate() | ship.vInterPosition[(i,j)]))
        for i in range(1, size + 1):
            for j in range(3, 4):
                e.add_constraint((((ship.vertical & ship.startPosition[(i,j-2)] & ~ship.size2) | (ship.vertical & ship.startPosition[(i,j-1)])) | ~ship.vInterPosition[(i,j)]))
                e.add_constraint((((ship.vertical & ship.startPosition[(i,j - 2)] & ~ship.size2) | (ship.vertical & ship.startPosition[(i,j - 1)])).negate() | ship.vInterPosition[(i,j)]))
        for i in range(1, size + 1):
            for j in range(4, size + 1):
                e.add_constraint((((ship.vertical & ship.startPosition[(i,j-3)] & ship.size4) | (ship.vertical & ship.startPosition[(i,j-2)] & ~ship.size2) | (ship.vertical &
                ship.startPosition[(i, j-1)])) | ~ship.vInterPosition[(i, j)]))
                e.add_constraint((((ship.vertical & ship.startPosition[(i,j - 3)] & ship.size4) | (ship.vertical & ship.startPosition[(i,j - 2)] & ~ship.size2) | (ship.vertical &
                ship.startPosition[(i,j - 1)])).negate() | ship.vInterPosition[(i,j)]))
        # Generation of final board
        for i in range(1,size + 1):
            for j in range(1,size + 1):
                for ship in fleet:
                    placements.append(ship.startPosition[(i,j)])
                    placements.append(ship.hInterPosition[(i,j)])
                    placements.append(ship.vInterPosition[(i,j)])
                e.add_constraint((nnf.Or(placements)) | ~s1.position[(i,j)])
                placements = []
        for i in range(1,size + 1):
            for j in range(1,size + 1):
                for ship in fleet:
                    placements.append(ship.startPosition[(i,j)])
                    placements.append(ship.hInterPosition[(i,j)])
                    placements.append(ship.vInterPosition[(i,j)])
                e.add_constraint((nnf.Or(placements)).negate() | s1.position[(i,j)])
                placements = []


    return e

# Checks to make sure that there are no overlap in position between the ships
def noOverlap():
    e = Encoding()
    for i in range(1,size + 1):
        for j in range(1,size + 1):
            e.add_constraint((s1.startPosition[(i,j)] & ~s2.startPosition[(i,j)] & ~s3.startPosition[(i,j)])
                             | (~s1.startPosition[(i,j)] & s2.startPosition[(i,j)] & ~s3.startPosition[(i,j)])
                             | (~s1.startPosition[(i,j)] & ~s2.startPosition[(i,j)] & s3.startPosition[(i,j)])
                             | (~s1.startPosition[(i,j)] & ~s2.startPosition[(i,j)] & ~s3.startPosition[(i,j)]))

    return e

# Makes sure that a ship can only have one size and that there are 1 ship for size 2, 4, 5 and 2 size 3 ships
def sizes():
    e = Encoding()
    length_constraint = []
    for ship in fleet:
        # Makes sure that there is on 1 size for each ship
        e.add_constraint((ship.size2 & ~ship.size3 & ~ship.size4)
                         | (~ship.size2 & ship.size3 & ~ship.size4)
                         | (~ship.size2 & ~ship.size3 & ship.size4))
    e.add_constraint(((s1.size2 & ~s2.size2 & ~s3.size2)
                      | (~s1.size2 & s2.size2 & ~s3.size2)
                      | (~s1.size2 & ~s2.size2 & s3.size2))
                     & ((s1.size3 & ~s2.size3 & ~s3.size3)
                        | (~s1.size3 & s2.size3 & ~s3.size3)
                        | (~s1.size3 & ~s2.size3 & s3.size3))
                     & ((s1.size4 & ~s2.size4 & ~s3.size4)
                        | (~s1.size4 & s2.size4 & ~s3.size4)
                        | (~s1.size4 & ~s2.size4 & s3.size4)))
    return e

# Determines orientation of ship
def orientation():
    e = Encoding()
    for ship in fleet:
        e.add_constraint((ship.vertical & ~ship.horizontal) | (ship.horizontal & ~ship.vertical))
        for i in range(1,size + 1):
            for j in range(size,size + 1):
                e.add_constraint(ship.horizontal | ~ship.startPosition[(i,j)])
        for i in range(size,size + 1):
            for j in range(1,size + 1):
                e.add_constraint(ship.vertical | ~ship.startPosition[(i,j)])
        for i in range(1,size + 1):
            for j in range(size - 1,size):
                e.add_constraint((~ship.horizontal & (ship.size3 | ship.size4)).negate() | ~ship.startPosition[(i,j)])
        for i in range(size - 1,size):
            for j in range(1,size + 1):
                e.add_constraint((~ship.vertical & (ship.size3 | ship.size4)).negate() | ~ship.startPosition[(i,j)])
        for i in range(1,size + 1):
            for j in range(size - 2,size - 1):
                e.add_constraint((~ship.horizontal & ship.size4).negate() | ~ship.startPosition[(i,j)])
        for i in range(size - 2,size - 1):
            for j in range(1,size + 1):
                e.add_constraint((~ship.vertical & ship.size4).negate() | ~ship.startPosition[(i,j)])
        e.add_constraint(nnf.Or(startingSquareHelper(ship)))
    return e

# An example of a future extension
def maxBasedOnShipPlacement():
    e = Encoding()
    # based on ships placement,The goal is to sink the ship (which has already been hit once) with a minimal number of misses.
    # ship S is given and can only be translated in grid then know, the coordinates of one grid cell of the ship.
    #in decision tree,  the set of possible positions at the root is P = S and P gets smaller at each new shot until
    #it is reduced to a singleton at the leaves of the tree.
    # If x is a hit, then the set of possible positions for the child becomes P ← P ∩ (S − x).
    #If x is a miss, then the set of possible positions for the child becomes P ← P \ (S − x).


    #Here are some examples of ways possible ship locations can be eliminated:
    #A 'miss' square disqualifies a bunch of intersecting locations.
    #A square where a ship has been marked 'sunk' disqualifies any other ships from crossing that square.
    #A ship that's been sunk has to cross the square where it was sunk.
    #Sunk ships cannot cross any square that is not a 'hit'.
    #Ships that are not sunk can't be located entirely on 'hit' squares.
    #If a certain spot on the board could only hold one certain ship, no other ships can cross any of those squares.
    #If a 'hit' square is surrounded by misses in 3 directions, there must be a ship pointing in the fourth direction.

    #optimized:
    #A list of 'hit' squares is used to check the configurations against, rather than going through all 100 squares each time.
    #saves the 5 ship locations for that configuration. Then, the ship location frequencies are used to calculate the squares' hit frequencies all in one go.
    #If any ship's location can be deduced, it gets removed from process

    #e.add_constraint()
    return e

def check_ship_spacing(ship1,ship2):
    # Full function should return false if ship1 is touching or on top of ship2
    # Unsure on how to check for or compare positions with location and orientation being boolean values
    # Initial thought is to check to see if each ship is true in the same spaces on the board
    # Any feedback on how to implement this would be greatly appreciated!
    return True


# Encoding just used to combine the other encoding and their respective constraints and was used for debugging the interactions between 2 or more constraints
def finalEncoding():
    final = Encoding()
    for E in [orientation(), sizes(), allFinalPositions(), noOverlap()]:
        for constraint in E.constraints:
            final.add_constraint(constraint)
    return final

# constraint to check if each ship is correctly placed
# function could be repeated for each ship (s1-s5)
# an example is located in D5 (documentation ppt - slide 5), we are
# having issues dealing with position and orientation variables as Var
# would appreciate feedback
"""
def isShipWithinBoard():
    e = Encoding()
    # based on ships placement, what is the max available hits a player can make
    # i.e. all water area
    # i.e. all ships area
    # i.e.
    e.add_constraint()

    return e
"""


if __name__ == "__main__":

    print("\n Grid size=", size)
    print("\n Ships count=", len(fleet))
    for i in range (1,(len(fleet)+1)):
        print ("\n Ship #"+str(i)+": size"+str(i+1))

    start = time.perf_counter()

    N = noOverlap()
    Si = sizes()
    F = finalEncoding()
    # T = test_encode()
    Fp = allFinalPositions()

    '''
    print("\nSatisfiable: %s" % N.is_satisfiable())
    print("# Solutions: %d" % N.count_solutions())
    print("   Solution: %s" % N.solve())
    '''
    '''
    print("\nSatisfiable: %s" % Si.is_satisfiable())
    print("# Solutions: %d" % Si.count_solutions())
    print("   Solution: %s" % Si.solve())
    '''
    """
    print("\nSatisfiable: %s" % S.is_satisfiable())
    print("# Solutions: %d" % S.count_solutions())
    print("   Solution: %s" % S.solve())
    """

    """
    print("\nSatisfiable: %s" % T.is_satisfiable())
    # print("# Solutions: %d" % F.count_solutions())
    print("   Solution: %s" % T.solve())
    """
    """
    print("\nSatisfiable: %s" % F.is_satisfiable())
    # print("# Solutions: %d" % F.count_solutions())
    print("   Solution: %s" % F.solve())
    """
    grid_positions = "%s" % F.solve()
    grid = ast.literal_eval(grid_positions)
    sorted_positions = sorted(grid.items())
    print(sorted_positions)
    sorted_squares = sorted_positions[:64]
    sorted_values = []
    for i in range(len(sorted_squares)):
        sorted_values.append(sorted_squares[i][1])
    final_grid = [sorted_values[r*8:(r+1)*8] for r in range(0,8)]
    final_grid = [[final_grid[j][i] for j in range(len(final_grid))] for i in range(len(final_grid[0]))]
    printGrid(final_grid)
    """
    print("\nSatisfiable: %s" % Fp.is_satisfiable())
    # print("# Solutions: %d" % F.count_solutions())
    print("   Solution: %s" % Fp.solve())
    """

    end = time.perf_counter()
    print(f"\nComputed solution in {end - start:0.4f} seconds")


    """
    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
    """

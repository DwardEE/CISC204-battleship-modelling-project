from nnf import Var
from lib204 import Encoding
import nnf


# Ship objects where properties inside are propositions
class Ship(object):

    # Names and sizes of ships for referencing: Carrier = 5, Battleship = 4, Cruiser = 3, Submarine = 3, Destroyer = 2
    # size param. = size of board
    def __init__(self,size,id):
        self.position = {}
        # Sizes of ship (only one can be true per ship object)
        self.size2 = Var("%d%s" % (id, "size2"))  # Destroyer
        self.size3 = Var("%d%s" % (id, "size3"))  # Cruiser or Submarine
        self.size4 = Var("%d%s" % (id, "size4"))  # Battleship
        self.size5 = Var("%d%s" % (id, "size5"))  # Carrier
        self.horizontal = Var("%d%s" % (id, "horizontal"))  # Horizontal if true, vertical if false
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship on the coordinate's (x, y) position
                self.position[(i + 1,j + 1)] = Var("%d(%d,%d)" % (id, i + 1, j + 1))


# Board object to contain the two boards and their propositions
class Board(object):
    def __init__(self, size):
        """
        # Board for ship placement with the individual squares as variables
        self.ship_board = {}
        # Standardized to 10x10 for now
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship on the coordinate's (x, y) position
                self.ship_board[(i + 1,j + 1)] = Var("(%d,%d)" % (i + 1,j + 1))
        """

        # Board for hit marking with the individual squares as variables
        self.hit_board = {}
        # Standardized to 10x10 for now
        for i in range(size):
            for j in range(size):
                # var for coordinate is true if the (x, y) position is hit
                self.hit_board[(i + 1,j + 1)] = Var("(%d,%d)" % (i + 1,j + 1))


def check_ship_spacing(ship1,ship2):
    # Full function should return false if ship1 is touching or on top of ship2
    # Unsure on how to check for or compare positions with location and orientation being boolean values
    # Initial thought is to check to see if each ship is true in the same spaces on the board
    # Any feedback on how to implement this would be greatly appreciated!
    return True


"""
# Call your variables whatever you want
a = Var('a')
b = Var('b')
c = Var('c')
x = Var('x')
y = Var('y')
z = Var('z')
"""
# size of board (size x size); scalable for debugging and expansion/extension
size = 10
# Initializes a board object of size 10x10 (what we are currently using as a standard for now)
player_board = Board(size)

# Variables for ship
s1 = Ship(size,1)
s2 = Ship(size,2)
s3 = Ship(size,3)
s4 = Ship(size,4)
s5 = Ship(size,5)

# Array if need (e.g. using for loops for a property of the ships)
fleet = [s1,s2,s3,s4,s5]


#
# Build an example full theory for your setting and return it.
#
# There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
# This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

# The constraints are separated for easier debugging

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
                        conjunct_list.append(ship.position[k,l])
                    else:
                        conjunct_list.append(~ship.position[k,l])
            constraint_list.append(nnf.And(conjunct_list))
            conjunct_list = []
    return constraint_list


#  Function to determine the starting square of each ship
def startingSquarePlacement():
    e = Encoding()
    # Each function determines the potential starting square of the given ship.
    e.add_constraint(nnf.Or(startingSquareHelper(s1)))
    e.add_constraint(nnf.Or(startingSquareHelper(s2)))
    e.add_constraint(nnf.Or(startingSquareHelper(s3)))
    e.add_constraint(nnf.Or(startingSquareHelper(s4)))
    e.add_constraint(nnf.Or(startingSquareHelper(s5)))

    """
    at_least_one = nnf.Or([s1.position[i,j] for i in range(1,size + 1) for j in range(1,size + 1)])
    e.add_constraint(at_least_one)
    """
    return e


# Checks to make sure that there are no overlap in position between the ships
def noOverlap():
    e = Encoding()

    for i in range(1,size + 1):
        for j in range(1,size + 1):
            e.add_constraint((s1.position[(i,j)] & ~s2.position[(i,j)] & ~s3.position[(i,j)] & ~s4.position[(i,j)] & ~s5.position[(i,j)])
                        | (~s1.position[(i,j)] & s2.position[(i,j)] & ~s3.position[(i,j)] & ~s4.position[(i,j)] & ~s5.position[(i,j)])
                        | (~s1.position[(i,j)] & ~s2.position[(i,j)] & s3.position[(i,j)] & ~s4.position[(i,j)] & ~s5.position[(i,j)])
                        | (~s1.position[(i,j)] & ~s2.position[(i,j)] & ~s3.position[(i,j)] & s4.position[(i,j)] & ~s5.position[(i,j)])
                        | (~s1.position[(i,j)] & ~s2.position[(i,j)] & ~s3.position[(i,j)] & ~s4.position[(i,j)] & s5.position[(i,j)])
                        | (~s1.position[(i,j)] & ~s2.position[(i,j)] & ~s3.position[(i,j)] & ~s4.position[(i,j)] & ~s5.position[(i,j)]))

    return e

# Makes sure that a ship can only have one size and that there are 1 ship for size 2, 4, 5 and 2 size 3 ships
def sizesAndOrientation():

    e = Encoding()
    length_constraint = []
    for ship in fleet:
        # Makes sure that there is on 1 size for each ship
        e.add_constraint((ship.size2 & ~ship.size3 & ~ship.size4 & ~ship.size5)
                         | (~ship.size2 & ship.size3 & ~ship.size4 & ~ship.size5)
                         | (~ship.size2 & ~ship.size3 & ship.size4 & ~ship.size5)
                         | (~ship.size2 & ~ship.size3 & ~ship.size4 & ship.size5))
    # Makes sure that each size can have only their limited amount of ships (1 2space, 2 3space, 1 4 space, 1 5 space)
    e.add_constraint(((s1.size2 & ~s2.size2 & ~s3.size2 & ~s4.size2 & ~s5.size2)
                     | (~s1.size2 & s2.size2 & ~s3.size2 & ~s4.size2 & ~s5.size2)
                     | (~s1.size2 & ~s2.size2 & s3.size2 & ~s4.size2 & ~s5.size2)
                     | (~s1.size2 & ~s2.size2 & ~s3.size2 & s4.size2 & ~s5.size2)
                     | (~s1.size2 & ~s2.size2 & ~s3.size2 & ~s4.size2 & s5.size2))
                     & ((s1.size4 & ~s2.size4 & ~s3.size4 & ~s4.size4 & ~s5.size4)
                     | (~s1.size4 & s2.size4 & ~s3.size4 & ~s4.size4 & ~s5.size4)
                     | (~s1.size4 & ~s2.size4 & s3.size4 & ~s4.size4 & ~s5.size4)
                     | (~s1.size4 & ~s2.size4 & ~s3.size4 & s4.size4 & ~s5.size4)
                     | (~s1.size4 & ~s2.size4 & ~s3.size4 & ~s4.size4 & s5.size4))
                     & ((s1.size5 & ~s2.size5 & ~s3.size5 & ~s4.size5 & ~s5.size5)
                     | (~s1.size5 & s2.size5 & ~s3.size5 & ~s4.size5 & ~s5.size5)
                     | (~s1.size5 & ~s2.size5 & s3.size5 & ~s4.size5 & ~s5.size5)
                     | (~s1.size5 & ~s2.size5 & ~s3.size5 & s4.size5 & ~s5.size5)
                     | (~s1.size5 & ~s2.size5 & ~s3.size5 & ~s4.size5 & s5.size5)))
    # hoping code would be able to determine orientation and length based on the orientation Var and the supposed starting point Var using implication. Currently computer is unable to compute; code
    # may be too inefficient. Trying to acomplish at least 1 ship. Hopefully code can be added to the starting position encoding to further model proper ship position
    for i in range(1,size):
        for j in range(1,size + 1):
            length_constraint.append(((s1.horizontal & s1.size2 & s1.position[(i, j)]).negate() | s1.position[(i+1, j)]))
    for i in range(1,size + 1):
        for j in range(1,size):
            length_constraint.append(((~s1.horizontal & s1.size2 & s1.position[(i, j)]).negate() | s1.position[(i, j+1)]))
    for i in range(1,size - 1):
        for j in range(1,size + 1):
            length_constraint.append(((s1.horizontal & s1.size3 & s1.position[(i, j)]).negate() | (s1.position[(i+1, j)] & s1.position[(i+2, j)])))
    for i in range(1,size + 1):
        for j in range(1,size - 1):
            length_constraint.append(((~s1.horizontal & s1.size3 & s1.position[(i, j)]).negate() | (s1.position[(i, j+1)] & s1.position[(i, j+2)])))
    for i in range(1,size - 2):
        for j in range(1,size + 1):
            length_constraint.append(((s1.horizontal & s1.size4 & s1.position[(i, j)]).negate() | (s1.position[(i+1, j)] & s1.position[(i+2, j)] & s1.position[(i+3, j)])))
    for i in range(1,size + 1):
        for j in range(1,size - 2):
            length_constraint.append(((~s1.horizontal & s1.size4 & s1.position[(i, j)]).negate() | (s1.position[(i, j+1)] & s1.position[(i, j+2)] & s1.position[(i, j+3)])))
    for i in range(1,size - 3):
        for j in range(1,size + 1):
            length_constraint.append(((s1.horizontal & s1.size5 & s1.position[(i, j)]).negate() | (s1.position[(i + 1, j)] & s1.position[(i + 2, j)] & s1.position[(i + 3, j)] & s1.position[(i+4, j)])))
    for i in range(1,size + 1):
        for j in range(1,size - 3):
            length_constraint.append(((~s1.horizontal & s1.size5 & s1.position[(i, j)]).negate() | (s1.position[(i, j + 1)] & s1.position[(i, j + 2)] & s1.position[(i, j + 3)] & s1.position[(i,j + 4)])))
    e.add_constraint(nnf.And(length_constraint))

    return e

# Determines orientation of ship
def orientation():
    e = Encoding()


    return e

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


# constraints to ensure all ships are located within the board
def areAllShipsWithinBoard():
    e = Encoding()
    # based on ships placements, are all ship pieces within board
    e.add_constraint(s1 & s2 & s3 & s4 & s5)

    return e


# constraint to check if each ship is correctly placed
# function could be repeated for each ship (s1-s5)
# an example is located in D5 (documentation ppt - slide 5), we are
# having issues dealing with position and orientation variables as Var
# would appreciate feedback
def isShipWithinBoard():
    e = Encoding()
    # based on ships placement, what is the max available hits a player can make
    # i.e. all water area
    # i.e. all ships area
    # i.e.
    e.add_constraint()

    return e


def areAllShipsOnBoard():
    e = Encoding()
    # making sure all ships are true

    # Unknown purpose of constraint
    """
    e.add_constraint(s1 & s2 & s3 & s4 & s5)
    """

    #C1 if all ships are present--> true
    #and if all board squares contain ship/ are filled--> true
    #then it is concluded that all the ships are on the board
    for ship in fleet:
        for i in range(1,(size + 1)):
            for j in range(1,(size + 1)):
                C1=(player_board.hit_board[(i,j)] & ship.position[(i,j)])

    #C2 inverse confirmed as well
    # if all ships are NOT present--> true
    #and if all board squares the DO NOT contain ship/ are empty--> true
    #then it is concluded that there are NO ships where the board should be empty

    for ship in fleet:
        for i in range(1,(size + 1)):
            for j in range(1,(size + 1)):
                C2=(~player_board.hit_board[(i,j)] & ~ship.position[(i,j)])

    e.add_constraint(C1 & C2)
    return e



if __name__ == "__main__":
    N = noOverlap()
    O = sizesAndOrientation()
    S = startingSquarePlacement()

    print("\nSatisfiable: %s" % N.is_satisfiable())
    print("# Solutions: %d" % N.count_solutions())
    print("   Solution: %s" % N.solve())

    print("\nSatisfiable: %s" % O.is_satisfiable())
    print("# Solutions: %d" % O.count_solutions())
    print("   Solution: %s" % O.solve())

    print("\nSatisfiable: %s" % S.is_satisfiable())
    print("# Solutions: %d" % S.count_solutions())
    print("   Solution: %s" % S.solve())

    """
    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
    """

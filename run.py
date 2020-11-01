
from nnf import Var
from lib204 import Encoding
import random


class Ship(object):

    # Names and sizes of ships for referencing: Carrier = 5, Battleship = 4, Cruiser = 3, Submarine = 3, Destroyer = 2
    def __init__(self, ship_id, size):
        # Ship id 1 - 5 in order of largest ship to smallest
        # Cruiser ship before Submarine if matters
        self.ship_id = ship_id
        # Size of ship; smallest: 2, largest: 5
        self.size = size
        # Position of most top left piece of ship; tuple for (x, y) coordinates
        # Lowest index 1
        self.position = (random.randint(1, 10), random.randint(1, 10))
        # true = horizontal; false = vertical
        self.orientation = bool(random.getrandbits(1))

    # Setter methods to set positions and orientations after initialization
    # if necessary.
    def set_pos(self, position):
        self.position = position

    def set_or(self, orientation):
        self.orientation = orientation

    def set_ship(self):
        # Maximum position ship can be placed on grid
        max_pos = 10 - (self.size - 1)
        # true = horizontal;
        if self.orientation:
            self.position = (random.randint(1, max_pos), random.randint(1, 10))
        #false = vertical
        else:
            self.position = (random.randint(1, 10), random.randint(1, max_pos))
    
    # I think im hashing it correctly; I'm not too sure -Edward
    def __hash__(self):
        return hash((self.ship_id, self.size, self.position, self.orientation))


class Board(object):

    def __init__(self, size):
        # Board for ship placement with the individual squares as variables
        self.ship_board = {}
        # Standardized to 10x10 for now
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship on the coordinate's (x, y) position
                self.ship_board[(i + 1, j + 1)] = Var("(%d,%d)" % (i + 1, j + 1))

        # Board for hit marking with the individual squares as variables
        self.hit_board = {}
        # Standardized to 10x10 for now
        for i in range(size):
            for j in range(size):
                # var for coordinate is true if the (x, y) position is hit
                self.hit_board[(i + 1, j + 1)] = Var("(%d,%d)" % (i + 1, j + 1))

    def __hash__(self):
        return hash((self.ship_board, self.hit_board))

"""
# Call your variables whatever you want
a = Var('a')
b = Var('b')
c = Var('c')
x = Var('x')
y = Var('y')
z = Var('z')
"""

player_board = Board(10)

# Variables for ship (position and orientation set randomly without considerations of constraints)
s1 = Ship("1", 5)  # Carrier ship
s2 = Ship("2", 4)  # Battleship
s3 = Ship("3", 3)  # Cruiser ship
s4 = Ship("4", 3)  # Submarine
s5 = Ship("5", 2)  # Destroyer Ship

# Array if need (e.g. using for loops for a property of the ships)
fleet = [s1, s2, s3, s4, s5]

# Alternative example of method of declaring propositions without objects
"""
s1 = Var('s1')  # Size of Carrier ship (5 space)
s2 = Var('s2')  # Size of Battleship (4 space)
s3 = Var('s3')  # Size of Cruiser ship (3 space)
s4 = Var('s4')  # Size of Submarine (3 space)    
s5 = Var('s5')  # Size of Destroyer ship (2 space)

p1 = Var('p1')  # placement of most top left part of Carrier ship (5 space)
p2 = Var('s2')  # placement of most top left part of Battleship (5 space)
p3 = Var('s3')  # placement of most top left part of Cruiser ship (5 space)
p4 = Var('s4')  # placement of most top left part of Submarine (5 space)
p5 = Var('s5')  # placement of most top left part of Destroyer ship (5 space)
"""

#
# Build an example full theory for your setting and return it.
#
# There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
# This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.


def example_theory():

    e = Encoding()

    """
    E.add_constraint(a | b)
    E.add_constraint(~a | ~x)
    E.add_constraint(c | y | z)
    """

    return e


if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())
    print(player_board.hit_board)

    """
    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
    """

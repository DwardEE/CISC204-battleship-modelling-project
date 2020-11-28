
from nnf import Var
from lib204 import Encoding
import random


# Ship objects where properties inside are propositions
class Ship(object):

    # Names and sizes of ships for referencing: Carrier = 5, Battleship = 4, Cruiser = 3, Submarine = 3, Destroyer = 2
    # As the properties can just be booleans, I'm not sure how to implement position or size
    def __init__(self, size):
        self.position = {}
        # Sizes of ship (only one can be true per ship object)
        self.size2 = Var("size2")  # Destroyer
        self.size3 = Var("size3")  # Cruiser or Submarine
        self.size4 = Var("size4")  # Battleship
        self.size5 = Var("size5")  # Carrier
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship on the coordinate's (x, y) position
                self.position[(i + 1, j + 1)] = Var("(%d,%d)" % (i + 1, j + 1))


# Board object to contain the two boards and their propositions
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

    """
    def __hash__(self):
        return hash((self.ship_board, self.hit_board))
    """


"""
# Call your variables whatever you want
a = Var('a')
b = Var('b')
c = Var('c')
x = Var('x')
y = Var('y')
z = Var('z')
"""

# Initializes a board object of size 10x10 (what we are currently using as a standard for now)
player_board = Board(10)

# Variables for ship
s1 = Ship(10)  # Carrier ship: Size 5
s2 = Ship(10)  # Battleship: Size 4
s3 = Ship(10)  # Cruiser ship: Size 3
s4 = Ship(10)  # Submarine: Size 3
s5 = Ship(10)  # Destroyer Ship: Size 2

# Array if need (e.g. using for loops for a property of the ships)
fleet = [s1, s2, s3, s4, s5]

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

    for i in range(10):
            e.add_constraint(s1 & s2 & s3 & s4 & s5)


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

from nnf import Var
from lib204 import Encoding
import random


# Ship objects where properties inside are propositions
class Ship(object):

    # Names and sizes of ships for referencing: Carrier = 5, Battleship = 4, Cruiser = 3, Submarine = 3, Destroyer = 2
    # As the properties can just be booleans, I'm not sure how to implement position or size
    def __init__(self):
        # Sizes of ship (only one would be true obviously)
        self.size2 = Var("size2")  # Destroyer
        self.size3 = Var("size3")  # Cruiser or Submarine
        self.size4 = Var("size4")  # Battleship
        self.size5 = Var("size5")  # Carrier

        # Issue with this method is that the Var position couldn't be a coordinate; must be a boolean instead
        # Position of ship (currently the position is the most top-left coordinate).
        self.position = Var("position")
        # true = horizontal; false = vertical (maybe I should change the variable name to horizontal?)
        self.orientation = Var("orientation")

        # Currently unsure how position and orientation should be done
        # One alternative was to make a grid of Vars like in Board where the squares that the ship resides on would be true
        # This alternative would render the ship_board variables in Board as well as the orientation variable here redundant
        """
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship on the coordinate's (x, y) position
                self.position[(i + 1, j + 1)] = Var("(%d,%d)" % (i + 1, j + 1))
        """

    # Setter methods to set positions and orientations after initialization if necessary.
    # Note: The position and orientation parameters should be Var objects
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

    # Not too sure if object has to be hashable anymore
    """
    # I think im hashing it correctly; I'm not following the convention in the example in library tutorial 
    def __hash__(self):
        return hash((self.ship_id, self.size, self.position, self.orientation))
    """


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

def check_ship_spacing(ship1, ship2) :
        #Full function should return false if ship1 is touching or on top of ship2
        #Unsure on how to check for or compare positions with location and orientation being boolean values
        #Initial thought is to check to see if each ship is true in the same spaces on the board
        #Any feedback on how to implement this would be greatly appreciated!
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

# Initializes a board object of size 10x10 (what we are currently using as a standard for now)
player_board = Board(10)


# Variables for ship (position and orientation set randomly without considerations of constraints)
s1 = Ship()  # Carrier ship: Size 5
s2 = Ship()  # Battleship: Size 4
s3 = Ship()  # Cruiser ship: Size 3
s4 = Ship()  # Submarine: Size 3
s5 = Ship()  # Destroyer Ship: Size 2

# Array if need (e.g. using for loops for a property of the ships)
fleet = [s1, s2, s3, s4, s5]

# Alternative example of initializing propositions without self-made objects (may be to troublesome for board grid variables) .
# I don't know if I should keep the proposition variables as is (in objects Board and Ship) or just leave it out of the objects.
# If your group has tried either method, any feedback is appreciated.
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

etc.
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

def maxBasedOnShipPlacement():

    e = Encoding()
    #based on ships placement, what is the max available hits a player can make
    #i.e. all water area
    #i.e. all ships area
    #i.e. 
    E.add_constraint()
    E.add_constraint(~a | ~x)
    E.add_constraint(c | y | z)
    

    return e    

#constraints to ensure all ships are located within the board
def areAllShipsWithinBoard():

    e = Encoding()
    #based on ships placements, are all ship pieces within board
    E.add_constraint(s1 & s2 & s3 & s4 & s5)
    
    return e 

#constraint to check if each ship is correctly placed
#function could be repeated for each ship (s1-s5)
#an example is located in D5 (documentation ppt - slide 5), we are 
#having issues dealing with position and orientation variables as Var
#would appreciate feedback
def isS1WithinBoard():
    
    e = Encoding()
    #based on ships placement, what is the max available hits a player can make
    #i.e. all water area
    #i.e. all ships area
    #i.e. 
    E.add_constraint()
    
    return e 


def areAllShipsOnBoard():

    e = Encoding()
    #making sure all ships are true
    E.add_constraint(s1 & s2 & s3 & s4 & s5)

    #s1=s1.callPostion
    #s1area=

    #[x11,x21
    #x11,x22]
    #=
    #[1,0
    #1,0]
    
    #need to double check that same locations are true on board 
    #s1 & x11 & x12
    E.add_constraint( player_board.ship_board[(1,1)] & s1 )

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

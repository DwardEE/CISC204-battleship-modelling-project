from nnf import Var
from lib204 import Encoding
import ast
import nnf
import time

"""
Battleship

Group 31
Edward Chen: 18etc4
Courtney McNamara: 14cpm3
Samantha Stinson: 15ss190
Ryan Licandro: 18rl50
"""


# Ship objects where properties inside are propositions
class Ship(object):
    """
    Names and sizes of ships for referencing: Battleship = 4, Cruiser = 3, Destroyer = 2 *Note: Names are arbitrary; they do not matter in any scenario
    size param. = size of board that the ship will be on, id param. = ID of instantiated Ship object
    """
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
                # var for coordinate should be true if the starting ship coordinate is at that (x, y) position
                self.startPosition[(i + 1,j + 1)] = Var("%ds(%d,%d)" % (id, i + 1, j + 1))
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if the remainder of the ships's coordinates are at that (x, y) position and the ship is placed horizontally
                self.hInterPosition[(i + 1,j + 1)] = Var("%dh(%d,%d)" % (id, i + 1, j + 1))
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if the remainder of the ships's coordinates are at that (x, y) position and the ship is placed vertically
                self.vInterPosition[(i + 1,j + 1)] = Var("%dv(%d,%d)" % (id, i + 1, j + 1))
        for i in range(size):
            for j in range(size):
                # var for coordinate should be true if there is a ship part on the coordinate's (x, y) position
                self.position[(i + 1,j + 1)] = Var("(%d,%d)" % (i + 1, j + 1))



class Board(object):
    # Board object to contain the two boards and their propositions
    def __init__(self, size):
        # Player board standardized to 6x6 for now due to computing limitations
        # May be used for any encoding assessing hits
        self.hit_board = {}
        for i in range(size):
            for j in range(size):
                # var for coordinate is true if the (x, y) position is hit
                self.hit_board[(i + 1,j + 1)] = Var("(%d,%d)" % (i + 1,j + 1))


# Prints grid
def printGrid(grid_data):
    # Axis for the y-side
    alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    print("  ", end=' ')
    # prints the x axis
    for i in range(size):
        if i != size:
            print(str(i + 1) + " ", end='')
        else:
            print(i + 1, end=' ')
    print("")
    # prints the y axis with the results of the corresponding grid
    for i in range(size):
        print(alpha[i] + " ", end=' ')
        for j in range(size):
            if grid_data[i][j]:
                print("O", end=' ')
            else:
                print("-", end=' ')
        print("")


# Size of board (size x size); scalable for debugging and expansion/extension or to avoid computation issues
# Size can be changed if you want to test out the possibility with different boards
size = 6  # Scalable
win_con = Var("playerWins")

# Initializes a board object; param size = size of board
player_board = Board(size)

# Variables for ship (size of ship, id); the application of 5 ships may be implemented by their instantiation and tweaking to the code.
s1 = Ship(size,1)
s2 = Ship(size,2)
s3 = Ship(size,3)

# Array if need (e.g. using for loops for a property of the ships)
fleet = [s1,s2,s3]



def winCondition():
    """
    Simple encoding to see if all ship coordinates are hit
    """
    e = Encoding()
    # List to hold conjunctions
    win = []
    # Checks to see if all ship parts are hit, win_con is true if all are hit, false otherwise
    for i in range(1,size + 1):
        for j in range(1,size + 1):
            win.append((s1.position[(i,j)] & player_board.hit_board[(i,j)]))
    e.add_constraint(nnf.And(win).negate() | win_con)
    e.add_constraint(nnf.And(win) | ~win_con)
    return e


def startingSquareHelper(ship):
    """
    Helper function that makes sure that the specified ship may only exist on one square. Returns a list of constraints
    specific for each ship which will be added as a constraint of disjunctions in the main starting square function.
    """
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


def allFinalPositions():
    """
    This encoding see where to place the remaining ship parts given the propositions size, orientation, and starting position
    There are two "boards" per ship. One to place the remaining squares horizontally, and one for vertical placement. With
    these boards completed, the final board can be obtained by "superimposing" all the ships' boards on one another, or in the
    case of propositional logic, this would be equivalent to checking the disjunction between all boards for a specific position
    to see if any of them are true; if so, there is a ship piece of some ship in that position and the "final board" position will
    return true as well.
    """
    e = Encoding()
    # List for placement conjunctions
    placements = []
    # Utilizes the startingSquare helper function in order to limit the starting location to one square
    e.add_constraint(nnf.Or(startingSquareHelper(s1)))
    # Iterates through the three ships checking to see if a square would have a ship part on it
    for ship in fleet:
        # As the minimum to starting square may be is at the first row or column, there cannot be any intermediate spaces in the first row or column for vInterPosition and hInterPosition respectively.
        for i in range(1, size + 1):
            e.add_constraint(~ship.vInterPosition[(i,1)])
            e.add_constraint(~ship.hInterPosition[(1,i)])
        # Used to check if the second column has a ship part that belongs to a ship of size 2
        for i in range(2, 3):
            for j in range(1, size + 1):
                e.add_constraint(((ship.horizontal & ship.startPosition[(i-1,j)]) | ~ship.hInterPosition[(i,j)]))
                e.add_constraint(((ship.horizontal & ship.startPosition[(i - 1,j)]).negate() | ship.hInterPosition[(i,j)]))
        # Used to check if the third column has a ship part that belongs to a ship of size 2 or size 3
        for i in range(3, 4):
            for j in range(1, size + 1):
                e.add_constraint((((ship.horizontal & ship.startPosition[(i - 2,j)] & ~ship.size2) | (ship.horizontal & ship.startPosition[(i - 1,j)])) | ~ship.hInterPosition[(i,j)]))
                e.add_constraint((((ship.horizontal & ship.startPosition[(i - 2,j)] & ~ship.size2) | (ship.horizontal & ship.startPosition[(i - 1,j)])).negate() | ship.hInterPosition[(i,j)]))
        # Used to check if the third column has a ship part that belongs to a ship of size 2 or size 3 or size 4
        for i in range(4, size + 1):
            for j in range(1, size + 1):
                e.add_constraint((((ship.horizontal & ship.startPosition[(i-3,j)] & ship.size4) | (ship.horizontal & ship.startPosition[(i-2,j)] & ~ship.size2) | (ship.horizontal &
                ship.startPosition[(i-1, j)])) | ~ship.hInterPosition[(i, j)]))
                e.add_constraint((((ship.horizontal & ship.startPosition[(i - 3,j)] & ship.size4) | (ship.horizontal & ship.startPosition[(i - 2,j)] & ~ship.size2) | (ship.horizontal &
                ship.startPosition[(i - 1,j)])).negate() | ship.hInterPosition[(i,j)]))
        # Used to check if the second row has a ship part that belongs to a ship of size 2
        for i in range(1, size + 1):
            for j in range(2, 3):
                e.add_constraint(((ship.vertical & ship.startPosition[(i,j-1)]) | ~ship.vInterPosition[(i,j)]))
                e.add_constraint(((ship.vertical & ship.startPosition[(i,j - 1)]).negate() | ship.vInterPosition[(i,j)]))
        # Used to check if the second row has a ship part that belongs to a ship of size 2 or size 3
        for i in range(1, size + 1):
            for j in range(3, 4):
                e.add_constraint((((ship.vertical & ship.startPosition[(i,j-2)] & ~ship.size2) | (ship.vertical & ship.startPosition[(i,j-1)])) | ~ship.vInterPosition[(i,j)]))
                e.add_constraint((((ship.vertical & ship.startPosition[(i,j - 2)] & ~ship.size2) | (ship.vertical & ship.startPosition[(i,j - 1)])).negate() | ship.vInterPosition[(i,j)]))
        # Used to check if the second row has a ship part that belongs to a ship of size 2 or size 3 or size 4
        for i in range(1, size + 1):
            for j in range(4, size + 1):
                e.add_constraint((((ship.vertical & ship.startPosition[(i,j-3)] & ship.size4) | (ship.vertical & ship.startPosition[(i,j-2)] & ~ship.size2) | (ship.vertical &
                ship.startPosition[(i, j-1)])) | ~ship.vInterPosition[(i, j)]))
                e.add_constraint((((ship.vertical & ship.startPosition[(i,j - 3)] & ship.size4) | (ship.vertical & ship.startPosition[(i,j - 2)] & ~ship.size2) | (ship.vertical &
                ship.startPosition[(i,j - 1)])).negate() | ship.vInterPosition[(i,j)]))
        # Generation of the final board
        for i in range(1,size + 1):
            for j in range(1,size + 1):
                # Appends the Var of all boards for this specific position
                for ship in fleet:
                    placements.append(ship.startPosition[(i,j)])
                    placements.append(ship.hInterPosition[(i,j)])
                    placements.append(ship.vInterPosition[(i,j)])
                # If none of the Var for the specific position on the board is true, then the position of the final board will be false.
                e.add_constraint((nnf.Or(placements)) | ~s1.position[(i,j)])
                placements = []
        # Loops through the same
        for i in range(1,size + 1):
            for j in range(1,size + 1):
                for ship in fleet:
                    placements.append(ship.startPosition[(i,j)])
                    placements.append(ship.hInterPosition[(i,j)])
                    placements.append(ship.vInterPosition[(i,j)])
                # If any one of the Var for the specific position on the board is true, then the position of the final board will be true as well.
                e.add_constraint((nnf.Or(placements)).negate() | s1.position[(i,j)])
                placements = []


    return e


def noOverlap():
    """
    Encoding that makes sure sees that the starting positions do not overlap. However, unfortunately, the ships may still overlap for all of positions,
    with given more time to implement and compute these constraints, as an extension, to have no overlap between the ships as well as the ability to judge
    spacing may be implemented as well.
    """
    e = Encoding()
    # Following loops through all start positions to make sure that one one start position occupies a single coordinate.
    for i in range(1,size + 1):
        for j in range(1,size + 1):
            e.add_constraint((s1.startPosition[(i,j)] & ~s2.startPosition[(i,j)] & ~s3.startPosition[(i,j)])
                             | (~s1.startPosition[(i,j)] & s2.startPosition[(i,j)] & ~s3.startPosition[(i,j)])
                             | (~s1.startPosition[(i,j)] & ~s2.startPosition[(i,j)] & s3.startPosition[(i,j)])
                             | (~s1.startPosition[(i,j)] & ~s2.startPosition[(i,j)] & ~s3.startPosition[(i,j)]))

    return e
"""
#Makes sure that a ship can only have one size and that there are 1 ship for size 2, 4, 5 and 2 size 3 ships
"""
def sizes():
    e = Encoding()
    # Makes sure that there is on 1 size for each ship
    for ship in fleet:
        e.add_constraint((ship.size2 & ~ship.size3 & ~ship.size4)
                         | (~ship.size2 & ship.size3 & ~ship.size4)
                         | (~ship.size2 & ~ship.size3 & ship.size4))
    # Makes sure that for each size, only one ship may have it (i.e only 1 ship may be of size 2, one ship of size 3, and one ship of size 4)
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



def orientation():
    """
    This encoding constrains the possible starting positions and orientations based on the sizes as this makes sure that
    that they are valid, constraining the ships to the board for once the rest of the pieces are "placed". The orientations
    are horizontal or vertical. The remainder of the ship parts will be places to the right if the orientation is horizontal
    and downwards if the orientation is vertical.
    """
    e = Encoding()
    for ship in fleet:
        # Each ship is assigned a random orientation
        e.add_constraint((ship.vertical & ~ship.horizontal) | (ship.horizontal & ~ship.vertical))
        # Loop constrains the ship to not be vertical when starting position is against the bottom side of the board
        for i in range(1,size + 1):
            for j in range(size,size + 1):
                e.add_constraint(ship.horizontal | ~ship.startPosition[(i,j)])
        # Loop constrains the ship to not be horizontal when starting position is against the right side of the board
        for i in range(size,size + 1):
            for j in range(1,size + 1):
                e.add_constraint(ship.vertical | ~ship.startPosition[(i,j)])
        # Loop constrains ship to not be vertical when starting position of size 3 or 4 is at the second column from the bottom
        for i in range(1,size + 1):
            for j in range(size - 1,size):
                e.add_constraint((~ship.horizontal & (ship.size3 | ship.size4)).negate() | ~ship.startPosition[(i,j)])
        # Loop constrains ship to not be horizontal when starting position of size 3 or 4 is at the second column from the right
        for i in range(size - 1,size):
            for j in range(1,size + 1):
                e.add_constraint((~ship.vertical & (ship.size3 | ship.size4)).negate() | ~ship.startPosition[(i,j)])
        # Loop constrains ship to not be vertical when starting position of size 4 is at the third column from the bottom
        for i in range(1,size + 1):
            for j in range(size - 2,size - 1):
                e.add_constraint((~ship.horizontal & ship.size4).negate() | ~ship.startPosition[(i,j)])
        # Loop constrains ship to not be horizontal when starting position of size 4 is at the third column from the right
        for i in range(size - 2,size - 1):
            for j in range(1,size + 1):
                e.add_constraint((~ship.vertical & ship.size4).negate() | ~ship.startPosition[(i,j)])
        # Adds the constraint to only select one coordinate from the valid positions to be the starting position
        e.add_constraint(nnf.Or(startingSquareHelper(ship)))
    return e


# An example of a future extension
def maxBasedOnShipPlacement():
    e = Encoding()
    """
    based on ships placement,The goal is to sink the ship (which has already been hit once) with a minimal number of misses.
    ship S is given and can only be translated in grid then know, the coordinates of one grid cell of the ship.
    in decision tree,  the set of possible positions at the root is P = S and P gets smaller at each new shot until
    it is reduced to a singleton at the leaves of the tree.
    If x is a hit, then the set of possible positions for the child becomes P ← P ∩ (S − x).
    If x is a miss, then the set of possible positions for the child becomes P ← P \ (S − x).


    Here are some examples of ways possible ship locations can be eliminated:
    A 'miss' square disqualifies a bunch of intersecting locations.
    A square where a ship has been marked 'sunk' disqualifies any other ships from crossing that square.
    A ship that's been sunk has to cross the square where it was sunk.
    Sunk ships cannot cross any square that is not a 'hit'.
    Ships that are not sunk can't be located entirely on 'hit' squares.
    If a certain spot on the board could only hold one certain ship, no other ships can cross any of those squares.
    If a 'hit' square is surrounded by misses in 3 directions, there must be a ship pointing in the fourth direction.

    optimized:
    A list of 'hit' squares is used to check the configurations against, rather than going through all 100 squares each time.
    saves the 5 ship locations for that configuration. Then, the ship location frequencies are used to calculate the squares' hit frequencies all in one go.
    If any ship's location can be deduced, it gets removed from process

    e.add_constraint()
    """
    return e


# Encoding used to combine the other encoding and their respective constraints and was used for debugging the interactions between 2 or more constraints
def finalEncoding():
    final = Encoding()
    # Combines all the encoding and their respective constraints
    for E in [orientation(), sizes(), allFinalPositions(), noOverlap()]:
        for constraint in E.constraints:
            final.add_constraint(constraint)
    return final


# Main function; certain functions are commented out and can be uncommented to test encodings individually
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
    print("# Solutions: %d" % F.count_solutions())
    print("   Solution: %s" % F.solve())
    """

    # The following code sorts the output for a possible solution and retrieves the corresponding final board and converts to a size*size 2D array.
    grid_positions = "%s" % F.solve()
    grid = ast.literal_eval(grid_positions)
    sorted_positions = sorted(grid.items())
    print(sorted_positions)
    sorted_squares = sorted_positions[:(size*size)]
    sorted_values = []
    for i in range(len(sorted_squares)):
        sorted_values.append(sorted_squares[i][1])
    final_grid = [sorted_values[r*size:(r+1)*size] for r in range(0,size)]
    final_grid = [[final_grid[j][i] for j in range(len(final_grid))] for i in range(len(final_grid[0]))]
    # Grid and all encodings are adapted to size changes. the grid will print solutions up to 10x10 only because that is how
    # many letters are in the array in print grid function but more can be added.
    printGrid(final_grid)

    """
    print("\nSatisfiable: %s" % Fp.is_satisfiable())
    # print("# Solutions: %d" % F.count_solutions())
    print("   Solution: %s" % Fp.solve())
    """
    # Returns the amount of time to compute everything
    end = time.perf_counter()
    print(f"\nComputed solution in {end - start:0.4f} seconds")


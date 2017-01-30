"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui


class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][
                    zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][
                    zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][
                    zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][
                    zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # check condition 1: Tile zero is positioned at (i, j)
        if self.current_position(0, 0) != (target_row, target_col):
            return False

        # check condition 2: All tiles in rows i + 1 or below are
        # positioned at their solved location
        if not self._solved_below(target_row, target_col):
            return False

        # check condition 3: All tiles in row i to the right of position (i, j) are
        # positioned at their solved location
        if not self._solved_right(target_row, target_col):
            return False

        # return true otherwise (conditions met)
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # check input
        assert self.lower_row_invariant(target_row, target_col)

        # init
        result = ""

        # debug
        # zero_row, zero_col = self.current_position(0, 0)
        # target_tile_row, target_tile_col = self.current_position(target_row, target_col)
        # print "zero pos, target pos 1:", (zero_row, zero_col), (target_tile_row, target_tile_col)

        # solution strategy 1-2: move the zero tile up and across to the target tile
        result += self._zero_to_target(target_row, target_col)

        # solution strategy 2-2: move target tile back to target position

        # init
        zero_row, zero_col = self.current_position(0, 0)
        target_tile_row, target_tile_col = self.current_position(target_row,
                                                                 target_col)
        # print "zero pos, target pos 2:", (zero_row, zero_col), (target_tile_row, target_tile_col)

        # print "zero pos, target pos:", (zero_row, zero_col), (target_tile_row, target_tile_col)

        # push target_tile left
        result += self._move_target_left(target_row, target_col)

        # push target_tile right
        result += self._move_target_right(target_row, target_col)

        # push target_tile down
        result += self._move_target_down(target_row, target_col)

        # update current position of zero tile and target_tile
        zero_row, dummy_zero_col = self.current_position(0, 0)
        target_tile_row, target_tile_col = self.current_position(target_row,
                                                                 target_col)

        # if zero above target, move zero left of target
        zero_row, zero_col = self.current_position(0, 0)
        target_tile_row, target_tile_col = self.current_position(target_row,
                                                                 target_col)
        if zero_row == (target_tile_row - 1) and zero_col == target_tile_col:
            self.update_puzzle("ld")
            result += "ld"

            # check output
        assert self.lower_row_invariant(target_row, target_col - 1)

        return result

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # init
        result = ""

        # input check
        assert self.lower_row_invariant(target_row, 0)

        # step 1a: move zero tile to target_tile
        result += self._zero_to_target(target_row, 0)

        # step 1b: move target tile to (i-1, 1) and zero tile to (i-1, 0)
        zero_row, zero_col = self.current_position(0, 0)
        target_tile_row, target_tile_col = self.current_position(target_row, 0)

        # target_tile not already in place
        if not (target_tile_row == target_row and target_tile_col == 0):

            # move target tile to (i-1, 1) and zero tile to (i-1, 0)
            while not (
                            target_tile_row == target_row - 1 and target_tile_col == 1 and zero_row == target_row - 1 and zero_col == 0):

                # move zero tile left of target_tile

                # zero_tile right of target_tile and both in top row
                if zero_row == target_tile_row and zero_col == target_tile_col + 1 and zero_row == 0 and target_tile_row == 0:
                    self.update_puzzle("dllu")
                    result += "dllu"

                    # zero_tile right of target_tile and both not in top row
                elif zero_row == target_tile_row and zero_col == target_tile_col + 1 and zero_row > 0 and target_tile_row > 0:
                    self.update_puzzle("ulld")
                    result += "ulld"

                # zero_tile above target_tile
                elif zero_row == target_tile_row - 1 and zero_col == target_tile_col:
                    self.update_puzzle("rdl")
                    result += "rdl"

                    # update target_tile
                target_tile_row, target_tile_col = self.current_position(
                    target_row, 0)
                zero_row, zero_col = self.current_position(0, 0)

                # bring target_tile down in cyclic moves
                if target_tile_row < target_row - 1:
                    self.update_puzzle("druld")
                    result += "druld"

                # bring target_tile left in cyclic moves
                if target_tile_col > 1:
                    self.update_puzzle("rulld")
                    result += "rulld"

                # update target_tile
                target_tile_row, target_tile_col = self.current_position(
                    target_row, 0)
                zero_row, zero_col = self.current_position(0, 0)

                # end position: zero_tile left of target_tile

        # step 2: apply move string of 3x2 puzzle, described in homework 9
        if not (target_tile_row == target_row and target_tile_col == 0):
            self.update_puzzle("ruldrdlurdluurddlur")
            result += "ruldrdlurdluurddlur"

        # step3: move zero to right end of row i - 1
        zero_row, zero_col = self.current_position(0, 0)
        while zero_col < (self.get_width() - 1):
            self.update_puzzle("r")
            result += "r"
            zero_row, zero_col = self.current_position(0, 0)

        # output check
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)

        # return string path
        return result

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check 1: zero at (0, j)
        zero_row, zero_col = self.current_position(0, 0)
        if not (zero_row == 0 and zero_col == target_col):
            return False

        # check2a: positions below and to right of (1, j) solved
        if not (self._solved_below(1, target_col) and self._solved_right(1,
                                                                         target_col)):
            return False

        # check 2b: check if solved at position (1, j)
        if not self._solved_at(1, target_col):
            return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check 1: zero at (1, j)
        zero_row, zero_col = self.current_position(0, 0)
        if not (zero_row == 1 and zero_col == target_col):
            return False

        # check2: positions below or to right are solved
        if not self.lower_row_invariant(1, target_col):
            return False

        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # input check
        assert self.row0_invariant(target_col)

        # init
        result = ""

        # move zero from (0,j) to (1,j-1) using 'ld'
        self.update_puzzle("ld")
        result += "ld"

        # if target tile is at (0,j), assert and return result
        # if not, reposition target tile to (1,j-1) and zero to (1,j-2)
        target_tile_row, target_tile_col = self.current_position(0, target_col)
        zero_row, zero_col = self.current_position(0, 0)

        if not (target_tile_row == 0 and target_tile_col == target_col):

            # move zero to target, end position: zero is left of target
            result += self._zero_to_target(0, target_col)

            # reposition zero left of target
            target_tile_row, target_tile_col = self.current_position(0,
                                                                     target_col)
            zero_row, zero_col = self.current_position(0, 0)
            if zero_row == (
                target_tile_row - 1) and zero_col == target_tile_col:  # zero above target
                self.update_puzzle("ld")
                result += "ld"

                # move target down to row 1
            target_tile_row, target_tile_col = self.current_position(0,
                                                                     target_col)
            if target_tile_row < 1:
                result += self._move_target_down_to(1, 0, target_col)

            # move target right to j-1
            target_tile_row, target_tile_col = self.current_position(0,
                                                                     target_col)
            if target_tile_col < target_col - 1:
                result += self._move_target_right_to(target_col - 1, 0,
                                                     target_col)

            # move zero to (1,j-2)
            zero_row, zero_col = self.current_position(0, 0)
            if not (zero_row == 1 and zero_col == target_col - 2):
                pass

            # apply move string from homework question 10
            self.update_puzzle("urdlurrdluldrruld")
            result += "urdlurrdluldrruld"

        # output check
        assert self.row1_invariant(target_col - 1)

        return result

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # input check
        assert self.row1_invariant(target_col)

        # init
        result = ""

        # move zero to target_tile position
        result += self._zero_to_target(1, target_col)

        # move target_tile to target position
        result += self._move_target_down(1, target_col)
        result += self._move_target_right(1, target_col)

        # move zero above target_tile, if not already there
        zero_row, zero_col = self.current_position(0, 0)
        target_tile_row, target_tile_col = self.current_position(1, target_col)
        if not (
                zero_row == target_tile_row - 1 and zero_col == target_tile_col):
            self.update_puzzle("ur")
            result += "ur"

        # output check
        assert self.row0_invariant(target_col)

        return result

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # input check. tile zero is at (1,1)
        assert self.row1_invariant(1)

        # init
        result = ""
        count = 0

        # move zero to (0,0)
        self.update_puzzle("lu")
        result += "lu"

        while not self._solved_2x2():
            self.update_puzzle("rdlu")
            result += "rdlu"
            count += 1
            if count == 3:
                break

        assert self._solved_2x2()

        return result

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """

        # init
        result = ""
        width = self.get_width()
        height = self.get_height()

        # bring zero to last tile
        result += self._zero_to_end()
        zero_row, zero_col = self.current_position(0, 0)

        if width == 2 and height == 2:
            result += self.solve_2x2()
        else:
            while True:
                if zero_row > 1 and zero_col > 0:
                    # print '1'
                    result += self.solve_interior_tile(zero_row, zero_col)
                    zero_row, zero_col = self.current_position(0, 0)
                if zero_row > 1 and zero_col == 0:
                    # print '2'
                    result += self.solve_col0_tile(zero_row)
                    zero_row, zero_col = self.current_position(0, 0)
                if zero_row == 1 and zero_col > 1:
                    # print '3'
                    result += self.solve_row1_tile(zero_col)
                    zero_row, zero_col = self.current_position(0, 0)
                if zero_row == 0 and zero_col > 1:
                    # print '4'
                    result += self.solve_row0_tile(zero_col)
                    zero_row, zero_col = self.current_position(0, 0)
                if zero_row < 2 and zero_col < 2:
                    break

            result += self.solve_2x2()
        return result

    ###########################################################
    # helper functions

    def _solved_below(self, target_row, target_col):
        """
        helper function. checks if puzzle is solved below target_row
        """
        height = self.get_height()
        width = self.get_width()
        solved_puzzle = Puzzle(height, width)
        if target_row + 1 <= height - 1:
            for row_index in range(target_row + 1, height):
                for col_index in range(width):
                    if solved_puzzle.get_number(row_index,
                                                col_index) != self.get_number(
                            row_index, col_index):
                        return False
        return True

    def _solved_right(self, target_row, target_col):
        """
        helper function. checks if puzzle is solved to the right of target_col
        """
        height = self.get_height()
        width = self.get_width()
        solved_puzzle = Puzzle(height, width)
        if target_col + 1 <= width - 1:
            for col_index in range(target_col + 1, width):
                if solved_puzzle.get_number(target_row,
                                            col_index) != self.get_number(
                        target_row, col_index):
                    return False
        return True

    def _solved_at(self, target_row, target_col):
        """
        helper function. checks if puzzle is solved at target position
        """
        height = self.get_height()
        width = self.get_width()
        solved_puzzle = Puzzle(height, width)
        if solved_puzzle.get_number(target_row, target_col) == self.get_number(
                target_row, target_col):
            return True
        else:
            return False

    def _zero_to_target(self, target_row, target_col):
        """
        helper function. moves zero tile to position of target_tile
        end position: zero left of target
        """
        result = ""
        target_tile_row, target_tile_col = self.current_position(target_row,
                                                                 target_col)
        zero_row, zero_col = self.current_position(0, 0)

        while not (
                zero_row == target_tile_row and zero_col == target_tile_col):
            # move up or down
            if zero_row > target_tile_row:
                self.update_puzzle("u")
                result += "u"
            elif zero_row < target_tile_row:
                self.update_puzzle("d")
                result += "d"

            # move left or right
            if zero_col > target_tile_col:
                self.update_puzzle("l")
                result += "l"
            elif zero_col < target_tile_col:
                self.update_puzzle("r")
                result += "r"

            # update current position of zero
            zero_row, zero_col = self.current_position(0, 0)

        # position zero left of target
        zero_row, zero_col = self.current_position(0, 0)
        target_tile_row, target_tile_col = self.current_position(target_row,
                                                                 target_col)

        # target not already in place
        if not (
                target_tile_row == target_row and target_tile_col == target_col):

            # zero above target
            if zero_row == target_tile_row - 1 and zero_col == target_tile_col:
                if zero_col == 0:
                    self.update_puzzle("rdl")
                    result += "rdl"
                else:
                    self.update_puzzle("ld")
                    result += "ld"

            # zero right of target
            elif zero_row == target_tile_row and zero_col == target_tile_col + 1:
                self.update_puzzle("l")
                result += "l"

        return result

    def _move_target_down(self, target_row, target_col):
        """
        moves target_tile down until target_row is reached
        start and end position of zero left of target tile
        """
        result = ""
        target_tile_row, dummy_target_tile_col = self.current_position(
            target_row, target_col)
        while not (target_tile_row == target_row):
            self.update_puzzle("druld")
            result += "druld"
            target_tile_row, dummy_target_tile_col = self.current_position(
                target_row, target_col)
        return result

    def _move_target_right(self, target_row, target_col):
        """
        moves target_tile right until target_col is reached
        start and end position of zero left of target tile
        """
        result = ""
        target_tile_row, target_tile_col = self.current_position(target_row,
                                                                 target_col)
        while not target_tile_col == target_col:
            if target_tile_row == 0:
                self.update_puzzle("drrul")
                result += "drrul"
            else:
                self.update_puzzle("urrdl")
                result += "urrdl"
            target_tile_row, target_tile_col = self.current_position(
                target_row, target_col)
        return result

    def _move_target_left(self, target_row, target_col):
        """
        moves target tile left
        zero tile starts and ends left of target
        """

        # init
        result = ""
        zero_row, dummy_zero_col = self.current_position(0, 0)
        dummy_target_tile_row, target_tile_col = self.current_position(
            target_row, target_col)

        while target_tile_col > target_col:

            if zero_row > 0:
                self.update_puzzle("rulld")
                result += "ldrul"
            elif zero_row == 0:
                self.update_puzzle("rdllu")
                result += "rdllu"

            # update current position of zero tile and target_tile
            zero_row, dummy_zero_col = self.current_position(0, 0)
            dummy_target_tile_row, target_tile_col = self.current_position(
                target_row, target_col)

        return result

    def _solved_2x2(self):
        """
        checks if 2x2 puzzle is solved
        """
        if self.get_number(0, 0) == 0 and self.get_number(0,
                                                          1) == 1 and self.get_number(
                1, 0) == self.get_width() and self.get_number(1, 1) == (
            self.get_width() + 1):
            return True
        return False

    def _move_target_down_to(self, specified_row, target_row, target_col):
        """
        moves target_tile down until specified_row is reached
        start and end position of zero left of target tile
        """
        result = ""
        target_tile_row, dummy_target_tile_col = self.current_position(
            target_row, target_col)
        while not (target_tile_row == specified_row):
            self.update_puzzle("druld")
            result += "druld"
            target_tile_row, dummy_target_tile_col = self.current_position(
                target_row, target_col)
        return result

    def _move_target_right_to(self, specified_col, target_row, target_col):
        """
        moves target_tile right until specified_col is reached
        start and end position of zero left of target tile
        """
        result = ""
        dummy_target_tile_row, target_tile_col = self.current_position(
            target_row, target_col)
        while not target_tile_col == specified_col:
            self.update_puzzle("urrdl")
            result += "urrdl"
            dummy_target_tile_row, target_tile_col = self.current_position(
                target_row, target_col)
        return result

    def _zero_to_end(self):
        """
        moves zero to end
        """
        result = ""
        zero_row, zero_col = self.current_position(0, 0)
        while not (
                zero_row == self.get_height() - 1 and zero_col == self.get_width() - 1):

            # move up or down
            if zero_row < self.get_height() - 1:
                self.update_puzzle("d")
                result += "d"

            # move left or right
            if zero_col < self.get_width() - 1:
                self.update_puzzle("r")
                result += "r"

            # update current position of zero
            zero_row, zero_col = self.current_position(0, 0)

        return result

# Start interactive simulation
puzzle = Puzzle(4, 4, [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
poc_fifteen_gui.FifteenGUI(puzzle)


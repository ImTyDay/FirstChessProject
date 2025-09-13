class Position:
    """
    Position is the class used by Pieces, so they can know where they are.
    Position is not a square in the board, is just the location of a piece.
    """
    def __init__(self, xpos: int, ypos: int):

        # lpos is the "letters" position
        # npos is the "numbers" position
        self.xpos = xpos
        self.ypos = ypos

        self.on_board = 0 < xpos <= 8 and 0 < ypos <= 8  # boolean

    @property
    def xpos(self):
        # Get the x coordinate by a method
        return self._xpos

    @property
    def ypos(self):
        # Get the y coordinate by a method
        return self._ypos

    @xpos.setter
    def xpos(self, value):
        """Set the value of x as an integer between 1 and 8 (inclusive)"""
        if not isinstance(value, int):
            raise ValueError("Value of letters position must be an integer")
        if not 1 <= value <= 8:
            # old ValueError method for checking if position is on board
            # raise ValueError ("Value of letters position must be between 1 and 8")
            pass

        self._xpos = value

    @ypos.setter
    def ypos(self, value):
        """Set the value of y as an integer between 1 and 8 (inclusive)"""
        if not isinstance(value, int):
            raise ValueError("Value of letters position must be an integer")
        # if not 1 <= value <= 8:
            # raise ValueError ("Value of letters position must be between 1 and 8")

        self._ypos = value

    def __add__(self, other):
        """Overloads the '+' operator to add a tuple (x, y) to a Position."""
        if not isinstance(other, tuple) or len(other) != 2:  # bad input
            raise TypeError("Can only add a tuple of (dx, dy) to a Position.")
        dx, dy = other  # unpacksthe tuple
        return Position(self.xpos + dx, self.ypos + dy)

    def __repr__(self):
        file = chr(ord('A') + self.xpos - 1)
        return F"{file}{self.ypos}"

    def __eq__(self, other) -> bool:
        """
        Defines a way to compare if 2 positions represent the same square on the board,
        Compares only xpos and ypos for both self and other

        :param other:
        :return boolean:
        """

        # if we are comparing a position to a non-position
        if not isinstance(other, Position):  # this doesn't even make sense, they are not equal
            return False

        return self.xpos == other.xpos and self.ypos == other.ypos

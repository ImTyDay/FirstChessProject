from __future__ import annotations

from position import Position
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board

class Piece:
    """
    Parent class of all types of pieces, defines common attributes to all pieces.
    Also, the parent class for SlidingPiece, witch is a subclass representing all pieces that have a slide-based
    movement, based on directions: Rook, Bishop, Queen
    """

    def __init__(self, color, position:Position):
        """
        Common attributes for all pieces, child classes of Piece.

        :param color: Black or White
        :param position: Position
        """

        self.color = color
        self.position = position


    def __str__(self):
        # will be overridden by child class
        return f"{self.color} Piece"

    def get_legal_moves(self, board):
        # will be overridden by the child class, if not, raises error
        raise NotImplementedError ("Each piece must have their own get_legal_moves method")


class SlidingPiece(Piece):
    """
    A parent class for pieces that move by going in lines until blocked (Rook, Bishop, Queen).
    The logic for sliding is defined here and used by all child classes.
    """

    def __init__(self, color, position):
        super().__init__(color, position)

        # define a temporary attribute that is overridden by child classes
        self.allowed_directions = []

    def get_legal_moves(self, board: Board):
        """
        Get the *Pseudo-Legal* move for a given piece, ignoring if the team's king is in check,
        and ignoring if making the move would make their own king in check


        :param board:Board
        :return legal_moves:List[Position]
        """

        legal_moves = []

        for direction in self.allowed_directions:

            current_position = self.position + direction # checks the first square in the direction

            """
            Check if the move is valid, considering the conditions:
            - The desired position must be on board
            - The desired position not be occupied by a piece of the same color
            - Capturing is allowed, but that makes the last possible move in the direction
            """
            while current_position.on_board:  # we cant go off the board, attempting that breaks out of the loop

                # if there are more than 64 moves, something is going wrong. This is just for debugging
                if len(legal_moves) > 64:
                    raise RecursionError (f"Too much legal moves: the function broke. Current moves: {legal_moves}")
                piece_on_square = board.get_piece(current_position)  # check what is in the position we want to go

                if not piece_on_square: # If the square is empty
                                        # It is a legal move
                    legal_moves.append(current_position)
                    current_position = current_position + direction  # update for next iteration
                else:  # means there is a piece here
                    if piece_on_square.color != self.color: # there is an enemy piece
                        legal_moves.append(current_position) # we can capture it as the last move for the direction

                    break  # our path is blocked in this direction anyway

        return legal_moves



class Pawn(Piece):

    def __init__(self, color, position):
        super().__init__(color, position)

        # has_moved is useful for determining if the pawn can move 2 squares
        self.has_moved = False

    def __str__(self):
        return f"{"P" if self.color == 'white' else "p"}{self.position}"

    def get_legal_moves(self, board: 'Board'):
        if not self.has_moved:
            pass
        pass


class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

        # has_moved is useful to determine if castle is possible
        self.has_moved = False

        # is_exposed is useful to determine if king is in check
        self.is_exposed = False

    def __str__(self):
        return f"{"K" if self.color == 'white' else "k"}{self.position}"

    def get_legal_moves(self, board: Board):
        pass


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def __str__(self):
        return f"{"Q" if self.color == 'white' else "q"}{self.position}"

    def get_legal_moves(self, board: Board):
        pass


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    # TODO: add color of square, so we can differentiate the bishops
    def __str__(self):
        return f"{"B" if self.color == 'white' else "b"}{self.position}"

    def get_legal_moves(self, board: Board):
        """
        Get the *Pseudo-Legal* move for a given piece, ignoring if the team's king is in check,
        and ignoring if making the move would make their own king in check


        :param board:Board
        :return legal_moves:List[Position]
        """

        legal_moves = []  # define a list that we will append all legal positions
        allowed_directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]  # directions the piece can move (vector x, y)
        # a Bishop can move in diagonals, what translates to both directions moving

        for direction in allowed_directions:

            current_position = self.position + direction  # checks the first square in the direction

            """
            Check if the move is valid, considering the conditions:
            - The desired position must be on board
            - The desired position not be occupied by a piece of the same color
            - Capturing is allowed, but that makes the last possible move in the direction
            """
            while current_position.on_board:  # we cant go off the board, attempting that breaks out of the loop

                # if there are more than 64 moves, something is going wrong. This is just for debugging
                if len(legal_moves) > 64:
                    # TODO: DEBUGGING
                    break
                    # raise RecursionError("More than 64 legal moves, the game broke.")
                piece_on_square = board.get_piece(current_position)  # check what is in the position we want to go

                if not piece_on_square:  # If the square is empty
                    # It is a legal move
                    legal_moves.append(current_position)
                    current_position = current_position + direction  # update for next iteration
                else:  # means there is a piece here
                    if piece_on_square.color != self.color:  # there is an enemy piece
                        legal_moves.append(current_position)  # we can capture it as the last move for the direction

                    break  # our path is blocked in this direction anyway

        return legal_moves


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def __str__(self):
        return f"{"N" if self.color == 'white' else "n"}{self.position}"

    def get_legal_moves(self, board: Board):
        pass


class Rook(Piece):

    def __init__(self, color, position):
        super().__init__(color, position)

        # has_moved is useful to determine if the rook can castle
        self.has_moved = False

    def __str__(self):
        return f"{"R" if self.color == 'white' else "r"}{self.position}"

    def get_legal_moves(self, board: Board):
        """
        Get the *Pseudo-Legal* move for a given piece, ignoring if the team's king is in check,
        and ignoring if making the move would make their own king in check


        :param board:Board
        :return legal_moves:List[Position]
        """

        legal_moves = []  # define a list that we will append all legal positions
        allowed_directions = [(1, 0), (-1,0), (0, 1), (0, -1)]  # directions the piece can move (vector x, y)
        # a Rook can move in any line, in any direction

        for direction in allowed_directions:

            current_position = self.position + direction # checks the first square in the direction

            """
            Check if the move is valid, considering the conditions:
            - The desired position must be on board
            - The desired position not be occupied by a piece of the same color
            - Capturing is allowed, but that makes the last possible move in the direction
            """
            while current_position.on_board:  # we cant go off the board, attempting that breaks out of the loop

                # if there are more than 64 moves, something is going wrong. This is just for debugging
                if len(legal_moves) > 64:
                    # TODO: DEBUGGING
                    break
                    # raise RecursionError("More than 64 legal moves, the game broke.")
                piece_on_square = board.get_piece(current_position)  # check what is in the position we want to go

                if not piece_on_square: # If the square is empty
                                        # It is a legal move
                    legal_moves.append(current_position)
                    current_position = current_position + direction  # update for next iteration
                else:  # means there is a piece here
                    if piece_on_square.color != self.color: # there is an enemy piece
                        legal_moves.append(current_position) # we can capture it as the last move for the direction

                    break  # our path is blocked in this direction anyway

        return legal_moves



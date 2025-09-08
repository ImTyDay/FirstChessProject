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
    Also, the parent class for OneMovePiece, that are not blocked by other pieces like SlidingPieces (Knight, King)
    The pawn has a unique movement, so it is just a child from Piece
    """

    def __init__(self, color, position: Position):
        """
        Common attributes for all pieces, child classes of Piece.

        :param color: Black or White
        :param position: Position
        """

        self.color = color
        self.position = position

        # define a temporary attribute that is overridden by child classes, used to check legal moves
        self.allowed_directions = []
        self.has_moved = False  # define a general attribute for easier registration, its used only by some pieces

    def __str__(self):
        # will be overridden by child class
        return f"{self.color} Piece"

    def get_legal_moves(self, board):
        # will be overridden by the child class, if not, raises error
        raise NotImplementedError("Each piece must have their own get_legal_moves method")


class SlidingPiece(Piece):
    """
    A parent class for pieces that move by going in lines until blocked (Rook, Bishop, Queen).
    The logic for sliding is defined here and used by all child classes.
    """

    def __init__(self, color, position):
        super().__init__(color, position)

    def get_legal_moves(self, board: Board):
        """
        Get the *Pseudo-Legal* move for a given piece, ignoring if the team's king is in check,
        and ignoring if making the move would make their own king in check


        :param board:Board
        :return legal_moves:List[Position]
        """

        legal_moves = []

        for direction in self.allowed_directions:

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
                    raise RecursionError(f"Too much legal moves: the function broke. Current moves: {legal_moves}")
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


class OneMovePiece(Piece):

    def get_legal_moves(self, board: Board):

        legal_moves = []

        for direction in self.allowed_directions:
            # there is no need to iterate, there are max 8 moves

            current_position = self.position + direction

            if current_position.on_board:  # don't go out of bounds
                piece_on_square = board.get_piece(current_position)
                # validate the move by capturing or moving to an empty space
                if not piece_on_square or piece_on_square.color != self.color:
                    legal_moves.append(current_position)

        return legal_moves


class Pawn(Piece):

    def __init__(self, color, position):
        super().__init__(color, position)

    def __str__(self):
        return f"{"P" if self.color == 'white' else "p"}{self.position}"

    def get_legal_moves(self, board: 'Board'):
        """
        The Pawn moving logic is unique, we need to make their own function

        :param board: Board
        :return: list
        """

        legal_moves = []  # standardize the  output of the function

        non_capture_directions = [(0, 1)]  # one square ahead
        if not self.has_moved:  # if it is the first move
            non_capture_directions.append((0, 2))  # we can move 2 squares
        for direction in non_capture_directions:
            if not board.get_piece(self.position + direction):  # if the square is empty
                legal_moves.append(direction)  # the square must not be blocked
        capture_directions = (1, 1), (-1, 1)   # we must have an enemy piece to go diagonally
        for direction in capture_directions:
            piece_on_square = board.get_piece(self.position + direction)
            if piece_on_square and piece_on_square.color != self.color:  # enemy piece in there
                legal_moves.append(direction)

        return legal_moves


class King(OneMovePiece):
    def __init__(self, color, position):
        super().__init__(color, position)

        self.allowed_directions = [(1, 1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, -1)]
        # a king can move one square in every direction

        # is_exposed is useful to determine if king is in check
        self.is_exposed = False

    def __str__(self):
        return f"{"K" if self.color == 'white' else "k"}{self.position}"


class Queen(SlidingPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.allowed_directions = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (1, 0), (0, -1), (-1, 0)]
        # a Queen can move in any direction

    def __str__(self):
        return f"{"Q" if self.color == 'white' else "q"}{self.position}"


class Bishop(SlidingPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.allowed_directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        # a Bishop can move diagonally, witch means both directions should move at the same time

    def __str__(self):
        return f"{"B" if self.color == 'white' else "b"}{self.position}"


class Knight(OneMovePiece):
    def __init__(self, color, position):
        super().__init__(color, position)

        self.allowed_directions = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        # the knight can move 2 pos in a direction if 1 pos is moved in the other direction

    def __str__(self):
        return f"{"N" if self.color == 'white' else "n"}{self.position}"


class Rook(SlidingPiece):

    def __init__(self, color, position):
        super().__init__(color, position)

        self.allowed_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        # a Rook can move in every straight direction, one direction at a time

    def __str__(self):
        return f"{"R" if self.color == 'white' else "r"}{self.position}"

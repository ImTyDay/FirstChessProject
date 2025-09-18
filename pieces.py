"""
Defines all pieces of the game, and define their legal moves.
"""

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

        self.allowed_directions = []
        self.has_moved = False

    def __str__(self):
        # will be overridden by child class
        return f"{self.color} Piece"

    def get_legal_moves(self, board):
        """ will be overridden by the child class, if not, raises error"""
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

            current_position = self.position + direction

            """
            Check if the move is valid, considering the conditions:
            - The desired position must be on board
            - The desired position not be occupied by a piece of the same color
            - Capturing is allowed, but that makes the last possible move in the direction
            """
            while current_position.on_board:

                # if there are more than 64 moves, something is going wrong. This is just for debugging
                if len(legal_moves) > 64:
                    raise RecursionError(f"Too much legal moves: the function broke. Current moves: {legal_moves}")
                piece_on_square = board.get_piece(current_position)

                if not piece_on_square:  # If the square is empty
                    # It is a legal move
                    legal_moves.append(current_position)
                    current_position = current_position + direction
                else:
                    if piece_on_square.color != self.color:  # capture
                        legal_moves.append(current_position)

                    break  # our path is blocked in this direction

        return legal_moves


class OneMovePiece(Piece):

    def get_legal_moves(self, board: Board):

        legal_moves = []

        for direction in self.allowed_directions:

            current_position = self.position + direction

            if current_position.on_board:
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

    def get_legal_moves(self, board: 'Board') -> list:
        """
        The Pawn moving logic is unique, we need to make their own function

        :param board: Board
        :return: list
        """

        legal_moves = []

        # if color is white, it moves upward in the board, if it's black, we move downwards.
        forward = 1 if self.color == 'white' else -1

        # Define straight directions the pawn can go
        non_capture_directions = [(0, forward)]
        if not self.has_moved:
            non_capture_directions.append((0, 2 * forward))
        for direction in non_capture_directions:
            desired_square = self.position + direction
            if not board.get_piece(desired_square):
                legal_moves.append(desired_square)
            else:
                break  # if the first square is occupied, we cant go 2 squares forward as well

        # Define diagonal directions the pawn can go
        capture_directions = [(1, forward), (-1, forward)]
        for direction in capture_directions:
            desired_square = self.position + direction
            piece_on_square = board.get_piece(desired_square)
            if piece_on_square and piece_on_square.color != self.color:
                legal_moves.append(desired_square)

        return legal_moves

    def promote(self):
        """
        TODO: Implement
        Triggered when
        self.position.ypos == 8 if self.color == 'white' else 1
        This means the piece has reached the other side of the board.

        Asks the user to choose between Queen, Knight, Bishop, Rook, and morphs self into the chosen class

        :return:
        """
        pass


class King(OneMovePiece):
    def __init__(self, color, position):
        super().__init__(color, position)

        self.allowed_directions = [(1, 1), (1, 0), (0, 1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, -1)]
        # a king can move one square in every direction

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

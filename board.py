"""
Manages the core components of the chessboard, including its state and pieces.

This module defines the Board class, which is central to the chess game's
state management. It utilizes a pandas DataFrame to represent the 8x8 grid,
providing a robust and efficient way to store and access piece information.

A critical convention to understand in this module is the handling of coordinates:

Position Objects (x, y): Throughout the program, board squares are
represented by Position objects. These objects use a standard Cartesian-style
coordinate system where position.xpos corresponds to the file (A-H, or 1-8)
and position.ypos corresponds to the rank (1-8). This is the intuitive
"file, then rank" system used in chess.

DataFrame Access (.loc[y, x]): When directly accessing the pandas
DataFrame grid, the .loc accessor must be used in [row, column] format.
In the context of the chessboard, this translates to grid.loc[rank, file]
or, using Position attributes, grid.loc[position.ypos, position.xpos].

Failing to respect this (y, x) order for DataFrame access while using
(x, y) for Position objects will lead to pieces having a different internal
position that the one the board displays.
"""

import pandas as pd
import copy
from pieces import *
from typing import Optional


class Board:

    """
    Represents the chessboard and the state of all pieces on it
    Manages the 8x8 dataframe and the initial setup of the game
    """
    def __init__(self, setup_pieces=True):

        # Create a 8x8 DataFrame, filling it with None initially
        # The index represents the ranks (y) and columns the files (x)
        self.grid = pd.DataFrame(None, index=range(1, 9), columns=range(1, 9))
        if setup_pieces:
            self._setup_pieces()

    def get_piece(self, position: Position) -> Optional[Piece]:
        """
        The method should always return a subclass of Piece, if the position is occupied.
        If it is not occupied, or if there is no Piece there for any reason, returns None.
        This is the best way to padronize the outputs, so we don't get NaN in any way.

        :param position:
        :return: Piece or None
        """

        if not position.on_board: return None

        # get the piece based on the grid
        piece = self.grid.loc[position.ypos, position.xpos]

        return None if pd.isna(piece) else piece

    def _setup_pieces(self):
        """
        Private method to place all pieces in their starting positions when creating the object
        """
        # black pieces
        for i in range(1, 9):  # place all pawns
            self.grid.loc[7, i] = Pawn('black', Position(i, 7))
        self.grid.loc[8, 1] = Rook('black', Position(1, 8))
        self.grid.loc[8, 8] = Rook('black', Position(8, 8))
        self.grid.loc[8, 2] = Knight('black', Position(2, 8))
        self.grid.loc[8, 7] = Knight('black', Position(7, 8))
        self.grid.loc[8, 3] = Bishop('black', Position(3, 8))
        self.grid.loc[8, 6] = Bishop('black', Position(6, 8))
        self.grid.loc[8, 4] = Queen('black', Position(4, 8))
        self.grid.loc[8, 5] = King('black', Position(5, 8))

        # white pieces
        for i in range(1, 9):
            self.grid.loc[2, i] = Pawn('white', Position(i, 2))
        self.grid.loc[1, 1] = Rook('white', Position(1, 1))
        self.grid.loc[1, 8] = Rook('white', Position(8, 1))
        self.grid.loc[1, 2] = Knight('white', Position(2, 1))
        self.grid.loc[1, 7] = Knight('white', Position(7, 1))
        self.grid.loc[1, 3] = Bishop('white', Position(3, 1))
        self.grid.loc[1, 6] = Bishop('white', Position(6, 1))
        self.grid.loc[1, 4] = Queen('white', Position(4, 1))
        self.grid.loc[1, 5] = King('white', Position(5, 1))

        # reverse the index to match a real chessboard visually
        # where rank 1 is at the bottom.
        self.grid = self.grid.sort_index(ascending=False)

    def __str__(self):
        """
        Returns a string representation of the current representation of the board
        Allows you to simply print(board_object)
        """
        display_grid = self.grid.copy()

        # Label files as letters for display
        file_labels = [chr(ord('A') + i) for i in range(8)]
        display_grid.columns = file_labels

        # Make the empty squares display as 'Empty'
        filled_grid = display_grid.fillna('Empty')
        return filled_grid.replace('None', 'Empty').to_string()

    def move_piece(self, start_pos: Position, end_pos: Position):
        """
        Moves the piece in the starting position to the end position on the board.
        This method does not check if the move is legal, just performs the move by a state change.

        :param start_pos:
        :param end_pos:
        :return: None
        """

        piece_to_move = self.get_piece(start_pos)

        if piece_to_move:  # safety check
            # Update the piece
            piece_to_move.position = end_pos

            piece_to_move.has_moved = True

            # Update the Board
            self.grid.loc[start_pos.ypos, start_pos.xpos] = None
            self.grid.loc[end_pos.ypos, end_pos.xpos] = piece_to_move

    def perform_castle(self, king_start_pos: Position, king_end_pos: Position):
        """
        Performs the special two-part castling move on the board.

        It first moves the king, then determines which rook to move based on
        the king's destination and moves it accordingly.

        :param king_start_pos: The starting position of the King.
        :param king_end_pos: The ending position of the King (G or C file).
        """

        print(f"Debug: castling {king_start_pos}, {king_start_pos}")

        castling_rank = king_start_pos.ypos

        # Move King
        self.move_piece(king_start_pos, king_end_pos)

        # Move the Rook
        if king_end_pos.xpos == 7:
            castling_rook_pos = Position(8, castling_rank)
            rook_destination = Position(6, castling_rank)
        else:
            castling_rook_pos = Position(1, castling_rank)
            rook_destination = Position(4, castling_rank)

        self.move_piece(castling_rook_pos, rook_destination)

    def promote_pawn(self, position: Position, promotion_choice: type[Piece]) -> None:
        """
        Replaces the pawn at the given position with a new piece of the chosen class.

        :param position: The square where the promotion is happening
        :param promotion_choice: The class of the new piece
        """

        pawn_to_promote = self.get_piece(position)
        if not isinstance(pawn_to_promote, Pawn):
            raise Exception("Only paws can be promoted!")  # safety check

        # Switch the class of the piece
        new_piece = promotion_choice(pawn_to_promote.color, position)
        new_piece.has_moved = True

        # Replace in the board
        self.grid.loc[position.ypos, position.xpos] = new_piece

    def deep_copy(self):
        """
        Creates a new, completely independent copy of the Board object.

        This is important for validating moves, allowing for simulating
        moves on a temporary board without affecting the actual game state.

        Even a copy.deepcopy or a pandas copy(deep=True) isn't enough for
        creating a independent instance, so we have to copy piece by piece.

        :return: A new Board instance with a deep copy of the grid.
        """

        new_board = Board(setup_pieces=False)

        # define a helper function to copy piece by piece
        def _copy_piece(piece_to_copy: Piece):
            if not piece_to_copy or pd.isna(piece_to_copy):
                return None

            # generate a new Piece copying the original attributes, and it's class
            new_piece = piece_to_copy.__class__(piece_to_copy.color, copy.deepcopy(piece_to_copy.position))
            new_piece.has_moved = piece_to_copy.has_moved

            return new_piece

        # apply the copy function to all pieces
        new_board.grid = self.grid.map(_copy_piece)

        return new_board

if __name__ == '__main__':
    tab = Board()
    print(tab)

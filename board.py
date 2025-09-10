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
from pieces import *
from typing import Optional


class Board:

    """
    Represents the chessboard and the state of all pieces on it
    Manages the 8x8 dataframe and the initial setup of the game
    """
    def __init__(self):
        # Create a 8x8 DataFrame, filling it with None initially
        # The index represents the ranks (y) and columns the files (x)
        self.grid = pd.DataFrame(None, index=range(1, 9), columns=range(1, 9))
        self._setup_pieces()

    def get_piece(self, position: Position) -> Optional[Piece]:
        """
        The method should always return a subclass of Piece, if the position is occupied.
        If it is not occupied, or if there is no Piece there for any reason, returns None.
        This is the best way to padronize the outputs, so we don't get NaN in any way.

        :param position:
        :return: Piece or None
        """

        # get None if the position is not on board
        if not position.on_board: return None

        # get the piece based on the grid
        piece = self.grid.loc[position.ypos, position.xpos]

        return None if pd.isna(piece) else piece

    def _setup_pieces(self):
        """
        Private method to place all pieces in their starting positions when creating the object
        """
        # place black pieces
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

        # place white pieces
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

        if piece_to_move:  # just to be sure we are moving something
            # Update the piece Position attribute
            piece_to_move.position = end_pos

            # Update the has_moves flag, used by Pawn, Rook, King
            piece_to_move.has_moved = True

            # Update the Board grid as well
            self.grid.loc[start_pos.ypos, start_pos.xpos] = None  # remove the piece from the original square
            self.grid.loc[end_pos.ypos, end_pos.xpos] = piece_to_move  # move the piece into the end square


if __name__ == '__main__':
    tab = Board()
    print(tab)

"""
Provides the core game logic and state management for a chess game.

This module defines the GameEngine class, which acts as the central
controller for the chess game. It is responsible for initializing the board,
tracking player turns, validating moves against the rules of chess, and
determining game-ending conditions like checkmate or stalemate.
"""

from board import *
from typing import Optional


class GameEngine:
    """
    Create the GameEngine class, responsible for keeping the game running, alternating moves,
    asking for moves, checking for checkmates,
    """
    def __init__(self):

        self.board = Board()
        self.current_turn = 'white'
        self.moves_count = 0

    @staticmethod
    def ask_for_position() -> Optional[Position]:
        """
        Asks the user for a square in the board.

        :return Position:
        """

        # TODO: Make it return None when user cancel, and handle it later

        while True:
            selected_position = input("Select a position: A-H 1-8").upper()  # standardize the input to UPPERCASE

            if selected_position.lower() == 'cancel':
                return Position(0, 0)
            try:
                selected_square = Position(xpos=ord(selected_position[0]) - ord('A') + 1,  # letter input to numeric
                                           ypos=int(selected_position[1]))  # the second letter of the input must be 1-8
                if not selected_square.on_board:  # if the position is not on board, but valid
                    print("Selected position out of board. Select a position A-H 1-8")
                    continue
                else:
                    return selected_square
            except ValueError:  # input was not correct
                print("Bad input: Inform your position in simple file-rank format, as A1, B2, C3, etc.")
                continue

    def ask_select_piece(self) -> Piece:
        """
        Asks the user for a piece to move, forces the user to select a valid piece, considering the selected piece
        must be something, and the color of the piece must be the same as the current turn's player

        :return:
        """

        while True:
            position = self.ask_for_position()
            if position is None:  # TODO: integrate with the None expected return, when user cancels
                continue
            selected_piece = self.board.get_piece(position)
            if not selected_piece or selected_piece.color != self.current_turn:
                print("Selected square must have a piece in the same color as the current player turn")
                continue
            return selected_piece

    def move(self):
        """
        Takes a piece selected by the user;
        Calculate the legal moves for that piece;
        Asks the user for a move;
        Moves the piece on the board.

        :return:
        """

        # TODO: Handle the case where user wants to change moving piece, identified by ask_for_position returning (0, 0)

        moving_piece = self.ask_select_piece()  # asks the user for a piece to move
        legal_moves = moving_piece.get_legal_moves(self.board)  # calculates the pseudo legal moves for the piece

        # shows the legal moves to the user
        print(f"Legal moves:", end=" ")
        for move in legal_moves:
            print(move, end=" ,")
            print("\n")

        while True:
            desired_square = self.ask_for_position()  # asks the user for the square in witch he wants to move the piece
            if desired_square not in legal_moves:  # checks if the move is legal
                print("Illegal movement. Please select a valid movement for the piece")
                continue
            self.board.move_piece(moving_piece.position, desired_square)

        pass

"""
Provides the core game logic and state management for a chess game.

This module defines the GameEngine class, which acts as the central
controller for the chess game. It is responsible for initializing the board,
tracking player turns, validating moves against the rules of chess, and
determining game-ending conditions like checkmate or stalemate.
"""

from board import *
from typing import Optional

from pieces import Piece


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
        Only validates if the position is on board.


        :return Position: the selected position by the user | None: User cancelled
        """

        while True:
            # Asks the user for an input position
            selected_position = input("Select a position: A-H 1-8").upper()  # standardize the input to UPPERCASE

            # if input is greater than 2 chars, we will ignore the rest.
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

    # noinspection PyTypeChecker
    def ask_select_piece(self) -> Piece:
        """
        Asks the user for a piece to move,
        Uses static method ask_for_position(), witch validates if the position is on the board
        Validates if the selection is occupied, so the function always returns a Piece
        Validates if the piece is the same color as current_turn.

        :return Piece:
        """

        while True:
            position = self.ask_for_position()
            selected_piece = self.board.get_piece(position)  # gets the Piece (or None) from selected square

            # validated if there is a piece, and if it is a piece of the same color as self.current_turn
            if not selected_piece or selected_piece.color != self.current_turn:  # validate selected piece
                print("Selected square must have a piece in the same color as the current player turn")
                continue  # ask again
            return selected_piece

    def play_turn(self):
        """
        Takes a piece selected by the user;
        Calculate the legal moves for that piece;
        Asks the user for a move;
        Moves the piece on the board.

        :return:
        """

        # while True:  # infinite loop that breaks only if a piece actually moves

        # Ask the user for a (first) piece to move
        print("Select a piece to move:")
        moving_piece = self.ask_select_piece()

        def calculate_and_show_moves(piece) -> list:
            legal_moves_list = piece.get_legal_moves(self.board)  # calculates the pseudo legal moves for the piece

            # tell the user what piece he selected
            print(f"Moving piece: {piece}")
            # shows the legal moves to the user
            print(f"Legal moves:", end=" ")
            for move in legal_moves_list:
                print(move, end=" ,")
                print("\n")

            return legal_moves_list

        # create an infinite loop that only breaks when a piece actually moves
        while True:

            # define and show the legal moves for the selected piece
            legal_moves = calculate_and_show_moves(moving_piece)

            # Ask the user what square he wants to go
            desired_square = self.ask_for_position()  # already validates if square is valid

            # check if the user wants to change the moving piece, by selecting a square with a same color piece
            desired_square_occupant = self.board.get_piece(desired_square)
            # assume the user wants to change piece if he selected a piece with the same color
            if desired_square_occupant and desired_square_occupant.color == self.current_turn:
                print("Moving piece changed to ", desired_square_occupant)
                moving_piece = desired_square_occupant  # change the moving_piece
                continue  # calculate again

            # Check if the desired move is illegal
            if desired_square not in legal_moves:
                print("Illegal movement. Please select a valid movement for the piece")
                continue

            # perform the actual move
            self.board.move_piece(start_pos=moving_piece.position, end_pos=desired_square)

            # change the turn
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            print("Current turn: ", self.current_turn)

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
        self.game_winner = None

        # Define the starting positions of the king, useful for dealing with checks
        self.white_king_pos = Position(5, 1)
        self.black_king_pos = Position(5, 7)

    @staticmethod
    def ask_for_position() -> Optional[Position]:
        """
        Asks the user for a square in the board.
        Only validates if the position is on board.


        :return Position: the selected position by the user | None: User cancelled
        """

        while True:
            # Asks the user for an input position
            selected_position = input("Select a position: A-H 1-8: ").upper()  # standardize the input to UPPERCASE

            # if input is greater than 2 chars, we will ignore the rest.
            try:
                selected_square = Position(xpos=ord(selected_position[0]) - ord('A') + 1,  # letter input to numeric
                                           ypos=int(selected_position[1]))  # the second letter of the input must be 1-8
                if not selected_square.on_board:  # if the position is not on board, but valid
                    print("Selected position out of board. Select a position A-H 1-8")
                    continue
                else:
                    print("Selected position: ", selected_square)
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
            print('\n')

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

            # Check if the user is moving the king, so we can store its position on the board
            if isinstance(moving_piece, King):
                # check what color is the moving king, and update the board
                if moving_piece.color == 'white':
                    self.white_king_pos = desired_square
                else:  # It must be the black king
                    self.black_king_pos = desired_square

            # Display the current state of the board in console
            print(self.board)

            # TODO: Remove, this should be the responsibility of game_run
            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            print("Current turn: ", self.current_turn)

            # end the turn
            break

    def check_game_ended(self) -> bool:
        """
        Checks natural conditions for the game to end, including:
        - Checkmate
        - Stalemate
        - More than 50 moves without captures or pawn movement
        - Repeating positions

        :return bool:
        """

        # TODO: Implement

        pass

    def is_in_check(self, color: str, board: Board) -> bool:
        """
        Checks if the king of the specified color is under attack on the given board.

        :param color: The color of the king to check ('white' or 'black').
        :param board: The board state to check against.
        :return: True if the king is in check, False otherwise.
        """

        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        attacker_color = 'black' if color == 'white' else 'white'


        """
        Check for enemy knights that might be attacking the king
        """
        # Try every direction a knight can move
        for direction in [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            suspect_piece = board.get_piece(king_pos + direction)
            if isinstance(suspect_piece, Knight) and suspect_piece.color != color: # we check if it is an enemy knight
                return True # it's attacking us

        """
        Check the straight lines around the king for enemy pieces,
        and when found, check if the piece is actually attacking the King.
        """
        straight_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        all_directions = straight_directions + diagonal_directions

        for direction in all_directions:
            current_pos = king_pos
            while current_pos.on_board:
                current_pos = current_pos + direction  # Take one step

                suspect_piece = board.get_piece(current_pos)

                # check cases where there is not an enemy piece in that line of sight
                if not suspect_piece:  # if square is empty
                    continue  # go to next square in that direction
                elif suspect_piece.color == color:  # if it is a friendly piece
                    break  # we won't go further in that direction

                # if we got here, we have a enemy piece in line of sight.
                if direction in straight_directions:  # we are checking straight.
                    return True if isinstance(suspect_piece, (Rook, Queen)) else False

                # if we are not in a straight line, we are in a diagonal line
                if isinstance(suspect_piece, (Bishop, Queen)): return True  # they can threaten us
                elif isinstance(suspect_piece, Pawn):
                    pass

                # TODO: Continue



        pass

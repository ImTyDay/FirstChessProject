"""
Provides the core game logic and state management for a chess game.

This module defines the GameEngine class, which acts as the central
controller for the chess game. It is responsible for initializing the board,
tracking player turns, validating moves against the rules of chess, and
determining game-ending conditions like checkmate or stalemate.
"""

from board import *

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
        self.no_action_turns = 0

        # Define the starting positions of the king, useful for dealing with checks
        self.white_king_pos = Position(5, 1)
        self.black_king_pos = Position(5, 8)

    def game_run(self):
        """
        Runs the main game loop, orchestrating the chess match turn by turn.

        This method acts as the primary entry point to start and play a game.
        It continuously alternates between players, prints the current board state,
        and calls the play_turn() method to handle the logic for a single move.

        The game loop will run indefinitely until game end
        """

        print("Game start!")
        while not self.game_winner:

            print("Current turn: ", self.current_turn)
            print(self.board)
            self.play_turn()

            print(self.board)

            self.current_turn = self._opposite_color(self.current_turn)
            if self._is_in_check(self.current_turn, self.board,
                                 self.white_king_pos if self.current_turn == 'white' else self.black_king_pos):
                print(f"\nCHECK! The {self.current_turn} king is under attack!")
            self.check_game_ended()

    # noinspection PyTypeChecker
    @staticmethod
    def ask_for_position() -> Position | str:
        """
        Asks the user for a square in the board.
        Only validates if the position is on board.


        :return Position: the selected position by the user | None: User cancelled
        """

        while True:
            # Asks the user for an input position
            selected_position = input("Select a position: A-H 1-8: ").upper()  # standardize the input to UPPERCASE

            # Define a way to resign by input
            if selected_position.lower() == 'resign':
                return 'resign'

            # if input is greater than 2 chars, we will ignore the rest.
            try:
                selected_square = Position(xpos=ord(selected_position[0]) - ord('A') + 1,  # letter input to numeric
                                           ypos=int(selected_position[1]))  # the second letter of the input must be 1-8
                if not selected_square.on_board:
                    print("Selected position out of board. Select a position A-H 1-8")
                    continue
                else:
                    print("Selected position: ", selected_square)
                    return selected_square
            except (ValueError, IndexError):
                print("Bad input: Inform your position in simple file-rank format, as A1, B2, C3, etc.")
                continue

    # noinspection PyTypeChecker
    def ask_select_piece(self) -> Piece | str:
        """
        Asks the user for a piece to move,
        Uses static method ask_for_position(), witch validates if the position is on the board
        Validates if the selection is occupied, so the function always returns a Piece
        Validates if the piece is the same color as current_turn.

        :return Piece:
        """

        while True:
            position = self.ask_for_position()

            # Implement a way for the user to resign
            if position == 'resign':
                return position

            selected_piece = self.board.get_piece(position)

            if not selected_piece or selected_piece.color != self.current_turn:
                print("Selected square must have a piece in the same color as the current player turn")
                continue
            return selected_piece

    def calculate_and_show_moves(self, piece: Piece) -> list:
        """
        Calculate and show all the pseudo-legal moves for a given piece

        :param piece:
        :return legal_moves: List with all legal moves the piece can perform in the board's current state.
        """

        legal_moves_list = self.get_fully_legal_moves(piece)

        print(f"Moving piece: {piece}")
        print(f"Legal moves:", end=" ")
        for move in legal_moves_list:
            print(move, end=", ")
        print('\n')

        return legal_moves_list

    def play_turn(self):
        """
        Takes a piece selected by the user;
        Calculate the legal moves for that piece;
        Asks the user for a move;
        Moves the piece on the board.

        Checks for resignation

        :return:
        """

        # Ask the user for a (first) piece to move
        print("Select a piece to move:")
        moving_piece = self.ask_select_piece()

        # Check for resignation when selecting a piece
        if moving_piece == 'resign':
            self.resign()
            return

        # create an infinite loop that only breaks when a piece actually moves
        while True:

            legal_moves = self.calculate_and_show_moves(moving_piece)

            # Ask the user what square he wants to go
            desired_square = self.ask_for_position()

            # Check again for resignation after a piece was selected
            if desired_square == 'resign':
                self.resign()
                return

            # check if the user wants to change the moving piece, by selecting a square with a same color piece
            desired_square_occupant = self.board.get_piece(desired_square)

            if desired_square_occupant and desired_square_occupant.color == self.current_turn:
                print("Moving piece changed to ", desired_square_occupant)
                moving_piece = desired_square_occupant
                continue

            # Check if the desired move is illegal
            if desired_square not in legal_moves:
                print("Illegal movement. Please select a valid movement for the piece")
                continue

            self.board.move_piece(start_pos=moving_piece.position, end_pos=desired_square)

            # Define if the current turn is an action turn: a pawn movement or a capture
            # These types of move reset the 50 move limit that makes the game end in draw
            is_pawn_move = isinstance(moving_piece, Pawn)
            if is_pawn_move or desired_square_occupant:
                self.no_action_turns = 0
            else:
                self.no_action_turns += 1

            # Check if a pawn has reached promotion rank
            if is_pawn_move and desired_square.ypos in (1, 8):
                self._handle_promotion(desired_square)

            # Check if the user is moving the king, so we can store its position on the board
            if isinstance(moving_piece, King):
                if moving_piece.color == 'white':
                    self.white_king_pos = desired_square
                else:
                    self.black_king_pos = desired_square

            break

    @staticmethod
    def _ask_promotion_choice() -> type[Piece]:
        """
        Asks the user for their choice when promoting, and validates the input.

        :return type[Piece]: The type of piece we are promoting to
        """

        while True:
            choice = input("Pawn promotion: Choose (Q) Queen, (R)ook, (B) Bishop or (N) Knight").upper()
            match choice:
                case 'Q' | 'QUEEN':
                    return Queen
                case 'R' | 'ROOK':
                    return Rook
                case 'B' | 'BISHOP':
                    return Bishop
                case 'N' | 'Knight':
                    return Knight
            print("Invalid choice. Choose (Q) Queen, (R)ook, (B) Bishop or (N) Knight")

    def _handle_promotion(self, reached_square: Position) -> None:
        """
        Manages the pawn promotion process

        :param reached_square: The position the pawn we are promotion has reached
        :return:
        """

        new_piece = self._ask_promotion_choice()

        self.board.promote_pawn(reached_square, new_piece)


    def get_fully_legal_moves(self, piece: Piece) -> list[Position]:
        """
        Calculates all fully legal moves for a given piece, considering king safety.

        This method first gets all pseudo-legal moves (moves that follow the
        piece's basic movement rules). It then filters this list by simulating
        each move on a temporary copy of the board. A move is only considered
        fully legal if it does not leave the player's own king in check after
        the move is made.

        :param piece: The Piece object to calculate moves for.
        :return: A list of Position objects representing all valid, king-safe moves.
        """
        # get all moves the piece can make, ignoring king safety.
        pseudo_legal_moves = piece.get_legal_moves(self.board)
        fully_legal_moves = []

        # for each of those moves, simulate it and check for self-check.
        for move in pseudo_legal_moves:
            hypothetical_board = self.board.deep_copy()  # generate a board to simulate the moves

            piece_to_move_on_copy = hypothetical_board.get_piece(piece.position)
            hypothetical_board.move_piece(piece_to_move_on_copy.position, move)

            king_pos_to_check = self.white_king_pos if piece.color == 'white' else self.black_king_pos

            if isinstance(piece, King):
                king_pos_to_check = move

            # We now pass the correct king position to validate if it would be in check
            if not self._is_in_check(piece.color, hypothetical_board, king_pos_to_check):
                fully_legal_moves.append(move)

        return fully_legal_moves

    def check_game_ended(self) -> bool:
        """
        Checks natural conditions for the game to end, including:
        - Checkmate
        - Stalemate
        - More than 50 moves without captures or pawn movement
        - Repeating positions

        :return str or None: 'white', 'black' or 'draw', whoever has won None if game gas not ended
        """

        # check if the game is a draw by having 50 or more moves without captures or pawn movement
        if self.no_action_turns >= 50:
            self.game_winner = 'draw'
            return False

        # verify if current turn player has any legal moves at all: we need to iterate the entire board
        for file in range(1, 9):
            for rank in range(1, 9):
                piece = self.board.get_piece(Position(file, rank))
                if piece and piece.color == self.current_turn and self.get_fully_legal_moves(piece):
                    return False

        # getting here means no legal moves were found, so we need to differentiate between checkmate and stalemate
        if not self._is_in_check(self.current_turn, self.board,
                                 king_pos=self.white_king_pos if self.current_turn == 'white' else self.black_king_pos):
            self.game_winner = 'draw'
            print("Stalemate! It's a draw!")
            return True
        else:  # checkmate
            self.game_winner = self._opposite_color(self.current_turn)
            print(f"Checkmate! {self.game_winner} wins!")

        return False

    @staticmethod
    def _opposite_color(color: str):
        return 'black' if color == 'white' else 'white'

    def resign(self):
        """
        Sets game_winner to the opposite color of the one resigned.
        One can only resign on the turn he is playing.

        :return:
        """
        print(f"{self.current_turn} resigned! {self._opposite_color(self.current_turn)} wins!")
        self.game_winner = self._opposite_color(self.current_turn)

    def _possible_castles(self) -> tuple[bool, bool]:
        """
        Checks the side a king can castle:
        Checks all conditions that impede a castle

        :return tuple(bool(king_side_castle), bool(queen_side_castle): True for each side castle is possible
        """

        king_side_castle = True
        queen_side_castle = True

        king_pos = self.white_king_pos if self.current_turn == 'white' else self.black_king_pos
        king = self.board.get_piece(king_pos)
        castle_rank = 1 if self.current_turn == 'white' else 8

        if king.has_moved:
            return False, False

        potential_king_rook = self.board.get_piece(Position(8, castle_rank))
        potential_queen_rook = self.board.get_piece(Position(1, castle_rank))

        for potential_rook in (potential_king_rook, potential_queen_rook):
            if not isinstance(potential_rook, Rook) or potential_rook.has_moved:
                if potential_rook is potential_king_rook:
                    king_side_castle = False
                else:
                    queen_side_castle = False

        king_empty_needed_files = [6, 7]
        king_safe_needed_files = [5, 6, 7]

        return king_side_castle, queen_side_castle

    @staticmethod
    def _is_in_check(color: str, board: Board, king_pos: Position) -> bool:
        """
        Checks if the king of the specified color is under attack on the given board.

        Uses the king position and look outwards for threats.

        :param color: The color of the king to check ('white' or 'black').
        :param board: The board state to check against.
        :param king_pos: The current position of the king we are checking
        :return: True if the king is in check, False otherwise.
        """

        """
        Check for enemy knights that might be attacking the king
        """
        # Try every direction a knight can move
        for direction in [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            suspect_piece = board.get_piece(king_pos + direction)
            if isinstance(suspect_piece, Knight) and suspect_piece.color != color:
                return True

        """
        Check the straight lines around the king for enemy pieces,
        and when found, check if the piece is actually attacking the King.
        """
        straight_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        diagonal_down_directions = [(1, -1), (-1, -1)]  # separating is useful for checking pawn attacks
        diagonal_up_directions = [(1, 1), (-1, 1)]
        diagonal_directions = diagonal_down_directions + diagonal_up_directions
        all_directions = straight_directions + diagonal_directions

        for direction in all_directions:
            current_pos = king_pos
            steps = 0
            while current_pos.on_board:
                current_pos += direction  # Take one step
                steps += 1

                suspect_piece = board.get_piece(current_pos)

                # check cases where there is not an enemy piece in that line of sight
                if not suspect_piece:
                    continue  # go to next square in that direction
                elif suspect_piece.color == color:
                    break

                # if we got here, we have an enemy piece in line of sight.
                if direction in straight_directions:
                    if isinstance(suspect_piece, (Rook, Queen)):
                        return True
                    break

                # if we are not in a straight line, we are in a diagonal line
                if isinstance(suspect_piece, (Bishop, Queen)):
                    return True
                elif isinstance(suspect_piece, Pawn) and steps == 1:  # the pawn must be diagonal and near to threaten
                    if direction in diagonal_up_directions and color == 'white':
                        return True
                    if direction in diagonal_down_directions and color == 'black':
                        return True
                else:
                    break

        return False

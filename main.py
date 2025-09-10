
"""
Phase 1: The Foundation - The Static Board (What you are doing now)
Goal: Represent a chessboard in its starting state.

Position Class: A simple class to hold coordinates.

Piece and Subclasses: Define all the piece types (Pawn, Rook, etc.), inheriting from a base Piece. For now, they only
 need to know their color, position, and how to represent themselves as a string (e.g., 'R' or 'r').

Board Class: Contains a 8x8 pandas DataFrame. Its only job right now is to create all 32 pieces and place them correctly
 in the DataFrame upon initialization.

main.py: A tiny script that creates a Board object and prints its DataFrame to the console.

✅ You are done with this phase when you can run main.py and see the starting board printed perfectly.

Phase 2: The Core Mechanic - Piece Movement
Goal: Make a single piece move on the board according to its rules.

Implement get_legal_moves() for the Rook. The Rook is the best piece to start with because its "sliding" logic is
 reusable for the Bishop and Queen.

Create a move_piece() Method in Board. This method will take a start and end Position. It will update the DataFrame by
 moving the piece object from the start cell to the end cell and setting the start cell to None.

Update main.py: Hard-code a move and see if it works. For example:

Python

# In main.py
board = Board()
print("Board before move:")
print(board.grid)

# Manually check a legal move for a piece
a_white_rook = board.grid.iloc[7, 0] # Get the piece at a1
# Note: You'll need a way to get the piece from the board.
# Maybe a board.get_piece(Position(1,1)) method?

legal_moves = a_white_rook.get_legal_moves(board)
# Check if a target position is in legal_moves, then...

board.move_piece(Position(1, 1), Position(1, 4)) # Move from a1 to a4
print("\nBoard after move:")
print(board.grid)
✅ You are done with this phase when you can successfully calculate legal moves for a Rook and see the board state
 change correctly after a move.

Phase 3: The Game Engine - Rules and Turns
Goal: Create a simple, text-based game loop.

GameEngine Class: This class will manage the game state. It should have a Board object, and an attribute for
 current_turn (e.g., 'white').

Game Loop: In main.py, create a while True loop.

Player Input: Inside the loop, ask the user to input a move (e.g., "e2 e4").

Move Validation: The GameEngine will be responsible for checking:

Is there a piece at the start position?

Does the piece's color match current_turn?

Is the end position in the piece's get_legal_moves() list?

Switch Turns: If the move is valid, tell the Board to move the piece, then switch current_turn from 'white' to 'black'
 (or vice versa).

✅ You are done with this phase when you can play a back-and-forth game in your terminal using only Rooks.

Phase 4: Expansion - Completing the Army
Goal: Implement move logic for all the other pieces.

One by one, implement get_legal_moves() for Knight, Bishop, Queen, King, and Pawn.

Start with the easier ones (Knight, Bishop). The Queen will be easy because it just combines the logic
from the Rook and Bishop.

The Pawn is the most complex; save it for last in this phase. For now, just implement its forward moves and basic
captures. Ignore en passant and promotion.

✅ You are done when you can play a full game (minus special rules) between two people in the terminal.

Phase 5: The Finer Points - Special Rules & End Game
Goal: Implement the complex rules that make chess, chess.

Check Detection: Create a method in GameEngine that checks if a player's King is under attack after a move.

Checkmate & Stalemate: This is the hardest logic. After a move puts a player in check, you must check if they have any
legal moves to get out of check. If not, it's checkmate.

Special Moves: Now you can add the logic for:

Pawn Promotion

Castling

En Passant

✅ You are done when your text-based engine correctly handles all the rules of chess.

Phase 6: The Presentation Layer - The GUI
Goal: Create the graphical interface.

Design the Window: Use tkinter to create a window and draw a 8x8 grid of squares.

Draw the Pieces: Write a function that reads your board.grid DataFrame and draws the pieces on the tkinter canvas.
 You can use Unicode chess characters or simple images.

Handle Clicks: Implement click handlers. The first click saves the start square. The second click saves the end square
. Then, you pass these coordinates to your existing GameEngine to validate and make the move.

Update the Display: After your engine confirms a move was made, call your drawing function again to show the new board.
"""

#from board import Board
#from position import Position

from gameengine import GameEngine

# Temporary Phase 1. Main process
if __name__ == '__main__':
    gameengine = GameEngine()
    print("Game start! \n Current turn: White \n")
    print(gameengine.board, '\n')
    gameengine.play_turn()
    print("First turn ended")
    gameengine.play_turn()
    print(gameengine.board, '\n')
    print("Second turn Ended")
    gameengine.play_turn()


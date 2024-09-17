from enum import Enum
from typing import Dict, Optional
from ...domain.entities.player import Player
from ...domain.value_objects.move import Move
import uuid
import random

class GameStatus(Enum):
    """Enum representing the possible states of a game."""
    ONGOING = "ongoing"
    COMPLETED = "completed"

class Game:
    """
    Represents a game of Rock-Paper-Scissors.

    This class manages the game state, including players, moves, and scores.
    It also handles the logic for determining round winners and updating game status.
    """

    def __init__(self, player1: Player, player2: Player):
        """
        Initialize a new game with two players.

        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
        """
        self.id = str(uuid.uuid4())  # Generate a unique ID for the game
        self.player1 = player1
        self.player2 = player2
        self.scores = {player1.id: 0, player2.id: 0}  # Initialize scores to 0

        # Initialize current moves for both players to None
        self.current_moves: Dict[str, Optional[Move]] = {
            player1.id: None,
            player2.id: None
        }
        self.status = GameStatus.ONGOING
        self.last_round_moves: Dict[str, Move] = {}  # Store last round's moves
        self.last_round_winner: Optional[str] = None  # ID of the last round's winner, if any

    def make_move(self, player_id: str, move: Move) -> None:
        """
        Record a player's move and process the round if both players have moved.

        Args:
            player_id (str): The ID of the player making the move.
            move (Move): The move chosen by the player.

        Raises:
            Exception: If the game has already ended or if an invalid player_id is provided.
        """
        if self.status != GameStatus.ONGOING:
            raise Exception("Game has already ended.")
        
        if player_id not in [self.player1.id, self.player2.id]:
            raise Exception("Invalid player ID.")

        self.current_moves[player_id] = move  # Record the player's move

        # Generate move for the computer player if necessary
        self._generate_computer_move()

        # If both players have moved, determine the winner and reset for next round
        if all(self.current_moves.values()):
            self._determine_round_winner()
            self._reset_current_moves()

    def _generate_computer_move(self) -> None:
        """
        Generate a move for the computer player if necessary.
        """
        for player in [self.player1, self.player2]:
            if player.is_computer and self.current_moves[player.id] is None:
                self.current_moves[player.id] = random.choice(list(Move))
                break  # Only one player can be a computer, so we can stop after generating a move

    def _determine_round_winner(self) -> None:
        """Determine the winner of the current round and update game state."""
        move1 = self.current_moves[self.player1.id]
        move2 = self.current_moves[self.player2.id]
        
        # Store moves for history
        self.last_round_moves = {
            self.player1.id: move1,
            self.player2.id: move2
        }
        
        # Compare moves and update scores
        result = Move.compare_moves(move1, move2)
        self._update_scores_and_winner(result)

    def _update_scores_and_winner(self, result: int) -> None:
        """
        Update scores and set the round winner based on the result.

        Args:
            result (int): 1 if player1 wins, -1 if player2 wins, 0 if tie.
        """
        if result == 1:
            self.scores[self.player1.id] += 1
            self.last_round_winner = self.player1.id
        elif result == -1:
            self.scores[self.player2.id] += 1
            self.last_round_winner = self.player2.id
        else:
            self.last_round_winner = None  # Tie

    def _reset_current_moves(self) -> None:
        """Reset current moves for the next round."""
        self.current_moves = {
            self.player1.id: None,
            self.player2.id: None
        }
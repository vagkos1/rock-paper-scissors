import unittest
from unittest.mock import patch
import uuid

from src.domain.entities.game import Game, GameStatus
from src.domain.entities.player import Player
from src.domain.value_objects.move import Move

class TestGame(unittest.TestCase):

    def setUp(self):
        """Set up a new game before each test."""
        self.player1 = Player("Alice", is_computer=False)
        self.player2 = Player("Bob", is_computer=False)
        self.game = Game(self.player1, self.player2)

    def test_game_initialization(self):
        """Test that the game is initialized correctly."""
        self.assertIsInstance(self.game.id, str)
        self.assertTrue(uuid.UUID(self.game.id, version=4))
        self.assertEqual(self.game.player1, self.player1)
        self.assertEqual(self.game.player2, self.player2)
        self.assertEqual(self.game.scores, {self.player1.id: 0, self.player2.id: 0})
        self.assertEqual(self.game.status, GameStatus.ONGOING)
        self.assertIsNone(self.game.last_round_winner)
        self.assertEqual(self.game.current_moves, {self.player1.id: None, self.player2.id: None})
        self.assertEqual(self.game.last_round_moves, {})

    def test_make_move_single_player(self):
        """Test that a single player's move is recorded correctly."""
        self.game.make_move(self.player1.id, Move.ROCK)
        self.assertEqual(self.game.current_moves[self.player1.id], Move.ROCK)
        self.assertIsNone(self.game.current_moves[self.player2.id])

    def test_make_move_game_ended(self):
        """Test that an exception is raised when trying to make a move in a completed game."""
        self.game.status = GameStatus.COMPLETED
        with self.assertRaises(Exception) as context:
            self.game.make_move(self.player1.id, Move.ROCK)
        self.assertEqual(str(context.exception), "Game has already ended.")

    def test_make_move_invalid_player(self):
        """Test that an exception is raised when an invalid player ID is provided."""
        with self.assertRaises(Exception) as context:
            self.game.make_move("invalid_id", Move.ROCK)
        self.assertEqual(str(context.exception), "Invalid player ID.")

    @patch('src.domain.entities.game.random.choice')
    def test_computer_move_generation(self, mock_choice):
        """Test that the computer player generates a move automatically."""
        human_player = Player("Human", is_computer=False)
        computer_player = Player("Computer", is_computer=True)
        game = Game(human_player, computer_player)
        mock_choice.return_value = Move.PAPER

        # Make a move for the human player
        game.make_move(human_player.id, Move.ROCK)

        # Check that both moves have been made and stored in last_round_moves
        self.assertEqual(game.last_round_moves[human_player.id], Move.ROCK)
        self.assertEqual(game.last_round_moves[computer_player.id], Move.PAPER)

        # Check that current_moves have been reset
        self.assertIsNone(game.current_moves[human_player.id])
        self.assertIsNone(game.current_moves[computer_player.id])

        # Check that the score has been updated
        self.assertEqual(game.scores[computer_player.id], 1)  # Paper beats Rock
        self.assertEqual(game.scores[human_player.id], 0)

        # Check that the last_round_winner is set correctly
        self.assertEqual(game.last_round_winner, computer_player.id)

    def test_multiple_rounds(self):
        """Test that multiple rounds are scored correctly."""
        rounds = [
            (Move.ROCK, Move.SCISSORS, self.player1.id),
            (Move.SCISSORS, Move.ROCK, self.player2.id),
            (Move.PAPER, Move.PAPER, None)
        ]

        for round_num, (move1, move2, expected_winner) in enumerate(rounds, 1):
            with self.subTest(f"Round {round_num}"):
                self.game.make_move(self.player1.id, move1)
                self.game.make_move(self.player2.id, move2)
                self.assertEqual(self.game.last_round_winner, expected_winner)
                self.assertEqual(self.game.last_round_moves, {self.player1.id: move1, self.player2.id: move2})
                self.assertIsNone(self.game.current_moves[self.player1.id])
                self.assertIsNone(self.game.current_moves[self.player2.id])

        self.assertEqual(self.game.scores[self.player1.id], 1)
        self.assertEqual(self.game.scores[self.player2.id], 1)

    def test_all_move_combinations(self):
        """Test all possible move combinations and their outcomes."""
        move_combinations = [
            (Move.ROCK, Move.SCISSORS, self.player1.id),
            (Move.ROCK, Move.PAPER, self.player2.id),
            (Move.ROCK, Move.ROCK, None),
            (Move.PAPER, Move.ROCK, self.player1.id),
            (Move.PAPER, Move.SCISSORS, self.player2.id),
            (Move.PAPER, Move.PAPER, None),
            (Move.SCISSORS, Move.PAPER, self.player1.id),
            (Move.SCISSORS, Move.ROCK, self.player2.id),
            (Move.SCISSORS, Move.SCISSORS, None)
        ]

        for p1_move, p2_move, expected_winner in move_combinations:
            with self.subTest(f"{p1_move.value} vs {p2_move.value}"):
                self.game = Game(self.player1, self.player2)  # Reset game for each combination
                self.game.make_move(self.player1.id, p1_move)
                self.game.make_move(self.player2.id, p2_move)
                self.assertEqual(self.game.last_round_winner, expected_winner)
                if expected_winner:
                    self.assertEqual(self.game.scores[expected_winner], 1)
                    self.assertEqual(self.game.scores[self.player1.id if expected_winner == self.player2.id else self.player2.id], 0)
                else:
                    self.assertEqual(self.game.scores[self.player1.id], 0)
                    self.assertEqual(self.game.scores[self.player2.id], 0)

    def test_game_status_remains_ongoing(self):
        """Test that the game status remains ONGOING after multiple rounds."""
        for _ in range(5):
            self.game.make_move(self.player1.id, Move.ROCK)
            self.game.make_move(self.player2.id, Move.SCISSORS)
        self.assertEqual(self.game.status, GameStatus.ONGOING)

if __name__ == '__main__':
    unittest.main()
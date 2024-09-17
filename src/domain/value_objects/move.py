from enum import Enum

class Move(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    @staticmethod
    def compare_moves(move1, move2):
        rules = {
            Move.ROCK: Move.SCISSORS,
            Move.SCISSORS: Move.PAPER,
            Move.PAPER: Move.ROCK,
        }
        if move1 == move2:
            return 0  # Tie
        elif rules[move1] == move2:
            return 1  # Move1 wins
        else:
            return -1  # Move2 wins

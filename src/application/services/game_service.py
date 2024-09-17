from ..interfaces.igame_repository import IGameRepository
from ...domain.entities.player import Player
from ...domain.entities.game import Game
from ...domain.value_objects.move import Move

class GameService:
    """
    Service class for managing Rock-Paper-Scissors games.

    This class provides methods to start new games and make moves,
    using a game repository for data persistence.
    """

    def __init__(self, game_repository: IGameRepository):
        """
        Initialize the GameService with a game repository.

        Args:
            game_repository (IGameRepository): The repository used for game data persistence.
        """
        self.game_repository = game_repository

    def start_game(self, player1_name: str, player2_name: str, vs_computer: bool = False) -> Game:
        """
        Start a new game with two players.

        This method creates a new game instance, initializes players,
        and saves the initial game state to the repository.

        Args:
            player1_name (str): The name of the first player.
            player2_name (str): The name of the second player (or "Computer" if vs_computer is True).
            vs_computer (bool, optional): Whether the second player is a computer. Defaults to False.

        Returns:
            Game: The newly created game instance.
        """
        # Create the first player
        player1 = Player(name=player1_name)

        # Create the second player, either human or computer
        if vs_computer:
            player2 = Player(name="Computer", is_computer=True)
        else:
            player2 = Player(name=player2_name)

        # Initialize a new game with the two players
        game = Game(player1=player1, player2=player2)

        # Save the initial game state to the repository
        self.game_repository.save(game)

        return game

    def make_move(self, game_id: str, player_id: str, move: Move) -> Game:
        """
        Make a move in an existing game.

        This method retrieves the game from the repository,
        applies the player's move and saves the updated game state.

        Args:
            game_id (str): The ID of the game to make a move in.
            player_id (str): The ID of the player making the move.
            move (Move): The move being made by the player.

        Returns:
            Game: The updated game instance after the move has been made.
        """
        # Retrieve the current game state from the repository
        game = self.game_repository.get(game_id)

        # Apply the player's move to the game
        game.make_move(player_id, move)

        # Save the updated game state to the repository
        self.game_repository.save(game)

        return game
# infrastructure/repositories/sqlite_game_repository.py

from application.interfaces.igame_repository import IGameRepository
from domain.entities.game import Game
from typing import List

class SQLiteGameRepository(IGameRepository):

    def save(self, game: Game):
        """Save or update a game."""
        pass

    def get(self, game_id: str) -> Game:
        """Retrieve a game by its ID."""
        pass

    def delete(self, game_id: str):
        """Delete a game by its ID."""
        pass

    def list_all(self) -> List[Game]:
        """List all games."""
        pass

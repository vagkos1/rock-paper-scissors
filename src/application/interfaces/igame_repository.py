from abc import ABC, abstractmethod
from typing import List
from ...domain.entities.game import Game

class IGameRepository(ABC):

    @abstractmethod
    def save(self, game: Game):
        """Save or update a game."""
        pass

    @abstractmethod
    def get(self, game_id: str) -> Game:
        """Retrieve a game by its ID."""
        pass

    @abstractmethod
    def delete(self, game_id: str):
        """Delete a game by its ID."""
        pass

    @abstractmethod
    def list_all(self) -> List[Game]:
        """List all games."""
        pass

from typing import Dict, List
from ...domain.entities.game import Game
from ...application.interfaces.igame_repository import IGameRepository

class InMemoryGameRepository(IGameRepository):
    def __init__(self):
        self._games: Dict[str, Game] = {}

    def save(self, game: Game):
        self._games[game.id] = game

    def get(self, game_id: str) -> Game:
        return self._games.get(game_id)

    def delete(self, game_id: str):
        self._games.pop(game_id, None)

    def list_all(self) -> List[Game]:
        return list(self._games.values())

from threading import RLock
from uuid import UUID
from datasource.model.game import DataGame

class GameStorage:
    def __init__(self):
        self._games: dict[UUID, DataGame] = {}
        self._lock = RLock()

    def save(self, game: DataGame) -> None:
        with self._lock:
            self._games[game.game_id] = game

    def get(self, game_id: UUID) -> DataGame | None:
        with self._lock:
            return self._games.get(game_id)

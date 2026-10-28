from uuid import UUID
from datasource.repository.game_repository import GameRepository
from datasource.repository.game_storage import GameStorage
from datasource.mapper.game_mapper import DataGameMapper
from domain.model.game import Game

class InMemoryGameRepository(GameRepository):
    def __init__(self, storage: GameStorage):
        self._storage = storage

    def save(self, game: Game) -> None:
        self._storage.save(DataGameMapper.to_data(game))

    def get(self, game_id: UUID) -> Game | None:
        data_game = self._storage.get(game_id)
        return DataGameMapper.to_domain(data_game) if data_game else None

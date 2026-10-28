from uuid import uuid4
from domain.model.game import Game
from domain.model.game_field import GameField
from datasource.repository.game_repository import GameRepository
from domain.service.game_service import GameService

class GameModule:
    def __init__(self, repository: GameRepository, service: GameService):
        self._repository = repository
        self._service = service

    def create_game(self) -> Game:
        game = Game(uuid4(), GameField.empty())
        self._repository.save(game)
        return game

    def play(self, game_id, submitted_field: GameField) -> Game:
        previous = self._repository.get(game_id)
        if previous is None:
            raise LookupError("Game with this UUID not found")
        self._service.validate_field(previous, submitted_field)
        updated = Game(game_id, submitted_field)
        if not self._service.is_finished(submitted_field):
            updated = Game(game_id, self._service.next_move(submitted_field))
        self._repository.save(updated)
        return updated

    def is_finished(self, game: Game) -> bool:
        return self._service.is_finished(game.field)

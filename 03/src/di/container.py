from datasource.repository.game_storage import GameStorage
from datasource.repository.in_memory_game_repository import InMemoryGameRepository
from domain.service.minimax_game_service import MinimaxGameService
from web.module.game_module import GameModule
from web.route.game_route import create_game_blueprint

class Container:
    """A simplest dependency container. The storge is created once"""
    def __init__(self):
        self.storage = GameStorage()
        self.repository = InMemoryGameRepository(self.storage)
        self.game_service = MinimaxGameService()
        self.game_module = GameModule(self.repository, self.game_service)

    def register_routes(self, app):
        app.register_blueprint(create_game_blueprint(self.game_module))

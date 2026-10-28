from domain.model.game import Game
from domain.model.game_field import GameField
from web.model.game import WebGame
from web.model.game_field import WebGameField

class WebGameMapper:
    @staticmethod
    def to_domain(game: WebGame) -> Game:
        return Game(game.game_id, GameField(game.field.cells))

    @staticmethod
    def to_web(game: Game, finished: bool = False) -> WebGame:
        return WebGame(game.game_id, WebGameField(game.field.cells), finished)
